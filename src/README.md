# RJW-IDD Agent Framework - Source Code

This directory contains the Python implementation of the RJW-IDD (Intelligence Driven Development) agent framework. The framework enforces rigorous development processes with research-driven decision making and full traceability.

## Architecture

The framework is organized into five core modules, each implementing a specific aspect of the RJW-IDD methodology:

### 1. Discovery & Research (`discovery/`)

**Module:** `src.discovery.research.ResearchHarvester`

Implements METHOD-0001 Discovery Layer principles for evidence harvesting.

**Key Features:**
- Gathers research evidence and generates EVD-#### files
- Enforces evidence-first approach (research before decisions)
- Validates that all decisions and specifications reference valid evidence
- Tracks and registers all evidence artifacts

**Core Constraint:** No DEC or SPEC can be created without referencing valid EVD IDs.

**Example:**
```python
from src.discovery.research import ResearchHarvester

harvester = ResearchHarvester(output_dir="research/evidence")

# Harvest evidence on a topic
evd_id = harvester.harvest(
    topic="secure authentication patterns",
    source_type="Research",
    curator="Agent"
)

# Validate evidence exists before creating decisions
harvester.validate_evidence_exists(evd_id)  # True

# Enforce evidence requirement
harvester.require_evidence_for_artifact("DEC", [evd_id])  # Validates or raises error
```

### 2. Interaction Layer (`interaction/`)

**Module:** `src.interaction.optimizer.PromptOptimizer`

Orchestrates the RJW-IDD workflow from user input to specification.

**Key Features:**
- Accepts raw user strings as input
- Extracts research topics from user requests
- Delegates to ResearchHarvester to gather facts FIRST
- Creates decisions and specifications backed by evidence
- Maintains workflow state and traceability

**Core Principle:** Does NOT write Specs immediately. First delegates to Research Engine, then fills templates.

**Example:**
```python
from src.interaction.optimizer import PromptOptimizer

optimizer = PromptOptimizer()

# Process user input - automatically harvests evidence
result = optimizer.process_user_input(
    "I need to implement secure authentication for the API"
)

print(f"Research topics: {result['research_topics']}")
print(f"Evidence IDs: {result['evidence_ids']}")

# Create decision backed by evidence
dec_id = optimizer.create_decision_with_evidence(
    decision_title="Choose authentication method",
    evidence_refs=result['evidence_ids'],
    options=["JWT", "OAuth2", "Session-based"],
    chosen_option="JWT",
    rationale="Best balance of security and simplicity"
)

# Create spec with full traceability
spec_id = optimizer.create_spec_with_traceability(
    spec_title="JWT Authentication Implementation",
    evidence_refs=result['evidence_ids'],
    decision_refs=[dec_id],
    requirements=["REQ-001", "REQ-002"]
)
```

### 3. Governance & Autonomy (`governance/`)

**Module:** `src.governance.manager.GovernanceManager`

Implements METHOD-0004 trust ladder and METHOD-0002 checklist enforcement.

**Key Features:**
- YOLO mode: Agent self-approves if ChecklistEnforcer passes
- Standard mode: Trust-based approval with manual fallback
- Four trust levels: Supervised, Guided, Autonomous, Trusted Partner
- Phase gate checklist validation
- Comprehensive approval logging

**Example:**
```python
from src.governance.manager import GovernanceManager, TrustLevel

# Create manager in YOLO mode
manager = GovernanceManager(
    yolo_mode=True,
    trust_level=TrustLevel.AUTONOMOUS
)

# Request approval
approval = manager.request_approval(
    action="Create evidence file",
    phase="research",
    artifacts={'evidence_ids': ['EVD-0001']},
    risk_level="medium"
)

if approval['approved']:
    print(f"Approved via {approval['mode']}: {approval['reason']}")
else:
    print(f"Rejected: {approval['reason']}")

# Toggle modes
manager.set_yolo_mode(False)  # Switch to standard mode
manager.set_trust_level(TrustLevel.TRUSTED_PARTNER)  # Upgrade trust
```

### 4. Context Engine (`context/`)

**Module:** `src.context.engine.ContextCurator`

Implements METHOD-0006 Context Curation Engine with static analysis.

**Key Features:**
- AST-based static analysis (no LLM selection)
- Dependency graph construction
- Code slicing: extracts signatures, not full files
- Programmatic CTX-INDEX building
- Related code discovery

**Example:**
```python
from src.context.engine import ContextCurator

curator = ContextCurator(project_root="./src")

# Find related code
related = curator.find_related_code("authentication", max_depth=2)

# Build context index for a task
ctx_id = curator.build_context_index(
    task_id="AUTH-001",
    focus_areas=["authentication", "security"]
)

# Slice specific code elements
signatures = curator.slice_code(
    file_path="src/auth/manager.py",
    element_names=["AuthManager", "validate_token"]
)

# Get project structure
stats = curator.get_project_structure()
print(f"Analyzed {stats['files_analyzed']} files")
print(f"Found {stats['classes']} classes, {stats['functions']} functions")
```

### 5. The Jailer - System Guard (`system/`)

