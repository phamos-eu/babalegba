# Templates

Fill every section. Leave out a section only where it says "optional". Plain, direct English, short sentences, lists over paragraphs.

## Child item (issue description)

Shape of phamos/phamos#1665.

```markdown
<One or two lines: what this child is part of (parent #N) and what is a separate issue (#M).>

Status: <filled in later: merged via !A (develop) and !B (production), released in [vX.Y.Z](<release link>).>

## Where we are on develop

<What the code does today, checked in the code. Name the fields, files and functions.>

- <each concrete problem, one per line>

## Solution

<One short paragraph: the idea, with the key decision in bold.>

### 1. <Part, e.g. Doctype (<DocType>, section "<Section>")>

| Field | Type | Shown for | Notes |
|---|---|---|---|
| `<fieldname>` | <Type> | <when> | <new / existing, label, default> |

<Rules as a list: validation on save, what happens on errors.>

### 2. <Next part>

- ...

### Out of scope

- <what this child does not do, and where it goes instead (#N or "as agreed in #M")>

### Existing data

<Patch name and what it does to existing records. "None" if nothing changes.>

### Translations and tests

- German strings in `<translations file>`: "<English>" → "<German>", ...
- new `<test file>`:
  - <one line per behaviour the tests check>

## Acceptance

- [ ] <observable result a tester can check>
- [ ] ...

## Code touched

`<file>`, `<file>`, new `<file>` (<what it holds>), the patch, translations, tests.

## Decisions

1. <each decision from the grill, one line, so the reason stays with the issue>
```

## Develop MR

Shape of phamos/phamos!999. Title: `<type>(<scope>): <what changes, for the user> (#<issue>)`.

```markdown
## Description

<One or two lines: what this fixes or adds, and where it came from (issue, review of !N).>

**1. <First change, in plain words>** (`<module.function>`)
<What was wrong or missing. What the code does now.>
- <details as a list>

**2. <Second change>**
<...>

**German:** <new and removed strings in de.csv>

**Related issue(s)/ticket(s):**
- phamos/phamos#<issue>

**Testing done:**
- <N> new tests:
  - `<test module>`: `<test name>`, ...
- All <N> fail on the code before this change and pass after it.
- `<test module>` (<count>), ... pass. They ran with this branch's code against the local bench site `dev.localhost`.
- <what was not tested>

**To test locally (`<site>`, branch `<branch>`):**
1. <page to open> → <what to click or enter> → <what you should see>
2. ...
- <edge case worth trying, and its expected result>

**To test (staging):**
1. <step and expected result>
2. ...

**Further comments/notes (optional):**
- **AI-assisted:** written with Claude Code; needs a human peer review before merge.

**Checklist:**
* [x] The name of the branch follows conventions
* [x] I created logical commits with clear messages
* [x] I added tests that fail without the change
* [x] I pushed changes to the remote branch
* [x] I created a Pull Request with title and description as described in the guideline
* [ ] I checked if there is any conflict after creating the PR
```

## Production MR (version-15)

Shape of phamos/phamos!997. Title: `<type>(<scope>): <what ships> (#<issue>) [v15, release 15.X.Y]`.

```markdown
## Description

Brings <feature> from `develop` to `version-15` by cherry-picking, completing phamos/phamos#<issue>.

<What runs on `version-15` today, and what this release replaces it with, as a list.>

Every change was reviewed and merged on `develop`.

**Commits:**
1. `<sha>`: cherry-pick (`-x -m 1`) of `<develop merge sha>`, the merge of `<branch>` (!<N>).
2. ...
3. `<sha>`: release version update, 15.A.B → **15.X.Y** (<minor: needs migrate | patch>).

Merge without squashing, so every cherry-pick stays traceable to `develop`.

**Conflicts resolved while cherry-picking:**
- `hooks.py`: only <feature> parts were taken: <list>. <What stays out and why.>
- `patches.txt`: <feature> patches only.
- `translations/de.csv`: rebuilt: `version-15`'s file plus the <N> strings this release adds, without `develop`-only strings.
- `.github/workflows/foundation.yml`, `TESTING.md`: don't exist on `version-15`, dropped.
- <or: "None.">

I checked that the branch does not depend on `develop`-only code:
- every changed Python file compiles;
- every `phamos.*` import and every hook and patch path resolves on the branch;
- <further checks>

**Related issue(s)/ticket(s):**
- phamos/phamos#<issue>, with its child tasks #<a>, #<b>
- !<develop MRs>

**Testing done:**
- QA on `develop`: <MRs>.
- On this branch, <N> tests pass: <modules with counts>.
  They ran with this branch's code (worktree first on `PYTHONPATH`) against the local bench site `dev.localhost`, whose schema comes from the local integration branch. So they did not go through `bench migrate` on a `version-15` site.
- Not checked on this branch: <list>.

**To test on staging (Frappe Cloud):**
1. Take a backup, then deploy. Migrate runs: <patches, as a list>. The version is 15.X.Y.
2. <check>
3. ...
4. Production: same steps.

**Further comments/notes (optional):**
- **Reverting:** <what a revert needs>
- **AI-assisted:** written with Claude Code; needs a human peer review before merge.

**Checklist:**
* [x] Changes come from `develop` by cherry-pick, as the development process describes
* [x] The name of the branch follows conventions (`feat/<issue>-<keywords>-v15`)
* [x] I created logical commits with clear messages
* [x] I resolved the conflicts and checked nothing on `version-15` depends on `develop`-only code
* [x] I pushed changes to the remote branch
* [x] I created a Pull Request with title and description as described in the guideline
* [x] I checked if there is any conflict after creating the PR
```

## Release notes

Shape of the phamos/phamos v15.118.0 release. Title blank (GitLab uses the tag).

```markdown
**<Area>: <what changed, in one line> (#<issue>)**

- <what changed for the user, one line each>
- ...

## Deploy

<Run `bench migrate`? Which patches run and what they do to existing data. Manual steps after deploy. Or: "No migrate needed.">

MRs: !<production MR> (version-15), !<develop MR> and !<develop MR> (develop).
```

Several features in one release: one bold line plus list per feature, then one `## Deploy` section and one `MRs:` line.
