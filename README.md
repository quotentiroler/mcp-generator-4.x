# MCP Generator 4.x

[![PyPI](https://img.shields.io/pypi/v/mcp-generator)](https://pypi.org/project/mcp-generator/)
[![GitHub Release](https://img.shields.io/github/v/release/quotentiroler/mcp-generator-4.x?label=version)](https://github.com/quotentiroler/mcp-generator-4.x/releases)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://github.com/quotentiroler/mcp-generator-4.x/blob/main/LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-3776ab.svg)](https://www.python.org/downloads/)
[![Docs](https://img.shields.io/badge/docs-GitHub%20Pages-blue.svg)](https://quotentiroler.github.io/mcp-generator-4.x/)

MCP Generator reads an OpenAPI 3.0, OpenAPI 3.1 or Swagger 2.0 specification (JSON or YAML)
and writes a [FastMCP](https://github.com/PrefectHQ/fastmcp) server that exposes each API
operation as an MCP tool. The output is a Python package with one sub-server per API tag, a
typed API client, authentication and logging middleware, a runtime configuration file, a
Dockerfile and a test suite. Generated servers target FastMCP 4 by default and FastMCP 3 with
`--fastmcp-target 3`.

## Installation

```bash
pip install mcp-generator
```

Python 3.11 or later is required. The generator is pure Python; no Java or Node.js runtime is
needed. See [Installation](https://quotentiroler.github.io/mcp-generator-4.x/getting-started/installation/)
for installing from source.

## Quick start

```bash
generate-mcp --url https://petstore3.swagger.io/api/v3/openapi.json
pip install -e ./generated_mcp
python generated_mcp/swagger_petstore_openapi_mcp_generated.py --transport http --port 8000
```

The server listens on `http://localhost:8000/mcp`. Without `--transport http` it uses STDIO and
sends the `API_TOKEN` environment variable to the backend API.

The [quick start guide](https://quotentiroler.github.io/mcp-generator-4.x/getting-started/quickstart/)
covers local spec files, client configuration, the local server registry and the generated
tests.

## Features

- One FastMCP sub-server per OpenAPI tag, mounted under a namespace in a main server
- Typed Python API client generated from the spec
- STDIO and Streamable HTTP transports
- Backend token forwarding, optional JWT validation over HTTP, and OAuth2 settings taken from
  the spec's security schemes
- Middleware for error handling, timing, logging, response size limits, keepalive pings and
  optional rate limiting
- Runtime switches in `fastmcp.json` for tool search, CodeMode, version filtering,
  OpenTelemetry and auth providers
- Generated pytest suite and test runner
- `register-mcp` and `run-mcp` for starting generated servers by name

Optional flags add MCP resources for GET endpoints (`--enable-resources`), a storage backend
and cache decorator (`--enable-storage`, `--enable-caching`), MCP Apps display tools
(`--enable-apps`, `--generate-ui`), OpenAPI Overlay processing (`--overlay`,
`--auto-overlay`) and an A2A adapter scaffold (`--enable-a2a`).

## Documentation

Full documentation: <https://quotentiroler.github.io/mcp-generator-4.x/>

| Topic | Page |
|---|---|
| Command-line options | [CLI reference](https://quotentiroler.github.io/mcp-generator-4.x/guide/cli/) |
| Generated code layout | [Architecture](https://quotentiroler.github.io/mcp-generator-4.x/guide/architecture/) |
| Optional flags | [Optional features](https://quotentiroler.github.io/mcp-generator-4.x/guide/features/) |
| Tokens and JWT validation | [Authentication](https://quotentiroler.github.io/mcp-generator-4.x/guide/authentication/) |
| `fastmcp.json` and environment variables | [Configuration](https://quotentiroler.github.io/mcp-generator-4.x/guide/configuration/) |
| Middleware stack | [Middleware](https://quotentiroler.github.io/mcp-generator-4.x/guide/middleware/) |
| Test suite and MCP Inspector | [Testing](https://quotentiroler.github.io/mcp-generator-4.x/guide/testing/) |

The same pages are in [`docs/`](https://github.com/quotentiroler/mcp-generator-4.x/tree/main/docs) in this repository.

## Contributing

See [CONTRIBUTING.md](https://github.com/quotentiroler/mcp-generator-4.x/blob/main/CONTRIBUTING.md) for the development setup, branch flow and checks.
Report bugs and request features in the [issue tracker](https://github.com/quotentiroler/mcp-generator-4.x/issues).

## License

Apache License 2.0. See [LICENSE](https://github.com/quotentiroler/mcp-generator-4.x/blob/main/LICENSE).

Code produced by the generator is not considered a derivative work of the generator. You may
license your generated servers as you choose.
