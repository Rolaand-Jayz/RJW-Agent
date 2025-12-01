# Rolaand Jayz Wayz – Coding with Natural Language: Intelligence Driven Development (RJW-IDD)

> **A disciplined methodology for AI-assisted software development** — no code, just the pure method and templates for the artefacts you create when applying it.

## What is RJW-IDD?

RJW-IDD (Intelligence Driven Development) is a methodology that replaces vibe-driven AI coding with a disciplined loop where **reality** (fresh research, explicit trade-offs) leads specification and implementation. It provides:

- **Traceable decisions** captured in individual Markdown records
- **Research-first development** with curated evidence driving requirements
- **Specification-driven design** before implementation begins
- **Test-driven execution** with living documentation

## Repository Structure

This repository contains the **pure methodology** and **templates** only — no implementation code.

```text
rjw-idd-methodology/
├── core/                    # Core method principles
│   └── METHOD-0001-core-method.md
├── governance/              # Phase checklists and role handbooks
│   ├── METHOD-0002-phase-driver-checklists.md (Unified Lifecycle & Checklists)
│   └── METHOD-0003-role-handbook.md
├── operations/              # Execution playbooks
│   ├── METHOD-0004-ai-agent-workflows.md (Unified Agent Handbook)
│   ├── METHOD-0005-operations-production-support.md
│   └── METHOD-0006-context-curation-engine.md (Context Curation Engine)
├── templates/               # Artifact templates (organised by category)
│   ├── decisions/           # Decision record templates
│   ├── requirements/        # Requirement templates
│   ├── specs/               # Specification templates
│   ├── evidence/            # Research evidence templates
│   ├── testing/             # Test case templates
│   ├── documentation/       # Standards, runbooks, guides
│   ├── governance/          # Change logs, audit logs, ledgers
│   └── context/             # Context curation templates
├── addons/                  # Domain-specific methodology extensions
│   ├── config/              # Central feature registry
│   │   └── features.yml
│   ├── 3d-game-core/
│   └── video-ai-enhancer/
├── docs/                    # Method-level documentation
│   ├── change-log.md
│   └── decisions/
└── logs/                    # Stage audit reflections

docs/                        # Reference documentation
└── README.md
```

## Core Methodology Components

The methodology is organized into **six core documents**:

### 1. Core Method (`METHOD-0001`)

The foundational document describing:

- **Discovery Layer** — Research intake, evidence curation, and specification synthesis
- **Execution Layer** — Test-driven development, living documentation, integration-first delivery
- **Stage Gates** — Checkpoints ensuring each phase completes before the next begins

### 2. Unified Lifecycle & Checklists (`METHOD-0002`)

The **single source of truth** for all process checklists:

- **Risk Selection Logic** — Entry point for classifying change risk level
- **Streamlined Pathways** — Fast tracks for Minimal/Low/Medium risk changes
- **Full Discovery→Execution Loop** — High/Critical risk change processes
- **Prototype Mode** — Keep/Flex/Unknown tagging and relaxed gates for POC/spike work
- **Agent Trust Integration** — Trust levels linked to pathway access

### 3. Role Handbook (`METHOD-0003`)

Responsibilities for:

- Agent Conductor
- Spec Curator
- Doc Steward
- Governance Sentinel

### 4. Unified Agent Handbook (`METHOD-0004`)

The **single source of truth** for all AI agent rules and behaviors:

- **Trust Ladder Model** — Four levels from Supervised to Trusted Partner
- **Behavioral Contracts** — Explicit commitments agents make for transparency, quality, and safety
- **Continuous Verification** — Automated checks that build trust evidence
- **Graduated Response Protocol** — Proportionate responses to trust violations
- **Workflow Selection** — Trust levels linked to process pathways

### 5. Operations & Production Support (`METHOD-0005`)

Guidance for post-deployment phases including:

- Deployment strategies (blue-green, canary)
- SLO management
- Incident response
- User feedback collection

### 6. Context Curation Engine (`METHOD-0006`)

A framework for continuously managing context available to AI agents:

- **Context Index** — Per-task documents listing in-scope files, decisions, and assumptions
- **Turn-Based Curation** — Evaluate, remove, and load context on every agent turn
- **Automatic Updates** — Propagate changes to affected context indexes automatically
- **Living Documentation** — Governed source of truth for technologies, architecture, and conventions
- **Agent Integration** — Trust-level context access and escalation triggers

## Templates

Copy these templates into your project when applying RJW-IDD:

| Category | Template | Purpose |
|----------|----------|---------|
| **Decisions** | `templates/decisions/DEC-template.md` | Capture strategic choices with options and rationale |
| **Decisions** | `templates/DEC-LITE-template.md` | Lightweight decision record for Low/Medium risk |
| **Prototypes** | `templates/PROTO-template.md` | Prototype record for POC/spike work |
| **Agent Trust** | `templates/AGENT-TRUST-template.md` | Document agent trust level changes |
| **Requirements** | `templates/requirements/REQ-template.md` | Define system requirements with acceptance criteria |
| **Specifications** | `templates/specs/SPEC-template.md` | Technical design addressing requirements |
| **Evidence** | `templates/evidence/EVD-template.md` | Research findings supporting decisions |
| **Testing** | `templates/testing/TEST-template.md` | Verify specifications meet acceptance criteria |
| **Documentation** | `templates/documentation/DOC-template.md` | Standards, runbooks, guides, and references |
| **Governance** | `templates/governance/CHANGE-LOG-template.md` | Track methodology/project changes |
| **Governance** | `templates/governance/STAGE-AUDIT-LOG-template.md` | Phase gate audit reflections |
| **Governance** | `templates/governance/REQ-LEDGER-template.md` | Requirement traceability matrix |
| **Governance** | `templates/governance/LIVING-DOCS-RECONCILIATION-template.md` | Documentation debt tracking |
| **Context** | `templates/context/CTX-INDEX-template.md` | Task-specific context index for AI agents |
| **Context** | `templates/context/LIVING-DOCS-template.md` | Project living documentation |

See `rjw-idd-methodology/templates/README.md` for detailed usage instructions.

## Using This Methodology

1. **Study the core method** — Read `rjw-idd-methodology/core/METHOD-0001-core-method.md` to understand the lifecycle
2. **Copy templates** — Clone templates from `rjw-idd-methodology/templates/` into your project workspace; never modify the originals
3. **Classify risk level** — Use the Risk Selection Logic in `METHOD-0002` Section 1 to determine the appropriate pathway
4. **Apply the checklists** — Use `METHOD-0002` to guide each phase transition
5. **Assign roles** — Follow `METHOD-0003` to establish ownership
6. **Document decisions** — Create `DEC-####` records using the decision template for every strategic choice
7. **Track requirements** — Use the requirement ledger template to maintain traceability
8. **Maintain governance** — Update change logs and audit logs at each phase gate

## Addons (Domain Extensions)

The methodology includes optional extensions for specific domains:

- **3D Game Core** — Specs and checklists for game development with Unity, Unreal, Godot
- **Video AI Enhancer** — Quality gates for real-time video enhancement pipelines

## Contributing

Methodology changes require a new decision record (`DEC-####`) justifying the modification. See `CONTRIBUTING.md` for details.

## License

See `LICENSE` for terms.
