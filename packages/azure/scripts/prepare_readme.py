import re
import shutil
import sys

GITHUB_URL = "https://github.com/mistralai/client-python.git"
BRANCH = "main"
REPO_SUBDIR = "packages/azure"
LINK_PATTERN = re.compile(r"(\[[^\]]+\]\()((?![a-zA-Z][a-zA-Z0-9+.-]*:|#)[^\)]+)(\))")


def _build_base_url(repo_url: str, branch: str, repo_subdir: str) -> str:
    normalized = repo_url[:-4] if repo_url.endswith(".git") else repo_url
    subdir = repo_subdir.strip("/")
    if subdir:
        subdir = f"{subdir}/"
    return f"{normalized}/blob/{branch}/{subdir}"


def _normalize_relative_path(path: str) -> str:
    if path.startswith("./"):
        path = path[2:]
    elif path.startswith("/"):
        path = path[1:]
    return path


def _rewrite_relative_links(contents: str, base_url: str) -> str:
    return LINK_PATTERN.sub(
        lambda m: f"{m.group(1)}{base_url}{_normalize_relative_path(m.group(2))}{m.group(3)}",
        contents,
    )


try:
    with open("README.md", "r", encoding="utf-8") as fh:
        readme_contents = fh.read()

    base_url = _build_base_url(GITHUB_URL, BRANCH, REPO_SUBDIR)
    readme_contents = _rewrite_relative_links(readme_contents, base_url)

    with open("README-PYPI.md", "w", encoding="utf-8") as fh:
        fh.write(readme_contents)
except Exception as e:
    try:
        print("Failed to rewrite README.md to README-PYPI.md, copying original instead")
        print(e)
        shutil.copyfile("README.md", "README-PYPI.md")
    except Exception as ie:
        print("Failed to copy README.md to README-PYPI.md")
        print(ie)
        sys.exit(1)
