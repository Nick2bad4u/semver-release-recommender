# Semver Release Recommender Skill

[![npm version.](https://flat.badgen.net/npm/v/semver-release-recommender-skill?color=cyan)](https://www.npmjs.com/package/semver-release-recommender-skill) [![npm license.](https://flat.badgen.net/npm/license/semver-release-recommender-skill?color=purple)](https://github.com/Nick2bad4u/semver-release-recommender/blob/main/LICENSE) [![npm total downloads.](https://flat.badgen.net/npm/dt/semver-release-recommender-skill?color=pink)](https://www.npmjs.com/package/semver-release-recommender-skill) [![latest GitHub release.](https://flat.badgen.net/github/release/Nick2bad4u/semver-release-recommender?color=cyan)](https://github.com/Nick2bad4u/semver-release-recommender/releases) [![GitHub stars.](https://flat.badgen.net/github/stars/Nick2bad4u/semver-release-recommender?color=yellow)](https://github.com/Nick2bad4u/semver-release-recommender/stargazers) [![GitHub forks.](https://flat.badgen.net/github/forks/Nick2bad4u/semver-release-recommender?color=green)](https://github.com/Nick2bad4u/semver-release-recommender/forks) [![GitHub open issues.](https://flat.badgen.net/github/open-issues/Nick2bad4u/semver-release-recommender?color=red)](https://github.com/Nick2bad4u/semver-release-recommender/issues) [![GitHub PRs.](https://flat.badgen.net/github/open-prs/Nick2bad4u/semver-release-recommender?color=orange)](https://github.com/Nick2bad4u/semver-release-recommender/pulls?q=sort%3Aupdated-desc+is%3Apr+is%3Aopen) [![GitHub Dependabot](https://flat.badgen.net/github/dependabot/Nick2bad4u/semver-release-recommender?color=blue)](https://github.com/Nick2bad4u/semver-release-recommender/network/updates)

An open-agent skill for analyzing all material changes since the last release and recommending a Semantic Versioning bump.

This repository provides:

- a reusable `semver-release-recommender` skill (`SKILL.md`)
- a portable helper script for release-range evidence collection
- OpenAI-compatible display metadata in `agents/openai.yaml`
- package metadata for local validation and installation through `npx skills`

## What This Skill Does

The skill guides Codex to identify the latest SemVer release tag, inspect commits and diffs through the current revision, classify compatibility impact, and produce a defensible `patch`, `minor`, or `major` recommendation. It explicitly treats real public-surface diffs as stronger evidence than commit labels.

## Repository Layout

```text
SKILL.md
agents/
  openai.yaml
assets/
  semver-release-recommender-small.svg
  semver-release-recommender.svg
scripts/
  analyze_release_semver.py
README.md
CONTRIBUTING.md
SECURITY.md
CHANGELOG.md
```

## Installation

Install from a local checkout:

```powershell
npx skills add . -g --agent universal -y
```

Install from GitHub after publishing the repository:

```powershell
npx skills add Nick2bad4u/semver-release-recommender -g --agent universal -y
```

## Validation

```powershell
python "C:\Users\Nick\.codex\skills\.system\skill-creator\scripts\quick_validate.py" .
npm run release:verify
```
