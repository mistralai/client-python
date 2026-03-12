import importlib.util
from pathlib import Path

import pytest

SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "prepare_readme.py"
SPEC = importlib.util.spec_from_file_location("prepare_readme", SCRIPT_PATH)
if SPEC is None or SPEC.loader is None:
    raise ImportError(f"Unable to load prepare_readme from {SCRIPT_PATH}")
prepare_readme = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(prepare_readme)

BASE_URL = "https://example.com/blob/main/"


def test_rewrite_relative_links_keeps_absolute() -> None:
    contents = "[Migration](MIGRATION.md)\n[Docs](https://docs.mistral.ai)"
    expected = (
        f"[Migration]({BASE_URL}MIGRATION.md)\n"
        "[Docs](https://docs.mistral.ai)"
    )
    assert prepare_readme._rewrite_relative_links(contents, BASE_URL) == expected


def test_rewrite_relative_links_keeps_http() -> None:
    contents = "[Site](http://example.com)"
    assert prepare_readme._rewrite_relative_links(contents, BASE_URL) == contents


def test_rewrite_relative_links_keeps_anchors() -> None:
    contents = "[Retries](#retries)\n[File](docs/README.md#upload)"
    expected = (
        "[Retries](#retries)\n"
        f"[File]({BASE_URL}docs/README.md#upload)"
    )
    assert prepare_readme._rewrite_relative_links(contents, BASE_URL) == expected


def test_rewrite_relative_links_keeps_mailto() -> None:
    contents = "[Email](mailto:user@example.com)"
    assert prepare_readme._rewrite_relative_links(contents, BASE_URL) == contents


def test_rewrite_relative_links_keeps_ftp() -> None:
    contents = "[FTP](ftp://files.example.com/data)"
    assert prepare_readme._rewrite_relative_links(contents, BASE_URL) == contents


def test_rewrite_strips_leading_dot_slash() -> None:
    contents = "[Errors](./src/errors.py)"
    expected = f"[Errors]({BASE_URL}src/errors.py)"
    assert prepare_readme._rewrite_relative_links(contents, BASE_URL) == expected


def test_rewrite_strips_leading_slash() -> None:
    contents = "[Examples](/examples/azure)"
    expected = f"[Examples]({BASE_URL}examples/azure)"
    assert prepare_readme._rewrite_relative_links(contents, BASE_URL) == expected


def test_rewrite_multiple_links_same_line() -> None:
    contents = "[A](a.md) and [B](b.md)"
    expected = f"[A]({BASE_URL}a.md) and [B]({BASE_URL}b.md)"
    assert prepare_readme._rewrite_relative_links(contents, BASE_URL) == expected


def test_build_base_url_strips_git_suffix() -> None:
    url = prepare_readme._build_base_url(
        "https://github.com/org/repo.git", "main", ""
    )
    assert url == "https://github.com/org/repo/blob/main/"


def test_build_base_url_no_git_suffix() -> None:
    url = prepare_readme._build_base_url(
        "https://github.com/org/repo", "main", ""
    )
    assert url == "https://github.com/org/repo/blob/main/"


def test_build_base_url_with_subdir() -> None:
    url = prepare_readme._build_base_url(
        "https://github.com/org/repo.git", "main", "packages/azure"
    )
    assert url == "https://github.com/org/repo/blob/main/packages/azure/"


def test_build_base_url_strips_subdir_slashes() -> None:
    url = prepare_readme._build_base_url(
        "https://github.com/org/repo.git", "main", "/packages/azure/"
    )
    assert url == "https://github.com/org/repo/blob/main/packages/azure/"
