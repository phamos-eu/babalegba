---
name: frappe-custom-app-builder
description: Load this skill when initiating a new custom app for the Frappe Framework / ERPNext (v15 or v16) — "create an app", "initialize a custom app for client X", "set up a new Frappe app in repo Y". It runs a structured intake interview (app name, license, publisher and contact, target Frappe/ERPNext version, hosting such as Frappe Cloud, repository and branch model, conventions), scaffolds with bench new-app, hardens the scaffold for Frappe Cloud, verifies it on a real site, and publishes it to the agreed repository. Not for adding features to an existing app.
---

# Frappe Custom App Builder

Initialize a new Frappe / ERPNext custom app that installs cleanly on a local bench, on a self-hosted server and on Frappe Cloud from its very first commit, with every decision that is hard to change later made explicitly by the person who initiates it.

## Core Principles

1. **Ask before you build.** App name, license, publisher and target framework version are expensive or legally sensitive to change later. Never pick them silently. Run the intake in intake-questionnaire.md first and get an explicit go.
2. **Never hand-write the scaffold.** Always generate it with bench new-app from a bench of the target major version. The scaffold differs between v15 and v16, and hand-written scaffolds repeatedly fail on Frappe Cloud (wrong pyproject location, missing package subdirectory, missing version table).
3. **bench new-app is not the finish line.** Its output is not Frappe-Cloud-ready and leaves placeholders behind. Always apply the hardening steps in Phase 4.
4. **Verify on a real site before publishing.** Install the app on a site of the target version, with the required apps, before anything is pushed.
5. **The initiator decides what happens to existing repository content.** Show what is there, then let them choose: add on top, wipe content but keep history, or wipe content and history. Never delete, overwrite or force-push without that explicit decision.
6. **Record the decisions in the repository.** The intake answers go into the app README so the next developer (human or AI) does not have to rediscover them.

## Process Overview

| Phase | Goal | Gate |
|---|---|---|
| 0. Context scan | Learn what exists before asking anything | none |
| 1. Intake interview | Collect every decision from the initiator | Initiator confirms the intake summary |
| 2. Preflight checks | Prove the environment can deliver the decisions | All checks pass or blockers are reported |
| 3. Scaffold | Generate the app with bench new-app | Scaffold exists, first commit made |
| 4. Harden | Fix what bench new-app does not do | Checklist items H1–H9 done |
| 5. Verify | Install and build on a real site | Install, build and migrate succeed |
| 6. Publish | Push to the agreed repository and branch | Initiator approved the push target |
| 7. Handover | Summarize, record, list follow-ups | Report delivered |

## Phase 0 — Context Scan (no questions yet)

Gather facts so the interview only asks what cannot be looked up:

- Available benches and their versions (frappe and erpnext __version__, Python version, installed apps, sites per bench).
- Sibling custom apps of the same organization: publisher string, contact email, license, pyproject layout, branch names, MR/PR templates, CI files, lint configuration. These become the proposed defaults.
- The target repository if one was named: does it exist, default branch, protected branches, what is already committed (often only a README from the hosting service), visibility.
- Requirements material in the working directory (process documentation, requirement lists) that indicates whether ERPNext or other apps are needed.

## Phase 1 — Intake Interview

Use intake-questionnaire.md. Rules:

- Ask in as few rounds as possible, grouped by topic. If the environment offers a structured question tool, use it; otherwise ask in one numbered message.
- For every question, offer the proposed default discovered in Phase 0 and say where it came from. The initiator may accept all defaults of a group at once.
- Groups A (identity), B (ownership, contact, license) and C (platform) are blocking, and so is D2 (existing repository content) whenever the repository is not empty. Do not scaffold before they are answered.
- The rest of groups D, E and F may fall back to the stated defaults if the initiator explicitly says so.
- Never decide the license yourself. Explain the options neutrally; if the initiator is unsure, recommend they ask whoever owns the commercial or legal relationship.
- End the phase by writing the filled intake record (template at the end of intake-questionnaire.md) back to the initiator and asking for confirmation. Only an explicit confirmation opens Phase 2.

## Phase 2 — Preflight Checks

Stop and report if any check fails; propose the fix, do not improvise around it.

- The chosen bench runs the target major version (for example frappe 16.x for a v16 app).
- Every required app (ERPNext, HRMS, …) is present in that bench and installed on the verification site.
- The app name is a valid Python identifier, lowercase, and not already used: not a folder in the bench's apps directory, not importable in the bench's Python environment, not the name of a well-known Frappe app.
- The remote repository is reachable with the current credentials (git ls-remote), its current content matches what was shown to the initiator for D2, and nothing was pushed to it since.
- If D2 is "Wipe content and history" on a protected branch: force-pushing has been allowed by an administrator, or the blocker is reported.
- If the license text will be fetched by bench (it calls the GitHub license API), network access to api.github.com works. Offline, bench writes "No license text found" into license.txt.
- If the target is Frappe Cloud and the repository is not on GitHub: the initiator has confirmed how Frappe Cloud will get the code (see references.md, Frappe Cloud section).

