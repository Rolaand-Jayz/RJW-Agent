"""
Governance & Autonomy Module

Implements the GovernanceManager with trust-based approval mechanisms.
This enforces METHOD-0004 trust ladder and METHOD-0002 checklist requirements.
"""
from enum import Enum
from typing import Dict, List, Optional, Callable
from datetime import datetime


class TrustLevel(Enum):
    """Trust levels for agent autonomy (METHOD-0004 Section 1.2)."""
    SUPERVISED = 0  # All actions require approval
    GUIDED = 1  # Routine actions auto-approved
    AUTONOMOUS = 2  # Most actions auto-approved
    TRUSTED_PARTNER = 3  # Full autonomy with oversight


class RiskLevel(Enum):
    """Risk levels for deployment pathways (METHOD-0002 Section 1)."""
    STREAMLINED = "streamlined"  # Consolidates former Minimal/Low/Medium/High/Critical
    YOLO = "yolo"  # Autonomous self-approval mode
    PROTOTYPE = "prototype"  # POC/spike/experimental work


class ChecklistStatus(Enum):
    """Status of checklist validation."""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    PASSED = "passed"
    FAILED = "failed"


class ChecklistEnforcer:
    """
    Enforces phase gate checklists per METHOD-0002.
    
    This class validates that required checkpoints are met before
    proceeding to the next phase.
    """
    
    def __init__(self):
        """Initialize the ChecklistEnforcer."""
        self.checklists: Dict[str, List[Dict]] = {
            'research': [
                {'item': 'Evidence harvested', 'required': True},
                {'item': 'Sources documented', 'required': True},
                {'item': 'Key insights extracted', 'required': True}
            ],
            'decision': [
                {'item': 'Evidence references provided', 'required': True},
                {'item': 'Options evaluated', 'required': True},
                {'item': 'Rationale documented', 'required': True}
            ],
            'specification': [
                {'item': 'Requirements defined', 'required': True},
                {'item': 'Evidence backing provided', 'required': True},
                {'item': 'Technical design complete', 'required': True}
            ],
            'implementation': [
                {'item': 'Tests written', 'required': True},
                {'item': 'Code implements spec', 'required': True},
                {'item': 'Tests passing', 'required': True}
            ]
        }
        
        self.validation_results: Dict[str, ChecklistStatus] = {}
    
    def validate_phase(self, phase: str, artifacts: Dict) -> bool:
        """
        Validate that a phase meets its checklist requirements.
        
        Args:
            phase: Phase to validate ('research', 'decision', 'specification', 'implementation')
            artifacts: Dictionary of artifacts for validation
            
        Returns:
            True if all required checklist items pass
        """
        if phase not in self.checklists:
            raise ValueError(f"Unknown phase: {phase}")
        
        checklist = self.checklists[phase]
        all_passed = True
        
        for item in checklist:
            if item['required']:
                # Check if required artifact exists
                passed = self._check_item(phase, item['item'], artifacts)
                if not passed:
                    all_passed = False
        
        status = ChecklistStatus.PASSED if all_passed else ChecklistStatus.FAILED
        self.validation_results[phase] = status
        
        return all_passed
    
    def _check_item(self, phase: str, item: str, artifacts: Dict) -> bool:
        """
        Check a specific checklist item.
        
        Args:
            phase: Current phase
            item: Checklist item description
            artifacts: Available artifacts
            
        Returns:
            True if item requirement is met
        """
        # Simple validation logic
        if phase == 'research':
            if 'Evidence harvested' in item:
                return bool(artifacts.get('evidence_ids'))
            if 'Sources documented' in item:
                return bool(artifacts.get('evidence_ids'))
        
        elif phase == 'decision':
            if 'Evidence references' in item:
                return bool(artifacts.get('evidence_refs'))
            if 'Options evaluated' in item:
                return bool(artifacts.get('options'))
        
        elif phase == 'specification':
            if 'Requirements defined' in item:
                return bool(artifacts.get('requirements'))
            if 'Evidence backing' in item:
                return bool(artifacts.get('evidence_refs'))
        
        elif phase == 'implementation':
            if 'Tests written' in item:
                return bool(artifacts.get('test_files'))
            if 'Tests passing' in item:
                return artifacts.get('tests_passing', False)
        
        return True
    
    def get_checklist(self, phase: str) -> List[Dict]:
        """Get checklist for a specific phase."""
        return self.checklists.get(phase, [])


