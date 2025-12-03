#!/usr/bin/env python3
"""
CLI Demo Script

This script demonstrates programmatic usage of the RJW-IDD CLI components.
For interactive usage, use: rjw
"""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.cli.session import Session
from src.cli.formatter import Formatter
from src.interaction.optimizer import PromptOptimizer
from src.governance.manager import GovernanceManager, TrustLevel


def demo_session_management():
    """Demonstrate session management."""
    print("=" * 60)
    print("DEMO: Session Management")
    print("=" * 60)
    
    formatter = Formatter()
    
    # Create a session
    session = Session(output_dir="/tmp/demo_sessions")
    print(formatter.success(f"✓ Created session: {session.session_id}"))
    
    # Add some conversation turns
    session.add_turn(
        "Add authentication to API",
        {
            "status": "research_complete",
            "evidence_ids": ["EVD-0001", "EVD-0002"],
            "research_topics": ["authentication", "API"]
        }
    )
    
    session.add_turn(
        "What's the best approach?",
        {
            "status": "decision_needed",
            "decision_id": "DEC-0001"
        }
    )
    
    # Get session summary
    summary = session.get_summary()
    print("\n" + formatter.section("Session Summary:"))
    print(formatter.format_dict(summary))
    
    # List sessions
    print("\n" + formatter.section("Available Sessions:"))
    sessions = Session.list_sessions(output_dir="/tmp/demo_sessions")
    for sid in sessions:
        print(formatter.list_item(sid))
    
    print()


def demo_workflow():
    """Demonstrate RJW-IDD workflow."""
    print("=" * 60)
    print("DEMO: RJW-IDD Workflow")
    print("=" * 60)
    
    formatter = Formatter()
    
    # Initialize components
    optimizer = PromptOptimizer(
        research_output_dir="/tmp/demo_workflow/research",
        specs_output_dir="/tmp/demo_workflow/specs",
        decisions_output_dir="/tmp/demo_workflow/decisions"
    )
    
    governance = GovernanceManager(
        yolo_mode=True,  # Enable YOLO mode for demo
        trust_level=TrustLevel.AUTONOMOUS
    )
    
    # Process user input
    print("\n" + formatter.dim("Processing: 'Add JWT authentication'"))
    result = optimizer.process_user_input("Add JWT authentication")
    
    # Request approval
    approval = governance.request_approval(
        action="Process authentication request",
        phase="research",
        artifacts={"evidence_ids": result.get("evidence_ids", [])},
        risk_level="minimal"
    )
    
    # Display results
    print("\n" + formatter.success("✓ Research Complete"))
    print()
    
    if result.get("research_topics"):
        print(formatter.section("Research Topics:"))
        for topic in result["research_topics"]:
            print(formatter.list_item(topic))
    
    print()
    if result.get("evidence_ids"):
        print(formatter.section("Evidence Generated:"))
        for evd_id in result["evidence_ids"]:
            print(formatter.list_item(evd_id))
    
    print()
    print(formatter.section("Governance:"))
    print(formatter.list_item(f"Approved: {formatter.bold(str(approval['approved']))}"))
    print(formatter.list_item(f"Mode: {approval['mode']}"))
    print(formatter.list_item(f"Trust Level: {governance.trust_level.name}"))
    
    # Get workflow summary
    print()
    print(formatter.section("Workflow State:"))
    summary = optimizer.get_workflow_summary()
    print(formatter.list_item(f"Evidence Count: {summary['evidence_count']}"))
    print(formatter.list_item(f"Decisions Count: {summary['decisions_count']}"))
    print(formatter.list_item(f"Specs Count: {summary['specifications_count']}"))
    
    print()


def demo_formatter():
    """Demonstrate formatter capabilities."""
    print("=" * 60)
    print("DEMO: Terminal Formatting")
    print("=" * 60)
    
    formatter = Formatter()
    
    print()
    print(formatter.header("Headers look like this"))
    print(formatter.section("Sections look like this"))
    print(formatter.success("✓ Success messages"))
    print(formatter.error("✗ Error messages"))
    print(formatter.warning("⚠ Warning messages"))
    print(formatter.info("ℹ Info messages"))
    print(formatter.dim("Dim text for less important info"))
    print(formatter.bold("Bold text for emphasis"))
    print()
    
    # List items
    print(formatter.section("List items:"))
    print(formatter.list_item("First item"))
    print(formatter.list_item("Second item"))
    print(formatter.list_item("Third item"))
    print()
    
    # Table
    print(formatter.section("Table formatting:"))
    headers = ["Name", "Status", "Count"]
    rows = [
        ["Evidence", "Complete", "3"],
        ["Decisions", "Pending", "1"],
        ["Specs", "Not Started", "0"]
    ]
    print(formatter.format_table(headers, rows))
    print()
    
    # Dictionary
    print(formatter.section("Dictionary formatting:"))
    data = {
        "session_id": "demo_session",
        "trust_level": "AUTONOMOUS",
        "artifacts": {
            "evidence": 3,
            "decisions": 1
        }
    }
    print(formatter.format_dict(data))
    print()


def demo_trust_levels():
    """Demonstrate trust levels."""
    print("=" * 60)
    print("DEMO: Trust Levels")
    print("=" * 60)
    
    formatter = Formatter()
    
    print()
    print(formatter.section("Trust Level Comparison:"))
    print()
    
    levels = [
        (TrustLevel.SUPERVISED, "All actions require approval"),
        (TrustLevel.GUIDED, "Routine actions auto-approved"),
        (TrustLevel.AUTONOMOUS, "Most actions auto-approved"),
        (TrustLevel.TRUSTED_PARTNER, "Full autonomy with oversight")
    ]
    
    for level, description in levels:
        governance = GovernanceManager(trust_level=level, yolo_mode=False)
        
        print(formatter.bold(f"{level.name}:"))
        print(formatter.dim(f"  {description}"))
        
        # Test authorization
        can_minimal = governance._check_trust_authorization("minimal")
        can_medium = governance._check_trust_authorization("medium")
        can_high = governance._check_trust_authorization("high")
        
        print(f"  Minimal: {formatter.success('✓') if can_minimal else formatter.error('✗')}", end="  ")
        print(f"Medium: {formatter.success('✓') if can_medium else formatter.error('✗')}", end="  ")
        print(f"High: {formatter.success('✓') if can_high else formatter.error('✗')}")
        print()
    
    print()


def main():
    """Run all demos."""
    print()
    print("=" * 60)
    print("RJW-IDD CLI - Programmatic Demo")
    print("=" * 60)
    print()
    print("This demo shows how to use RJW-IDD components programmatically.")
    print("For interactive CLI usage, run: rjw")
    print()
    
    try:
        demo_formatter()
        demo_session_management()
        demo_workflow()
        demo_trust_levels()
        
        print("=" * 60)
        print("✓ All demos completed successfully!")
        print("=" * 60)
        print()
        print("Try the interactive CLI:")
        print("  rjw                  # Start interactive session")
        print("  rjw run \"Add auth\"   # One-shot command")
        print("  rjw --help           # See all options")
        print()
        
    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user.")
        return 1
    except Exception as e:
        print(f"\n\nError: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
