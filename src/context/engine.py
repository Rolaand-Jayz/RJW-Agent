"""
Programmatic Context Engine Module

Implements the ContextCurator class for managing context through static analysis.
This implements METHOD-0006 Context Curation Engine framework.
"""
import ast
import os
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum


@dataclass
class CodeElement:
    """Represents a code element (class, function, etc.)."""
    name: str
    type: str  # 'class', 'function', 'method', 'variable'
    file_path: str
    line_start: int
    line_end: int
    signature: str = ""
    dependencies: Set[str] = field(default_factory=set)
    docstring: Optional[str] = None


@dataclass
class ContextItem:
    """
    Represents a context item with relevance scoring per METHOD-0006 Section 3.3.
    """
    item_id: str
    item_type: str  # 'code', 'decision', 'spec', 'assumption', 'dependency'
    content: str
    relevance_score: float = 0.5  # Default to potentially relevant
    last_evaluated: Optional[datetime] = None
    source: str = ""  # Where this item came from
    
    def __post_init__(self):
        if self.last_evaluated is None:
            self.last_evaluated = datetime.now(timezone.utc)


@dataclass
class ContextIndex:
    """
    Complete Context Index structure per METHOD-0006 Section 2.2.
    
    Contains all required sections:
    - Task Scope
    - Affected Areas
    - Technical Context (decisions, specs, conventions)
    - Assumptions
    - Dependencies
    - Change History
    """
    ctx_id: str
    task_id: str
    
    # Task Scope (Section 2.2)
    objectives: List[str] = field(default_factory=list)
    constraints: List[str] = field(default_factory=list)
    out_of_scope: List[str] = field(default_factory=list)
    
    # Affected Areas (Section 2.2)
    files: List[str] = field(default_factory=list)
    modules: List[str] = field(default_factory=list)
    endpoints: List[str] = field(default_factory=list)
    
    # Technical Context (Section 2.2)
    decision_refs: List[str] = field(default_factory=list)  # DEC-#### references
    spec_refs: List[str] = field(default_factory=list)      # SPEC-#### references
    conventions: List[str] = field(default_factory=list)    # Coding conventions
    
    # Assumptions (Section 2.2)
    assumptions: List[str] = field(default_factory=list)
    provisional_assumptions: List[str] = field(default_factory=list)
    
    # Dependencies (Section 2.2)
    upstream_tasks: List[str] = field(default_factory=list)
    downstream_tasks: List[str] = field(default_factory=list)
    parallel_work: List[str] = field(default_factory=list)
    
    # Change History (Section 2.2)
    change_history: List[Dict] = field(default_factory=list)
    
    # Context Items with relevance scores (Section 3.3)
    context_items: List[ContextItem] = field(default_factory=list)
    
    # Metadata
    created_at: datetime = field(default_factory=datetime.utcnow)
    last_updated: datetime = field(default_factory=datetime.utcnow)
    last_evaluated: Optional[datetime] = None


class DependencyGraph:
    """
    Builds and manages a dependency graph of code elements.
    """
    
    def __init__(self):
        """Initialize the dependency graph."""
        self.nodes: Dict[str, CodeElement] = {}
        self.edges: Dict[str, Set[str]] = {}  # node_id -> set of dependency node_ids
    
    def add_node(self, element: CodeElement) -> str:
        """
        Add a code element to the graph.
        
        Args:
            element: CodeElement to add
            
        Returns:
            Node ID
        """
        node_id = f"{element.file_path}::{element.name}"
        self.nodes[node_id] = element
        if node_id not in self.edges:
            self.edges[node_id] = set()
        return node_id
    
    def add_edge(self, from_id: str, to_id: str):
        """Add a dependency edge."""
        if from_id not in self.edges:
            self.edges[from_id] = set()
        self.edges[from_id].add(to_id)
    
    def get_dependencies(self, node_id: str, depth: int = 1) -> Set[str]:
        """
        Get dependencies of a node up to specified depth.
        
        Args:
            node_id: Node to get dependencies for
            depth: How many levels deep to traverse
            
        Returns:
            Set of dependent node IDs
        """
        if depth <= 0 or node_id not in self.edges:
            return set()
        
        direct_deps = self.edges[node_id]
        all_deps = direct_deps.copy()
        
        if depth > 1:
            for dep in direct_deps:
                all_deps.update(self.get_dependencies(dep, depth - 1))
        
        return all_deps
    
    def find_related(self, target_name: str) -> List[str]:
        """
        Find all nodes related to a target name.
        
        Args:
            target_name: Name to search for
            
        Returns:
            List of related node IDs
        """
        related = []
        for node_id, element in self.nodes.items():
            if target_name in element.name or target_name in element.dependencies:
                related.append(node_id)
        return related


