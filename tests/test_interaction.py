"""Tests for the Interaction Layer module."""
import pytest
import tempfile
import shutil
from pathlib import Path
from src.interaction.optimizer import PromptOptimizer


class TestPromptOptimizer:
    """Test suite for PromptOptimizer class."""
    
    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory for tests."""
        temp = tempfile.mkdtemp()
        yield temp
        shutil.rmtree(temp)
    
    @pytest.fixture
    def optimizer(self, temp_dir):
        """Create a PromptOptimizer instance."""
        research_dir = Path(temp_dir) / "research"
        specs_dir = Path(temp_dir) / "specs"
        decisions_dir = Path(temp_dir) / "decisions"
        
        return PromptOptimizer(
            research_output_dir=str(research_dir),
            specs_output_dir=str(specs_dir),
            decisions_output_dir=str(decisions_dir)
        )
    
    def test_process_user_input_empty_raises_error(self, optimizer):
        """Test that empty user input raises ValueError."""
        with pytest.raises(ValueError, match="User input cannot be empty"):
            optimizer.process_user_input("")
    
    def test_process_user_input_extracts_topics(self, optimizer):
        """Test that user input is processed and topics are extracted."""
        result = optimizer.process_user_input(
            "I need to implement secure authentication for the API"
        )
        
        assert result['status'] == 'research_complete'
        assert len(result['research_topics']) > 0
        assert len(result['evidence_ids']) > 0
        # Should extract at least 'authentication' from the input
        assert 'authentication' in result['research_topics']
    
    def test_process_user_input_generates_evidence(self, optimizer):
        """Test that processing user input generates evidence files."""
        result = optimizer.process_user_input("Implement database caching")
        
        # Should have generated evidence
        assert len(result['evidence_ids']) > 0
        
        # Evidence IDs should be valid
        for evd_id in result['evidence_ids']:
            assert evd_id.startswith("EVD-")
    
    def test_process_user_input_updates_workflow_state(self, optimizer):
        """Test that workflow state is updated."""
        user_input = "Add logging to the application"
        result = optimizer.process_user_input(user_input)
        
        summary = optimizer.get_workflow_summary()
        assert summary['user_input'] == user_input
        assert summary['evidence_count'] > 0
        assert summary['research_topics_count'] > 0
    
    def test_create_decision_with_evidence(self, optimizer):
        """Test creating a decision with evidence references."""
        # First, generate evidence
        result = optimizer.process_user_input("Test authentication methods")
        evd_ids = result['evidence_ids']
        
        # Create decision
        dec_id = optimizer.create_decision_with_evidence(
            decision_title="Choose authentication method",
            evidence_refs=evd_ids,
            options=["JWT", "OAuth2", "Session-based"],
            chosen_option="JWT",
            rationale="Best for our use case"
        )
        
        assert dec_id.startswith("DEC-")
        
        # Check workflow state
        summary = optimizer.get_workflow_summary()
        assert summary['decisions_count'] == 1
        assert dec_id in summary['decision_ids']
    
    def test_create_decision_without_evidence_raises_error(self, optimizer):
        """Test that creating a decision without evidence raises error."""
        with pytest.raises(ValueError, match="Cannot create DEC without evidence references"):
            optimizer.create_decision_with_evidence(
                decision_title="Test decision",
                evidence_refs=[],
                options=["A", "B"],
                chosen_option="A",
                rationale="Test"
            )
    
    def test_create_spec_with_traceability(self, optimizer):
        """Test creating a specification with full traceability."""
        # Generate evidence
        result = optimizer.process_user_input("Design API endpoints")
        evd_ids = result['evidence_ids']
        
        # Create spec
        spec_id = optimizer.create_spec_with_traceability(
            spec_title="API endpoint specification",
            evidence_refs=evd_ids,
            decision_refs=[],
            requirements=["REQ-001", "REQ-002"]
        )
        
        assert spec_id.startswith("SPEC-")
        
        # Check workflow state
        summary = optimizer.get_workflow_summary()
        assert summary['specifications_count'] == 1
    
    def test_create_spec_without_evidence_raises_error(self, optimizer):
        """Test that creating a spec without evidence raises error."""
        with pytest.raises(ValueError, match="Cannot create SPEC without evidence references"):
            optimizer.create_spec_with_traceability(
                spec_title="Test spec",
                evidence_refs=[],
                decision_refs=[],
                requirements=["REQ-001"]
            )
    
    def test_workflow_summary(self, optimizer):
        """Test getting workflow summary."""
        # Initial state
        summary = optimizer.get_workflow_summary()
        assert summary['evidence_count'] == 0
        assert summary['decisions_count'] == 0
        assert summary['specifications_count'] == 0
        
        # After processing input
        optimizer.process_user_input("Test workflow")
        summary = optimizer.get_workflow_summary()
        assert summary['evidence_count'] > 0
