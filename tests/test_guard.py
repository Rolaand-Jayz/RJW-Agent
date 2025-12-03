"""Tests for the System Guard module."""
import pytest
import tempfile
import shutil
from pathlib import Path
from src.system.guard import SystemGuard, GuardViolation, TraceabilityChain, OperationType


class TestTraceabilityChain:
    """Test suite for TraceabilityChain class."""
    
    @pytest.fixture
    def chain(self):
        """Create a TraceabilityChain instance."""
        return TraceabilityChain()
    
    def test_register_evidence(self, chain):
        """Test registering evidence."""
        chain.register_evidence("EVD-0001", "/path/to/evd.md")
        assert "EVD-0001" in chain.evidence_files
    
    def test_register_spec_with_valid_evidence(self, chain):
        """Test registering spec with valid evidence."""
        chain.register_evidence("EVD-0001", "/path/to/evd.md")
        chain.register_spec("SPEC-0001", ["EVD-0001"])
        
        assert "SPEC-0001" in chain.spec_files
        assert chain.spec_files["SPEC-0001"] == ["EVD-0001"]
    
    def test_register_spec_without_evidence_raises_error(self, chain):
        """Test that registering spec without evidence raises error."""
        with pytest.raises(GuardViolation, match="Invalid evidence references"):
            chain.register_spec("SPEC-0001", ["EVD-9999"])
    
    def test_register_test_with_valid_spec(self, chain):
        """Test registering test with valid spec."""
        chain.register_evidence("EVD-0001", "/path/to/evd.md")
        chain.register_spec("SPEC-0001", ["EVD-0001"])
        chain.register_test("TEST-0001", ["SPEC-0001"], status="failing")
        
        assert "TEST-0001" in chain.test_files
        assert chain.test_files["TEST-0001"]["status"] == "failing"
    
    def test_register_test_without_spec_raises_error(self, chain):
        """Test that registering test without spec raises error."""
        with pytest.raises(GuardViolation, match="Invalid spec references"):
            chain.register_test("TEST-0001", ["SPEC-9999"])
    
    def test_link_code_to_test(self, chain):
        """Test linking code to test."""
        chain.register_evidence("EVD-0001", "/path/to/evd.md")
        chain.register_spec("SPEC-0001", ["EVD-0001"])
        chain.register_test("TEST-0001", ["SPEC-0001"])
        
        chain.link_code_to_test("/code/file.py", ["TEST-0001"])
        assert "/code/file.py" in chain.code_files
    
    def test_link_code_without_test_raises_error(self, chain):
        """Test that linking code without test raises error."""
        with pytest.raises(GuardViolation, match="Invalid test references"):
            chain.link_code_to_test("/code/file.py", ["TEST-9999"])
    
    def test_validate_chain_complete(self, chain):
        """Test validating a complete traceability chain."""
        # Build complete chain
        chain.register_evidence("EVD-0001", "/path/to/evd.md")
        chain.register_spec("SPEC-0001", ["EVD-0001"])
        chain.register_test("TEST-0001", ["SPEC-0001"], status="failing")
        chain.link_code_to_test("/code/file.py", ["TEST-0001"])
        
        # Should validate successfully
        assert chain.validate_chain("/code/file.py") is True
    
    def test_validate_chain_no_test_raises_error(self, chain):
        """Test that validation fails if code has no test."""
        with pytest.raises(GuardViolation, match="has no linked tests"):
            chain.validate_chain("/code/file.py")
    
    def test_validate_chain_test_no_spec_raises_error(self, chain):
        """Test that validation fails if test has no spec."""
        chain.register_test("TEST-0001", [], status="failing")
        chain.link_code_to_test("/code/file.py", ["TEST-0001"])
        
        with pytest.raises(GuardViolation, match="has no linked specifications"):
            chain.validate_chain("/code/file.py")
    
    def test_validate_chain_spec_no_evidence_raises_error(self, chain):
        """Test that validation fails if spec has no evidence."""
        chain.register_spec("SPEC-0001", [])
        chain.register_test("TEST-0001", ["SPEC-0001"])
        chain.link_code_to_test("/code/file.py", ["TEST-0001"])
        
        with pytest.raises(GuardViolation, match="has no evidence references"):
            chain.validate_chain("/code/file.py")
    
    def test_get_chain_info(self, chain):
        """Test getting chain information."""
        chain.register_evidence("EVD-0001", "/path/to/evd.md")
        chain.register_spec("SPEC-0001", ["EVD-0001"])
        chain.register_test("TEST-0001", ["SPEC-0001"])
        chain.link_code_to_test("/code/file.py", ["TEST-0001"])
        
        info = chain.get_chain_info("/code/file.py")
        assert info['code_file'] == "/code/file.py"
        assert len(info['tests']) == 1
        assert info['tests'][0]['test_id'] == "TEST-0001"


