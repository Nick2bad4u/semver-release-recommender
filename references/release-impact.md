# Release Impact

Use this reference after collecting release-range evidence and before recommending a semantic version bump.

## Public Surface Inventory

Inspect, as applicable:

- public API files, exports, CLI entrypoints, schemas, types, config names, plugin rules, generated declarations, and docs that define supported behavior
- package manifests, peer dependencies, engine requirements, bin names, exports maps, module type, runtime dependencies, and lockfiles
- migrations, database schemas, wire formats, environment variables, auth scopes, file formats, and external service contracts
- tests, fixtures, snapshots, examples, and changelog entries that reveal intended behavior

For npm packages, inspect `package.json` changes directly:

- `exports`, `main`, `module`, `types`, `bin`, `files`, `type`, `engines`, `peerDependencies`, `dependencies`, and published package contents
- generated `.d.ts` or public type changes
- `npm pack --dry-run --json` when packaging scope matters

For libraries or plugins, compare documented public names and generated API docs before deciding that a source change is internal.

## Classification

Recommend `major` when the range includes:

- removed or renamed public APIs, CLI commands, flags, config keys, package exports, rule names, schemas, events, or documented behaviors
- changed defaults or stricter validation that can break existing valid consumers
- changed runtime requirements such as minimum Node version, required peer dependency major, required auth scope, or incompatible data format
- conventional commits with `!` or `BREAKING CHANGE` that are confirmed by the diff
- security or correctness fixes that intentionally reject previously accepted user input

Recommend `minor` when the range includes:

- new backwards-compatible APIs, CLI options, config keys, rules, features, outputs, integrations, or documented capabilities
- newly supported platforms, formats, package exports, metadata, or workflows
- deprecations that do not remove behavior yet

Recommend `patch` when the range includes only:

- bug fixes, docs clarifications, test additions, dependency updates, CI changes, refactors, formatting, or internal maintenance that preserve the public contract
- performance improvements without observable API or compatibility changes
- release/package metadata fixes that do not alter consumer behavior

## Confidence

- `high`: actual diffs, public contract files, package metadata, and tests/docs agree.
- `medium`: most evidence is direct, but one public surface could not be fully verified.
- `low`: missing tags, generated artifacts, changelog context, or domain-specific compatibility rules prevent a strong conclusion.

## Defaults

- If both `minor` and `patch` changes exist, recommend `minor`.
- If both `major` and lower-impact changes exist, recommend `major`.
- If no previous release exists, suggest an initial version such as `0.1.0` for pre-stable work or `1.0.0` only when the public contract is ready.
- If the repository uses pre-1.0 semantics, state whether the project treats `0.x` minor bumps as breaking before applying normal SemVer strictly.
