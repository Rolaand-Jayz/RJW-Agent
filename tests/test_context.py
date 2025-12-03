"""Tests for the Context Engine module."""
import pytest
import tempfile
import shutil
from pathlib import Path
from src.context.engine import ContextCurator, ASTAnalyzer, DependencyGraph, CodeElement


class TestASTAnalyzer:
    """Test suite for ASTAnalyzer class."""
    
    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory for tests."""
        temp = tempfile.mkdtemp()
        yield temp
        shutil.rmtree(temp)
    
    @pytest.fixture
    def analyzer(self):
        """Create an ASTAnalyzer instance."""
        return ASTAnalyzer()
    
    def test_analyze_file_with_class(self, analyzer, temp_dir):
        """Test analyzing a file with a class."""
        test_file = Path(temp_dir) / "test_class.py"
        test_file.write_text('''
class TestClass:
    """A test class."""
    def method(self):
        pass
''')
        
        elements = analyzer.analyze_file(str(test_file))
        
        # Should find the class and method
        assert len(elements) >= 1
        class_element = next(e for e in elements if e.type == 'class')
        assert class_element.name == 'TestClass'
        assert class_element.docstring == 'A test class.'
    
    def test_analyze_file_with_function(self, analyzer, temp_dir):
        """Test analyzing a file with a function."""
        test_file = Path(temp_dir) / "test_func.py"
        test_file.write_text('''
def my_function(arg1, arg2):
    """A test function."""
    return arg1 + arg2
''')
        
        elements = analyzer.analyze_file(str(test_file))
        
        # Should find the function
        assert len(elements) >= 1
        func_element = next(e for e in elements if e.type == 'function')
        assert func_element.name == 'my_function'
        assert 'arg1' in func_element.signature
        assert 'arg2' in func_element.signature
    
    def test_analyze_invalid_file(self, analyzer):
        """Test analyzing a non-existent file."""
        elements = analyzer.analyze_file("/nonexistent/file.py")
        assert elements == []


class TestDependencyGraph:
    """Test suite for DependencyGraph class."""
    
    @pytest.fixture
    def graph(self):
        """Create a DependencyGraph instance."""
        return DependencyGraph()
    
    def test_add_node(self, graph):
        """Test adding nodes to the graph."""
        element = CodeElement(
            name="TestClass",
            type="class",
            file_path="/test/file.py",
            line_start=1,
            line_end=10
        )
        
        node_id = graph.add_node(element)
        assert node_id == "/test/file.py::TestClass"
        assert node_id in graph.nodes
    
    def test_add_edge(self, graph):
        """Test adding edges to the graph."""
        elem1 = CodeElement("Class1", "class", "/test/file1.py", 1, 10)
        elem2 = CodeElement("Class2", "class", "/test/file2.py", 1, 10)
        
        id1 = graph.add_node(elem1)
        id2 = graph.add_node(elem2)
        
        graph.add_edge(id1, id2)
        
        assert id2 in graph.edges[id1]
    
    def test_get_dependencies(self, graph):
        """Test getting dependencies."""
        elem1 = CodeElement("A", "class", "/test/a.py", 1, 10)
        elem2 = CodeElement("B", "class", "/test/b.py", 1, 10)
        elem3 = CodeElement("C", "class", "/test/c.py", 1, 10)
        
        id1 = graph.add_node(elem1)
        id2 = graph.add_node(elem2)
        id3 = graph.add_node(elem3)
        
        # A -> B -> C
        graph.add_edge(id1, id2)
        graph.add_edge(id2, id3)
        
        # Depth 1: should get B
        deps1 = graph.get_dependencies(id1, depth=1)
        assert id2 in deps1
        assert id3 not in deps1
        
        # Depth 2: should get B and C
        deps2 = graph.get_dependencies(id1, depth=2)
        assert id2 in deps2
        assert id3 in deps2
    
    def test_find_related(self, graph):
        """Test finding related nodes."""
        elem1 = CodeElement("AuthManager", "class", "/test/auth.py", 1, 10)
        elem2 = CodeElement("AuthHelper", "class", "/test/helper.py", 1, 10)
        elem1.dependencies.add("AuthHelper")
        
        id1 = graph.add_node(elem1)
        id2 = graph.add_node(elem2)
        
        # Find nodes related to "Auth"
        related = graph.find_related("Auth")
        assert len(related) >= 2


class TestContextCurator:
    """Test suite for ContextCurator class."""
    
    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory for tests."""
        temp = tempfile.mkdtemp()
        # Create some test Python files
        test_file1 = Path(temp) / "module1.py"
        test_file1.write_text('''
class MyClass:
    """A test class."""
    def my_method(self):
        pass
''')
        
        test_file2 = Path(temp) / "module2.py"
        test_file2.write_text('''
def my_function():
    """A test function."""
    return 42
''')
        
        yield temp
        shutil.rmtree(temp)
    
    @pytest.fixture
    def curator(self, temp_dir):
        """Create a ContextCurator instance."""
        return ContextCurator(temp_dir)
    
    def test_initialization_scans_project(self, curator):
        """Test that initialization scans the project."""
        stats = curator.get_project_structure()
        assert stats['files_analyzed'] > 0
        assert stats['total_elements'] > 0
    
    def test_find_related_code(self, curator):
        """Test finding related code."""
        related = curator.find_related_code("MyClass")
        
        # Should find the class
        assert len(related) > 0
        assert any(e.name == "MyClass" for e in related)
    
    def test_extract_signature(self, curator):
        """Test extracting code signatures."""
        element = CodeElement(
            name="TestFunc",
            type="function",
            file_path="/test.py",
            line_start=1,
            line_end=5,
            signature="def TestFunc(arg1, arg2)",
            docstring="A test function."
        )
        
        signature = curator.extract_signature(element)
        assert "def TestFunc(arg1, arg2)" in signature
        assert "A test function." in signature
    
    def test_build_context_index(self, curator):
        """Test building a context index."""
        ctx_id = curator.build_context_index(
            task_id="TASK-001",
            focus_areas=["MyClass", "my_function"]
        )
        
        assert ctx_id == "CTX-TASK-001"
        
        # Retrieve the context
        context = curator.get_context(ctx_id)
        assert context is not None
        assert context['task_id'] == "TASK-001"
        assert len(context['focus_areas']) == 2
        assert len(context['related_files']) > 0
    
    def test_slice_code(self, curator, temp_dir):
        """Test slicing code from a file."""
        test_file = Path(temp_dir) / "module1.py"
        
        sliced = curator.slice_code(str(test_file), ["MyClass"])
        
        assert "MyClass" in sliced
        assert "class MyClass" in sliced["MyClass"]
    
    def test_get_project_structure(self, curator):
        """Test getting project structure stats."""
        stats = curator.get_project_structure()
        
        assert 'files_analyzed' in stats
        assert 'classes' in stats
        assert 'functions' in stats
        assert 'total_elements' in stats
        assert stats['total_elements'] > 0
