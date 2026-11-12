---
hide:
  - navigation
---

# MCP Generator 4.x

[![PyPI](https://img.shields.io/pypi/v/mcp-generator)](https://pypi.org/project/mcp-generator/)
[![GitHub Release](https://img.shields.io/github/v/release/quotentiroler/mcp-generator-4.x?label=version)](https://github.com/quotentiroler/mcp-generator-4.x/releases)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-3776ab.svg)](https://www.python.org/downloads/)

MCP Generator reads an OpenAPI 3.0, OpenAPI 3.1 or Swagger 2.0 specification and writes a
[FastMCP](https://github.com/PrefectHQ/fastmcp) server that exposes each API operation as an MCP
tool. The output is plain Python that you can read, edit and deploy. Generated servers target
FastMCP 4 by default; `--fastmcp-target 3` emits for the FastMCP 3 line.

## What it generates

- A typed Python client for the API, generated in pure Python (no Java or Node.js runtime)
- One FastMCP sub-server per API tag, mounted into a main server under a namespace
- Middleware for error handling, backend authentication, timing, logging, response size
  limits and keepalive pings
- JWT validation for the HTTP transport, plus OAuth2 configuration taken from the spec's
  security schemes
- A `fastmcp.json` file that switches runtime features on and off
- A `pyproject.toml`, a Dockerfile and a `docker-compose.yml`
- A pytest suite and a runner script for the generated server

Optional flags add MCP resources for GET endpoints, a storage backend, a response cache,
interactive display tools (MCP Apps), OpenAPI Overlay processing and an A2A adapter. See
[Optional features](guide/features.md).

## Example

```bash
pip install mcp-generator
generate-mcp --url https://petstore3.swagger.io/api/v3/openapi.json
python generated_mcp/swagger_petstore_openapi_mcp_generated.py --transport http --port 8000
```

The Petstore spec produces 19 tools in three sub-servers (`Pet`, `Store`, `User`), served at
`http://localhost:8000/mcp`.

## Supported input

| Format | Versions |
|---|---|
| OpenAPI | 3.0.x, 3.1.x |
| Swagger | 2.0 |
| Encoding | JSON or YAML |

## Next steps

- [Installation](getting-started/installation.md)
- [Quick start](getting-started/quickstart.md)
- [Architecture](guide/architecture.md)
- [CLI reference](guide/cli.md)
