#!/usr/bin/env python3
"""Copy GitLab releases (git.phamos.eu) to the project's GitHub mirror.

The push mirror copies tags but not releases. For each GitLab release whose
tag is on GitHub but has no GitHub release yet, create one with the same title
and notes. Oldest first; the newest GitLab release becomes GitHub's "Latest".

GitLab references in the notes are made into links to GitLab, because on GitHub
`#62` or `!23` would point at the GitHub repo's own (unrelated) issues:
  #62 -> [#62](https://git.phamos.eu/<project>/-/issues/62)
  !23 -> [!23](https://git.phamos.eu/<project>/-/merge_requests/23)
  group/repo#5 -> a GitLab link, if group/repo is a GitLab project
  @user -> `@user` (no ping of a GitHub account with the same name)
  /uploads/... -> absolute GitLab URL
Code spans and code blocks stay as they are.

Usage:
  gitlab-release-to-github.py <gitlab/project> <github-owner/repo> [tag ...] [--dry-run]
No tags: every release that is missing on GitHub.
Needs `glab` logged in to git.phamos.eu and `gh` logged in to github.com.
"""
import json
import re
import subprocess
import sys
import tempfile

GITLAB = "git.phamos.eu"
REF = re.compile(r"(?<![\w/\[`.-])(?:([A-Za-z0-9_.-]+/[A-Za-z0-9_./-]+?))?([#!])(\d+)\b")
MENTION = re.compile(r"(?<![\w`/.@-])@([A-Za-z0-9_][A-Za-z0-9_.-]*[A-Za-z0-9_])")
UPLOAD = re.compile(r"\]\((/uploads/[^)\s]+)\)")
CODE = re.compile(r"(```.*?```|`[^`\n]*`)", re.S)


def run(*args):
    return subprocess.run(args, check=True, capture_output=True, text=True).stdout


def gitlab_paths():
    """Paths of all GitLab projects I can see, lower case: to tell GitLab from GitHub references."""
    paths, page = set(), 1
    while True:
        batch = json.loads(run("glab", "api", "--hostname", GITLAB, f"projects?membership=true&per_page=100&page={page}"))
        paths |= {p["path_with_namespace"].lower() for p in batch}
        if len(batch) < 100:
            return paths
        page += 1


def convert(notes, project, known):
    def ref(m):
        other, kind, num = m.groups()
        target = other or project
        if other and other.lower() not in known:
            return m.group(0)  # e.g. phamos-eu/kefiya#163: a GitHub reference, leave it
        path = "issues" if kind == "#" else "merge_requests"
        return f"[{m.group(0)}](https://{GITLAB}/{target}/-/{path}/{num})"

    def text(part):
        part = REF.sub(ref, part)
        part = MENTION.sub(r"`@\1`", part)
        return UPLOAD.sub(lambda m: f"](https://{GITLAB}/{project}{m.group(1)})", part)

    return "".join(p if CODE.fullmatch(p) else text(p) for p in CODE.split(notes))


def main():
    args = [a for a in sys.argv[1:] if a != "--dry-run"]
    dry = "--dry-run" in sys.argv
    project, repo, only = args[0], args[1], set(args[2:])

    releases = json.loads(run("glab", "api", "--hostname", GITLAB,
                              f"projects/{project.replace('/', '%2F')}/releases?per_page=100"))
    releases.sort(key=lambda r: r["released_at"])
    on_github = {r["tagName"] for r in json.loads(run("gh", "release", "list", "--repo", repo, "--limit", "1000", "--json", "tagName"))}
    tags = {t["name"] for t in json.loads(run("gh", "api", "--paginate", f"repos/{repo}/tags?per_page=100"))}
    known = gitlab_paths()

    created = []
    for r in releases:
        tag = r["tag_name"]
        if only and tag not in only:
            continue
        if tag in on_github:
            print(f"{tag}: already on GitHub")
            continue
        if tag not in tags:
            print(f"{tag}: SKIPPED, tag not on GitHub (mirror not synced?)")
            continue
        notes = convert(r["description"] or "", project, known)
        title = r["name"] or tag
        if dry:
            print(f"===== {tag} | {title}\n{notes}\n")
            continue
        with tempfile.NamedTemporaryFile("w", suffix=".md") as f:
            f.write(notes)
            f.flush()
            run("gh", "release", "create", tag, "--repo", repo, "--verify-tag", "--title", title,
                "--notes-file", f.name, "--latest=false")
        created.append(tag)
        print(f"{tag}: created")

    newest = releases[-1]["tag_name"] if releases else None
    if created and newest in set(created) | on_github:
        run("gh", "release", "edit", newest, "--repo", repo, "--latest")
        print(f"{newest}: marked Latest")


if __name__ == "__main__":
    main()
