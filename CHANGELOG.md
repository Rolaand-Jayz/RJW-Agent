# Changelog

All notable changes to the RJW-IDD Methodology will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]

### Changed

- Restructured repository to contain pure methodology only
- Removed starter kit code, scripts, and tools
- Repository now focuses on method documentation and artifact templates

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
