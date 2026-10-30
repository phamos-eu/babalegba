---
name: gitlab-issue-workflow
description: Take a GitLab issue in a phamos repo from "shall we work on this?" through grill, child items, develop MRs, code review, a local test of the branch on the PM's own bench before any merge, testing, the production cherry-pick MR, tag and GitLab release, with one status label at a time. Use when working on, triaging, grilling, releasing or labeling a GitLab issue in a phamos repo.
---

# GitLab issue workflow

One routine for every issue, from the first question to the production OK. It keeps one status label per issue, so anyone can see where an issue stands.

Roles:
- **PM**: the user. Decides, answers the grill, tests, deploys, merges to production, gives the final OK.
- **Agent**: you. Writes issues and MRs, builds, reviews, merges to develop, cherry-picks, tags, releases.

Before you start in a repo, read its profile in `repos.md`. A repo without a profile: ask the PM once for the branch, version and release details, then add a profile there.

Templates for child items, MRs and release notes are in `templates.md`.

## Writing style

Issues, MRs, comments and release notes:
- plain, direct English; short sentences
- lists over long paragraphs
- name the code (files, functions) and the MRs and issues by reference

## Labels

**Status labels.** An issue has exactly one at a time:

| Label | Means |
|---|---|
| Working | someone works on it: grill, build of the develop MR, or the PM's local test of the unmerged branch |
| Ready for Dev | child item is fully specified, no open questions; ready to build |
| PM Review | a review finding needs a PM decision |
| Testing | merged to develop; PM tests on the hosted develop site |
| Ready for Production | PM gave the OK; goes into the production MR |
| Testing on Production | merged to the production branch, tagged and released; PM checks it on production |

Setting a new status label **removes the old one in the same call**. Never leave two.

**Markers** sit next to a status:
- **Discussion**: open questions; the grill runs
- **P:1**, **P:2**, **P:3**: priority
- **On Hold**: parked; always with a comment giving the reason

Labels not in these lists (for example "Ready for Staging", "Ready for Release", "Testing on Staging") are not used by this routine. Don't set them; remove them when you set a status from this routine.

**Linked issues.** Issues linked to a child item (for example review findings split out of it) carry the same status label as that child and close with it.

## The routine

| Step | Parent | Children | Who |
|---|---|---|---|
| 1. "Shall we work on this?" | Yes: assign the PM, **Working** + Discussion. No: ask whether to set **On Hold** (with a reason) or leave it as it is | — | PM |
| 2. Grill | Working + Discussion | Created from the child template, no open questions, one MR each → **Ready for Dev**. Ships later or stands alone → a related issue in the same milestone instead | PM answers, agent writes |
| 2b. Consistency check | — | After each new child: check it against the parent and the other children; name conflicts right away. A final pass before the grill closes. A changed child loses Ready for Dev until the PM confirms it again; note the change in its thread | both |
| 3. Grill closed | remove Discussion | — | PM confirms |
| 4. Build | Working | **Working** while its develop MR is built. Needs a test that fails without the change | agent |
| 5. Review | — | `senior-code-reviewer`. Mechanical fixes: apply them. Fixes that need a decision: **PM Review** + grill in the child's thread, then fix or split into issues | agent / PM |
| 5b. Local test | — | Stays **Working**. Agent puts the MR branch on the PM's local bench; PM clicks through it. Problems are fixed on the same branch and tested again | agent sets up, PM tests |
| 6. Merge to develop | — | Agent merges only after the PM's local OK (see merge rules) → **Testing** | agent |
| 7. All children merged | **Testing**. PM: "please deploy the hosted develop site", then tests there | — | PM deploys and tests |
| 8. PM's OK | **Ready for Production** | **Ready for Production** | PM |
| 9. Production MR | Cherry-pick every child's develop merge in order, version bump, assigned to the PM, senior review | — | agent; PM merges |
| 10. After the PM's merge | **Testing on Production**; annotated tag + GitLab release | **Testing on Production** + closed | agent |
| 11. PM's OK on production | closed, keeps its label | — | agent, on the PM's OK |

A small issue with no children runs the child column on the issue itself.

### Step 1: shall we work on this?

Ask the PM in one line. Don't start the grill before a yes.

### Step 2: grill rules

- **One question at a time.** Give your recommendation with each question.
- Check the code before asking. Questions the code answers are not questions; write the answer into "Where we are" instead.
- Write each child as soon as its part is settled. Use the child template in `templates.md`.
- A child has **no open questions** and maps to **one develop MR**. If it needs two MRs, it is two children.
- **Child or related issue?** Child: it ships with the parent and the parent is not done without it. Related issue in the same milestone: it can ship later, or it stands on its own.
- Set Ready for Dev on a child only when it is complete.

### Step 2b: consistency check

After each new or changed child:
- compare it with the parent and every other child: same field names, same rules, no overlap, no gaps
- name a conflict to the PM right away; don't fix it silently
- a child that changes after Ready for Dev loses the label until the PM confirms it again; say what changed in its thread

Before the grill closes, do one final pass over all children together.

### Step 4: build

- One branch and one develop MR per child, from the develop MR template.
- The MR is linked to its child issue (see "Linking MRs to issues").
- Every MR has a test that fails without the change. Say in the MR that you checked it.

### Step 5: PM Review threshold

Run `senior-code-reviewer` on the MR.

