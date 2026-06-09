#!/usr/bin/env python3
"""Collect release-range evidence for semver bump analysis."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


SEMVER_TAG = re.compile(r"^v?(\d+)\.(\d+)\.(\d+)(?:[-+].*)?$")
BREAKING_FOOTER = re.compile(r"(?im)^BREAKING(?:[ -]CHANGE)?:")
CONVENTIONAL = re.compile(
    r"^(?P<type>[a-zA-Z]+)(?:\([^)]+\))?(?P<breaking>!)?:\s+(?P<subject>.+)$"
)
BRACKETED_TYPE = re.compile(
    r"^(?P<prefix>.*?)\[(?P<type>[a-zA-Z]+)\](?P<breaking>!)?(?:\s+|\s*\([^)]+\)\s+)(?P<subject>.+)$"
)

PUBLIC_SURFACE_PATTERNS = (
    re.compile(r"(^|/)(package\.json|pyproject\.toml|Cargo\.toml|go\.mod)$"),
    re.compile(r"(^|/)SKILL\.md$"),
    re.compile(r"(^|/)(README|CHANGELOG|SECURITY|MIGRATION|UPGRADING)(\..*)?$", re.I),
    re.compile(r"(^|/)(src|lib|bin|cli|schemas?|api|types?|docs?)/"),
    re.compile(r"\.(d\.ts|schema\.json|proto|graphql|openapi\.(json|ya?ml))$", re.I),
)


@dataclass(frozen=True)
class GitResult:
    stdout: str
    stderr: str


def run_git(args: list[str], *, check: bool = True) -> GitResult:
    completed = subprocess.run(
        ["git", *args],
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if check and completed.returncode != 0:
        message = completed.stderr.strip() or completed.stdout.strip()
        raise RuntimeError(f"git {' '.join(args)} failed: {message}")
    return GitResult(completed.stdout.strip(), completed.stderr.strip())


def semver_key(tag: str) -> tuple[int, int, int]:
    match = SEMVER_TAG.match(tag)
    if not match:
        return (-1, -1, -1)
    return tuple(int(part) for part in match.groups())


def latest_semver_tag(target: str) -> str | None:
    result = run_git(["tag", "--merged", target, "--list", "v[0-9]*.[0-9]*.[0-9]*"])
    tags = [line.strip() for line in result.stdout.splitlines() if SEMVER_TAG.match(line.strip())]
    if not tags:
        result = run_git(["tag", "--merged", target, "--list", "[0-9]*.[0-9]*.[0-9]*"])
        tags = [line.strip() for line in result.stdout.splitlines() if SEMVER_TAG.match(line.strip())]
    return max(tags, key=semver_key) if tags else None


def commit_rows(revision_range: str) -> list[dict[str, str]]:
    output = run_git(
        ["log", "--reverse", "--format=%H%x09%h%x09%s%x09%b%x1e", revision_range],
        check=False,
    ).stdout
    rows: list[dict[str, str]] = []
    for record in output.split("\x1e"):
        record = record.strip("\n")
        if not record:
            continue
        parts = record.split("\t", 3)
        while len(parts) < 4:
            parts.append("")
        full_hash, short_hash, subject, body = parts
        rows.append(
            {
                "hash": full_hash.strip(),
                "short": short_hash.strip(),
                "subject": subject.strip(),
                "body": body.strip(),
            }
        )
    return rows


def changed_files(base: str | None, target: str) -> list[dict[str, str]]:
    if base:
        args = ["diff", "--name-status", f"{base}..{target}"]
    else:
        empty_tree = "4b825dc642cb6eb9a060e54bf8d69288fbee4904"
        args = ["diff", "--name-status", empty_tree, target]
    output = run_git(args).stdout
    files: list[dict[str, str]] = []
    for line in output.splitlines():
        parts = line.split("\t")
        if len(parts) >= 2:
            files.append({"status": parts[0], "path": parts[-1]})
    return files


def diff_stat(base: str | None, target: str) -> str:
    if base:
        return run_git(["diff", "--stat", f"{base}..{target}"]).stdout
    empty_tree = "4b825dc642cb6eb9a060e54bf8d69288fbee4904"
    return run_git(["diff", "--stat", empty_tree, target]).stdout


def package_version() -> str | None:
    package_json = Path("package.json")
    if not package_json.exists():
        return None
    try:
        data = json.loads(package_json.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    version = data.get("version")
    return version if isinstance(version, str) else None


def classify_commits(commits: list[dict[str, str]]) -> dict[str, list[str]]:
    signals: dict[str, list[str]] = {"major": [], "minor": [], "patch": []}
    for commit in commits:
        text = f"{commit['subject']}\n{commit['body']}"
        conventional = CONVENTIONAL.match(commit["subject"])
        bracketed_type = BRACKETED_TYPE.match(commit["subject"])
        prefix = f"{commit['short']} {commit['subject']}"
        breaking_marker = (
            (conventional and conventional.group("breaking"))
            or (bracketed_type and bracketed_type.group("breaking"))
        )
        if BREAKING_FOOTER.search(text) or breaking_marker:
            signals["major"].append(prefix)
            continue
        typed_commit = conventional or bracketed_type
        if typed_commit:
            commit_type = typed_commit.group("type").lower()
            if commit_type == "feat":
                signals["minor"].append(prefix)
            elif commit_type in {"fix", "perf"}:
                signals["patch"].append(prefix)
    return {key: value for key, value in signals.items() if value}


def public_surface_files(files: list[dict[str, str]]) -> list[str]:
    paths = [entry["path"].replace("\\", "/") for entry in files]
    return [
        path
        for path in paths
        if any(pattern.search(path) for pattern in PUBLIC_SURFACE_PATTERNS)
    ]


def summarize(data: dict[str, Any]) -> str:
    lines = [
        f"Repository: {data['repository_root']}",
        f"Range: {data['range']}",
        f"Base tag: {data['base_tag'] or '(none found)'}",
        f"Target: {data['target_commit']}",
    ]
    if data.get("package_version"):
        lines.append(f"package.json version: {data['package_version']}")
    lines.extend(
        [
            f"Commits: {data['commit_count']}",
            f"Changed files: {data['changed_file_count']}",
            "",
            "Conventional commit signals:",
        ]
    )
    signals = data["conventional_signals"]
    if signals:
        for impact in ("major", "minor", "patch"):
            for item in signals.get(impact, []):
                lines.append(f"- {impact}: {item}")
    else:
        lines.append("- none detected")
    lines.append("")
    lines.append("Public-surface candidate files:")
    if data["public_surface_files"]:
        for path in data["public_surface_files"]:
            lines.append(f"- {path}")
    else:
        lines.append("- none detected")
    lines.append("")
    lines.append("Diff stat:")
    lines.append(data["diff_stat"] or "(empty)")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Collect release-range evidence for semver bump analysis."
    )
    parser.add_argument("--base-tag", help="Use this tag or revision as the release base.")
    parser.add_argument("--target", default="HEAD", help="Target revision to analyze.")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON.")
    args = parser.parse_args()

    try:
        root = run_git(["rev-parse", "--show-toplevel"]).stdout
        target_commit = run_git(["rev-parse", args.target]).stdout
        base = args.base_tag or latest_semver_tag(args.target)
        revision_range = f"{base}..{args.target}" if base else args.target
        commits = commit_rows(revision_range)
        files = changed_files(base, args.target)
        data: dict[str, Any] = {
            "repository_root": root,
            "range": revision_range,
            "base_tag": base,
            "target": args.target,
            "target_commit": target_commit,
            "package_version": package_version(),
            "commit_count": len(commits),
            "commits": commits,
            "changed_file_count": len(files),
            "changed_files": files,
            "public_surface_files": public_surface_files(files),
            "conventional_signals": classify_commits(commits),
            "diff_stat": diff_stat(base, args.target),
        }
    except RuntimeError as error:
        print(error, file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps(data, indent=2, sort_keys=True))
    else:
        print(summarize(data))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