class RiskClassifier:
    """
    Implements risk classification for deployment pathway selection.
    
    This class consolidates the former 6-pathway system (Minimal, Low, Medium, 
    High, Critical, Prototype) into exactly 3 pathways per METHOD-0002.
    """
    
    def classify(self, change: Dict) -> RiskLevel:
        """
        Classify change into one of three deployment pathways.
        
        Args:
            change: Dictionary describing the change with keys:
                - is_prototype: bool - POC/spike/experimental work
                - yolo_mode: bool - Autonomous self-approval requested
                
        Returns:
            RiskLevel: STREAMLINED, YOLO, or PROTOTYPE
        """
        # Is this prototype/POC/spike work?
        if change.get('is_prototype', False):
            return RiskLevel.PROTOTYPE
        
        # Is YOLO mode explicitly requested?
        if change.get('yolo_mode', False):
            return RiskLevel.YOLO
        
        # Default to streamlined path for all production-ready changes
        return RiskLevel.STREAMLINED
    
    def get_pathway(self, risk_level: RiskLevel) -> str:
        """
        Get the appropriate pathway documentation reference for risk level.
        
        Args:
            risk_level: The classified risk level
            
        Returns:
            String describing the pathway
        """
        pathways = {
            RiskLevel.STREAMLINED: "Section 2.1 - Streamlined Path (production-ready changes)",
            RiskLevel.YOLO: "Section 2.2 - YOLO Path (autonomous self-approval)",
            RiskLevel.PROTOTYPE: "Section 2.3 - Prototype Path (POC/spike/experimental)"
        }
        return pathways[risk_level]


