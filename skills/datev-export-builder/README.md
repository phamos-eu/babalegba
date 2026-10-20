# datev-export-builder (Skill)

A reusable AI agent skill that plans and builds a customer's **ERPNext to DATEV export** on top of the phamos/datev app (git.phamos.eu/phamos/datev), solving as much as possible through configuration and approving every step with the user.

- Preconditions: a discovery issue without blocking items, a fresh spec check, and phamos/datev read live from GitLab (its docs are the source of truth).
- Fit-gap in plain language, with a clear order of preference: configuration, then a generic extension of phamos/datev (a new setting, not customer code paths), then the customer app.
- Small, testable increments (build-stepwise), automation only as a toggle, Frappe standards and fixtures.
- Hard rules: never invent BU-Schlüssel, accounts or mappings; one file per period with at most 99,999 rows; never send test files to the productive Mandant.
- Festschreibung (default 0) and "submitted vouchers only" (default on) are DATEV Settings, not hard-coded.
- Done only after three gates: regex self-check (datev-spec-extf validator), Steuerberater test import, accounting user sign-off.

## Files

- SKILL.md: the process an AI agent loads and follows.

## DATEV skill family

| Skill | Job |
|---|---|
| datev-spec-extf | Reference: DATEV-Format (EXTF CSV) |
| datev-spec-xml-online | Reference: XML-Schnittstelle online (DUO document packages) |
| datev-customer-discovery | Structured customer/Steuerberater discovery, recorded as a GitLab issue |
| datev-export-builder | Build ERPNext to DATEV exports on top of phamos/datev, configuration first |
| datev-file-reviewer | Review files, packages, exporter code, DATEV error logs and configuration |
| datev-importer | DATEV to ERPNext imports via a reviewable DATEV Import tool |
| datev-functional-advisor | Explain DATEV concepts and the ERPNext mapping; route to the other skills |

## Adoption in Different AI Environments

- Agent CLIs with a skills directory: copy or symlink this folder into the tool's skills directory (for example .claude/skills/ for Claude Code).
- Agent CLIs that read instruction files from the repository root (AGENTS.md, CLAUDE.md, .cursor/rules): add an entry such as "When building or changing a DATEV export, follow skills/datev-export-builder/SKILL.md".
- One-off usage: paste SKILL.md into the conversation.

Keep this repository folder as the source of truth; update the skill here first, then propagate copies to the individual environments.