**Module:** `src.system.guard.SystemGuard`

Strict wrapper for file operations enforcing RJW-IDD traceability.

**Key Features:**
- Blocks code writes unless complete traceability chain exists
- Chain: EVD → SPEC → TEST (failing) → CODE
- Comprehensive operation logging
- Strict mode and relaxed mode support
- Traceability chain validation

**Core Rule:** No code write unless a failing TEST exists that is linked to a SPEC which is linked to EVD.

**Example:**
```python
from src.system.guard import SystemGuard

guard = SystemGuard(strict_mode=True)

# Build complete traceability chain
guard.register_evidence("EVD-0001", "/path/to/evd.md")
guard.register_spec("SPEC-0001", ["EVD-0001"], "/path/to/spec.md")
guard.register_test("TEST-0001", ["SPEC-0001"], "/path/to/test.py", "failing")

# Now write code (only works with complete chain)
try:
    guard.write_code(
        code_file="/path/to/implementation.py",
        content="def authenticate(user, password):\n    pass\n",
        test_refs=["TEST-0001"]
    )
    print("Code written successfully!")
except GuardViolation as e:
    print(f"Guard violation: {e}")

# Get traceability info
info = guard.get_traceability_info("/path/to/implementation.py")
print(f"Traceability chain: {info}")
```

## Utilities (`utils.py`)

**Module:** `src.utils.TemplateManager`

Manages template loading and artifact generation.

**Features:**
- Loads templates from `rjw-idd-methodology/templates/`
- Fills templates with data
- Generates artifact IDs (EVD-####, DEC-####, etc.)
- Saves artifacts to disk

## Installation

Install the framework in development mode:

```bash
# Install with dev dependencies
pip install -e ".[dev]"

# Or install just the framework
pip install -e .
```

## Running Tests

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest tests/ --cov=src --cov-report=html

# Run specific test module
pytest tests/test_discovery.py -v
```

## Usage Example: Complete Workflow

Here's how all modules work together in a complete RJW-IDD workflow:

```python
from src.interaction.optimizer import PromptOptimizer
from src.governance.manager import GovernanceManager, TrustLevel
from src.system.guard import SystemGuard

# 1. Initialize components
optimizer = PromptOptimizer()
governance = GovernanceManager(yolo_mode=True, trust_level=TrustLevel.AUTONOMOUS)
guard = SystemGuard(strict_mode=True)

# 2. Process user request (generates evidence automatically)
result = optimizer.process_user_input(
    "Implement JWT authentication for the REST API"
)

# 3. Request approval for research phase
approval = governance.request_approval(
    action="Research phase complete",
    phase="research",
    artifacts={'evidence_ids': result['evidence_ids']},
    risk_level="medium"
)

if not approval['approved']:
    raise Exception(f"Research phase not approved: {approval['reason']}")

# 4. Create decision with evidence
dec_id = optimizer.create_decision_with_evidence(
    decision_title="Select JWT library",
    evidence_refs=result['evidence_ids'],
    options=["PyJWT", "python-jose", "Authlib"],
    chosen_option="PyJWT",
    rationale="Most widely used, well-maintained"
)

# 5. Create specification
spec_id = optimizer.create_spec_with_traceability(
    spec_title="JWT Authentication Implementation",
    evidence_refs=result['evidence_ids'],
    decision_refs=[dec_id],
    requirements=["REQ-AUTH-001", "REQ-AUTH-002"]
)

# 6. Register with guard system
for evd_id in result['evidence_ids']:
    guard.register_evidence(evd_id, f"research/evidence/{evd_id}.md")

guard.register_spec(spec_id, result['evidence_ids'], f"specs/{spec_id}.md")
guard.register_test("TEST-0001", [spec_id], "tests/test_auth.py", "failing")

# 7. Write implementation (guard enforces traceability)
guard.write_code(
    code_file="src/auth/jwt_manager.py",
    content="# JWT implementation...\n",
    test_refs=["TEST-0001"]
)

print("Workflow complete with full traceability!")
```

## Design Principles

1. **Evidence First**: All decisions and specifications must be backed by research evidence
2. **Traceability**: Complete chain from evidence through to code
3. **Gated Workflow**: Each phase must pass checkpoints before proceeding
4. **Trust-Based Autonomy**: Agent autonomy scales with demonstrated reliability
5. **Static Analysis**: Context curation uses AST, not LLM guessing
6. **Explicit Constraints**: Guard system enforces rules at runtime

## Integration with RJW-IDD Methodology

This implementation directly maps to the RJW-IDD methodology documents:

- **METHOD-0001** (Core Method): Discovery & Research module
- **METHOD-0002** (Lifecycle): Governance Manager checklist enforcement
- **METHOD-0004** (Agent Workflows): Trust ladder and behavioral contracts
- **METHOD-0006** (Context Curation): Context Engine implementation

## Contributing

When adding new functionality:

1. Follow existing module patterns
2. Add comprehensive tests
3. Update this README
4. Ensure all five modules remain decoupled
5. Maintain the evidence-first principle

## License

See repository LICENSE file.
