This client is inspired from [cohere-python](https://github.com/cohere-ai/cohere-python)

# Mistral Python Client

You can use the Mistral Python client to interact with the Mistral AI API.

## Installing

```bash
pip install mistralai
```

### From Source

This client uses `poetry` as a dependency and virtual environment manager.

You can install poetry with

```bash
pip install poetry
```

`poetry` will set up a virtual environment and install dependencies with the following command:

```bash
poetry install
```

## Run examples

You can run the examples in the `examples/` directory using `poetry run` or by entering the virtual environment using `poetry shell`. You should have a `MISTRAL_API_KEY` environment variable defined containing your API key to run those examples.

### Using poetry run

```bash
cd examples
poetry run python chat_no_streaming.py
```

### Using poetry shell

```bash
poetry shell
cd examples

>> python chat_no_streaming.py
```
