# datev-functional-advisor (Skill)

A reusable AI agent skill that answers "what does that mean, why does DATEV do it that way, and how does it map to ERPNext?" for phamos consultants, developers and customer accounting users. It explains; it does not build, review or import, and routes those jobs to the matching skill.

- Adapts depth to the audience and answers in the user's language, keeping DATEV terms in German.
- Short explanations of the core DATEV concepts (Mandant, EXTF/DTVF, Buchungsstapel, Konto/Gegenkonto, BU-Schlüssel vs Automatikkonto, OPOS, Festschreibung, KOST, Unternehmen online, …).
- ERPNext to DATEV mapping table based on phamos/datev, and a guide to choosing the right DATEV interface.
- Tax boundary: explains concepts and typical setups, but never decides a BU-Schlüssel or tax treatment for a customer; turns such questions into precise questions for the Steuerberater.

## Files

- SKILL.md: the explanations and routing an AI agent loads.

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
- Agent CLIs that read instruction files from the repository root (AGENTS.md, CLAUDE.md, .cursor/rules): add an entry such as "For DATEV questions, start with skills/datev-functional-advisor/SKILL.md".
- One-off usage: paste SKILL.md into the conversation.

Keep this repository folder as the source of truth; update the skill here first, then propagate copies to the individual environments.
