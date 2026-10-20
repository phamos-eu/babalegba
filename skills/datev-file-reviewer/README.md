# datev-file-reviewer (Skill)

A reusable AI agent skill that checks **whether what we send to DATEV is right**, and if not, why, traced back to the ERPNext document, setting or line of code that caused it.

- Review modes: EXTF files, DUO XML packages, exporter code, DATEV error logs (Stapelverarbeitung protocol, Prüfprogramm, Belegtransfer; PDF, screenshot or text) and ERPNext DATEV configuration.
- Reviews against the customer's discovery issue, the current DATEV spec and phamos/datev as read live, never against memory.
- Includes the double-booking check (payments, and vouchers sent both via EXTF and DUO ledger data).
- Findings ranked as Blocker, Wrong data, Spec deviation or Cosmetic, each with example, root cause, fix, owner and how to verify.
- Reports in chat first; files GitLab issues only after approval, after checking for duplicates, in phamos/datev (generic) or the customer project (configuration and customer code). Never changes code or configuration itself.

## Files

- SKILL.md: the review process an AI agent loads and follows.

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
- Agent CLIs that read instruction files from the repository root (AGENTS.md, CLAUDE.md, .cursor/rules): add an entry such as "To check a DATEV file, error log or configuration, follow skills/datev-file-reviewer/SKILL.md".
- One-off usage: paste SKILL.md into the conversation.

Keep this repository folder as the source of truth; update the skill here first, then propagate copies to the individual environments.