class GovernanceManager:
    """
    Manages governance and autonomy decisions for the RJW-IDD agent.
    
    This class implements:
    - YOLO mode: Agent self-approves if ChecklistEnforcer passes
    - Standard mode: Manual approval required (TrustLadder)
    - Trust level verification per METHOD-0004
    
    Attributes:
        yolo_mode: If True, enables self-approval with checklist validation
        trust_level: Current trust level of the agent
        checklist_enforcer: Instance for validating phase gates
        approval_log: Log of all approval decisions
    """
    
    def __init__(self, 
                 yolo_mode: bool = False,
                 trust_level: TrustLevel = TrustLevel.SUPERVISED):
        """
        Initialize the GovernanceManager.
        
        Args:
            yolo_mode: Enable self-approval mode (default: False)
            trust_level: Initial trust level (default: SUPERVISED)
        """
        self.yolo_mode = yolo_mode
        self.trust_level = trust_level
        self.checklist_enforcer = ChecklistEnforcer()
        self.approval_log: List[Dict] = []
    
    def request_approval(self, 
                        action: str,
                        phase: str,
                        artifacts: Dict,
                        risk_level: str = "medium") -> Dict:
        """
        Request approval for an action.
        
        In YOLO mode: Auto-approve if ChecklistEnforcer passes
        In Standard mode: Require manual approval via callback
        
        Args:
            action: Description of the action requiring approval
            phase: Current phase (research, decision, specification, implementation)
            artifacts: Artifacts for validation
            risk_level: Risk level of the action (minimal, low, medium, high, critical)
            
        Returns:
            Dictionary with approval decision:
            - approved: bool
            - mode: 'yolo' or 'manual'
            - reason: str
            - checklist_status: ChecklistStatus
        """
        timestamp = datetime.now().isoformat()
        
        # Validate checklist
        checklist_passed = self.checklist_enforcer.validate_phase(phase, artifacts)
        
        if self.yolo_mode:
            # YOLO mode: Self-approve if checklist passes
            approved = checklist_passed
            mode = 'yolo'
            reason = "Auto-approved (YOLO mode) - checklist passed" if approved else \
                     "Auto-rejected (YOLO mode) - checklist failed"
        else:
            # Standard mode: Check trust level and risk
            can_auto_approve = self._check_trust_authorization(risk_level)
            
            if can_auto_approve and checklist_passed:
                approved = True
                mode = 'trust_based'
                reason = f"Auto-approved - Trust level {self.trust_level.name} authorized for {risk_level} risk"
            else:
                # Require manual approval
                approved = False
                mode = 'manual_required'
                reason = f"Manual approval required - Trust level {self.trust_level.name} insufficient for {risk_level} risk or checklist failed"
        
        # Log the decision
        approval_record = {
            'timestamp': timestamp,
            'action': action,
            'phase': phase,
            'approved': approved,
            'mode': mode,
            'reason': reason,
            'risk_level': risk_level,
            'trust_level': self.trust_level.name,
            'checklist_passed': checklist_passed,
            'yolo_mode': self.yolo_mode
        }
        self.approval_log.append(approval_record)
        
        return approval_record
    
    def _check_trust_authorization(self, risk_level: str) -> bool:
        """
        Check if current trust level authorizes the risk level.
        
        With three pathways (METHOD-0002):
        - Streamlined path: Appropriate scrutiny based on change scope
        - YOLO path: Handled by yolo_mode flag
        - Prototype path: Relaxed gates for POC work
        
        For backward compatibility, still supports old risk levels:
        - SUPERVISED (0): Minimal/Low risk
        - GUIDED (1): Minimal/Low/Medium risk  
        - AUTONOMOUS (2): All streamlined changes
        - TRUSTED_PARTNER (3): All pathways
        
        Args:
            risk_level: Risk level to check (streamlined, yolo, prototype, or legacy values)
            
        Returns:
            True if authorized
        """
        # Map new pathways to authorization
        if risk_level in ['streamlined', 'prototype']:
            # Streamlined and prototype paths available at GUIDED level and above
            return self.trust_level.value >= TrustLevel.GUIDED.value
        
        if risk_level == 'yolo':
            # YOLO path requires AUTONOMOUS or higher
            return self.trust_level.value >= TrustLevel.AUTONOMOUS.value
        
        # Backward compatibility for old risk levels
        trust_authorizations = {
            TrustLevel.SUPERVISED: ['minimal', 'low'],
            TrustLevel.GUIDED: ['minimal', 'low', 'medium'],
            TrustLevel.AUTONOMOUS: ['minimal', 'low', 'medium', 'high', 'streamlined', 'prototype'],
            TrustLevel.TRUSTED_PARTNER: ['minimal', 'low', 'medium', 'high', 'critical', 'streamlined', 'yolo', 'prototype']
        }
        
        return risk_level in trust_authorizations.get(self.trust_level, [])
    
    def set_yolo_mode(self, enabled: bool):
        """
        Enable or disable YOLO mode.
        
        Args:
            enabled: True to enable YOLO mode, False to disable
        """
        previous = self.yolo_mode
        self.yolo_mode = enabled
        
        self.approval_log.append({
            'timestamp': datetime.now().isoformat(),
            'action': 'yolo_mode_change',
            'previous': previous,
            'current': enabled,
            'reason': 'YOLO mode toggled by user'
        })
    
    def set_trust_level(self, trust_level: TrustLevel):
        """
        Update the agent's trust level.
        
        Args:
            trust_level: New trust level
        """
        previous = self.trust_level
        self.trust_level = trust_level
        
        self.approval_log.append({
            'timestamp': datetime.now().isoformat(),
            'action': 'trust_level_change',
            'previous': previous.name,
            'current': trust_level.name,
            'reason': 'Trust level updated based on performance'
        })
    
    def get_approval_history(self, limit: Optional[int] = None) -> List[Dict]:
        """
        Get approval history.
        
        Args:
            limit: Maximum number of records to return (None for all)
            
        Returns:
            List of approval records
        """
        if limit:
            return self.approval_log[-limit:]
        return self.approval_log.copy()
    
    def get_governance_status(self) -> Dict:
        """
        Get current governance status.
        
        Returns:
            Dictionary with governance state
        """
        return {
            'yolo_mode': self.yolo_mode,
            'trust_level': self.trust_level.name,
            'approval_count': len(self.approval_log),
            'checklist_results': self.checklist_enforcer.validation_results
        }