## Phase 3 — Scaffold

1. Run bench new-app <app_name> inside the chosen bench. Answer the prompts with the intake values. The prompt order differs by version, so check it in the bench's frappe/utils/boilerplate.py (function _get_user_inputs) before piping answers. See references.md for the verified order.
2. bench new-app also installs the app into the bench environment, builds its assets and creates a local git repository with a first commit "feat: Initialize App".
3. If the organization keeps app repositories outside the bench (intake E2), move the folder there and replace it with a symlink in the bench's apps directory.
4. Set the git author identity for this repository from intake B5. Do not rely on a global identity; an unset one produces hostname-based author emails.
5. Connect the remote and apply the decision from intake D2 exactly as described in references.md, section "Existing Repository Content". The commit message stays "feat: Initialize App". For "Add on top", show the files that exist in both versions and apply the per-file decision before committing.

## Phase 4 — Harden (what bench new-app does not do)

Each item is its own small change; commit them together as a chore or fix commit separate from the initial scaffold, so the generated baseline stays reviewable.

- **H1 Frappe version table.** Add [tool.bench.frappe-dependencies] to pyproject.toml with a range for frappe and one for every required app (for example erpnext). Frappe Cloud refuses to install an app without it, with the error "Could not find a compatible Frappe version in pyproject.toml".
- **H2 No framework in Python dependencies.** frappe, erpnext and other bench-managed apps must never appear in [project] dependencies. Bench installs them from git; listing them makes the Frappe Cloud build fail. Only real third-party packages belong there.
- **H3 Python version.** requires-python must match the framework (v15: >=3.10, v16: >=3.14). bench new-app normally gets this right; check it.
- **H4 Required apps.** Set required_apps in hooks.py for every hard dependency (for example ["erpnext"]).
- **H5 License consistency.** license.txt contains the full text of the chosen license, not "No license text found" and not unfilled placeholders such as [year] [fullname] (the MIT text from the GitHub API has them). hooks.py app_license uses the matching lowercase SPDX key. For a proprietary app, write the license.txt by hand with the copyright notice agreed in intake.
- **H6 README.** Replace the placeholder install URL with the real repository URL and branch, use bench --site $SITE install-app, state the supported Frappe/ERPNext versions, write the license as a readable sentence, and add a "Project facts" section with the confirmed intake record (no secrets, no personal data beyond the agreed contact).
- **H7 Repository templates.** Add the organization's MR/PR template (GitLab: .gitlab/merge_request_templates/, GitHub: .github/pull_request_template.md). Add CI only as agreed in intake D4; do not keep a GitHub Actions workflow in a GitLab-only repository.
- **H8 Lint and format standard.** If agreed (intake F3), apply the organization's lint, format and type-check standard as its own "chore:" commit, configuration only, no code reformatting in the same commit.
- **H9 Validation of pyproject.toml.** Parse it with Python's tomllib and print the frappe-dependencies table to prove it is valid TOML.

## Phase 5 — Verify

Run against the verification site from intake E1 and report each result:

- bench --site <site> install-app <app_name> succeeds.
- bench --site <site> list-apps shows the app with the expected version and branch.
- bench build --app <app_name> succeeds.
- bench --site <site> migrate succeeds.
- If the lint standard was applied: pre-commit run --all-files passes.
- Optional but recommended before a first Frappe Cloud deploy: bench get-app <repo_url> --branch <branch> into a disposable bench of the target version, to reproduce exactly what a fresh server does.

If a step fails, fix the cause in the app and repeat; do not push a failing app.

## Phase 6 — Publish

- Show the initiator the local commit list and the push target (remote, branch). Pushing is an outward-facing action: get confirmation unless the initiator already approved this exact target in intake D3.
- Push to the agreed working branch. If that branch is protected, push a feature branch and open a merge/pull request instead.
- Force-push only when intake D2 is "Wipe content and history", only to the agreed branches, only with --force-with-lease against the commit shown to the initiator, after the backup tag if one was agreed, and after the final confirmation. In every other case never force-push.
- Never change the default branch, branch protection or repository visibility yourself; list them as follow-ups if the intake asks for something different from the current settings.
- Frappe Cloud: the app is added in a private bench group from GitHub. If the code lives elsewhere, a GitHub mirror is needed first (references.md).

## Phase 7 — Handover

Report to the initiator, in this order:

1. Outcome: repository URL, branch, commit list, verification results.
2. Decisions recorded (the intake record, and where it now lives in the repository).
3. Deviations from the intake and why.
4. Open follow-ups that only the initiator or an administrator can do: default branch, branch protection, GitHub mirror for Frappe Cloud, Frappe Cloud bench group, marketplace listing, CI runners.

Before declaring the work done, walk through checklist.md and confirm every item.

## Files in This Skill

- intake-questionnaire.md — every question, why it matters, options, defaults, and the intake record template.
- references.md — version matrix, bench new-app prompt order, pyproject and hooks snippets, Frappe Cloud notes, commands and documentation links.
- checklist.md — definition of done.
