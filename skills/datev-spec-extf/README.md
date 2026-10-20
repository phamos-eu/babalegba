# datev-spec-extf (Skill)

Reference skill for the **DATEV-Format** (EXTF CSV files imported into DATEV Rechnungswesen). It is the single source of truth for field-level facts in the DATEV skill family. It does not build anything; it answers "what does DATEV expect in field X", checks files and keeps itself current.

- Stable core inline: CSV and encoding rules, header v700 (all 31 fields), Buchungsstapel v13 (column order and core fields), Debitoren/Kreditoren, Sachkontenbeschriftungen, other categories, import channels.
- Live lookup: the DATEV developer portal is a JavaScript app; the skill reads its JSON API directly (or through the browser as fallback) and checks the DATEV changelog for drift against the snapshot date.
- Known quirks in DATEV's own spec are listed instead of silently "fixed".
- validate_extf.py checks a file against the header and Buchungsstapel core rules (tested against DATEV's sample data).

Snapshot of the DATEV documentation: 2026-10-20 (latest changelog entry March 2025).

## Files

- SKILL.md: the reference an AI agent loads.
- validate_extf.py: regex self-check for EXTF files (`python3 -I validate_extf.py EXTF_Buchungsstapel.csv`).

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

Like the other skills in this repository, this skill is plain Markdown:

- Agent CLIs with a skills directory: copy or symlink this folder into the tool's skills directory (for example .claude/skills/ for Claude Code) so it loads when a task matches the description in the SKILL.md frontmatter.
- Agent CLIs that read instruction files from the repository root (AGENTS.md, CLAUDE.md, .cursor/rules): add an entry such as "For DATEV-Format field rules, follow skills/datev-spec-extf/SKILL.md".
- One-off usage: paste SKILL.md into the conversation.

Keep this repository folder as the source of truth; update the skill here first, then propagate copies to the individual environments.
