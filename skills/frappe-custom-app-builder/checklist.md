# Definition of Done: New Custom App

Walk through every item before reporting the app as initialized. Mark items that do not apply as n/a with a reason; report any open item explicitly.

## Intake

- [ ] Groups A, B and C were answered explicitly by the initiator.
- [ ] Defaults used for groups D, E and F were stated and accepted.
- [ ] The initiator confirmed the filled intake record.

## Scaffold

- [ ] Generated with bench new-app on a bench of the target major version.
- [ ] pyproject.toml is at the repository root; the app package is in <app_name>/ below it.
- [ ] Commit "feat: Initialize App" sits on top of the existing remote history; nothing was force-pushed.
- [ ] Commits carry the agreed git author identity, not a hostname-based email.

## Hardening

- [ ] H1 [tool.bench.frappe-dependencies] lists frappe and every required app with a range matching the target major.
- [ ] H2 frappe, erpnext and other bench-managed apps are not in [project] dependencies.
- [ ] H3 requires-python matches the framework of the target major.
- [ ] H4 required_apps in hooks.py lists every hard dependency.
- [ ] H5 license.txt holds the complete chosen license; no "No license text found", no [year] [fullname] placeholders; app_license in hooks.py matches; README names the same license.
- [ ] H6 README has the real install URL and branch, supported versions, readable license sentence and the Project facts section.
- [ ] H7 MR/PR template present; CI matches the agreed choice; no GitHub workflow in a GitLab-only repository.
- [ ] H8 Lint standard applied in its own configuration-only commit, or explicitly declined.
- [ ] H9 pyproject.toml parses with tomllib.

## Verification

- [ ] install-app succeeded on the verification site.
- [ ] list-apps shows the app with the expected version and branch.
- [ ] bench build --app succeeded.
- [ ] migrate succeeded.
- [ ] pre-commit run --all-files passed (if the lint standard was applied).
- [ ] Optional: fresh bench get-app from the remote succeeded.

## Publishing and Handover

- [ ] Push target confirmed by the initiator; pushed without force.
- [ ] Remote branch matches the local branch.
- [ ] Frappe Cloud path is clear: GitHub repository or mirror exists, or the follow-up is listed.
- [ ] Handover report lists outcome, recorded decisions, deviations and follow-ups for administrators.
