"""Tests for the Governance & Autonomy module."""
import pytest
from src.governance.manager import (
    GovernanceManager, TrustLevel, ChecklistEnforcer, ChecklistStatus
)


class TestChecklistEnforcer:
    """Test suite for ChecklistEnforcer class."""
    
    @pytest.fixture
    def enforcer(self):
        """Create a ChecklistEnforcer instance."""
        return ChecklistEnforcer()
    
    def test_validate_phase_research_pass(self, enforcer):
        """Test that research phase validation passes with valid artifacts."""
        artifacts = {
            'evidence_ids': ['EVD-0001', 'EVD-0002']
        }
        
        result = enforcer.validate_phase('research', artifacts)
        assert result is True
        assert enforcer.validation_results['research'] == ChecklistStatus.PASSED
    
    def test_validate_phase_research_fail(self, enforcer):
        """Test that research phase validation fails without evidence."""
        artifacts = {}
        
        result = enforcer.validate_phase('research', artifacts)
        assert result is False
        assert enforcer.validation_results['research'] == ChecklistStatus.FAILED
    
    def test_validate_phase_decision_pass(self, enforcer):
        """Test that decision phase validation passes."""
        artifacts = {
            'evidence_refs': ['EVD-0001'],
            'options': ['Option A', 'Option B']
        }
        
        result = enforcer.validate_phase('decision', artifacts)
        assert result is True
    
    def test_get_checklist(self, enforcer):
        """Test getting checklist for a phase."""
        checklist = enforcer.get_checklist('research')
        assert len(checklist) > 0
        assert any('Evidence harvested' in item['item'] for item in checklist)


class TestGovernanceManager:
    """Test suite for GovernanceManager class."""
    
    @pytest.fixture
    def manager_standard(self):
        """Create a GovernanceManager in standard mode."""
        return GovernanceManager(yolo_mode=False, trust_level=TrustLevel.SUPERVISED)
    
    @pytest.fixture
    def manager_yolo(self):
        """Create a GovernanceManager in YOLO mode."""
        return GovernanceManager(yolo_mode=True, trust_level=TrustLevel.SUPERVISED)
    
    def test_request_approval_yolo_mode_pass(self, manager_yolo):
        """Test approval in YOLO mode with passing checklist."""
        artifacts = {
            'evidence_ids': ['EVD-0001']
        }
        
        result = manager_yolo.request_approval(
            action="Create evidence file",
            phase="research",
            artifacts=artifacts,
            risk_level="minimal"
        )
        
        assert result['approved'] is True
        assert result['mode'] == 'yolo'
        assert result['checklist_passed'] is True
    
    def test_request_approval_yolo_mode_fail(self, manager_yolo):
        """Test approval in YOLO mode with failing checklist."""
        artifacts = {}  # Missing required artifacts
        
        result = manager_yolo.request_approval(
            action="Create decision",
            phase="decision",
            artifacts=artifacts,
            risk_level="minimal"
        )
        
        assert result['approved'] is False
        assert result['mode'] == 'yolo'
        assert result['checklist_passed'] is False
    
    def test_request_approval_standard_mode_supervised(self, manager_standard):
        """Test approval in standard mode with supervised trust level."""
        artifacts = {
            'evidence_ids': ['EVD-0001']
        }
        
        result = manager_standard.request_approval(
            action="Create evidence",
            phase="research",
            artifacts=artifacts,
            risk_level="minimal"
        )
        
        # Supervised level can handle minimal risk
        assert result['approved'] is True
        assert result['mode'] == 'trust_based'
    
    def test_request_approval_standard_mode_insufficient_trust(self, manager_standard):
        """Test that insufficient trust level requires manual approval."""
        artifacts = {
            'evidence_ids': ['EVD-0001']
        }
        
        result = manager_standard.request_approval(
            action="High risk operation",
            phase="research",
            artifacts=artifacts,
            risk_level="high"
        )
        
        # Supervised level cannot handle high risk
        assert result['approved'] is False
        assert result['mode'] == 'manual_required'
    
    def test_set_yolo_mode(self, manager_standard):
        """Test toggling YOLO mode."""
        assert manager_standard.yolo_mode is False
        
        manager_standard.set_yolo_mode(True)
        assert manager_standard.yolo_mode is True
        
        # Check log
        log = manager_standard.get_approval_history(limit=1)
        assert len(log) == 1
        assert log[0]['action'] == 'yolo_mode_change'
    
    def test_set_trust_level(self, manager_standard):
        """Test updating trust level."""
        assert manager_standard.trust_level == TrustLevel.SUPERVISED
        
        manager_standard.set_trust_level(TrustLevel.AUTONOMOUS)
        assert manager_standard.trust_level == TrustLevel.AUTONOMOUS
        
        # Check log
        log = manager_standard.get_approval_history(limit=1)
        assert log[0]['action'] == 'trust_level_change'
    
    def test_trust_authorization_levels(self, manager_standard):
        """Test trust level authorization for different risk levels."""
        # Supervised: only minimal
        assert manager_standard._check_trust_authorization('minimal') is True
        assert manager_standard._check_trust_authorization('low') is False
        assert manager_standard._check_trust_authorization('high') is False
        
        # Guided: minimal and low
        manager_standard.set_trust_level(TrustLevel.GUIDED)
        assert manager_standard._check_trust_authorization('minimal') is True
        assert manager_standard._check_trust_authorization('low') is True
        assert manager_standard._check_trust_authorization('medium') is False
        
        # Autonomous: minimal, low, medium
        manager_standard.set_trust_level(TrustLevel.AUTONOMOUS)
        assert manager_standard._check_trust_authorization('medium') is True
        assert manager_standard._check_trust_authorization('high') is False
        
        # Trusted Partner: all levels
        manager_standard.set_trust_level(TrustLevel.TRUSTED_PARTNER)
        assert manager_standard._check_trust_authorization('high') is True
        assert manager_standard._check_trust_authorization('critical') is True
    
    def test_get_governance_status(self, manager_yolo):
        """Test getting governance status."""
        status = manager_yolo.get_governance_status()
        
        assert status['yolo_mode'] is True
        assert status['trust_level'] == 'SUPERVISED'
        assert 'approval_count' in status
        assert 'checklist_results' in status
    
    def test_approval_history_logging(self, manager_standard):
        """Test that approval requests are logged."""
        artifacts = {'evidence_ids': ['EVD-0001']}
        
        manager_standard.request_approval("Action 1", "research", artifacts)
        manager_standard.request_approval("Action 2", "research", artifacts)
        
        history = manager_standard.get_approval_history()
        assert len(history) == 2
        
        # Test limit
        limited = manager_standard.get_approval_history(limit=1)
        assert len(limited) == 1
