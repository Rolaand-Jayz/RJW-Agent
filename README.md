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
├── core/                    # Core method principles (METHOD-0001)
├── governance/              # Phase checklists and role handbooks
│   ├── METHOD-0002-phase-driver-checklists.md
│   └── METHOD-0003-role-handbook.md
├── operations/              # Execution playbooks
│   ├── METHOD-0004-ai-agent-workflows.md
│   ├── METHOD-0005-operations-production-support.md
│   ├── METHOD-0006-agent-trust-and-autonomy.md
│   └── METHOD-0007-streamlined-operations.md
├── templates/               # Artifact templates
│   ├── PROJECT-DEC-template.md
│   ├── DEC-LITE-template.md
│   └── AGENT-TRUST-template.md
├── addons/                  # Domain-specific methodology extensions
│   ├── 3d-game-core/
│   └── video-ai-enhancer/
└── docs/                    # Method-level documentation
    ├── change-log.md
    └── decisions/

docs/                        # Reference documentation
├── governance.md
├── runbooks/
└── decisions/
```

## Core Methodology Components

### 1. Core Method (`METHOD-0001`)

The foundational document describing:

- **Discovery Layer** — Research intake, evidence curation, and specification synthesis
- **Execution Layer** — Test-driven development, living documentation, integration-first delivery
- **Stage Gates** — Checkpoints ensuring each phase completes before the next begins

### 2. Phase-Driver Checklists (`METHOD-0002`)

Gate-by-gate tasks for:

- Discovery Intake
- Discovery → Execution transition
- Execution → Release

### 3. Role Handbook (`METHOD-0003`)

Responsibilities for:

- Agent Conductor
- Spec Curator
- Doc Steward
- Governance Sentinel

### 4. AI Agent Workflows (`METHOD-0004`)

Playbooks for coordinating AI coding agents within the methodology.

### 5. Operations & Production Support (`METHOD-0005`)

Guidance for post-deployment phases including:

- Deployment strategies (blue-green, canary)
- SLO management
- Incident response
- User feedback collection

### 6. Agent Trust and Autonomy (`METHOD-0006`)

Framework for building and managing trust in AI agents:

- **Trust Ladder Model** — Four levels from Supervised to Trusted Partner
- **Behavioral Contracts** — Explicit commitments agents make for transparency, quality, and safety
- **Continuous Verification** — Automated checks that build trust evidence
- **Graduated Response Protocol** — Proportionate responses to trust violations

### 7. Streamlined Operations (`METHOD-0007`)

Refinements for speed and human-friendliness:

- **Parallel-First Architecture** — Maximize concurrent work where dependencies allow
- **Risk-Proportionate Process** — Simple changes deserve simple processes
- **Human-Centered Artifacts** — Progressive disclosure and visual checklists
- **Quick-Start Pathways** — Fast tracks for common scenarios

## Templates

Copy these templates into your project when applying RJW-IDD:

| Template | Purpose |
|----------|---------|
| `rjw-idd-methodology/templates/PROJECT-DEC-template.md` | Full decision record for High/Critical risk choices |
| `rjw-idd-methodology/templates/DEC-LITE-template.md` | Lightweight decision record for Low/Medium risk choices |
| `rjw-idd-methodology/templates/AGENT-TRUST-template.md` | Document agent trust level changes |

## Using This Methodology

1. **Study the core method** — Read `rjw-idd-methodology/core/METHOD-0001-core-method.md` to understand the lifecycle
2. **Copy templates** — Clone templates into your project workspace; never modify the originals
3. **Apply the checklists** — Use `METHOD-0002` to guide each phase transition
4. **Assign roles** — Follow `METHOD-0003` to establish ownership
5. **Document decisions** — Create `DEC-####` records using the template for every strategic choice

## Addons (Domain Extensions)

The methodology includes optional extensions for specific domains:

- **3D Game Core** — Specs and checklists for game development with Unity, Unreal, Godot
- **Video AI Enhancer** — Quality gates for real-time video enhancement pipelines

## Contributing

Methodology changes require a new decision record (`DEC-####`) justifying the modification. See `CONTRIBUTING.md` for details.

## License

See `LICENSE` for terms.
