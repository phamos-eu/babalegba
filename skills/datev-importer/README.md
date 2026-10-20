# datev-importer (Skill)

A reusable AI agent skill that brings **DATEV data into ERPNext reviewably**: nothing lands in the books without the user seeing a preview and approving it.

- Target design for a generic **DATEV Import** tool in phamos/datev (milestone "DATEV Import Tool", issues #30–#35): upload, detect, validate, preview with diff, approve, create; Journal Entries always as drafts; idempotent via row fingerprints; full automation only as a later toggle.
- Reading rules for EXTF/DTVF files (encoding, header checks against DATEV Settings, column mapping by heading row).
- Handlers: Kontenbeschriftungen to Accounts, Debitoren/Kreditoren to Customers and Suppliers, opening balances at go-live (with reconciliation against the Steuerberater's Summen- und Saldenliste), and the Steuerberater's own bookings back as draft Journal Entries.
- The bookings-back flow filters out ERPNext's own exported bookings in layers (Herkunft-Kz, known voucher numbers and GUIDs, fingerprints) before the accounting user ticks off the rest, and reverses BU-Schlüssel via the Item Tax Template mapping.

## Files

- SKILL.md: the design and process an AI agent loads and follows.

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
- Agent CLIs that read instruction files from the repository root (AGENTS.md, CLAUDE.md, .cursor/rules): add an entry such as "When importing DATEV data into ERPNext, follow skills/datev-importer/SKILL.md".
- One-off usage: paste SKILL.md into the conversation.

Keep this repository folder as the source of truth; update the skill here first, then propagate copies to the individual environments.
