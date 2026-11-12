# Testing

## Generated test suite

`generate-mcp` writes a pytest suite to `test/generated/` and a runner to
`test/run_tests.py`, both relative to the directory it ran in. The suite covers tool
registration and schemas, `tools/call` round trips, HTTP behavior, OpenAPI features,
transforms, and performance. Depending on the spec and flags it also covers authentication
flows, MultiAuth, resources, caching and OAuth token persistence.

```bash
python test/run_tests.py                                   # whole suite
python test/run_tests.py --test test_tools                 # pytest -k pattern
python test/run_tests.py --test test_behavioral_generated.py
```

The runner starts `generated_mcp/<title>_mcp_generated.py --transport http` with `uv run`,
waits for it on port 8000, runs pytest and stops the server. It needs
[uv](https://docs.astral.sh/uv/) plus `pytest` and `httpx` in the current environment. Set
`MCP_SERVER_PORT` to use another port, or `MCP_SERVER_URL` when the tests should call a
server you started yourself.

`test_behavioral_generated.py` holds edge-case tests that are expected to fail until you adapt
the server, so the default run skips it. Pass it with `--test` to run it.

## MCP Inspector

The [MCP Inspector](https://github.com/modelcontextprotocol/inspector) is an interactive client
for MCP servers. Start it with `npx` and let it launch the server through `main()`:

```bash
npx @modelcontextprotocol/inspector -e API_TOKEN=your-token \
  python generated_mcp/swagger_petstore_openapi_mcp_generated.py
```

In CLI mode the Inspector lists or calls tools without a browser:

```bash
npx @modelcontextprotocol/inspector --cli \
  python generated_mcp/swagger_petstore_openapi_mcp_generated.py \
  --method tools/list

npx @modelcontextprotocol/inspector --cli \
  python generated_mcp/swagger_petstore_openapi_mcp_generated.py \
  --method tools/call --tool-name Pet_find_pets_by_status --tool-arg status=available
```

To inspect a server that is already running over HTTP:

```bash
npx @modelcontextprotocol/inspector --cli http://localhost:8000/mcp --transport http --method tools/list
```

`fastmcp inspect generated_mcp/<title>_mcp_generated.py:create_server` prints a summary of the
server's tools, resources and templates without starting a client. Tool calls need the
middleware that `main()` adds, which `fastmcp dev inspector ...:create_server` skips, so use
the `npx` commands above to call tools.

## Generator tests

The generator's own tests live in `test/` of the repository:

```bash
uv sync --group dev
uv run pytest test/ --ignore=test/generated
uv run pytest test/ --cov=mcp_generator --ignore=test/generated
```

`scripts/test_examples.py` regenerates every example and runs its suite; see
[Examples](../getting-started/examples.md).
