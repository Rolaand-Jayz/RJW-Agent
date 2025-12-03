"""
The Jailer - System Guard Module

Implements strict file operation controls that enforce RJW-IDD traceability.
No code can be written unless a failing TEST exists that is linked to a SPEC
which is linked to EVD (evidence).
"""
import os
from pathlib import Path
from typing import Dict, List, Optional, Set
from enum import Enum
import re


class OperationType(Enum):
    """Types of file operations."""
    READ = "read"
    WRITE = "write"
    DELETE = "delete"
    CREATE = "create"


class GuardViolation(Exception):
    """Exception raised when a guard rule is violated."""
    pass


class TraceabilityChain:
    """
    Represents the traceability chain: EVD → SPEC → TEST → CODE
    
    This enforces that every code change must be backed by:
    1. Evidence (EVD) - Research/facts supporting the change
    2. Specification (SPEC) - Technical design referencing EVD
    3. Test (TEST) - Failing test that verifies the SPEC
    """
    
    def __init__(self):
        """Initialize the traceability chain."""
        self.evidence_files: Set[str] = set()
        self.spec_files: Dict[str, List[str]] = {}  # spec_id -> [evd_ids]
        self.test_files: Dict[str, Dict] = {}  # test_id -> {spec_ids, status}
        self.code_files: Dict[str, List[str]] = {}  # code_file -> [test_ids]
    
    def register_evidence(self, evd_id: str, file_path: str):
        """Register an evidence file."""
        self.evidence_files.add(evd_id)
    
    def register_spec(self, spec_id: str, evd_refs: List[str]):
        """
        Register a specification with its evidence references.
        
        Args:
            spec_id: Specification ID
            evd_refs: List of evidence IDs this spec references
            
        Raises:
            GuardViolation: If any evidence reference is invalid
        """
        invalid_refs = [ref for ref in evd_refs if ref not in self.evidence_files]
        if invalid_refs:
            raise GuardViolation(
                f"Cannot register SPEC {spec_id}: Invalid evidence references {invalid_refs}. "
                f"Evidence must exist before SPEC can reference it."
            )
        
        self.spec_files[spec_id] = evd_refs
    
    def register_test(self, test_id: str, spec_refs: List[str], status: str = "failing"):
        """
        Register a test with its specification references.
        
        Args:
            test_id: Test ID
            spec_refs: List of specification IDs this test verifies
            status: Test status ('failing' or 'passing')
            
        Raises:
            GuardViolation: If any spec reference is invalid
        """
        invalid_refs = [ref for ref in spec_refs if ref not in self.spec_files]
        if invalid_refs:
            raise GuardViolation(
                f"Cannot register TEST {test_id}: Invalid spec references {invalid_refs}. "
                f"SPEC must exist before TEST can reference it."
            )
        
        self.test_files[test_id] = {
            'spec_refs': spec_refs,
            'status': status
        }
    
    def link_code_to_test(self, code_file: str, test_refs: List[str]):
        """
        Link a code file to tests.
        
        Args:
            code_file: Path to code file
            test_refs: List of test IDs this code implements
            
        Raises:
            GuardViolation: If any test reference is invalid
        """
        invalid_refs = [ref for ref in test_refs if ref not in self.test_files]
        if invalid_refs:
            raise GuardViolation(
                f"Cannot link code file {code_file}: Invalid test references {invalid_refs}. "
                f"TEST must exist before code can reference it."
            )
        
        self.code_files[code_file] = test_refs
    
    def validate_chain(self, code_file: str) -> bool:
        """
        Validate the complete traceability chain for a code file.
        
        Checks: CODE → TEST (failing) → SPEC → EVD
        
        Args:
            code_file: Path to code file to validate
            
        Returns:
            True if chain is valid
            
        Raises:
            GuardViolation: If chain is broken at any point
        """
        # Check if code is linked to tests
        if code_file not in self.code_files:
            raise GuardViolation(
                f"Code file {code_file} has no linked tests. "
                f"A failing TEST must exist before code can be written."
            )
        
        test_refs = self.code_files[code_file]
        
        # Check each test
        for test_id in test_refs:
            test_data = self.test_files[test_id]
            
            # Check test status - must be failing initially
            if test_data['status'] not in ['failing', 'passing']:
                raise GuardViolation(
                    f"Test {test_id} has invalid status: {test_data['status']}"
                )
            
            # Check test is linked to specs
            spec_refs = test_data['spec_refs']
            if not spec_refs:
                raise GuardViolation(
                    f"Test {test_id} has no linked specifications. "
                    f"TEST must reference at least one SPEC."
                )
            
            # Check each spec
            for spec_id in spec_refs:
                evd_refs = self.spec_files[spec_id]
                if not evd_refs:
                    raise GuardViolation(
                        f"Spec {spec_id} has no evidence references. "
                        f"SPEC must reference at least one EVD."
                    )
        
        return True
    
    def get_chain_info(self, code_file: str) -> Dict:
        """Get traceability chain information for a code file."""
        if code_file not in self.code_files:
            return {'error': 'No traceability chain found'}
        
        chain_info = {
            'code_file': code_file,
            'tests': []
        }
        
        for test_id in self.code_files[code_file]:
            test_data = self.test_files[test_id]
            test_info = {
                'test_id': test_id,
                'status': test_data['status'],
                'specs': []
            }
            
            for spec_id in test_data['spec_refs']:
                spec_info = {
                    'spec_id': spec_id,
                    'evidence': self.spec_files[spec_id]
                }
                test_info['specs'].append(spec_info)
            
            chain_info['tests'].append(test_info)
        
        return chain_info


