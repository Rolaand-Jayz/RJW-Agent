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
