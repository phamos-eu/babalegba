# Repo profiles

One profile per repo. It holds what differs between repos: branches, how changes reach production, version, tests, tag and release.

A repo without a profile: ask the PM once, then add its profile here.

## phamos/phamos

GitLab: `git.phamos.eu/phamos/phamos`

**Branches**
- `develop`: all development. Child MRs target it.
- `version-15`: production. It shares **no history** with `develop`, so changes reach it by cherry-pick, never by merge.

**Production branch**
- `feat/<issue>-<keywords>-v15`, from `origin/version-15`
- cherry-pick each develop merge commit, in merge order:

  ```bash
  git cherry-pick -x -m 1 <develop-merge-commit>
  ```

- a single fix commit (not a merge): `git cherry-pick -x <commit>`
- merge the MR **without squashing**, so each cherry-pick stays traceable to `develop`

**Version**
- `__version__` in `phamos/__init__.py`
- its own commit: `chore: release version update`
- minor if the release needs `bench migrate`, otherwise patch

**Conflict rules**
- `hooks.py`, `patches.txt`, `modules.txt`: take only the lines of this feature. Lines from `develop`-only features stay out.
- `phamos/translations/de.csv`: rebuild it. `version-15`'s file plus the strings this release adds; no `develop`-only strings, no duplicate source strings.
- `.github/workflows/foundation.yml` and `TESTING.md`: don't exist on `version-15`; drop them.
- List every resolved conflict in the MR.
- Check the branch doesn't depend on `develop`-only code: changed Python compiles, every `phamos.*` import, hook and patch path resolves, Link/Table targets exist.

**Tests**

Run them with the worktree first on `PYTHONPATH`, against the local bench site:

```bash
PYTHONPATH=<worktree> bench --site dev.localhost run-tests --module <module>
```

Say in the MR that the site schema comes from the local integration branch, so this is not a `bench migrate` on a `version-15` site.

**Local bench** (for the PM's local test, step 5b)
- bench folder on the PM's Mac: `<ask the PM once, then fill in>`
- site: `dev.localhost`
- app folder: `apps/phamos`
- after switching the branch:

  ```bash
  bench --site dev.localhost migrate
  bench build --app phamos
  bench --site dev.localhost clear-cache
  ```

- after the PM's OK: switch `apps/phamos` back to the branch it was on and run the three commands again

**Tag**
- annotated tag `v15.X.Y` on the `version-15` merge commit, message `Version 15.X.Y`:

  ```bash
  git tag -a v15.X.Y -m "Version 15.X.Y" <merge-commit>
  git push origin v15.X.Y
  ```

**GitLab release**
- create it in the GitLab UI (Releases → New release) in the in-app browser
- tag: `v15.X.Y`; title: leave blank (GitLab uses the tag)
- notes: release notes template in `templates.md`, with a `## Deploy` section and an `MRs:` line

**GitHub release**
- GitLab push-mirrors to `github.com/phamos-eu/phamos` (public). Copy each release there after the tag has arrived:

  ```bash
  python3 -I scripts/gitlab-release-to-github.py phamos/phamos phamos-eu/phamos v15.X.Y
  ```

**Templates to follow**
- develop MR: !999
- version-15 MR: !997, !1003, !1005
- child item: #1665
- release notes: v15.118.0