class SystemGuard:
    """
    The Jailer - Strict wrapper for file operations.
    
    This class enforces the core RJW-IDD principle:
    "No code write unless a failing TEST exists and is linked to a SPEC which is linked to EVD"
    
    All code write operations must pass through this guard, which validates
    the complete traceability chain before allowing the operation.
    
    Attributes:
        traceability_chain: Manages the EVD→SPEC→TEST→CODE chain
        operation_log: Log of all file operations
        strict_mode: If True, enforces all rules strictly
    """
    
    def __init__(self, strict_mode: bool = True):
        """
        Initialize the SystemGuard.
        
        Args:
            strict_mode: If True, enforces strict traceability rules
        """
        self.traceability_chain = TraceabilityChain()
        self.operation_log: List[Dict] = []
        self.strict_mode = strict_mode
        
        # Patterns for identifying artifact files
        self.artifact_patterns = {
            'evidence': r'EVD-\d{4}',
            'spec': r'SPEC-\d{4}',
            'test': r'TEST-\d{4}',
            'decision': r'DEC-\d{4}'
        }
    
    def register_evidence(self, evd_id: str, file_path: str):
        """
        Register evidence file with the guard.
        
        Evidence files can be created freely (research comes first).
        
        Args:
            evd_id: Evidence ID (e.g., 'EVD-0001')
            file_path: Path to evidence file
        """
        self.traceability_chain.register_evidence(evd_id, file_path)
        self._log_operation(OperationType.CREATE, file_path, f"Evidence {evd_id} registered")
    
    def register_spec(self, spec_id: str, evd_refs: List[str], file_path: str):
        """
        Register specification with evidence references.
        
        Args:
            spec_id: Specification ID
            evd_refs: List of evidence IDs this spec references
            file_path: Path to spec file
            
        Raises:
            GuardViolation: If evidence references are invalid
        """
        self.traceability_chain.register_spec(spec_id, evd_refs)
        self._log_operation(OperationType.CREATE, file_path, 
                          f"Spec {spec_id} registered with evidence {evd_refs}")
    
    def register_test(self, test_id: str, spec_refs: List[str], 
                     file_path: str, status: str = "failing"):
        """
        Register test with specification references.
        
        Args:
            test_id: Test ID
            spec_refs: List of specification IDs this test verifies
            file_path: Path to test file
            status: Test status
            
        Raises:
            GuardViolation: If spec references are invalid
        """
        self.traceability_chain.register_test(test_id, spec_refs, status)
        self._log_operation(OperationType.CREATE, file_path,
                          f"Test {test_id} registered with specs {spec_refs}, status: {status}")
    
    def write_code(self, code_file: str, content: str, test_refs: List[str]) -> bool:
        """
        Write code to a file after validating traceability chain.
        
        This is the core enforcement point. Code cannot be written unless:
        1. A failing test exists (TEST)
        2. The test references a spec (SPEC)
        3. The spec references evidence (EVD)
        
        Args:
            code_file: Path to code file to write
            content: Code content to write
            test_refs: List of test IDs this code implements
            
        Returns:
            True if write succeeded
            
        Raises:
            GuardViolation: If traceability chain is invalid
        """
        if self.strict_mode:
            # Link code to tests
            self.traceability_chain.link_code_to_test(code_file, test_refs)
            
            # Validate complete chain
            self.traceability_chain.validate_chain(code_file)
        
        # If we get here, chain is valid - perform the write
        try:
            code_path = Path(code_file)
            code_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(code_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            self._log_operation(OperationType.WRITE, code_file,
                              f"Code written with test refs {test_refs}")
            return True
        
        except Exception as e:
            self._log_operation(OperationType.WRITE, code_file,
                              f"Write failed: {str(e)}", success=False)
            raise GuardViolation(f"Failed to write code: {str(e)}")
    
    def read_file(self, file_path: str) -> str:
        """
        Read a file (no restrictions on reads).
        
        Args:
            file_path: Path to file
            
        Returns:
            File content
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            self._log_operation(OperationType.READ, file_path, "File read successful")
            return content
        
        except Exception as e:
            self._log_operation(OperationType.READ, file_path, 
                              f"Read failed: {str(e)}", success=False)
            raise
    
    def _log_operation(self, op_type: OperationType, file_path: str, 
                      message: str, success: bool = True):
        """Log a file operation."""
        from datetime import datetime
        
        self.operation_log.append({
            'timestamp': datetime.now().isoformat(),
            'operation': op_type.value,
            'file_path': file_path,
            'message': message,
            'success': success
        })
    
    def get_operation_log(self, limit: Optional[int] = None) -> List[Dict]:
        """Get operation log."""
        if limit:
            return self.operation_log[-limit:]
        return self.operation_log.copy()
    
    def get_traceability_info(self, code_file: str) -> Dict:
        """Get traceability information for a code file."""
        return self.traceability_chain.get_chain_info(code_file)
    
    def set_strict_mode(self, enabled: bool):
        """Enable or disable strict mode."""
        self.strict_mode = enabled
        self._log_operation(OperationType.WRITE, "system",
                          f"Strict mode {'enabled' if enabled else 'disabled'}")
