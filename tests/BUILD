python_source(
    name="utils",
    source="utils.py",
)

python_source(
    name="conftest",
    source="conftest.py",
)

python_tests(
    name="tests",
    sources=["test_*.py"],
    dependencies=[
        ":utils",
        ":conftest",
    ],
)