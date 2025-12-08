# Rolaand Jayz Wayz – Coding with Natural Language: Intelligence Driven Development (RJW-IDD)

> **A disciplined methodology for AI-assisted software development** — providing the method, templates, and implementation guidance for building agents that follow this framework.

## What is RJW-IDD?

RJW-IDD (Intelligence Driven Development) is a methodology that replaces vibe-driven AI coding with a disciplined loop where **reality** (fresh research, explicit trade-offs) leads specification and implementation. It provides:

- **Traceable decisions** captured in individual Markdown records
- **Research-first development** with curated evidence driving requirements
- **Specification-driven design** before implementation begins
- **Test-driven execution** with living documentation

## Quick Start: CLI

Install and run the CLI:

```bash
# Install the package
pip install -e .

# Start interactive session
rjw

# Or use one-shot commands
rjw run "Add authentication to API"

# Get help
rjw --help
```

## Repository Structure

This repository contains the methodology, templates, and implementation guidance for building RJW-IDD compliant agents.

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

The **single source of truth** for all process checklists with **three deployment pathways**:

- **Deployment Pathway Selection** — Choose from exactly 3 pathways (Streamlined, YOLO, Prototype)
- **Streamlined Path** — Single production path for all changes with graduated response (consolidates former Minimal/Low/Medium/High/Critical)
- **YOLO Path** — Autonomous self-approval mode with checklist enforcement
- **Prototype Path** — Keep/Flex/Unknown tagging and relaxed gates for POC/spike work
- **Agent Trust Integration** — Trust levels linked to pathway access
- **User Evidence Handling** — Automatic parsing and reformatting of user-provided research

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

## Using the CLI

The RJW-IDD CLI provides an interactive interface similar to Google Gemini, Claude, and other AI tools.

### Interactive Mode

Start an interactive session:

```bash
# Basic interactive session
rjw

# Or explicitly use 'chat' command
rjw chat

# Resume a specific session
rjw --session my_project

# Start with YOLO mode (auto-approval)
rjw --yolo

# Set trust level
rjw --trust AUTONOMOUS
```

### Available Commands in Interactive Mode

Once in interactive mode, you can use these commands:

- `/help` - Show available commands
- `/status` - Show current session status (evidence, decisions, specs, context indexes)
- `/history [limit]` - Show conversation history
- `/clear` - Clear conversation history
- `/yolo` - Toggle YOLO mode on/off
- `/trust <level>` - Set trust level (SUPERVISED, GUIDED, AUTONOMOUS, TRUSTED_PARTNER)
- `/context <task_id> <focus_areas>` - Prepare implementation context (METHOD-0006)
- `/exit` or `/quit` - Exit the CLI (or use Ctrl+D)

### One-Shot Commands

Execute single commands without interactive mode:

```bash
# Process a request
rjw run "Add authentication to API"

# With YOLO mode
rjw run "Implement caching" --yolo

# With specific trust level
rjw run "Add logging" --trust GUIDED
```

### Session Management

```bash
# List all sessions
rjw sessions

# Show session info
rjw sessions --info session_20231203_143022_abc123

# Delete a session
rjw sessions --delete session_20231203_143022_abc123
```

### Trust Levels

The CLI supports four trust levels from the RJW-IDD methodology:

- **SUPERVISED** (default) - All actions require approval
- **GUIDED** - Routine actions auto-approved
- **AUTONOMOUS** - Most actions auto-approved
- **TRUSTED_PARTNER** - Full autonomy with oversight

### YOLO Mode

YOLO mode enables automatic self-approval when checklist requirements are met, allowing faster iteration while maintaining governance.

### Context Curation Engine (METHOD-0006)

The Context Curation Engine implements the complete METHOD-0006 framework for context management:

**Section 2: Context Index Structure**
- Task Scope (objectives, constraints)
- Affected Areas (files, modules, endpoints)
- Technical Context (decisions, specs, conventions)
- Assumptions and dependencies
- Change history tracking

**Section 3: Turn-Based Context Curation**
- Context evaluation cycle (EVALUATE → REMOVE → LOAD → PROCEED)
- Relevance scoring (0.0-1.0) for all context items
- Automatic filtering of low-relevance items (score < 0.2)

**Section 4: Context Update Triggers**
- File modifications, decision/spec updates
- Automatic propagation to affected contexts
- Change history tracking

**Section 5: Living Documentation Integration**
- Technologies, architecture, conventions
- Project-specific rules and constraints

**Implementation Details:**
- Uses static analysis (AST) to find related code elements
- Extracts signatures only, not full file contents
- No LLM inference for context selection

**Example Usage:**

```bash
# In interactive mode
rjw

# Prepare implementation context for a task
/context TASK-001 authentication,authorization

# Context Index Created: CTX-TASK-001
# Related Files: 5
# Signatures Extracted: 12 (with relevance scores)
```

