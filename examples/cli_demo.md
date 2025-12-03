# RJW-IDD CLI Demo

This document demonstrates the RJW-IDD CLI interface, which provides a similar experience to Google Gemini, Claude, and other AI CLI tools.

## Installation

```bash
# Clone the repository
git clone https://github.com/Rolaand-Jayz/RJW-Agent.git
cd RJW-Agent

# Install in development mode
pip install -e .
```

## Basic Usage

### Check Version

```bash
rjw version
```

Output:
```
RJW-IDD Agent CLI version 0.1.0
Intelligence Driven Development - Disciplined AI-assisted development
```

### Help Command

```bash
rjw --help
```

Shows all available commands and options.

## Interactive Mode

### Starting a Session

```bash
rjw
```

Or explicitly:

```bash
rjw chat
```

This starts an interactive session with a colorful prompt:

```
================================================================
                    RJW-IDD Agent CLI
================================================================
Session: session_20231203_143022_abc123
Trust Level: SUPERVISED
YOLO Mode: Disabled

Type /help for available commands
Type /exit or press Ctrl+D to quit

rjw>
```

### Interactive Commands

Once in interactive mode, you can:

1. **Ask questions or make requests:**
   ```
   rjw> Add authentication to my API
   ```

2. **Use special commands:**
   ```
   rjw> /help         # Show all commands
   rjw> /status       # Show session status
   rjw> /history 5    # Show last 5 turns
   rjw> /yolo         # Toggle YOLO mode
   rjw> /trust GUIDED # Change trust level
   rjw> /exit         # Exit the session
   ```

### Example Session

```
rjw> Add JWT authentication to the API

🔍 Processing your request...

✓ Research Complete

Research Topics:
  • authentication
  • API

Evidence Generated:
  • EVD-0001
  • EVD-0002

Governance:
  • Status: Approved
  • Mode: manual_required
  • Reason: Manual approval required - Trust level SUPERVISED insufficient for minimal risk or checklist failed

Next Steps:
  • Review generated evidence files
  • Create decision records (DEC) referencing evidence
  • Generate specifications (SPEC) backed by decisions
  • Write tests (TEST) to verify specifications

rjw> /status

================================================================
                      Session Status
================================================================

Session Info:
  • ID: session_20231203_143022_abc123
  • Turns: 1
  • Created: 2023-12-03T14:30:22

Artifacts:
  • Evidence: 2
  • Decisions: 0
  • Specifications: 0

Governance:
  • Trust Level: SUPERVISED
  • YOLO Mode: Disabled
  • Approvals: 1
```

## One-Shot Commands

For quick, non-interactive operations:

```bash
# Basic one-shot command
rjw run "Add authentication to API"

# With YOLO mode
rjw run "Implement caching" --yolo

# With specific trust level
rjw run "Add logging" --trust AUTONOMOUS

# Disable colors (for piping to files)
rjw run "Generate API docs" --no-color > output.txt
```

Example output:

```bash
$ rjw run "Add authentication to API" --yolo

Processing...

✓ Complete

Topics:
  • authentication

Evidence:
  • EVD-0001

Governance:
  • Approved: True
  • Mode: yolo
```

## Session Management

### List All Sessions

```bash
rjw sessions
```

Output:
```
================================================================
                   Available Sessions
================================================================

session_20231203_143022_abc123
  Created: 2023-12-03T14:30:22
  Turns: 5, Evidence: 3

session_20231203_150530_def456
  Created: 2023-12-03T15:05:30
  Turns: 2, Evidence: 1
```

### Resume a Session

```bash
rjw --session session_20231203_143022_abc123
```

### Show Session Details

```bash
rjw sessions --info session_20231203_143022_abc123
```

### Delete a Session

```bash
rjw sessions --delete session_20231203_143022_abc123
```

## Trust Levels

The CLI supports four trust levels from the RJW-IDD methodology:

### SUPERVISED (Default)
```bash
rjw --trust SUPERVISED
```
- All actions require approval
- Best for learning the methodology
- Highest governance oversight

