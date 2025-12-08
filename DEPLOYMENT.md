# Deployment Guide

This document provides instructions for deploying and using the RJW-IDD Agent CLI.

## Prerequisites

- Python 3.8 or higher
- pip package manager

## Installation

### From Source

1. Clone the repository:
```bash
git clone https://github.com/Rolaand-Jayz/RJW-Agent.git
cd RJW-Agent
```

2. Install the package:
```bash
pip install -e .
```

3. Verify installation:
```bash
rjw --version
```

### From PyPI (when published)

```bash
pip install rjw-idd-agent
```

## Quick Start

### Interactive Mode

Start an interactive session:

```bash
rjw
```

Or explicitly:

```bash
rjw chat
```

### One-Shot Commands

Execute a single command:

```bash
rjw run "Add authentication to API"
```

With options:

```bash
rjw run "Implement caching" --yolo --trust AUTONOMOUS
```

## Core Features

### 1. Research-Driven Development

The agent follows RJW-IDD methodology:
1. **Evidence Gathering** (EVD-#### files)
2. **Decision Making** (DEC-#### files)
3. **Specification** (SPEC-#### files)
4. **Testing** (TEST-#### files)

Every decision and specification must be backed by evidence.

### 2. Context Curation Engine (METHOD-0006)

The Context Curation Engine implements the complete METHOD-0006 framework:

**METHOD-0006 Components:**
- **Section 2**: Complete Context Index structure (Task Scope, Affected Areas, Technical Context, Assumptions, Dependencies, Change History)
- **Section 3**: Turn-based context evaluation with relevance scoring (0.0-1.0)
- **Section 4**: Context update triggers and automatic propagation
- **Section 5**: Living Documentation integration

**Technical Implementation:**
- Uses **static analysis** (AST) for code discovery (no LLM inference)
- Extracts **signatures only**, not full files
- Builds task-specific **Context Indexes** (CTX-####)
- Applies **relevance scores** (0.0-1.0) to all context items

**Usage:**

```bash
# In interactive mode
rjw

# Prepare implementation context
/context TASK-001 authentication,authorization
```

**Output:**
```
✓ Context Index Created

Context Information:
  • Context ID: CTX-TASK-001
  • Task ID: TASK-001
  • Focus Areas: authentication, authorization
  • Related Files: 5
  • Signatures Extracted: 12
  • Method: static_analysis (no LLM)
```

### 3. Governance & Trust Levels

Four trust levels from RJW-IDD methodology:

- **SUPERVISED** (default) - All actions require approval
- **GUIDED** - Routine actions auto-approved
- **AUTONOMOUS** - Most actions auto-approved
- **TRUSTED_PARTNER** - Full autonomy with oversight

Set trust level:

```bash
# CLI flag
rjw --trust AUTONOMOUS

# Interactive command
/trust AUTONOMOUS
```

### 4. YOLO Mode

Enable automatic self-approval when checklist requirements are met:

```bash
# CLI flag
rjw --yolo

# Interactive command
/yolo
```

## CLI Commands

### Interactive Mode Commands

| Command | Description |
|---------|-------------|
| `/help` | Show available commands |
| `/status` | Show session status (evidence, decisions, specs, context indexes) |
| `/history [limit]` | Show conversation history |
| `/clear` | Clear conversation history |
| `/yolo` | Toggle YOLO mode on/off |
| `/trust <level>` | Set trust level |
| `/context <task_id> <focus_areas>` | Prepare implementation context (METHOD-0006) |
| `/exit` or `/quit` | Exit the CLI (or use Ctrl+D) |

### Session Management

```bash
# List all sessions
rjw sessions

# Show session info
rjw sessions --info session_20231203_143022_abc123

# Delete a session
rjw sessions --delete session_20231203_143022_abc123
```

## Architecture

### Module Structure

```
src/
├── cli/                # CLI interface
│   ├── main.py        # Entry point
│   ├── interactive.py # REPL implementation
│   ├── session.py     # Session management
│   └── formatter.py   # Output formatting
├── interaction/        # Interaction layer
│   └── optimizer.py   # Prompt optimizer & workflow orchestration
├── discovery/          # Research & evidence gathering
│   └── research.py    # ResearchHarvester
├── context/            # Context curation engine
│   └── engine.py      # ContextCurator (METHOD-0006)
├── governance/         # Governance & autonomy
│   └── manager.py     # Trust levels & YOLO mode
└── system/             # System guard
    └── guard.py       # Traceability enforcement
```

### Key Principles

1. **Evidence First**: Every decision must reference EVD-####
2. **Traceability**: EVD → DEC → SPEC → TEST chain enforced
3. **METHOD-0006 Framework**: Complete context curation implementation
   - Turn-based evaluation cycle
   - Relevance scoring (0.0-1.0)
   - Context update triggers and propagation
   - Living Documentation integration
4. **Static Analysis**: No LLM-based context selection (AST-based code discovery)
5. **Signature Extraction**: Code slicing provides signatures, not full files

## Workflow Example

```bash
# Start interactive session
rjw

# Agent processes your request and gathers evidence
You> I need to implement user authentication

# Output:
✓ Research Complete

Research Topics:
  • authentication

Evidence Generated:
  • EVD-0001

# Prepare implementation context
/context TASK-001 authentication,user

# Output:
✓ Context Index Created
  • Context ID: CTX-TASK-001
  • Related Files: 5
  • Signatures Extracted: 12

# Check status
/status

# Output shows:
Session Status
  Evidence: 1
  Decisions: 0
  Specifications: 0
  Context Indexes: 1

Context Engine (METHOD-0006):
  • Context indexes created: 1
  Active indexes:
    - CTX-TASK-001
```

## Configuration

### Session Storage

Sessions are stored in `.rjw-sessions/` directory:

```
.rjw-sessions/
└── session_20231203_143022_abc123/
    ├── session.json
    ├── research/
    │   └── EVD-0001.md
    ├── decisions/
    └── specs/
```

### Output Directories

Default output directories (configurable):
- Evidence: `research/evidence/`
- Decisions: `decisions/`
- Specifications: `specs/`

## Testing

Run the test suite:

```bash
pytest tests/ -v
```

Current test coverage: 114 tests, all passing

## Troubleshooting

### CLI Not Found

If `rjw` command is not found:

```bash
# Check if installed
pip show rjw-idd-agent

# Reinstall
pip install -e . --force-reinstall

# Or run directly
python -m src.cli.main
```

### Context Engine Issues

If context engine fails to analyze code:

- Ensure project has Python files (`.py`)
- Check file permissions
- Verify no syntax errors in source files

### Session Issues

If session persistence fails:

```bash
# Clear sessions
rm -rf .rjw-sessions/

# Start fresh
rjw
```

## Best Practices

1. **Start with Evidence**: Always gather research before making decisions
2. **Use Context Engine**: Prepare context indexes before implementation
3. **Incremental Trust**: Start with SUPERVISED, increase as agent proves reliable
4. **Regular Status Checks**: Use `/status` to track progress
5. **Session Management**: Use named sessions for different projects

## Security Notes

- No secrets or credentials are stored in sessions
- All data stored locally in `.rjw-sessions/`
- Context engine uses static analysis only (no external calls)
- YOLO mode still enforces checklists

## Support

For issues, questions, or contributions:
- GitHub: https://github.com/Rolaand-Jayz/RJW-Agent
- Issues: https://github.com/Rolaand-Jayz/RJW-Agent/issues

## License

See LICENSE file for details.
