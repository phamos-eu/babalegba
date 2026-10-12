# Intake Questionnaire

Ask these questions before scaffolding. Each question lists why it matters, the options, and the default to propose. Defaults come from the Phase 0 context scan (sibling apps of the same organization); always say where a default came from.

Legend:

- **Blocking**: must be answered explicitly before Phase 3.
- **Defaultable**: the initiator may accept the proposed default.
- **Irreversible**: changing it later is a migration project, not an edit.

---

## Group A — Identity (blocking)

### A1 App name (irreversible)

The Python package and Frappe app name. It becomes the package directory, the module path in every import, the asset URL /assets/<app_name>/, the key in sites/apps.txt and installed-app records in every site database. Renaming later means a data migration on every site.

- Rules: lowercase, letters, digits and underscores, starts with a letter, valid Python identifier.
- Must not collide with existing apps or packages: frappe, erpnext, hrms, payments, crm, helpdesk, insights, lms, builder, raven, india_compliance, or anything importable in the bench environment.
- The repository slug may differ (hyphens are fine there): repository brecht-feinmechanik holds app brecht_feinmechanik.
- Ask explicitly when the client name, the repository name and the requested app name differ (for example repository lillesisters vs. brand lillestoff). Do not guess.

### A2 App title

Human-readable name shown in the desk and apps screen. Default: the app name in title case.

### A3 Description

One sentence, used in hooks.py, pyproject.toml and the README. Default: "Custom Frappe/ERPNext app for <Client>".

### A4 Purpose and reuse

Is this a client-specific app (one customer, one deployment) or a reusable product (several customers, possibly marketplace)? This influences license, naming (client name vs. product name), and how strictly client data must stay out of the repository.

---

## Group B — Ownership, contact, license (blocking)

### B1 Publisher

The legal entity named as publisher and copyright holder (hooks.py app_publisher, pyproject authors, license notice). Whether the agency or the client owns the code is a contract question. If the initiator does not know, they must find out before publishing.

### B2 Contact email

Appears in hooks.py (app_email), pyproject.toml and, for public repositories, on the internet. Recommend a role mailbox (for example post@ or support@) over a personal address. bench validates the format.

### B3 License (irreversible in practice)

Changing a license after code has been distributed does not revoke the old license for already distributed copies. Explain neutrally; do not choose for the initiator; this is not legal advice.

| Option | Key for bench | What it means in practice |
|---|---|---|
| MIT | mit | Permissive. Anyone may reuse, also in closed software. Frappe Framework itself is MIT. |
| GNU GPL v3 | gpl-3.0 | Copyleft. Distributed modified versions must stay GPL. ERPNext is GPL v3, so many ERPNext apps use it. |
| GNU AGPL v3 | agpl-3.0 | GPL plus: offering the software over a network counts as distribution. Strongest protection for hosted (SaaS) use. |
| Proprietary | custom | All rights reserved. bench writes only the word "custom"; license.txt must be written by hand. Check client contract and any marketplace terms. |

Points to raise:

- An app that imports and extends ERPNext code may be considered a derivative work of GPL v3 software when it is distributed. If the app is distributed outside the organization or the client, recommend checking license compatibility with whoever handles legal matters.
- The license should be consistent with repository visibility (A4, D5): a public repository with a proprietary license is unusual and should be confirmed.

### B4 Copyright notice

Year and holder for the license text (MIT needs them filled in; proprietary needs a full notice). Default: current year and the publisher from B1.

### B5 Git author identity

Name and email for commits in this repository. Default: the initiator's work identity as seen in sibling repositories. Required because a missing global git identity leads to hostname-based author emails.

---

## Group C — Platform (blocking)

### C1 Frappe major version (irreversible per branch)

v15 or v16 (or a newer major if available). Determines the bench used for scaffolding, Python and Node versions, and the version range in pyproject.toml. Supporting several majors normally means one branch per major (version-15, version-16) and is a decision, not a side effect. See the version matrix in references.md.

### C2 Required apps

Does the app need ERPNext? HRMS, Payments, India Compliance, CRM, other custom apps? Each hard dependency goes into required_apps in hooks.py and into [tool.bench.frappe-dependencies]. Ask whether requirement documents already imply ERPNext (sales, purchasing, stock, accounting usually do).

### C3 Minimum version within the major

