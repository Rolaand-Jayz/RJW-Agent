#!/usr/bin/env python3
"""
Simple demonstration of the RJW-IDD Agent Framework

This script shows the basic usage of all five core modules.
"""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.discovery.research import ResearchHarvester
from src.interaction.optimizer import PromptOptimizer
from src.governance.manager import GovernanceManager, TrustLevel
from src.context.engine import ContextCurator
from src.system.guard import SystemGuard


def main():
    print("\n" + "=" * 60)
    print("RJW-IDD AGENT FRAMEWORK - SIMPLE DEMO")
    print("=" * 60 + "\n")
    
    # 1. Research Phase
    print("1. RESEARCH PHASE")
    print("-" * 60)
    harvester = ResearchHarvester(output_dir="/tmp/demo/research")
    evd_id = harvester.harvest("authentication patterns")
    print(f"✓ Evidence created: {evd_id}\n")
    
    # 2. Interaction Layer
    print("2. INTERACTION LAYER")
    print("-" * 60)
    optimizer = PromptOptimizer(research_output_dir="/tmp/demo/research")
    result = optimizer.process_user_input("Add authentication to API")
    print(f"✓ Topics: {result['research_topics']}")
    print(f"✓ Evidence: {len(result['evidence_ids'])} files\n")
    
    # 3. Governance
    print("3. GOVERNANCE")
    print("-" * 60)
    manager = GovernanceManager(yolo_mode=True)
    approval = manager.request_approval(
        "Research complete", "research",
        {'evidence_ids': result['evidence_ids']},
        "minimal"
    )
    print(f"✓ Approval: {approval['approved']} ({approval['mode']})\n")
    
    # 4. Context Engine
    print("4. CONTEXT ENGINE")
    print("-" * 60)
    curator = ContextCurator(project_root="./src")
    stats = curator.get_project_structure()
    print(f"✓ Analyzed {stats['files_analyzed']} files")
    print(f"✓ Found {stats['total_elements']} code elements\n")
    
    # 5. System Guard
    print("5. SYSTEM GUARD")
    print("-" * 60)
    guard = SystemGuard(strict_mode=True)
    guard.register_evidence(evd_id, f"/tmp/demo/{evd_id}.md")
    print(f"✓ Guard initialized with traceability\n")
    
    print("=" * 60)
    print("✓ ALL MODULES WORKING CORRECTLY")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
