# frappe-custom-app-builder (Skill)

A reusable AI agent skill for initiating a new custom app for the Frappe Framework / ERPNext (v15 or v16). It turns "create an app for client X" into a repeatable process:

- A structured intake interview that makes the initiator decide everything that is hard to change later: app name, license, publisher and contact, target Frappe/ERPNext version, required apps, deployment target (including Frappe Cloud), repository and branch model, and team conventions.
- Scaffolding with bench new-app only, never by hand.
- Hardening of the scaffold for what bench new-app leaves out, so the app installs on Frappe Cloud from the first commit.
- Verification on a real site before anything is pushed, and a handover report with open follow-ups.

The process is distilled from real app initializations, including the failures they ran into: hand-written scaffolds rejected by Frappe Cloud, a missing [tool.bench.frappe-dependencies] table, frappe listed as a Python dependency, hostname-based commit authors, unfilled license placeholders, and push conflicts with a README created by the hosting service.

## Files

- SKILL.md — the process an AI agent loads and follows (eight phases with gates).
- intake-questionnaire.md — every intake question with reasons, options, defaults, and the intake record template.
- references.md — version matrix, bench new-app prompt order, hardening snippets, Frappe Cloud notes, commands and links.
- checklist.md — definition of done, walked through before the app is reported as initialized.

## Adoption in Different AI Environments

Like the other skills in this repository, this skill is plain Markdown so any AI coding tool can use it:

- Agent CLIs with a skills directory: copy or symlink this folder into the tool's skills directory (for example .claude/skills/ for Claude Code, or the Vibe skills directory) so it loads when a task matches the description in the SKILL.md frontmatter.
- Agent CLIs that read instruction files from the repository root (AGENTS.md, CLAUDE.md, .cursor/rules, or similar): add an entry such as "When creating a new Frappe app, follow skills/frappe-custom-app-builder/SKILL.md and finish with its checklist."
- One-off usage: paste SKILL.md into the conversation and attach intake-questionnaire.md for the interview.

Keep this repository folder as the source of truth; update the skill here first, then propagate copies to the individual environments.
