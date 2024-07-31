# Mistral Python Client

This client is inspired from [cohere-python](https://github.com/cohere-ai/cohere-python)

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

### Build System

Pants is setup in this repository to ease the developer experience. Follow instruction here to install Pants: [Pants build system](https://www.pantsbuild.org/docs)

Run tests:

```bash
pants test ::
```

Run lint + check + fmt:

```bash
make lint
```

## Run examples

You can run the examples in the `examples/` directory using `poetry run` or `pants run`

### API Key Setup

Running the examples requires a Mistral AI API key.

1. Get your own Mistral API Key: <https://docs.mistral.ai/#api-access>
2. Set your Mistral API Key as an environment variable. You only need to do this once.

```bash
# set Mistral API Key (using zsh for example)
$ echo 'export MISTRAL_API_KEY=[your_key_here]' >> ~/.zshenv

# reload the environment (or just quit and open a new terminal)
$ source ~/.zshenv
```

### Using poetry run

```bash
cd examples
poetry run python chat_no_streaming.py
```

### Using pants run

```bash
cd examples
pants run chat_no_streaming.py
```
