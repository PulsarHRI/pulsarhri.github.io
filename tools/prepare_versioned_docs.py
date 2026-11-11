#!/usr/bin/env python3
"""Build both local documentation versions so `mike serve` can switch between them."""

from __future__ import annotations

import json
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEGACY_COMMIT = "6e279824fc747ef88628bdf4ee74a322b0db61ed"


def run(*command: str, cwd: Path = ROOT) -> None:
    subprocess.run(command, cwd=cwd, check=True)


def deployed_versions() -> set[str]:
    result = subprocess.run(
        ("git", "show", "gh-pages:versions.json"),
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    if result.returncode:
        return set()
    return {entry["version"] for entry in json.loads(result.stdout)}


def deploy_legacy() -> None:
    with tempfile.TemporaryDirectory(prefix="pulsar-docs-") as temporary:
        worktree = Path(temporary) / "2.0.4"
        run("git", "worktree", "add", "--detach", str(worktree), LEGACY_COMMIT)
        try:
            config = worktree / "mkdocs.yml"
            text = config.read_text()
            marker = "\nnav:\n"
            if marker not in text:
                raise RuntimeError("Could not add the version selector to legacy mkdocs.yml")
            config.write_text(
                text.replace(
                    marker,
                    "\n  version:\n    provider: mike\n\nnav:\n",
                    1,
                )
            )
            run("mike", "deploy", "2.0.4", cwd=worktree)
        finally:
            run("git", "worktree", "remove", "--force", str(worktree))


def main() -> None:
    if "2.0.4" not in deployed_versions():
        deploy_legacy()
    run("mike", "deploy", "3.0.0")
    run("mike", "set-default", "3.0.0")
    print("Prepared versions 2.0.4 and 3.0.0. Run `mike serve` to preview them.")


if __name__ == "__main__":
    main()