class TestSystemGuard:
    """Test suite for SystemGuard class."""
    
    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory for tests."""
        temp = tempfile.mkdtemp()
        yield temp
        shutil.rmtree(temp)
    
    @pytest.fixture
    def guard(self):
        """Create a SystemGuard instance in strict mode."""
        return SystemGuard(strict_mode=True)
    
    @pytest.fixture
    def guard_relaxed(self):
        """Create a SystemGuard instance with strict mode off."""
        return SystemGuard(strict_mode=False)
    
    def test_register_evidence(self, guard):
        """Test registering evidence with guard."""
        guard.register_evidence("EVD-0001", "/path/to/evd.md")
        assert "EVD-0001" in guard.traceability_chain.evidence_files
    
    def test_register_spec(self, guard):
        """Test registering spec with guard."""
        guard.register_evidence("EVD-0001", "/path/to/evd.md")
        guard.register_spec("SPEC-0001", ["EVD-0001"], "/path/to/spec.md")
        
        assert "SPEC-0001" in guard.traceability_chain.spec_files
    
    def test_register_test(self, guard):
        """Test registering test with guard."""
        guard.register_evidence("EVD-0001", "/path/to/evd.md")
        guard.register_spec("SPEC-0001", ["EVD-0001"], "/path/to/spec.md")
        guard.register_test("TEST-0001", ["SPEC-0001"], "/path/to/test.py")
        
        assert "TEST-0001" in guard.traceability_chain.test_files
    
    def test_write_code_with_valid_chain(self, guard, temp_dir):
        """Test writing code with a valid traceability chain."""
        # Build complete chain
        guard.register_evidence("EVD-0001", "/path/to/evd.md")
        guard.register_spec("SPEC-0001", ["EVD-0001"], "/path/to/spec.md")
        guard.register_test("TEST-0001", ["SPEC-0001"], "/path/to/test.py", "failing")
        
        # Write code
        code_file = str(Path(temp_dir) / "code.py")
        result = guard.write_code(
            code_file=code_file,
            content="def my_function():\n    pass\n",
            test_refs=["TEST-0001"]
        )
        
        assert result is True
        assert Path(code_file).exists()
    
    def test_write_code_without_test_raises_error(self, guard, temp_dir):
        """Test that writing code without test raises error."""
        code_file = str(Path(temp_dir) / "code.py")
        
        with pytest.raises(GuardViolation, match="Invalid test references"):
            guard.write_code(
                code_file=code_file,
                content="def my_function():\n    pass\n",
                test_refs=["TEST-9999"]
            )
    
    def test_write_code_relaxed_mode(self, guard_relaxed, temp_dir):
        """Test that writing code works in relaxed mode without chain."""
        code_file = str(Path(temp_dir) / "code.py")
        
        # Should work even without proper chain
        result = guard_relaxed.write_code(
            code_file=code_file,
            content="def my_function():\n    pass\n",
            test_refs=[]
        )
        
        assert result is True
    
    def test_read_file(self, guard, temp_dir):
        """Test reading files."""
        test_file = Path(temp_dir) / "test.txt"
        test_file.write_text("Test content")
        
        content = guard.read_file(str(test_file))
        assert content == "Test content"
    
    def test_get_traceability_info(self, guard):
        """Test getting traceability info."""
        guard.register_evidence("EVD-0001", "/path/to/evd.md")
        guard.register_spec("SPEC-0001", ["EVD-0001"], "/path/to/spec.md")
        guard.register_test("TEST-0001", ["SPEC-0001"], "/path/to/test.py")
        guard.traceability_chain.link_code_to_test("/code/file.py", ["TEST-0001"])
        
        info = guard.get_traceability_info("/code/file.py")
        assert 'code_file' in info
        assert len(info['tests']) == 1
    
    def test_operation_logging(self, guard):
        """Test that operations are logged."""
        guard.register_evidence("EVD-0001", "/path/to/evd.md")
        
        log = guard.get_operation_log()
        assert len(log) > 0
        assert any(entry['operation'] == 'create' for entry in log)
    
    def test_set_strict_mode(self, guard):
        """Test toggling strict mode."""
        assert guard.strict_mode is True
        
        guard.set_strict_mode(False)
        assert guard.strict_mode is False
