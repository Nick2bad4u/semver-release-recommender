# Contributing

Keep this repository focused on the `semver-release-recommender` skill payload and packaging metadata.

Before submitting changes:

```powershell
python "C:\Users\Nick\.codex\skills\.system\skill-creator\scripts\quick_validate.py" .
npm run release:verify
```

Do not add automation that performs commits automatically. The skill should preserve agent judgment around grouping, message rules, staged content, and user-owned changes.
