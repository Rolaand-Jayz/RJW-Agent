# Copilot Instructions

## Repository Purpose

This repository contains the **RJW-IDD Methodology** — documentation, templates, and implementation guidance for building agents that adhere to this framework.

## Repo Structure

- `rjw-idd-methodology/` — Core method documentation
  - `core/` — Foundational principles (`METHOD-0001`)
  - `governance/` — Phase checklists and role handbooks (`METHOD-0002`, `METHOD-0003`)
  - `operations/` — Execution playbooks (`METHOD-0004`, `METHOD-0005`)
  - `templates/` — Artifact templates for downstream projects
  - `addons/` — Domain-specific extensions (3D game, video AI)
  - `docs/` — Method-level change log and decisions

- `docs/` — Reference documentation
  - `governance.md`, `runbooks/`, `decisions/`

- `src/` — Python implementation of the RJW-IDD framework
  - `cli/` — Command-line interface
  - `context/` — Context curation engine
  - `discovery/` — Research and evidence gathering
  - `governance/` — Checklist enforcement and phase gates
  - `interaction/` — Agent interaction and trust management
  - `system/` — Core system components

- `tests/` — Test suite using pytest

## Working with This Repository

### Template Boundaries

- Templates in `rjw-idd-methodology/templates/` should be copied to project workspaces, never modified in place
- Addons provide domain-specific templates and guidance

### When Making Changes

- Every methodology update requires a new decision record (`DEC-####`) justifying the change
- Update `rjw-idd-methodology/docs/change-log.md` for all changes
- Keep documentation clear and accessible

### What TO Add

- Method documentation and guidance
- Templates for artifacts (decisions, specs, requirements)
- Checklists and role definitions
- Domain-specific methodology extensions (addons)
- Implementation code snippets and examples for agent developers

## Development Workflow

### Installation and Setup

```bash
# Install the package in development mode
pip install -e .

# Install with development dependencies
pip install -e ".[dev]"
```

### Running Tests

```bash
# Run all tests
python3 -m pytest -v

# Run with coverage
python3 -m pytest --cov=src --cov-report=html

# Run specific test file
python3 -m pytest tests/test_cli.py -v

# Run tests matching a pattern
python3 -m pytest -k "test_session" -v
```

### Code Quality

```bash
# Format code with Black
black src/ tests/

# Check formatting without changing files
black --check src/ tests/

# Lint with flake8
flake8 src/ tests/

# Type check with mypy
mypy src/
```

### Running the CLI

```bash
# Start interactive mode
rjw

# One-shot command
rjw run "your task description"

# With YOLO mode (auto-approval)
rjw --yolo

# Set trust level
rjw --trust AUTONOMOUS
```

## Code Style and Conventions

### Python Style

- Follow PEP 8 style guide
- Use Black for formatting (line length: 88 characters)
- Use type hints for all functions and methods
- Use docstrings for all public functions, classes, and modules
- Use snake_case for functions and variables
- Use PascalCase for class names

### Testing Requirements

- All new features must include unit tests
- Tests should follow the AAA pattern (Arrange, Act, Assert)
- Test files should be named `test_*.py`
- Test classes should be named `Test*`
- Test functions should be named `test_*`
- Aim for meaningful test coverage of new code

### Documentation Requirements

- Update README.md for user-facing changes
- Update docstrings for API changes
- Document complex logic with inline comments (sparingly)
- Keep methodology documents synchronized with implementation

## Security Considerations

- Never commit secrets or credentials
- Use environment variables for sensitive configuration
- Validate all user inputs
- Follow principle of least privilege
- Review dependencies for known vulnerabilities before adding

## Common Pitfalls

### Template Modifications

❌ **Don't**: Modify templates in `rjw-idd-methodology/templates/` directly
✅ **Do**: Copy templates to project workspaces and modify copies

### Methodology Changes

❌ **Don't**: Make ad-hoc changes to methodology documents
✅ **Do**: Create a decision record (`DEC-####`) first, then update change log

### Testing

❌ **Don't**: Skip tests for "small" changes
✅ **Do**: Write tests for all code changes, no matter how small

### Documentation

❌ **Don't**: Let documentation drift from implementation
✅ **Do**: Update docs in the same PR as code changes

## Task Suitability

### Good Tasks for Copilot

- Adding new test cases
- Refactoring code for clarity
- Adding docstrings and documentation
- Implementing well-defined features
- Fixing bugs with clear reproduction steps
- Creating new templates following existing patterns

### Tasks Requiring Human Review

- Methodology design decisions
- Breaking API changes
- Security-sensitive code
- Complex architectural changes
- Risk classification logic

## Project-Specific Context

### RJW-IDD Methodology

This project implements a disciplined methodology for AI-assisted development with:

- **Discovery Layer**: Research, evidence curation, specification synthesis
- **Execution Layer**: Test-driven development, living documentation
- **Trust Ladder**: Four levels (Supervised, Guided, Autonomous, Trusted Partner)
- **Three Pathways**: Streamlined, YOLO, Prototype

### Key Concepts

- **Evidence (EVD-####)**: Research findings backing decisions
- **Decisions (DEC-####)**: Strategic choices with rationale
- **Requirements (REQ-####)**: System requirements with acceptance criteria
- **Specifications (SPEC-####)**: Technical designs addressing requirements
- **Context Index (CTX-####)**: Task-specific context for AI agents

### File Naming Conventions

- Decision records: `DEC-####-description.md`
- Evidence files: `EVD-####-topic.md`
- Requirements: `REQ-####-feature.md`
- Specifications: `SPEC-####-design.md`
- Test templates: `TEST-####-scenario.md`
