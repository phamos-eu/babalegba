# gitlab-issue-workflow (Skill)

A reusable AI agent skill that takes a GitLab issue in a phamos repo through one fixed routine:

- "Shall we work on this?", then a grill, one question at a time, that ends in child items with no open questions.
- Every MR linked to its issue (no closing keywords), checked on the issue after creating the MR.
- One develop MR per child, with a test that fails without the change, a senior code review and a clear line for which findings need a PM decision.
- A local test of each MR branch on the PM's own bench before it is merged to develop.
- Testing on the hosted develop site, then the production MR by cherry-pick, version bump, annotated tag and GitLab release.
- One status label per issue at a time (Working, Ready for Dev, PM Review, Testing, Ready for Production, Testing on Production), plus the markers Discussion, P:1–3 and On Hold.
- Comment rules (read the threads first, reply in the topic's existing thread, new thread only for a new topic) and closing rules (ask first).

## Files

- SKILL.md: the routine, label rules, grill rules, review threshold, local test, merge, comment and closing rules.
- repos.md: one profile per repo: branches, cherry-pick and conflict rules, version file, tests, tag and release. Starts with phamos/phamos.
- templates.md: child item, develop MR, production MR and release notes templates.

## Adoption in Different AI Environments

This skill is deliberately stored as plain Markdown so it can be consumed by any AI coding tool. Options:

- Agent CLIs with a skills or rules directory: copy or symlink this folder into the tool's skills directory (for example a .claude/skills/ directory for Claude Code, or your tool's equivalent) so it is loaded automatically when a task matches the description in the SKILL.md frontmatter.
- Agent CLIs that read instruction files from the repository root (AGENTS.md, CLAUDE.md, .cursor/rules, or similar): add a short entry there referencing this folder, e.g. "For any work on a GitLab issue in this repo, follow skills/gitlab-issue-workflow/SKILL.md and the repo's profile in repos.md."
- One-off usage: paste the content of SKILL.md into the conversation or prompt, together with the repo's profile from repos.md.
- Vibe (Mistral Work): copy this folder to the Vibe skills directory so it becomes a first-party selectable skill.

Keep this repository folder as the source of truth; update the skill here first, then propagate copies to the individual environments.