### GUIDED
```bash
rjw --trust GUIDED
```
- Routine actions auto-approved
- Good balance of safety and efficiency
- Medium governance oversight

### AUTONOMOUS
```bash
rjw --trust AUTONOMOUS
```
- Most actions auto-approved
- For experienced users
- Lower governance overhead

### TRUSTED_PARTNER
```bash
rjw --trust TRUSTED_PARTNER
```
- Full autonomy with oversight
- Requires earned trust
- Minimal governance overhead

## YOLO Mode

YOLO mode enables automatic self-approval when checklist requirements are met:

```bash
# Start with YOLO mode
rjw --yolo

# Or toggle it in interactive mode
rjw> /yolo
✓ YOLO mode enabled
```

**Benefits:**
- Faster iteration
- Maintains governance through checklist validation
- Perfect for rapid prototyping

**Note:** YOLO mode still enforces all checklist requirements from METHOD-0002.

## Advanced Features

### Named Sessions

Create or resume named sessions for projects:

```bash
# Start a project-specific session
rjw --session my_api_project

# Resume later
rjw --session my_api_project
```

### Combining Options

```bash
# YOLO mode with high trust level and named session
rjw --yolo --trust AUTONOMOUS --session my_project
```

### Output Redirection

Disable colors for scripting:

```bash
rjw run "Analyze codebase" --no-color > analysis.txt
```

## Tips and Best Practices

1. **Start with SUPERVISED** - Learn the methodology before increasing autonomy
2. **Use named sessions** - Organize work by project or feature
3. **Check /status regularly** - Monitor artifact generation
4. **Review evidence files** - Ensure research quality before proceeding
5. **Use YOLO mode for prototypes** - Speed up experimental work
6. **Earn trust levels** - Progress through trust levels as you demonstrate consistency

## Keyboard Shortcuts (Interactive Mode)

- `Ctrl+D` - Exit the CLI
- `Ctrl+C` - Cancel current operation (confirms before exiting)
- `Arrow Up/Down` - Navigate command history (via readline)
- `Tab` - Command completion (when available)

## Session Storage

Sessions are stored in `.rjw-sessions/` directory:

```
.rjw-sessions/
├── session_20231203_143022_abc123.json
├── session_20231203_143022_abc123/
│   ├── research/
│   │   └── EVD-0001.md
│   ├── decisions/
│   └── specs/
└── ...
```

This keeps your work organized and resumable across CLI invocations.

## Troubleshooting

### CLI Not Found

If `rjw` command is not found after installation:

```bash
# Reinstall with entry points
pip install -e .

# Or run directly with Python
python -m src.cli.main
```

### Session Not Saving

Check that `.rjw-sessions/` directory has write permissions:

```bash
ls -la .rjw-sessions/
```

### Colors Not Working

Some terminals don't support ANSI colors. Use `--no-color` flag:

```bash
rjw --no-color
```

## Comparison with Other CLIs

### Like Google Gemini CLI
- Interactive conversation mode
- Natural language input
- Session management
- Clear visual formatting

### Like Claude CLI
- Command history
- Context awareness
- Multi-turn conversations
- Governance integration

### Like GitHub Copilot CLI
- One-shot commands
- Quick operations
- Development workflow integration

### Unique to RJW-IDD
- Research-first approach
- Evidence tracking
- Trust levels
- YOLO mode with governance
- Full traceability (EVD → DEC → SPEC → TEST)

## Next Steps

After using the CLI:

1. Review generated evidence files in `.rjw-sessions/[session]/research/`
2. Create decision records referencing evidence
3. Generate specifications based on decisions
4. Write tests to verify specifications
5. Implement with full traceability

For more information on the methodology, see:
- [Core Method](../rjw-idd-methodology/core/METHOD-0001-core-method.md)
- [Phase Checklists](../rjw-idd-methodology/governance/METHOD-0002-phase-driver-checklists.md)
- [Agent Workflows](../rjw-idd-methodology/operations/METHOD-0004-ai-agent-workflows.md)
