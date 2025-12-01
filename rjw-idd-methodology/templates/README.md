# RJW-IDD Templates

This directory contains boilerplate templates for all artefact types used in the RJW-IDD methodology. Copy templates into your project workspace; **never modify the originals**.

## Directory Structure

```text
templates/
├── decisions/              # Decision record templates
│   └── DEC-template.md     # Tree-of-Thought decision capture
├── requirements/           # Requirement templates
│   └── REQ-template.md     # Requirement specification
├── specs/                  # Specification templates
│   └── SPEC-template.md    # Technical specification
├── evidence/               # Evidence templates
│   └── EVD-template.md     # Research evidence capture
├── testing/                # Test case templates
│   └── TEST-template.md    # Test case definition
├── documentation/          # Documentation templates
│   └── DOC-template.md     # Standards, runbooks, guides
├── governance/             # Governance templates
│   ├── CHANGE-LOG-template.md              # Change tracking
│   ├── STAGE-AUDIT-LOG-template.md         # Phase audit reflections
│   ├── REQ-LEDGER-template.md              # Requirement traceability
│   └── LIVING-DOCS-RECONCILIATION-template.md  # Documentation gap tracking
├── context/                # Context curation templates
│   ├── CTX-INDEX-template.md               # Task context index
│   └── LIVING-DOCS-template.md             # Project living documentation
├── PROTO-template.md       # Prototype record (POC/spike)
├── DEC-LITE-template.md    # Lightweight decision (Low/Medium risk)
└── AGENT-TRUST-template.md # Agent trust level changes
```

## Template Categories

### Decisions (`decisions/`)

| Template | Purpose | Identifier Pattern |
|----------|---------|-------------------|
| `DEC-template.md` | Capture strategic choices with options, trade-offs, and rationale | `DEC-####` |

### Requirements (`requirements/`)

| Template | Purpose | Identifier Pattern |
|----------|---------|-------------------|
| `REQ-template.md` | Define what the system must do or how it must behave | `REQ-####` |

### Specifications (`specs/`)

| Template | Purpose | Identifier Pattern |
|----------|---------|-------------------|
| `SPEC-template.md` | Technical design addressing requirements | `SPEC-####` |

### Evidence (`evidence/`)

| Template | Purpose | Identifier Pattern |
|----------|---------|-------------------|
| `EVD-template.md` | Research findings supporting decisions | `EVD-####` |

### Testing (`testing/`)

| Template | Purpose | Identifier Pattern |
|----------|---------|-------------------|
| `TEST-template.md` | Verify specifications meet acceptance criteria | `TEST-####` |

### Documentation (`documentation/`)

| Template | Purpose | Identifier Pattern |
|----------|---------|-------------------|
| `DOC-template.md` | Standards, runbooks, guides, and references | `DOC-####` |

### Governance (`governance/`)

| Template | Purpose | Usage |
|----------|---------|-------|
| `CHANGE-LOG-template.md` | Track methodology/project changes | `docs/change-log.md` |
| `STAGE-AUDIT-LOG-template.md` | Phase gate audit reflections | `logs/LOG-####-stage-audits.md` |
| `REQ-LEDGER-template.md` | Requirement traceability matrix | `artifacts/ledgers/requirement-ledger.md` |
| `LIVING-DOCS-RECONCILIATION-template.md` | Documentation debt tracking | `docs/living-docs-reconciliation.md` |

### Prototypes (Root Level)

| Template | Purpose | Identifier Pattern |
|----------|---------|-------------------|
| `PROTO-template.md` | Rapid POC/spike documentation with Keep/Flex/Unknown tagging | `PROTO-####` |

### Context Curation (`context/`)

| Template | Purpose | Usage |
|----------|---------|-------|
| `CTX-INDEX-template.md` | Task-specific context index for AI agent work | `docs/context/CTX-INDEX-####.md` |
| `LIVING-DOCS-template.md` | Project living documentation as governed source of truth | `docs/living-docs.md` |

## How to Use

### 1. Copy the Template

```bash
cp rjw-idd-methodology/templates/decisions/DEC-template.md \
   my-project/docs/decisions/DEC-0001.md
```

### 2. Rename with Sequential ID

Use monotonically increasing identifiers within your project namespace.

### 3. Fill in the Template

Replace placeholder values (XXXX, YYYY-MM-DD, etc.) with actual content.

### 4. Link to Related Artefacts

Populate traceability sections to maintain the audit trail.

### 5. Update Governance Logs

Record the new artefact in your change log and update relevant ledgers.

## Traceability Guidelines

Every artefact should trace to related artefacts:

```text
Evidence (EVD) → Requirements (REQ) → Specifications (SPEC) → Tests (TEST)
                          ↓
                    Decisions (DEC)
                          ↓
                  Documentation (DOC)
```

Maintain bidirectional links where possible to support audits.

## Integration with Method Phases

| Phase | Primary Templates |
|-------|-------------------|
| **Discovery — Research** | `EVD-template.md`, `DEC-template.md` |
| **Discovery — Specification** | `REQ-template.md`, `SPEC-template.md`, `DEC-template.md` |
| **Execution** | `TEST-template.md`, `DOC-template.md` |
| **Governance** | All governance templates |
| **Context Curation** | `CTX-INDEX-template.md`, `LIVING-DOCS-template.md` |

## Add-on Specific Templates

Domain-specific add-ons provide additional templates:

- **3D Game Core:** `addons/3d-game-core/specs/templates/`
- **Video AI Enhancer:** `addons/video-ai-enhancer/specs/templates/`

These extend the base templates with domain-specific sections and acceptance criteria.

## Related Documentation

- Core Method: `core/METHOD-0001-core-method.md`
- Unified Lifecycle & Checklists: `governance/METHOD-0002-phase-driver-checklists.md`
- Role Handbook: `governance/METHOD-0003-role-handbook.md`
- Unified Agent Handbook: `operations/METHOD-0004-ai-agent-workflows.md`
- Operations Support: `operations/METHOD-0005-operations-production-support.md`
- Context Curation Engine: `operations/METHOD-0006-context-curation-engine.md`
