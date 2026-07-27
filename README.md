Data Analyst Portfolio — Personal static site

Overview

This repository contains a lightweight personal portfolio site intended to be a living record of work, projects, learning, and life notes. Content is stored as simple JSON files in /data so updates can be made without touching the site code.

Quick start (non-developer friendly)

1. Edit content: open the data/ folder and edit the JSON files (about.json, work.json, projects.json, learning.json, journal.json). Add new entries to the appropriate file. Keep the JSON structure consistent.
2. Commit and push to the repository's main branch.
3. The GitHub Action (on push to main) will publish the site to GitHub Pages automatically. After the first push, open the repository settings → Pages to confirm the site URL if needed.

File structure

- index.html — single-page app shell and navigation
- assets/css/style.css — styling, light/dark mode support
- assets/js/app.js — loads data and renders sections; search and filters are client-side
- data/*.json — content files (edit these as plain text)
- .github/workflows/deploy.yml — GitHub Action to publish via GitHub Pages on push to main

Editing content safely

- Always make a branch and test locally if unsure. You can preview by opening index.html directly in a browser.
- Use a simple text editor (VS Code, Notepad) to edit JSON. Keep trailing commas out and ensure valid JSON.

Optional: LinkedIn update (manual)

- Automatic LinkedIn posting requires an app and OAuth tokens. For long-term simplicity, consider writing a short copy in the journal entry and manually post to LinkedIn.

Questions or help

If you want this repository adapted to a different layout, or to add more automation (e.g., image handling, project screenshots), say so and the site can be extended without changing the content format.
