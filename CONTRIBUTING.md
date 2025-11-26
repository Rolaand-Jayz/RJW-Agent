# Contributing to RJW-IDD Methodology

This repository contains the RJW-IDD methodology documentation and templates. Contributions are welcome.

## What This Repository Contains

- **Methodology documents** — Core method, phase checklists, role handbooks, operational playbooks
- **Templates** — Decision record templates, specification templates
- **Domain addons** — Extensions for 3D game development, video AI enhancement

## How to Contribute

### 1. Fork and Branch

1. Fork the repository
2. Create a topic branch: `feature/<short-desc>` or `fix/<short-desc>`

### 2. Making Changes

- **Methodology changes** require a new decision record (`DEC-####`) justifying the modification
- Update the change log (`rjw-idd-methodology/docs/change-log.md`) with every meaningful change
- Keep templates clean — they should be copied by downstream projects, not modified in place

### 3. Submit a Pull Request

1. Ensure markdown files pass linting (markdownlint)
2. Open a PR with a clear description
3. Reference any related decision records

## Change Control

Every change to the methodology must:

- Be captured in a decision record using `rjw-idd-methodology/templates/PROJECT-DEC-template.md`
- Be logged in `rjw-idd-methodology/docs/change-log.md`
- Be reviewed by at least one maintainer

## Style Guidelines

- Use clear, accessible language
- Follow existing document structure and naming conventions
- Keep templates domain-neutral so they can be applied to any project

## Security

For security issues, see `SECURITY.md`.
