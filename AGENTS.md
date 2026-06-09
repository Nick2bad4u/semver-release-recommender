# Semver Release Recommender Skill Guidance

This repository packages the `semver-release-recommender` Codex/open-agent skill. Keep changes focused on release-impact analysis, packaged skill metadata, and the evidence collection helper.

## Scope

- Treat `SKILL.md` as the skill entrypoint.
- Keep `agents/openai.yaml`, `assets/`, `scripts/`, and `LICENSE.txt` synchronized with the packaged skill.
- Keep `scripts/analyze_release_semver.py` portable: standard-library Python only.
- Do not make the skill create tags, releases, commits, or version bumps unless the invoking user explicitly asks.

## Validation

Run the narrowest useful checks after edits:

```powershell
python "C:\Users\Nick\.codex\skills\.system\skill-creator\scripts\quick_validate.py" .
npm run release:verify
```

## Style

- Keep the skill procedural and concise.
- Prefer direct git evidence over generic release advice.
- Treat public API, packaging, runtime, CLI, schema, and documented behavior changes as the core semver evidence.
