# RJW-IDD Methodology Pack

This pack houses the source-of-truth guidance for Rolaand Jayz Wayz – Coding with Natural Language: Intelligence Driven Development (RJW-IDD).

## Directory Layout

- `core/` — enduring principles and lifecycle design (`METHOD-0001`).
- `governance/` — phase control, checklists, and role handbooks (`METHOD-0002`, `METHOD-0003`).
- `operations/` — execution playbooks for specialised use cases such as AI coding agents (`METHOD-0004`, `METHOD-0005`).
- `templates/` — boilerplates that downstream projects clone; prefixed with the artefact namespace they generate (e.g., `PROJECT-DEC-template.md`).
- `addons/` — domain-specific methodology extensions (3D game development, video AI).

## How to Use

1. Treat every file as method-level doctrine. Only modify after capturing a new `DEC-####` in your project evidence stream.
2. Copy templates into a project workspace before editing; do **not** customise the originals.
3. Keep project artefacts (decisions, specs, ledgers, prompts) under a project-specific prefix to avoid collisions with the `METHOD-####` namespace.

RJW-IDD deliberately keeps method guidance separate from project execution assets. This pack describes *how* to operate; downstream projects implement the methodology with their own IDs and evidence.

## Add-ons

- [3D Game Core](addons/3d-game-core/README.md) — specs and templates for 3D game development.
- [Video AI Enhancer](addons/video-ai-enhancer/README.md) — quality gates for real-time video enhancement.
