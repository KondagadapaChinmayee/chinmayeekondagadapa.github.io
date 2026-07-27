#!/usr/bin/env python3
"""
Posts a LinkedIn feed update announcing new portfolio content.

This does NOT edit your LinkedIn profile (Experience/Projects/Certifications) —
LinkedIn does not expose that via API to individual developer apps. It posts a
normal status update ("share") to your feed, linking back to your portfolio,
whenever new entries are added to the data/*.json files.

Required environment variables (set as GitHub repo secrets):
  LINKEDIN_ACCESS_TOKEN  - OAuth token with the w_member_social scope
  LINKEDIN_PERSON_URN    - your LinkedIn member URN, e.g. "urn:li:person:abc123"
  PORTFOLIO_URL          - your GitHub Pages URL, e.g. "https://yourname.github.io"

Required environment variables (provided automatically by GitHub Actions):
  GITHUB_SHA, GITHUB_EVENT_BEFORE (set by the workflow)
"""

import json
import os
import subprocess
import sys

import urllib.request
import urllib.error

DATA_FILES = {
    "data/projects.json": ("project", "title"),
    "data/courses.json": ("course", "name"),
    "data/work.json": ("work entry", "role"),
    "data/journal.json": ("journal entry", "title"),
}


def git_show(ref, path):
    try:
        out = subprocess.run(
            ["git", "show", f"{ref}:{path}"],
            capture_output=True, text=True, check=True
        )
        return json.loads(out.stdout)
    except Exception:
        return []


def find_new_items(before_ref, after_ref, path, key_field):
    before = git_show(before_ref, path)
    after = git_show(after_ref, path)
    before_ids = {item.get("id") or item.get(key_field) for item in before}
    new_items = [item for item in after if (item.get("id") or item.get(key_field)) not in before_ids]
    return new_items


def build_message(new_by_file, portfolio_url):
    lines = ["Just updated my portfolio:"]
    any_items = False
    for path, (label, key_field) in DATA_FILES.items():
        items = new_by_file.get(path, [])
        for item in items:
            any_items = True
            name = item.get(key_field, "New entry")
            lines.append(f"• New {label}: {name}")
    if not any_items:
        return None
    lines.append("")
    lines.append(portfolio_url)
    return "\n".join(lines)


def post_to_linkedin(token, person_urn, message):
    url = "https://api.linkedin.com/rest/posts"
    body = {
        "author": person_urn,
        "commentary": message,
        "visibility": "PUBLIC",
        "distribution": {
            "feedDistribution": "MAIN_FEED",
            "targetEntities": [],
            "thirdPartyDistributionChannels": []
        },
        "lifecycleState": "PUBLISHED",
        "isReshareDisabledByAuthor": False
    }
    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(url, data=data, method="POST")
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Content-Type", "application/json")
    req.add_header("X-Restli-Protocol-Version", "2.0.0")
    req.add_header("LinkedIn-Version", "202405")
    try:
        with urllib.request.urlopen(req) as resp:
            print(f"LinkedIn post created: HTTP {resp.status}")
    except urllib.error.HTTPError as e:
        print(f"LinkedIn API error {e.code}: {e.read().decode()}", file=sys.stderr)
        sys.exit(1)


def main():
    token = os.environ.get("LINKEDIN_ACCESS_TOKEN")
    person_urn = os.environ.get("LINKEDIN_PERSON_URN")
    portfolio_url = os.environ.get("PORTFOLIO_URL", "")
    before_ref = os.environ.get("GITHUB_EVENT_BEFORE", "HEAD~1")
    after_ref = os.environ.get("GITHUB_SHA", "HEAD")

    if not token or not person_urn:
        print("Missing LINKEDIN_ACCESS_TOKEN or LINKEDIN_PERSON_URN secret — skipping post.")
        return

    new_by_file = {}
    for path, (label, key_field) in DATA_FILES.items():
        new_by_file[path] = find_new_items(before_ref, after_ref, path, key_field)

    message = build_message(new_by_file, portfolio_url)
    if not message:
        print("No new entries detected — nothing to post.")
        return

    print("Posting to LinkedIn:\n" + message)
    post_to_linkedin(token, person_urn, message)


if __name__ == "__main__":
    main()
