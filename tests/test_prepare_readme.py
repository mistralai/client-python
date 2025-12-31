import importlib.util
from pathlib import Path

SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "prepare_readme.py"
SPEC = importlib.util.spec_from_file_location("prepare_readme", SCRIPT_PATH)
if SPEC is None or SPEC.loader is None:
    raise ImportError(f"Unable to load prepare_readme from {SCRIPT_PATH}")
prepare_readme = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(prepare_readme)


def test_rewrite_relative_links_keeps_absolute() -> None:
    base_url = "https://example.com/blob/main/"
    contents = "[Migration](MIGRATION.md)\n[Docs](https://docs.mistral.ai)"
    expected = (
        "[Migration](https://example.com/blob/main/MIGRATION.md)\n"
        "[Docs](https://docs.mistral.ai)"
    )
    assert prepare_readme.rewrite_relative_links(contents, base_url) == expected


def test_main_prints_rewritten_readme_with_defaults(tmp_path, capsys) -> None:
    original = "[Migration](MIGRATION.md)\n"
    base_url = prepare_readme.build_base_url(
        prepare_readme.DEFAULT_REPO_URL,
        prepare_readme.DEFAULT_BRANCH,
        "",
    )
    expected = f"[Migration]({base_url}MIGRATION.md)\n"
    readme_path = tmp_path / "README.md"
    readme_path.write_text(original, encoding="utf-8")

    exit_code = prepare_readme.main(["--readme", str(readme_path)])

    captured = capsys.readouterr()
    assert exit_code == 0
    assert captured.out == expected