Default: the whole major (">=16.0.0,<17.0.0"). Tighten only if the app depends on a feature introduced in a specific minor release.

### C4 Deployment target

Where will the app run? Frappe Cloud (private bench group), self-hosted bench, Docker (frappe_docker with apps.json), on-premise server of the client, several of these. This decides which hardening and publish steps apply.

### C5 Frappe Cloud repository access (only if C4 includes Frappe Cloud)

Frappe Cloud adds custom apps to private bench groups through its GitHub integration. There is no native GitLab support. If the repository is on GitLab or elsewhere: who sets up and owns a GitHub mirror, which organization, which branches are mirrored? Note: users with SSH access to that bench group can read the app code.

### C6 Existing site and existing customizations

Will the app be installed on a site that already has data? Are there Custom Fields, Property Setters, Client Scripts, Server Scripts or Print Formats made in the UI that should move into the app as fixtures? This does not change the scaffold, but it must be recorded so the first feature work does not create duplicates.

---

## Group D — Repository and workflow (defaultable)

### D1 Repository host and URL

GitLab (which instance, which group) or GitHub (which organization)? Does the repository exist already? If yes, what is in it (often only a README created by the hosting service)? The scaffold is committed on top of existing history.

### D2 Branch model and push target

Default (Phamos): work on develop, main is protected. Which branch receives the first push? Direct push or merge/pull request? Should the default branch be changed (only an administrator should do that)?

### D3 Continuous integration

None, GitHub Actions (bench new-app can generate a unit-test workflow, only useful on GitHub), or GitLab CI. Default: whatever sibling apps on the same host use.

### D4 Merge/pull request template

Default: copy the organization's template from a sibling repository.

### D5 Visibility

Private, internal or public. Must fit the license (B3) and the client's confidentiality expectations. Changing visibility is an administrator action, not part of this skill.

---

## Group E — Development environment (defaultable)

### E1 Bench and verification site

Which local bench (must match C1) and which site is used to verify the installation? That site must have every required app from C2 installed. Default: the bench of the matching major and its ERPNext site.

### E2 Location on disk

Inside the bench's apps directory, or in a projects directory with a symlink into the bench? Default: follow how sibling apps on the same host are organized.

### E3 Developer mode

Developer mode must be on for the verification site if DocTypes will be created in the app. Confirm whether it may be enabled.

---

## Group F — Conventions and scope (defaultable)

### F1 Modules

bench new-app creates one module named after the app title. Are more modules needed from the start (for example by business area)? Default: one module, add more when the first feature needs them.

### F2 Languages

Default language and translations needed (for example German). Translatable strings must use _() in Python and __() in JavaScript from the first feature on.

### F3 Lint, format and type-check standard

Apply the organization's standard (Ruff, Prettier, ESLint, Pyright, pre-commit) as a separate configuration-only commit now? Default: yes, if the organization has one.

### F4 Personal data

Will the app store personal data (customers, employees, contacts)? If yes, record it: it affects permissions, data retention and deletion handling in later feature work.

### F5 Marketplace and apps screen

Will the app be published on the Frappe Cloud Marketplace? Should it appear on the apps screen with its own logo (add_to_apps_screen in hooks.py)? Default: no and no.

### F6 Versioning

Default: start at 0.0.1 (set in <app_name>/__init__.py), semantic versioning, git tags for releases.

---

## Intake Record Template

Fill this in, show it to the initiator for confirmation, and later add it to the README under "Project facts" (omit anything confidential).

```markdown
## Project facts

| Topic | Decision |
|---|---|
| App name / title | <app_name> / <App Title> |
| Description | <one sentence> |
| Purpose | client-specific for <Client> / reusable product |
| Publisher / copyright | <legal entity>, <year> |
| Contact | <email> |
| License | <license name> (<bench key>) |
| Frappe version | v<NN> (>=NN.x.0,<NN+1.0.0) |
| Required apps | <erpnext, …> |
| Deployment | <Frappe Cloud private bench group / self-hosted / Docker> |
| Repository | <URL>, work branch <develop>, default branch <main> |
| Frappe Cloud source | <GitHub repo or mirror, or n/a> |
| CI | <none / GitLab CI / GitHub Actions> |
| Languages | <de, en> |
| Lint standard | <applied / not applied> |
| Personal data | <yes: which / no> |
| Existing UI customizations to migrate | <list / none> |
| Initialized | <date> by <initiator> |
```
