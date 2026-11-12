# Installation

## Requirements

- Python 3.11 or later
- An OpenAPI 3.0.x, OpenAPI 3.1.x or Swagger 2.0 specification in JSON or YAML

The generator and the API client it produces are pure Python. No Java or Node.js runtime is
needed.

## From PyPI

```bash
pip install mcp-generator
# or
uv pip install mcp-generator
```

The package installs three commands: `generate-mcp`, `register-mcp` and `run-mcp`.

## From source

```bash
git clone https://github.com/quotentiroler/mcp-generator-4.x.git
cd mcp-generator-4.x
uv sync            # or: pip install -e .
```

## Check the installation

```bash
generate-mcp --help
```

The output starts with:

```text
usage: generate-mcp [-h] [--file FILE] [--url URL] [--enable-storage] [--enable-caching]
```

The full option list is in the [CLI reference](../guide/cli.md).

## Runtime dependencies of generated servers

A generated server declares its own dependencies in `generated_mcp/pyproject.toml`
(`fastmcp`, `openapi-py-fetch`, `pydantic` and the auth libraries). Install them in the
environment that runs the server:

```bash
pip install -e ./generated_mcp
```

Next: [Quick start](quickstart.md).
