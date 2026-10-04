# frappe-website-builder (Skill)

A reusable AI agent skill for building public-facing websites on the Frappe Framework / ERPNext v15 with the classic server-rendered website module. It enforces:

- Reuse of built-in Frappe elements (Website Settings, Website Theme, Web Templates, the base template block system) over new components.
- SEO best practices for high Google search scores.
- Design that is useful both to AI crawlers/generative engines (llms.txt, structured data, semantic HTML) and to human AI researchers navigating the codebase.

## Files

- SKILL.md — the skill instructions an AI agent loads and follows.
- seo-ai-checklist.md — validation checklist walked through before any website task is declared complete.
- references.md — bench commands, verification steps, and curated official documentation links.

## Adoption in Different AI Environments

This skill is deliberately stored as plain Markdown so it can be consumed by any AI coding tool. Options:

- Agent CLIs with a skills or rules directory: copy or symlink this folder into the tool's skills directory (for example a .claude/skills/ directory for Claude Code, or your tool's equivalent) so it is loaded automatically when a task matches the description in the SKILL.md frontmatter.
- Agent CLIs that read instruction files from the repository root (AGENTS.md, CLAUDE.md, .cursor/rules, or similar): add a short entry there referencing this folder, e.g. "For any website work on this app, follow skills/frappe-website-builder/SKILL.md and its checklist before finishing."
- One-off usage: paste the content of SKILL.md into the conversation or prompt and attach the checklist when reviewing the result.
- Vibe (Mistral Work): copy this folder to the Vibe skills directory so it becomes a first-party selectable skill.

Keep this repository folder as the source of truth; update the skill here first, then propagate copies to the individual environments.