The context engine helps identify relevant code through static analysis, reducing context bloat and supporting focused implementation.

## Using This Methodology

1. **Study the core method** — Read `rjw-idd-methodology/core/METHOD-0001-core-method.md` to understand the lifecycle
2. **Copy templates** — Clone templates from `rjw-idd-methodology/templates/` into your project workspace; never modify the originals
3. **Classify risk level** — Use the Risk Selection Logic in `METHOD-0002` Section 1 to determine the appropriate pathway
4. **Apply the checklists** — Use `METHOD-0002` to guide each phase transition
5. **Assign roles** — Follow `METHOD-0003` to establish ownership
6. **Document decisions** — Create `DEC-####` records using the decision template for every strategic choice
7. **Track requirements** — Use the requirement ledger template to maintain traceability
8. **Maintain governance** — Update change logs and audit logs at each phase gate

## Implementing RJW-IDD in Your Agent

This section provides guidance for developers building AI agents that adhere to the RJW-IDD methodology.

### Agent Core Structure

When building an RJW-IDD compliant agent, implement these core components:

```python
class RJWIDDAgent:
    """Base class for RJW-IDD compliant agents."""
    
    def __init__(self, agent_id: str, initial_trust_level: int = 0):
        self.agent_id = agent_id
        # Trust levels: 0=Supervised, 1=Guided, 2=Autonomous, 3=Trusted Partner
        # See METHOD-0004 Section 1.2 for full definitions
        self.trust_level = initial_trust_level
        self.action_log = []
        self.decision_records = []
        
    def classify_risk(self, change_description: str) -> str:
        """Classify change risk per METHOD-0002 Section 1."""
        # Implement risk classification logic
        # Returns: 'minimal', 'low', 'medium', 'high', 'critical', 'prototype'
        pass
    
    def check_authorization(self, risk_level: str) -> bool:
        """Verify agent has authority for this risk level."""
        trust_access = {
            0: ['minimal'],  # Level 0: Supervised
            1: ['minimal', 'low'],  # Level 1: Guided
            2: ['minimal', 'low', 'medium'],  # Level 2: Autonomous
            3: ['minimal', 'low', 'medium', 'high', 'critical']  # Level 3: Trusted Partner
        }
        return risk_level in trust_access.get(self.trust_level, [])
    
    def log_action(self, action_type: str, details: dict):
        """Log all actions per METHOD-0004 Section 7.5."""
        self.action_log.append({
            'timestamp': datetime.utcnow().isoformat(),
            'agent_id': self.agent_id,
            'trust_level': self.trust_level,
            'action_type': action_type,
            'details': details
        })
```

### Decision Record Integration

Integrate decision tracking into your agent:

```python
def create_decision_record(self, decision_id: str, options: list, 
                           chosen: str, rationale: str) -> dict:
    """Create a DEC-#### record per METHOD-0001 Section 2."""
    record = {
        'id': decision_id,
        'date': datetime.utcnow().strftime('%Y-%m-%d'),
        'options': options,
        'chosen': chosen,
        'rationale': rationale,
        'evidence_refs': [],  # Link to EVD-#### records
        'spec_refs': []  # Link to SPEC-#### records
    }
    self.decision_records.append(record)
    return record
```

### Trust Level Verification

Implement continuous trust verification:

```python
def calculate_trust_score(self) -> float:
    """Calculate rolling trust score per METHOD-0004 Section 3.3."""
    weights = {
        'process_compliance': 0.25,
        'output_quality': 0.30,
        'behavioral_alignment': 0.30,
        'human_assessment': 0.15
    }
    
    scores = {
        'process_compliance': self._measure_process_compliance(),
        'output_quality': self._measure_output_quality(),
        'behavioral_alignment': self._measure_behavioral_alignment(),
        'human_assessment': self._get_human_assessment_score()
    }
    
    return sum(weights[k] * scores[k] for k in weights)

def check_promotion_eligibility(self) -> bool:
    """Check if agent meets promotion criteria."""
    score = self.calculate_trust_score()
    return score >= 0.90  # Promotion threshold
```

For detailed implementation patterns, see:

- `rjw-idd-methodology/operations/METHOD-0004-ai-agent-workflows.md` — Trust framework and behavioral contracts
- `rjw-idd-methodology/governance/METHOD-0002-phase-driver-checklists.md` — Risk classification and workflow selection

## Addons (Domain Extensions)

The methodology includes optional extensions for specific domains:

- **3D Game Core** — Specs and checklists for game development with Unity, Unreal, Godot
- **Video AI Enhancer** — Quality gates for real-time video enhancement pipelines

## Contributing

Methodology changes require a new decision record (`DEC-####`) justifying the modification. See `CONTRIBUTING.md` for details.

## License

See `LICENSE` for terms.
