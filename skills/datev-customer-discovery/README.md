# datev-customer-discovery (Skill)

A reusable AI agent skill that finds out **how a customer's DATEV world works** before anyone builds or changes a DATEV export, DUO transfer or import. The result is a GitLab issue in the customer's project that the other DATEV skills rely on.

- Reads what the ERPNext site already shows first (chart of accounts, DATEV Settings, Tax Categories, Item Tax Templates, Party Accounts, voucher volumes) and asks only for confirmation there.
- Grills one question at a time across six sections: people and handoff, DATEV Mandant data, scope, booking logic, optional DATEV features, test and acceptance.
- Separates questions for the Steuerberater from questions for the customer and marks blocking items, such as payments exported while the Steuerberater also books bank data, or a voucher type booked both via EXTF and DUO ledger data.
- Classifies every requirement as configuration, generic phamos/datev extension or customer app, after reading phamos/datev live.

Never copies another customer's answers as facts; similar customers may only be named as inspiration.

## Files

- SKILL.md: the process and the GitLab issue template.

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
- Agent CLIs that read instruction files from the repository root (AGENTS.md, CLAUDE.md, .cursor/rules): add an entry such as "Before any DATEV work for a customer, follow skills/datev-customer-discovery/SKILL.md".
- One-off usage: paste SKILL.md into the conversation.

Keep this repository folder as the source of truth; update the skill here first, then propagate copies to the individual environments.
