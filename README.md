# Mistral Python Client

This client uses `poetry` as a dependency and virtual environment manager.

You can install poetry with

```bash
pip install poetry
```

## Installing

`poetry` will set up a virtual environment and install dependencies with the following command:

```bash
poetry install
```

## Run examples

You can run the examples using `poetry run` or by entering the virtual environment using `poetry shell`.

### Using poetry run

```bash
cd examples
poetry run python chat_no_streaming.py
```

### Using poetry shell

```bash
cd examples
poetry shell

>> python chat_no_streaming.py
```
