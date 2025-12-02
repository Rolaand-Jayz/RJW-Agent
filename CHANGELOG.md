# Changelog

All notable changes to the RJW-IDD Methodology will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]

### Added

- Implementation code snippets throughout documentation for agent developers
- Guidance on how to hardcode the framework into custom agents

### Changed

- Updated repository to include implementation guidance alongside methodology
- Repository now provides method documentation, templates, and code examples for building compliant agents

### Removed

- `rjw-idd-starter-kit/` directory (Python code, tests, tools)
- `scripts/` directory (Python/shell scripts)
- `bin/` directory (CLI tools)
- `ci_samples/` directory (sample CI files)
- Code-focused GitHub Actions workflows
- Python-specific linting and testing infrastructure

### Kept

- `rjw-idd-methodology/` — Core method documentation
  - Core principles (`METHOD-0001`)
  - Phase checklists (`METHOD-0002`)
  - Role handbook (`METHOD-0003`)
  - AI agent workflows (`METHOD-0004`)
  - Operations support (`METHOD-0005`)
- `rjw-idd-methodology/templates/` — Artifact templates
- `rjw-idd-methodology/addons/` — Domain-specific extensions
- `docs/` — Reference documentation
