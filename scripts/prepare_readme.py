"""Rewrite README links for PyPI builds and run a command or print to stdout."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

DEFAULT_REPO_URL = "https://github.com/mistralai/client-python.git"
DEFAULT_BRANCH = "main"
LINK_PATTERN = re.compile(r"(\[[^\]]+\]\()((?!https?:)[^\)]+)(\))")


def build_base_url(repo_url: str, branch: str, repo_subdir: str) -> str:
    """Build the GitHub base URL used to rewrite relative README links."""
    normalized_repo_url = repo_url[:-4] if repo_url.endswith(".git") else repo_url
    normalized_subdir = repo_subdir.strip("/")
    if normalized_subdir:
        normalized_subdir = f"{normalized_subdir}/"
    return f"{normalized_repo_url}/blob/{branch}/{normalized_subdir}"


def rewrite_relative_links(contents: str, base_url: str) -> str:
    """Rewrite Markdown relative links to absolute GitHub URLs."""
    return LINK_PATTERN.sub(
        lambda match: f"{match.group(1)}{base_url}{match.group(2)}{match.group(3)}",
        contents,
    )


def run_with_rewritten_readme(
    readme_path: Path, base_url: str, command: list[str]
) -> int:
    """Rewrite README links, run a command, and restore the original README."""
    original_contents = readme_path.read_text(encoding="utf-8")
    rewritten_contents = rewrite_relative_links(original_contents, base_url)
    readme_path.write_text(rewritten_contents, encoding="utf-8")
    try:
        if not command:
            return 0
        result = subprocess.run(command, check=False)
        return result.returncode
    finally:
        readme_path.write_text(original_contents, encoding="utf-8")


def parse_args(argv: list[str]) -> argparse.Namespace:
    """Parse command-line arguments for README rewriting."""
    parser = argparse.ArgumentParser(
        description=(
            "Rewrite README links to absolute GitHub URLs while running a command."
        )
    )
    parser.add_argument(
        "--readme",
        type=Path,
        default=Path("README.md"),
        help="Path to the README file to rewrite.",
    )
    parser.add_argument(
        "--repo-url",
        default=DEFAULT_REPO_URL,
        help="Repository URL used to build absolute links.",
    )
    parser.add_argument(
        "--branch",
        default=DEFAULT_BRANCH,
        help="Repository branch used for absolute links.",
    )
    parser.add_argument(
        "--repo-subdir",
        default="",
        help="Repository subdirectory that contains the README.",
    )
    parser.add_argument(
        "command",
        nargs=argparse.REMAINDER,
        help=(
            "Command to run (prefix with -- to stop option parsing). "
            "If omitted, the rewritten README is printed to stdout."
        ),
    )
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    """Entry point for rewriting README links during build commands."""
    args = parse_args(argv)
    readme_path = args.readme
    if not readme_path.is_file():
        raise FileNotFoundError(f"README file not found: {readme_path}")
    base_url = build_base_url(args.repo_url, args.branch, args.repo_subdir)
    command = (
        args.command[1:]
        if args.command and args.command[0] == "--"
        else args.command
    )
    if not command:
        rewritten_contents = rewrite_relative_links(
            readme_path.read_text(encoding="utf-8"),
            base_url,
        )
        sys.stdout.write(rewritten_contents)
        return 0
    return run_with_rewritten_readme(readme_path, base_url, command)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
