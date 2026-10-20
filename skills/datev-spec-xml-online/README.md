# datev-spec-xml-online (Skill)

Reference skill for the **DATEV XML-Schnittstelle online**: ZIP document packages that bring documents (Belege) and optional booking data into DATEV Unternehmen online (DUO). It is the companion of datev-spec-extf.

- Package rules: one document.xml, optional ledger XML files, the document files, size and count limits, ASCII file names.
- Character set and XML rules (UTF-8 allow-list, element order, no empty elements).
- document.xml and ledger XML field by field, with types and lengths taken from the official XSD v6.0 files, not only from the prose.
- phamos usage patterns: route A (PDF + GUID, bookings via EXTF with Beleglink) and route B (PDF + ledger data, per company).
- XSD validation snippet, transfer channels (DATEV Belegtransfer, accounting:dxso-jobs) and known contradictions between XSD and prose.

Snapshot of the DATEV documentation and XSD files: 2026-10-20 (interface version 6.0, latest changelog entry March 2023).

## Files

- SKILL.md: the reference an AI agent loads.

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
- Agent CLIs that read instruction files from the repository root (AGENTS.md, CLAUDE.md, .cursor/rules): add an entry such as "For DATEV Unternehmen online XML packages, follow skills/datev-spec-xml-online/SKILL.md".
- One-off usage: paste SKILL.md into the conversation.

Keep this repository folder as the source of truth; update the skill here first, then propagate copies to the individual environments.