Apply without asking: mechanical fixes (bugs with one clear fix, missing tests, naming, dead code, comments).

Set **PM Review** and grill in the child's thread when the fix needs a decision:
- UX or wording the user sees
- data model (new fields, doctypes, migrations of existing data)
- permissions and who can see what
- money or tax
- legal or privacy
- choosing between options

Then fix it in the MR or split it into a linked issue.

### Step 5b: local test before merge

The PM should see the change running on their own bench while it is still an open branch. A problem found here is fixed on the same branch in minutes; after the merge it costs a new MR on `develop` and mixes with the other children.

Start once the review is done and the tests are green.

1. **Set up the bench** (agent, on the PM's computer through the linked-computer shell). The bench folder, site and app folder come from the repo profile's "Local bench" block. If the profile has none, ask the PM once and add it.
   - Note which branch the app folder is on now, and whether it has uncommitted changes. Uncommitted changes: stop and ask the PM. Don't stash or overwrite their work.
   - Fetch and check out the MR branch, then `bench --site <site> migrate`, `bench build --app <app>`, `bench --site <site> clear-cache`.
   - If a git command fails because files can't be deleted, request delete permission for the bench folder once, saying it is needed for the branch switch.
   - If the computer isn't reachable, post the same commands in the MR comment so the PM can run them.
2. **Hand over** with one MR comment (a reply in the MR's local-test thread if one exists, so every test round stays in one thread): "Ready for your local test on `<site>`", the branch name, and the MR's "To test locally" checklist (see the develop MR template). The checklist is for a user clicking through the app: page, action, expected result. No code.
3. **The PM tests.** The child stays **Working**; this stage has no label of its own.
   - Problem found: fix it on the same branch, rerun the tests (and the review if the fix is more than mechanical), update the bench, ask again.
   - PM's OK: note it in the MR thread, then go to step 6.
4. **Restore the bench** after the OK: switch the app folder back to the branch it was on, then migrate, build and clear the cache again, unless the PM says to leave it.

A small issue with no children runs this step on the issue's own MR.

If the develop MR template in `templates.md` has no "To test locally" section yet, add one to the MR anyway, right above "To test (staging)": `**To test locally (<site>, branch <branch>):**`, then numbered steps of the form page → action → expected result, plus any edge case worth trying.

### Step 6: merge rules (develop)

Merge a develop MR only when:
- the review passed
- the tests are green
- every finding is fixed or split into a linked issue
- the PM gave the OK on the local test (step 5b)
- the MR is linked to its issue and shows up on it

Then set the child to **Testing**.

### Step 9: production MR

Follow the repo profile in `repos.md`: branch name, cherry-pick command, conflict rules, version file, how to test.
- Cherry-pick every child's develop merge, in merge order.
- Version bump: **minor** if the release needs `bench migrate` (new fields, patches), otherwise **patch**.
- Use the production MR template in `templates.md`. Assign it to the PM.
- Link it to the parent and every child (see "Linking MRs to issues").
- Run `senior-code-reviewer` on it. Fix findings on develop first, then cherry-pick the fix.
- **Never merge the production MR.** The PM merges it.

### Step 10: tag and release

After the PM's merge:
- annotated tag on the merge commit, as the profile says
- GitLab release from the release notes template
- parent → Testing on Production (stays open); children and their linked issues → Testing on Production + closed, each with a short comment naming the MR and release

## Linking MRs to issues

Every MR belongs to an issue. The issue then lists its MRs, and anyone can trace a change back to the decision behind it.

- **No issue, no MR.** Know the MR's issue before opening it: the child for a develop MR; the parent and all children for the production MR. No issue yet: ask the PM whether to create one first.
- **Link it in the MR**, as the templates show:
  - issue number in the title: `(#<issue>)`
  - full reference under "Related issue(s)/ticket(s)": `<group>/<repo>#<issue>`, plus any linked issues split out of review findings
- **No closing keywords** (`Closes`, `Fixes`, `Resolves`, `Implements`) in the title, description or commits. They close the issue on merge to the default branch and skip the closing rules below.
- **Check the link** right after creating the MR: read the issue's related merge requests. MR missing there: add a comment on the issue naming the MR, in the topic's thread if there is one (see comment rules).
- An MR that is not linked is not merged.

## Comment rules

A work item should read as a set of topics, each in its own thread, so the PM can follow one topic from start to end and resolve it on its own. Scattered top-level comments on the same topic break that.

- **Read the threads first.** Before every comment, load the work item's discussions (issue or MR), resolved ones included.
- **Topic already has a thread** (whoever started it: PM, agent, colleague): **reply in that thread**.
  - Resolved thread: reply there anyway, so the history stays together. GitLab may reopen it; that is wanted, it needs attention again.
  - Topic started on the issue and comes up again on its MR: reply in the original issue thread and name the MR there.
- **New topic:** start a new thread. One topic per thread.
- **Several topics at once:** one reply or new thread per topic, never one comment covering all of them.
- **Label changes** get a short note: what changed and why, with the MR or release. Put it in the thread of the topic that caused the change (for example the local-test thread when the PM's local OK moves the child on). No such thread: a new comment.

## Closing rules

- **Ask before closing** any issue. Merged to develop is not done.
- Exceptions:
  - step 10: children and their linked issues close once their code is merged to the production branch and released
  - step 11: close the parent on the PM's OK on production
- A closed issue keeps its last status label.
