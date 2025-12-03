"""
Interaction Layer Module

Implements the PromptOptimizer class that orchestrates the RJW-IDD workflow.
This class accepts raw user input and coordinates the research → template filling flow.
"""
from typing import Dict, List, Optional
from pathlib import Path
from ..discovery.research import ResearchHarvester
from ..utils import TemplateManager
from ..brain import get_provider, LLMProvider


class PromptOptimizer:
    """
    Orchestrates the RJW-IDD workflow from user input to specification.
    
    This class enforces the proper flow:
    1. Accept raw user strings
    2. Delegate to ResearchEngine to gather facts (EVD files)
    3. Fill templates with evidence-backed data
    4. Ensure proper traceability: EVD → DEC → SPEC → TEST
    
    Key principle: It does NOT write Specs immediately. It first delegates
    to the Research Engine to get facts, then fills templates.
    
    Attributes:
        research_harvester: Instance of ResearchHarvester for evidence gathering
        template_manager: Instance of TemplateManager for artifact generation
        workflow_state: Current state of the workflow
    """
    
    def __init__(self, 
                 research_output_dir: str = "research/evidence",
                 specs_output_dir: str = "specs",
                 decisions_output_dir: str = "decisions",
                 provider: Optional[str] = None):
        """
        Initialize the PromptOptimizer.
        
        Args:
            research_output_dir: Directory for evidence files
            specs_output_dir: Directory for specification files
            decisions_output_dir: Directory for decision files
            provider: Optional LLM provider name
        """
        # Initialize LLM provider
        try:
            self.llm_provider = get_provider(provider)
        except Exception as e:
            # Fall back to None if provider initialization fails
            # This allows the tool to work without LLM for now
            self.llm_provider = None
            import warnings
            warnings.warn(f"Failed to initialize LLM provider: {e}")
        
        self.research_harvester = ResearchHarvester(research_output_dir, llm_provider=self.llm_provider)
        self.template_manager = TemplateManager()
        
        self.specs_output_dir = Path(specs_output_dir)
        self.decisions_output_dir = Path(decisions_output_dir)
        
        self.specs_output_dir.mkdir(parents=True, exist_ok=True)
        self.decisions_output_dir.mkdir(parents=True, exist_ok=True)
        
        self.workflow_state: Dict = {
            'user_input': None,
            'research_topics': [],
            'evidence_ids': [],
            'decisions': [],
            'specifications': []
        }
    
    def process_user_input(self, user_input: str) -> Dict:
        """
        Process raw user input and orchestrate the RJW-IDD workflow.
        
        This method enforces the correct sequence:
        1. Parse user intent and extract research topics
        2. Delegate to ResearchHarvester to gather evidence
        3. Create decision records backed by evidence
        4. Generate specifications backed by decisions and evidence
        
        Args:
            user_input: Raw natural language input from user
            
        Returns:
            Dictionary containing workflow results:
            - research_topics: List of identified topics
            - evidence_ids: List of generated EVD IDs
            - recommendations: Next steps for the user
            
        Raises:
            ValueError: If user input is empty or invalid
        """
        if not user_input or not user_input.strip():
            raise ValueError("User input cannot be empty")
        
        self.workflow_state['user_input'] = user_input
        
        # Step 1: Extract research topics from user input
        research_topics = self._extract_research_topics(user_input)
        self.workflow_state['research_topics'] = research_topics
        
        # Step 2: Conduct research for each topic (gather evidence first!)
        evidence_ids = []
        for topic in research_topics:
            evd_id = self.research_harvester.harvest(
                topic=topic,
                source_type="User Request Analysis",
                curator="PromptOptimizer"
            )
            evidence_ids.append(evd_id)
        
        self.workflow_state['evidence_ids'] = evidence_ids
        
        # Step 3: Return results and recommendations
        return {
            'status': 'research_complete',
            'research_topics': research_topics,
            'evidence_ids': evidence_ids,
            'recommendations': self._generate_recommendations(user_input, evidence_ids),
            'next_steps': [
                'Review generated evidence files',
                'Create decision records (DEC) referencing evidence',
                'Generate specifications (SPEC) backed by decisions',
                'Write tests (TEST) to verify specifications'
            ]
        }
    
    def _extract_research_topics(self, user_input: str) -> List[str]:
        """
        Extract research topics from user input.
        
        Uses the LLM to analyze user input and identify key research topics
        when available. Falls back to keyword-based extraction if LLM is not available.
        
        Args:
            user_input: User's natural language input
            
        Returns:
            List of research topics
        """
        # Try to use LLM for intelligent topic extraction
        if self.llm_provider:
            try:
                prompt = f"""Analyze this user request and extract 1-3 key technical topics that would need research:

User request: "{user_input}"

Return a JSON array of topics (strings). Each topic should be specific and researchable.
Example: ["authentication patterns", "database design", "API security"]"""
                
                schema = {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Array of research topics"
                }
                
                result = self.llm_provider.generate_json(prompt, schema)
                
                # Extract topics from result
                if isinstance(result, dict) and 'topics' in result:
                    topics = result['topics']
                elif isinstance(result, list):
                    topics = result
                else:
                    # Try to find a list in the result
                    for key, value in result.items():
                        if isinstance(value, list) and len(value) > 0:
                            topics = value
                            break
                    else:
                        topics = []
                
                if topics and len(topics) > 0:
                    return topics[:3]  # Limit to 3 topics
            except Exception as e:
                # Fall back to keyword-based extraction on error
                import warnings
                warnings.warn(f"LLM topic extraction failed, falling back to keywords: {e}")
        
        # Fallback: Simple keyword-based extraction
        topics = []
        
        # Look for common patterns
        keywords = [
            'authentication', 'authorization', 'security', 'database',
            'API', 'testing', 'deployment', 'architecture', 'design',
            'performance', 'scalability', 'monitoring', 'logging'
        ]
        
        user_input_lower = user_input.lower()
        for keyword in keywords:
            if keyword in user_input_lower:
                topics.append(keyword)
        
        # If no specific topics found, use the full input as a general topic
        if not topics:
            # Create a general topic from the input
            topics.append(user_input[:50] if len(user_input) > 50 else user_input)
        
        return topics
    
    def process_user_research(self, research_content: str, 
                             user_priority: bool = False,
                             curator: str = "User") -> Dict:
        """
        Process user-provided research and automatically parse/reformat it.
        
        This method:
        1. Detects that user has provided research directly
        2. Automatically parses the research regardless of format
        3. Reformats to EVD-#### standard template
        4. Registers the evidence with appropriate priority
        
        User research receives equal weight as agent research by default.
        User research receives higher weight ONLY when user_priority=True.
        
        Args:
            research_content: User-provided research in any format
            user_priority: If True, user explicitly wants elevated priority (default: False)
            curator: Name of person providing research
            
        Returns:
            Dictionary containing:
            - evd_id: Generated evidence ID
            - status: Processing status
            - user_priority: Whether elevated priority was set
            - message: Success message
            
        Raises:
            ValueError: If research_content is empty
        """
        if not research_content or not research_content.strip():
            raise ValueError("User research content cannot be empty")
        
        # Harvest user research using automatic parsing and reformatting
        evd_id = self.research_harvester.harvest_user_research(
            raw_input=research_content,
            user_priority=user_priority,
            curator=curator
        )
        
        # Update workflow state
        self.workflow_state['evidence_ids'].append(evd_id)
        
        priority_msg = "elevated priority (user-specified)" if user_priority else "standard priority (equal weight)"
        
        return {
            'status': 'user_research_processed',
            'evd_id': evd_id,
            'user_priority': user_priority,
            'priority_explanation': priority_msg,
            'message': f"User research automatically parsed and formatted as {evd_id} with {priority_msg}.",
            'note': "User-provided research has been reformatted to EVD template structure while preserving all original content."
        }
    
    def _generate_recommendations(self, user_input: str, evidence_ids: List[str]) -> str:
        """
        Generate recommendations based on research findings.
        
        Args:
            user_input: Original user input
            evidence_ids: List of evidence IDs generated
            
        Returns:
            Recommendation text
        """
        return f"""
Based on your request: "{user_input[:100]}..."

Evidence has been gathered and documented in:
{chr(10).join([f'  - {evd_id}' for evd_id in evidence_ids])}

Next, you should:
1. Review the evidence files to understand the research findings
2. Create decision records (DEC) that reference this evidence
3. Write specifications (SPEC) based on your decisions
4. Implement tests (TEST) to verify the specifications

Remember: In RJW-IDD, every decision and specification must be backed by evidence!
"""
    
    def create_decision_with_evidence(self, 
                                     decision_title: str,
                                     evidence_refs: List[str],
                                     options: List[str],
                                     chosen_option: str,
                                     rationale: str) -> str:
        """
        Create a decision record that references evidence.
        
        This enforces the constraint: No DEC can be created without EVD references.
        
        Args:
            decision_title: Title of the decision
            evidence_refs: List of EVD IDs supporting this decision
            options: List of considered options
            chosen_option: The option that was chosen
            rationale: Rationale for the choice
            
        Returns:
            Decision ID (e.g., 'DEC-0001')
            
        Raises:
            ValueError: If evidence references are invalid
        """
        # Enforce evidence requirement
        self.research_harvester.require_evidence_for_artifact('DEC', evidence_refs)
        
        # Generate decision ID
        existing_decs = [d['id'] for d in self.workflow_state['decisions']]
        dec_id = self.template_manager.generate_artifact_id('DEC', existing_decs)
        
        # Store decision metadata
        decision_data = {
            'id': dec_id,
            'title': decision_title,
            'evidence_refs': evidence_refs,
            'options': options,
            'chosen': chosen_option,
            'rationale': rationale
        }
        self.workflow_state['decisions'].append(decision_data)
        
        return dec_id
    
    def create_spec_with_traceability(self,
                                     spec_title: str,
                                     evidence_refs: List[str],
                                     decision_refs: List[str],
                                     requirements: List[str]) -> str:
        """
        Create a specification with full traceability.
        
        This enforces: SPEC must reference EVD and may reference DEC.
        
        Args:
            spec_title: Title of the specification
            evidence_refs: List of EVD IDs supporting this spec
            decision_refs: List of DEC IDs this spec implements
            requirements: List of requirements this spec addresses
            
        Returns:
            Specification ID (e.g., 'SPEC-0001')
            
        Raises:
            ValueError: If evidence references are invalid
        """
        # Enforce evidence requirement
        self.research_harvester.require_evidence_for_artifact('SPEC', evidence_refs)
        
        # Generate spec ID
        existing_specs = [s['id'] for s in self.workflow_state['specifications']]
        spec_id = self.template_manager.generate_artifact_id('SPEC', existing_specs)
        
        # Store spec metadata
        spec_data = {
            'id': spec_id,
            'title': spec_title,
            'evidence_refs': evidence_refs,
            'decision_refs': decision_refs,
            'requirements': requirements
        }
        self.workflow_state['specifications'].append(spec_data)
        
        return spec_id
    
    def get_workflow_summary(self) -> Dict:
        """
        Get a summary of the current workflow state.
        
        Returns:
            Dictionary with workflow state information
        """
        return {
            'user_input': self.workflow_state['user_input'],
            'research_topics_count': len(self.workflow_state['research_topics']),
            'evidence_count': len(self.workflow_state['evidence_ids']),
            'decisions_count': len(self.workflow_state['decisions']),
            'specifications_count': len(self.workflow_state['specifications']),
            'evidence_ids': self.workflow_state['evidence_ids'],
            'decision_ids': [d['id'] for d in self.workflow_state['decisions']],
            'spec_ids': [s['id'] for s in self.workflow_state['specifications']]
        }