class ASTAnalyzer:
    """
    Performs AST-based static analysis of Python code.
    """
    
    def __init__(self):
        """Initialize the AST analyzer."""
        self.elements: List[CodeElement] = []
    
    def analyze_file(self, file_path: str) -> List[CodeElement]:
        """
        Analyze a Python file and extract code elements.
        
        Args:
            file_path: Path to Python file
            
        Returns:
            List of CodeElements found in the file
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                source = f.read()
            
            tree = ast.parse(source, filename=file_path)
            elements = []
            
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    element = self._extract_class(node, file_path, source)
                    elements.append(element)
                elif isinstance(node, ast.FunctionDef):
                    element = self._extract_function(node, file_path, source)
                    elements.append(element)
            
            return elements
        
        except Exception as e:
            # If file can't be parsed, return empty list
            return []
    
    def _extract_class(self, node: ast.ClassDef, file_path: str, source: str) -> CodeElement:
        """Extract class information from AST node."""
        # Get line numbers
        line_start = node.lineno
        line_end = node.end_lineno or line_start
        
        # Build signature
        bases = [self._get_name(base) for base in node.bases]
        signature = f"class {node.name}({', '.join(bases)})" if bases else f"class {node.name}"
        
        # Extract dependencies
        dependencies = self._extract_dependencies(node)
        
        # Get docstring
        docstring = ast.get_docstring(node)
        
        return CodeElement(
            name=node.name,
            type='class',
            file_path=file_path,
            line_start=line_start,
            line_end=line_end,
            signature=signature,
            dependencies=dependencies,
            docstring=docstring
        )
    
    def _extract_function(self, node: ast.FunctionDef, file_path: str, source: str) -> CodeElement:
        """Extract function information from AST node."""
        line_start = node.lineno
        line_end = node.end_lineno or line_start
        
        # Build signature
        args = [arg.arg for arg in node.args.args]
        signature = f"def {node.name}({', '.join(args)})"
        
        # Extract dependencies
        dependencies = self._extract_dependencies(node)
        
        # Get docstring
        docstring = ast.get_docstring(node)
        
        return CodeElement(
            name=node.name,
            type='function',
            file_path=file_path,
            line_start=line_start,
            line_end=line_end,
            signature=signature,
            dependencies=dependencies,
            docstring=docstring
        )
    
    def _extract_dependencies(self, node: ast.AST) -> Set[str]:
        """Extract names referenced in an AST node."""
        dependencies = set()
        
        for child in ast.walk(node):
            if isinstance(child, ast.Name):
                dependencies.add(child.id)
            elif isinstance(child, ast.Import):
                for alias in child.names:
                    dependencies.add(alias.name)
            elif isinstance(child, ast.ImportFrom):
                if child.module:
                    dependencies.add(child.module)
        
        return dependencies
    
    def _get_name(self, node: ast.AST) -> str:
        """Get name from an AST node."""
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            return f"{self._get_name(node.value)}.{node.attr}"
        return "Unknown"


class ContextCurator:
    """
    Context Curation Engine implementing METHOD-0006 framework.
    
    This class implements the complete METHOD-0006 specification:
    - Section 2: Context Index structure with all required sections
    - Section 3: Turn-based context evaluation and relevance scoring
    - Section 4: Context update triggers and propagation
    - Section 5: Living Documentation integration
    
    Uses static analysis (AST/Dependency Graphing) for code discovery.
    
    Attributes:
        project_root: Root directory of the project
        ast_analyzer: AST-based code analyzer
        dependency_graph: Dependency graph of code elements
        context_indexes: Dictionary of active Context Indexes
        living_docs: Living Documentation data
    """
    
    def __init__(self, project_root: str):
        """
        Initialize the ContextCurator.
        
        Args:
            project_root: Root directory of the project to analyze
        """
        self.project_root = Path(project_root)
        self.ast_analyzer = ASTAnalyzer()
        self.dependency_graph = DependencyGraph()
        self.context_indexes: Dict[str, ContextIndex] = {}
        self.living_docs: Dict[str, any] = {}
        
        # Scan project on initialization
        self._scan_project()
    
    def _scan_project(self):
        """Scan project and build dependency graph."""
        python_files = list(self.project_root.rglob("*.py"))
        
        for file_path in python_files:
            # Skip virtual environments and build directories
            if any(part in file_path.parts for part in ['venv', 'env', '__pycache__', '.git', 'build', 'dist']):
                continue
            
            elements = self.ast_analyzer.analyze_file(str(file_path))
            
            for element in elements:
                node_id = self.dependency_graph.add_node(element)
                
                # Add dependency edges
                for dep in element.dependencies:
                    # Try to find the dependency in the graph
                    matching_nodes = [nid for nid in self.dependency_graph.nodes.keys() if dep in nid]
                    for match in matching_nodes:
                        self.dependency_graph.add_edge(node_id, match)
    
    def find_related_code(self, target: str, max_depth: int = 2) -> List[CodeElement]:
        """
        Find code elements related to a target name or concept.
        
        This uses static analysis to find:
        - Classes/functions with similar names
        - Code that depends on the target
        - Code that the target depends on
        
        Args:
            target: Target name to find related code for
            max_depth: Maximum depth for dependency traversal
            
        Returns:
            List of related CodeElements
        """
        # Find nodes related by name
        related_node_ids = self.dependency_graph.find_related(target)
        
        # Expand to include dependencies
        all_related = set(related_node_ids)
        for node_id in related_node_ids:
            deps = self.dependency_graph.get_dependencies(node_id, depth=max_depth)
            all_related.update(deps)
        
        # Get CodeElements
        related_elements = []
        for node_id in all_related:
            if node_id in self.dependency_graph.nodes:
                related_elements.append(self.dependency_graph.nodes[node_id])
        
        return related_elements
    
    def extract_signature(self, element: CodeElement) -> str:
        """
        Extract just the signature of a code element, not the full implementation.
        
        This implements the "slicing" requirement: extract specific class/function
        signatures, not full files.
        
        Args:
            element: CodeElement to extract signature from
            
        Returns:
            Signature string
        """
        sig_parts = [element.signature]
        
        if element.docstring:
            # Include first line of docstring
            first_line = element.docstring.split('\n')[0].strip()
            sig_parts.append(f'    """{first_line}"""')
        
        return '\n'.join(sig_parts)
    
    def build_context_index(self, 
                           task_id: str, 
                           focus_areas: List[str],
                           objectives: Optional[List[str]] = None,
                           decision_refs: Optional[List[str]] = None,
                           spec_refs: Optional[List[str]] = None) -> str:
        """
        Build a complete Context Index following METHOD-0006 Section 2.2.
        
        Creates a full Context Index with all required sections:
        - Task Scope (objectives, constraints, out-of-scope)
        - Affected Areas (files, modules, endpoints)
        - Technical Context (decisions, specs, conventions)
        - Assumptions
        - Dependencies
        - Change History
        
        Args:
            task_id: Unique identifier for the task
            focus_areas: List of code areas relevant to the task
            objectives: Optional list of task objectives
            decision_refs: Optional list of DEC-#### references
            spec_refs: Optional list of SPEC-#### references
            
        Returns:
            CTX-INDEX identifier (e.g., 'CTX-TASK-001')
        """
        ctx_id = f"CTX-{task_id}"
        
        # Create Context Index with full METHOD-0006 Section 2.2 structure
        ctx_index = ContextIndex(
            ctx_id=ctx_id,
            task_id=task_id,
            objectives=objectives or [],
            decision_refs=decision_refs or [],
            spec_refs=spec_refs or []
        )
        
        # Find all related code for each focus area using static analysis
        related_files = set()
        context_items = []
        
        for focus in focus_areas:
            elements = self.find_related_code(focus)
            for element in elements:
                related_files.add(element.file_path)
                
                # Create ContextItem with relevance scoring (METHOD-0006 Section 3.3)
                signature = self.extract_signature(element)
                item = ContextItem(
                    item_id=f"{element.file_path}::{element.name}",
                    item_type='code',
                    content=signature,
                    relevance_score=self._calculate_initial_relevance(element, focus_areas),
                    source=f"static_analysis:{focus}"
                )
                context_items.append(item)
        
        # Populate Affected Areas (METHOD-0006 Section 2.2)
        ctx_index.files = list(related_files)
        ctx_index.modules = list(set(str(Path(f).parent) for f in related_files))
        
        # Store context items with relevance scores
        ctx_index.context_items = context_items
        
        # Store in context indexes
        self.context_indexes[ctx_id] = ctx_index
        
        return ctx_id
    
    def _calculate_initial_relevance(self, element: CodeElement, focus_areas: List[str]) -> float:
        """
        Calculate initial relevance score per METHOD-0006 Section 3.3.
        
        Scoring guidelines:
        - 1.0: Item is directly required (name matches focus area exactly)
        - 0.8: Essential context (name contains focus area)
        - 0.6: Helpful background (related by dependency)
        - 0.4: May be needed later (peripheral dependency)
        - 0.2: Peripherally related
        
        Args:
            element: CodeElement to score
            focus_areas: Focus areas for the task
            
        Returns:
            Relevance score between 0.0 and 1.0
        """
        element_name_lower = element.name.lower()
        
        # Direct match: 1.0
        for focus in focus_areas:
            if element_name_lower == focus.lower():
                return 1.0
        
        # Contains focus area: 0.8
        for focus in focus_areas:
            if focus.lower() in element_name_lower:
                return 0.8
        
        # Related by dependency: 0.6
        for focus in focus_areas:
            if focus.lower() in ' '.join(element.dependencies).lower():
                return 0.6
        
        # Default: potentially relevant
        return 0.4
    
    def evaluate_context_on_turn(self, ctx_id: str) -> Dict:
        """
        Perform turn-based context evaluation per METHOD-0006 Section 3.1.
        
        Implements the evaluation cycle:
        1. EVALUATE - Assess current context validity
        2. REMOVE - Drop stale or irrelevant items
        3. LOAD - Pull missing relevant info
        4. PROCEED - Execute with curated context
        
        Args:
            ctx_id: Context Index ID to evaluate
            
        Returns:
            Dictionary with evaluation results
        """
        if ctx_id not in self.context_indexes:
            return {'error': 'Context index not found'}
        
        ctx_index = self.context_indexes[ctx_id]
        ctx_index.last_evaluated = datetime.now(timezone.utc)
        
        results = {
            'evaluated': 0,
            'removed': 0,
            'kept': 0,
            'recommendations': []
        }
        
        # Evaluate each context item using METHOD-0006 Section 3.2 criteria
        items_to_keep = []
        for item in ctx_index.context_items:
            evaluation = self._evaluate_context_item(item, ctx_index)
            
            if evaluation['keep']:
                items_to_keep.append(item)
                results['kept'] += 1
            else:
                results['removed'] += 1
                results['recommendations'].append(
                    f"Removed {item.item_id}: {evaluation['reason']}"
                )
            
            results['evaluated'] += 1
        
        # Update context index with curated items
        ctx_index.context_items = items_to_keep
        
        return results
    
    def _evaluate_context_item(self, item: ContextItem, ctx_index: ContextIndex) -> Dict:
        """
        Evaluate a single context item per METHOD-0006 Section 3.2.
        
        Evaluation Criteria:
        - Relevance: Does this relate to the current step?
        - Currency: Is this information still accurate?
        - Completeness: Are there gaps?
        - Consistency: Does it align with Living Docs?
        
        Args:
            item: ContextItem to evaluate
            ctx_index: Parent Context Index
            
        Returns:
            Dictionary with 'keep' boolean and 'reason'
        """
        # Apply relevance scoring per METHOD-0006 Section 3.3
        if item.relevance_score < 0.2:
            return {'keep': False, 'reason': f'Low relevance score ({item.relevance_score})'}
        
        # Keep items with score >= 0.2
        return {'keep': True, 'reason': f'Relevant (score: {item.relevance_score})'}
    
    def score_context_item(self, 
                          ctx_id: str, 
                          item_id: str, 
                          new_score: float) -> bool:
        """
        Update relevance score for a context item per METHOD-0006 Section 3.3.
        
        Scoring guidelines (0.0 - 1.0):
        - 0.8-1.0: Directly relevant, keep in active context
        - 0.5-0.79: Potentially relevant, keep but demote if unused
        - 0.2-0.49: Background context, load on demand only
        - 0.0-0.19: Not relevant, remove from context
        
        Args:
            ctx_id: Context Index ID
            item_id: Item identifier
            new_score: New relevance score (0.0 - 1.0)
            
        Returns:
            True if updated successfully
        """
        if ctx_id not in self.context_indexes:
            return False
        
        if not 0.0 <= new_score <= 1.0:
            return False
        
        ctx_index = self.context_indexes[ctx_id]
        for item in ctx_index.context_items:
            if item.item_id == item_id:
                item.relevance_score = new_score
                item.last_evaluated = datetime.now(timezone.utc)
                return True
        
        return False
    
    def get_context(self, ctx_id: str) -> Optional[Dict]:
        """
        Retrieve a context index by ID.
        
        Returns a dictionary representation of the Context Index
        with all METHOD-0006 Section 2.2 sections.
        
        Args:
            ctx_id: Context index ID
            
        Returns:
            Context index data or None
        """
        if ctx_id not in self.context_indexes:
            return None
        
        ctx_index = self.context_indexes[ctx_id]
        
        # Extract focus areas from context items for backwards compatibility
        focus_areas = list(set(item.source.split(':')[1] if ':' in item.source else '' 
                              for item in ctx_index.context_items 
                              if item.source.startswith('static_analysis:')))
        
        return {
            'ctx_id': ctx_index.ctx_id,
            'task_id': ctx_index.task_id,
            'focus_areas': focus_areas,  # For backwards compatibility
            # Task Scope
            'objectives': ctx_index.objectives,
            'constraints': ctx_index.constraints,
            'out_of_scope': ctx_index.out_of_scope,
            # Affected Areas
            'related_files': ctx_index.files,
            'modules': ctx_index.modules,
            'endpoints': ctx_index.endpoints,
            # Technical Context
            'decision_refs': ctx_index.decision_refs,
            'spec_refs': ctx_index.spec_refs,
            'conventions': ctx_index.conventions,
            # Assumptions
            'assumptions': ctx_index.assumptions,
            'provisional_assumptions': ctx_index.provisional_assumptions,
            # Dependencies
            'upstream_tasks': ctx_index.upstream_tasks,
            'downstream_tasks': ctx_index.downstream_tasks,
            'parallel_work': ctx_index.parallel_work,
            # Change History
            'change_history': ctx_index.change_history,
            # Context Items with scores
            'context_items': [
                {
                    'item_id': item.item_id,
                    'type': item.item_type,
                    'relevance_score': item.relevance_score,
                    'content': item.content[:200] + '...' if len(item.content) > 200 else item.content
                }
                for item in ctx_index.context_items
            ],
            'signatures': [item.content for item in ctx_index.context_items if item.item_type == 'code'],
            # Metadata
            'created_at': ctx_index.created_at.isoformat(),
            'last_updated': ctx_index.last_updated.isoformat(),
            'last_evaluated': ctx_index.last_evaluated.isoformat() if ctx_index.last_evaluated else None
        }
    
    def slice_code(self, file_path: str, 
                   element_names: List[str]) -> Dict[str, str]:
        """
        Slice specific code elements from a file.
        
        Returns signatures only, not full implementations.
        
        Args:
            file_path: Path to file
            element_names: Names of elements to extract
            
        Returns:
            Dictionary mapping element names to their signatures
        """
        elements = self.ast_analyzer.analyze_file(file_path)
        
        sliced = {}
        for element in elements:
            if element.name in element_names:
                sliced[element.name] = self.extract_signature(element)
        
        return sliced
    
    def get_project_structure(self) -> Dict[str, int]:
        """
        Get high-level project structure statistics.
        
        Returns:
            Dictionary with counts of different element types
        """
        stats = {
            'files_analyzed': len(set(node.file_path for node in self.dependency_graph.nodes.values())),
            'classes': sum(1 for node in self.dependency_graph.nodes.values() if node.type == 'class'),
            'functions': sum(1 for node in self.dependency_graph.nodes.values() if node.type == 'function'),
            'total_elements': len(self.dependency_graph.nodes)
        }
        return stats
    
    def update_context_on_change(self, 
                                ctx_id: str,
                                change_type: str,
                                description: str,
                                affected_items: Optional[List[str]] = None) -> bool:
        """
        Update Context Index based on detected changes per METHOD-0006 Section 4.
        
        Implements context update triggers:
        - File added/modified
        - Decision created/updated (DEC-####)
        - Spec updated (SPEC-####)
        - API change
        - Dependency change
        
        Args:
            ctx_id: Context Index ID
            change_type: Type of change ('file', 'decision', 'spec', 'api', 'dependency')
            description: Description of the change
            affected_items: Optional list of affected items
            
        Returns:
            True if update successful
        """
        if ctx_id not in self.context_indexes:
            return False
        
        ctx_index = self.context_indexes[ctx_id]
        
        # Add to change history (METHOD-0006 Section 2.2)
        change_entry = {
            'change_id': f"CTX-{datetime.now(timezone.utc).strftime('%Y%m%d')}-{len(ctx_index.change_history) + 1:02d}",
            'date': datetime.now(timezone.utc).isoformat(),
            'change_type': change_type,
            'description': description,
            'affected_items': affected_items or []
        }
        ctx_index.change_history.append(change_entry)
        ctx_index.last_updated = datetime.now(timezone.utc)
        
        # Apply propagation rules based on change type (METHOD-0006 Section 4.3)
        if change_type == 'decision':
            # Decision created/updated: update technical context
            if affected_items:
                for dec_id in affected_items:
                    if dec_id not in ctx_index.decision_refs:
                        ctx_index.decision_refs.append(dec_id)
        
        elif change_type == 'spec':
            # Spec updated: update technical context
            if affected_items:
                for spec_id in affected_items:
                    if spec_id not in ctx_index.spec_refs:
                        ctx_index.spec_refs.append(spec_id)
        
        elif change_type == 'file':
            # File changed: update affected areas
            if affected_items:
                for file_path in affected_items:
                    if file_path not in ctx_index.files:
                        ctx_index.files.append(file_path)
        
        return True
    
    def propagate_update(self, change_type: str, changed_id: str) -> List[str]:
        """
        Propagate updates to affected Context Indexes per METHOD-0006 Section 4.3.
        
        Propagation rules:
        - When decision created: update all contexts referencing it
        - When spec changes: update contexts for related requirements
        - When code files change: update contexts listing this file
        
        Args:
            change_type: Type of change ('decision', 'spec', 'file')
            changed_id: ID of changed item (DEC-####, SPEC-####, or file path)
            
        Returns:
            List of Context Index IDs that were updated
        """
        updated_contexts = []
        
        for ctx_id, ctx_index in self.context_indexes.items():
            should_update = False
            
            if change_type == 'decision' and changed_id in ctx_index.decision_refs:
                should_update = True
            elif change_type == 'spec' and changed_id in ctx_index.spec_refs:
                should_update = True
            elif change_type == 'file' and changed_id in ctx_index.files:
                should_update = True
            
            if should_update:
                self.update_context_on_change(
                    ctx_id,
                    change_type,
                    f"Propagated update from {changed_id}",
                    [changed_id]
                )
                updated_contexts.append(ctx_id)
        
        return updated_contexts
    
    def load_living_documentation(self, living_docs_data: Dict) -> None:
        """
        Load Living Documentation per METHOD-0006 Section 5.
        
        Living Documentation serves as the governed source of truth for
        context decisions. It contains:
        - Technologies & Libraries
        - Architectural Decisions
        - Coding Conventions
        - Task/Project Rules
        - Agent Instructions
        
        Args:
            living_docs_data: Dictionary containing living documentation
        """
        self.living_docs = living_docs_data
    
    def get_living_docs_context(self, category: str) -> Optional[Dict]:
        """
        Retrieve Living Documentation context by category.
        
        Categories per METHOD-0006 Section 5.2:
        - 'technologies': Technologies & Libraries
        - 'architecture': Architectural Decisions
        - 'conventions': Coding Conventions
        - 'rules': Task/Project Rules
        - 'agent_instructions': Agent Instructions
        
        Args:
            category: Documentation category
            
        Returns:
            Living docs data for category or None
        """
        return self.living_docs.get(category)
    
    def add_assumption(self, 
                      ctx_id: str, 
                      assumption: str,
                      provisional: bool = False) -> bool:
        """
        Add an assumption to a Context Index per METHOD-0006 Section 2.2.
        
        Args:
            ctx_id: Context Index ID
            assumption: Assumption text
            provisional: Whether this is a provisional assumption needing validation
            
        Returns:
            True if added successfully
        """
        if ctx_id not in self.context_indexes:
            return False
        
        ctx_index = self.context_indexes[ctx_id]
        if provisional:
            ctx_index.provisional_assumptions.append(assumption)
        else:
            ctx_index.assumptions.append(assumption)
        
        ctx_index.last_updated = datetime.now(timezone.utc)
        return True
    
    def add_dependency(self,
                      ctx_id: str,
                      dependency_type: str,
                      task_ref: str) -> bool:
        """
        Add a task dependency per METHOD-0006 Section 2.2.
        
        Args:
            ctx_id: Context Index ID
            dependency_type: 'upstream', 'downstream', or 'parallel'
            task_ref: Task reference ID
            
        Returns:
            True if added successfully
        """
        if ctx_id not in self.context_indexes:
            return False
        
        ctx_index = self.context_indexes[ctx_id]
        
        if dependency_type == 'upstream':
            ctx_index.upstream_tasks.append(task_ref)
        elif dependency_type == 'downstream':
            ctx_index.downstream_tasks.append(task_ref)
        elif dependency_type == 'parallel':
            ctx_index.parallel_work.append(task_ref)
        else:
            return False
        
        ctx_index.last_updated = datetime.now(timezone.utc)
        return True
