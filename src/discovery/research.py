"""
Discovery & Research Module

Implements the ResearchHarvester class for gathering evidence and generating
EVD-#### files following RJW-IDD METHOD-0001 Discovery Layer principles.
"""
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
from ..utils import TemplateManager


class ResearchHarvester:
    """
    Harvests research evidence and generates EVD-#### files.
    
    This class enforces METHOD-0001 principles:
    - Evidence must be harvested before decisions are made
    - All facts must be traceable to external sources
    - EVD files must be created before DEC or SPEC files can reference them
    
    Attributes:
        output_dir: Directory where evidence files are saved
        template_manager: Instance of TemplateManager for generating artifacts
        evidence_registry: Registry of harvested evidence IDs
    """
    
    def __init__(self, output_dir: str = "research/evidence", 
                 templates_dir: Optional[str] = None):
        """
        Initialize the ResearchHarvester.
        
        Args:
            output_dir: Directory to save evidence files
            templates_dir: Path to templates directory (optional)
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.template_manager = TemplateManager(templates_dir)
        self.evidence_registry: Dict[str, Dict] = {}
        
        # Load existing evidence files
        self._load_existing_evidence()
    
    def _load_existing_evidence(self):
        """Scan output directory for existing EVD files and register them."""
        if self.output_dir.exists():
            for file_path in self.output_dir.glob("EVD-*.md"):
                evd_id = file_path.stem
                self.evidence_registry[evd_id] = {
                    'path': str(file_path),
                    'loaded': datetime.now()
                }
    
    def harvest(self, 
                topic: str,
                source_type: str = "Research",
                source_url: str = "",
                raw_content: str = "",
                curator: str = "ResearchAgent") -> str:
        """
        Harvest research on a topic and generate an EVD file.
        
        This method simulates or implements research gathering. In a real implementation,
        this would:
        - Query external sources (documentation, forums, papers)
        - Extract relevant information
        - Synthesize key insights
        - Generate a properly formatted EVD file
        
        Args:
            topic: Research topic (e.g., "secure authentication patterns")
            source_type: Type of source (GitHub, Publication, Forum, etc.)
            source_url: URL or reference to source material
            raw_content: Raw content from research (optional)
            curator: Name/role of the curator
            
        Returns:
            Evidence ID (e.g., 'EVD-0001')
            
        Raises:
            ValueError: If topic is empty or invalid
        """
        if not topic or not topic.strip():
            raise ValueError("Topic cannot be empty")
        
        # Generate next evidence ID
        existing_ids = list(self.evidence_registry.keys())
        evd_id = self.template_manager.generate_artifact_id('EVD', existing_ids)
        
        # Simulate research gathering (in production, this would query external sources)
        summary, key_insights = self._conduct_research(topic, raw_content)
        
        # Generate evidence file
        evidence_content = self.template_manager.fill_evidence_template(
            evidence_id=evd_id,
            title=f"Research: {topic}",
            source_type=source_type,
            source_url=source_url or f"Research query: {topic}",
            summary=summary,
            key_insights=key_insights,
            curator=curator
        )
        
        # Save evidence file
        output_path = self.output_dir / f"{evd_id}.md"
        self.template_manager.save_artifact(evidence_content, str(output_path))
        
        # Register evidence
        self.evidence_registry[evd_id] = {
            'topic': topic,
            'path': str(output_path),
            'created': datetime.now(),
            'source_type': source_type,
            'source_url': source_url
        }
        
        return evd_id
    
    def _conduct_research(self, topic: str, raw_content: str = "") -> tuple:
        """
        Conduct research and extract insights.
        
        This is a simulation. In production, this would:
        - Query search engines, documentation sites, GitHub, etc.
        - Use web scraping or APIs to gather information
        - Apply NLP to extract key insights
        - Synthesize findings
        
        Args:
            topic: Research topic
            raw_content: Optional raw content to analyze
            
        Returns:
            Tuple of (summary, key_insights_list)
        """
        # Simulated research output
        if raw_content:
            summary = f"Research findings on '{topic}' based on provided content."
            key_insights = [
                "Content has been analyzed for relevant patterns.",
                "Key concepts extracted from source material.",
                "Findings documented for traceability."
            ]
        else:
            summary = f"Comprehensive research conducted on '{topic}' to establish evidence base."
            key_insights = [
                f"Industry best practices for {topic} have been documented.",
                f"Technical specifications and standards related to {topic} have been reviewed.",
                f"Trade-offs and considerations for {topic} have been identified."
            ]
        
        return summary, key_insights
    
    def get_evidence(self, evd_id: str) -> Optional[Dict]:
        """
        Retrieve evidence information by ID.
        
        Args:
            evd_id: Evidence ID (e.g., 'EVD-0001')
            
        Returns:
            Evidence metadata dictionary or None if not found
        """
        return self.evidence_registry.get(evd_id)
    
    def validate_evidence_exists(self, evd_id: str) -> bool:
        """
        Check if evidence with given ID exists.
        
        This enforces the constraint: No DEC or SPEC can be created
        without referencing a valid EVD ID.
        
        Args:
            evd_id: Evidence ID to validate
            
        Returns:
            True if evidence exists, False otherwise
        """
        return evd_id in self.evidence_registry
    
    def list_evidence(self, topic_filter: Optional[str] = None) -> List[str]:
        """
        List all evidence IDs, optionally filtered by topic.
        
        Args:
            topic_filter: Optional string to filter topics
            
        Returns:
            List of evidence IDs
        """
        if topic_filter:
            return [
                evd_id for evd_id, data in self.evidence_registry.items()
                if 'topic' in data and topic_filter.lower() in data['topic'].lower()
            ]
        return list(self.evidence_registry.keys())
    
    def require_evidence_for_artifact(self, artifact_type: str, 
                                      evidence_refs: List[str]) -> bool:
        """
        Enforce that an artifact references valid evidence.
        
        This implements the core constraint: No DEC or SPEC can be created
        without referencing an EVD ID.
        
        Args:
            artifact_type: Type of artifact being created (DEC, SPEC, etc.)
            evidence_refs: List of evidence IDs being referenced
            
        Returns:
            True if all evidence references are valid
            
        Raises:
            ValueError: If any evidence reference is invalid or missing
        """
        if artifact_type in ['DEC', 'SPEC', 'REQ'] and not evidence_refs:
            raise ValueError(
                f"Cannot create {artifact_type} without evidence references. "
                f"Harvest evidence first using ResearchHarvester.harvest()."
            )
        
        invalid_refs = [ref for ref in evidence_refs if not self.validate_evidence_exists(ref)]
        if invalid_refs:
            raise ValueError(
                f"Invalid evidence references: {invalid_refs}. "
                f"These EVD IDs do not exist. Available: {list(self.evidence_registry.keys())}"
            )
        
        return True
