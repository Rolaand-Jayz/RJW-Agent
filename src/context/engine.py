"""
Programmatic Context Engine Module

Implements the ContextCurator class for managing context through static analysis.
This follows METHOD-0006 Context Curation Engine principles.
"""
import ast
import os
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple
from dataclasses import dataclass, field


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
    Programmatic Context Engine that uses static analysis to curate context.
    
    This class implements METHOD-0006 principles:
    - Static analysis (AST/Dependency Graphing) to find related code
    - Code slicing: Extract specific class/function signatures, not full files
    - CTX-INDEX building programmatically
    - No LLM-based selection (pure static analysis)
    
    Attributes:
        project_root: Root directory of the project
        ast_analyzer: AST-based code analyzer
        dependency_graph: Dependency graph of code elements
        context_index: Current context index
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
        self.context_index: Dict[str, List[str]] = {}
        
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
    
    def build_context_index(self, task_id: str, focus_areas: List[str]) -> str:
        """
        Build a CTX-INDEX programmatically for a specific task.
        
        This creates a context index following METHOD-0006 template:
        - Lists in-scope files based on static analysis
        - Documents key decisions and assumptions
        - Tracks dependencies
        
        Args:
            task_id: Unique identifier for the task
            focus_areas: List of code areas relevant to the task
            
        Returns:
            CTX-INDEX identifier
        """
        ctx_id = f"CTX-{task_id}"
        
        # Find all related code for each focus area
        related_files = set()
        signatures = []
        
        for focus in focus_areas:
            elements = self.find_related_code(focus)
            for element in elements:
                related_files.add(element.file_path)
                signatures.append(self.extract_signature(element))
        
        # Store in context index
        self.context_index[ctx_id] = {
            'task_id': task_id,
            'focus_areas': focus_areas,
            'related_files': list(related_files),
            'signatures': signatures,
            'created': 'programmatically',
            'method': 'static_analysis'
        }
        
        return ctx_id
    
    def get_context(self, ctx_id: str) -> Optional[Dict]:
        """
        Retrieve a context index by ID.
        
        Args:
            ctx_id: Context index ID
            
        Returns:
            Context index data or None
        """
        return self.context_index.get(ctx_id)
    
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
