# Architecture

## Generation pipeline

`generate-mcp` runs these steps in the current working directory:

1. Load the spec from `--file` or download it from `--url`. JSON and YAML are both accepted.
2. Apply `--overlay` and `--auto-overlay`, if given, to a copy of the spec and write it as
   `<name>_enhanced.<ext>` next to the original.
3. Write the resolved spec to `generated_openapi/openapi.json` and generate a typed Python
   client from it with [openapi-py-fetch](https://pypi.org/project/openapi-py-fetch/). Every
   later step reads this resolved spec.
4. Introspect the client's API classes and the spec: operations, parameters, request bodies,
   security schemes and GET endpoints.
5. Render one server module per API class, the middleware, the main server and the package
   files into `generated_mcp/`.
6. Render the test suite into `test/generated/` and the runner into `test/run_tests.py`.

## Generated layout

```text
generated_openapi/
├── openapi.json                 resolved spec used for generation
└── openapi_client/              typed API client
generated_mcp/
├── <title>_mcp_generated.py     main server and CLI entry point
├── servers/<tag>_server.py      one FastMCP sub-server per API tag
├── middleware/
│   ├── authentication.py        ApiClientContextMiddleware, JWT backend
│   ├── oauth_provider.py        verifier and auth provider factories
│   └── event_store.py
├── fastmcp.json                 runtime feature switches
├── pyproject.toml
├── README.md
├── Dockerfile, docker-compose.yml, .dockerignore
├── storage.py                   with --enable-storage
├── cache.py                     with --enable-storage --enable-caching
├── apps/                        with --enable-apps
└── agent_card.json, a2a_adapter.py   with --enable-a2a
```

`<title>` is the spec's `info.title` converted to a Python identifier, for example
`swagger_petstore_openapi` for "Swagger Petstore - OpenAPI 3.0".

## Sub-servers and composition

The client generator creates one API class per OpenAPI tag. Operations without a tag go to a
`default` class. Tags that operations use but the top-level `tags` list does not declare are
added before generation, so they still get their own class.

Each API class becomes a module under `servers/` with its own `FastMCP` instance. An operation
listed under several tags is generated once, in the first module that reaches it. The main
server mounts every module under a namespace named after the API class:

```python
app.mount(Pet_mcp, namespace="Pet")
app.mount(Store_mcp, namespace="Store")
app.mount(User_mcp, namespace="User")
```

FastMCP prefixes tool names with the namespace, so clients see `Pet_add_pet`,
`Store_place_order` and so on.

Mounting happens in `_compose_mcp_servers()`, which `main()` calls after adding the
middleware. `create_server()` mounts the sub-servers without adding middleware: use it with
`fastmcp inspect` to list components, and start the server through `main()` to call tools.

## Tools

Each operation becomes an async tool that builds the client call from its arguments:

```python
@mcp.tool(tags=["pet"], timeout=30)
async def get_pet_by_id(ctx: Context, pet_id: str) -> dict[str, Any]:
    ...
```

- `tags` holds the module's tag.
- `timeout` is 30 seconds for every tool.
- An operation whose summary or description mentions "deprecated" also gets
  `version="deprecated"`.
- On the FastMCP 3 target, a tool asks the client for missing required parameters with
  `ctx.elicit()` and uses `ctx.sample()` to suggest a fix after an API error. On the FastMCP 4
  target, the tool returns the list of missing parameters and raises API errors unchanged,
  since the sessionless `2026-07-28` protocol has no server-to-client requests.

## Resources

With `--enable-resources`, GET operations that have an `operationId` also become MCP resource
templates. Path and query parameters map to an RFC 6570 URI template, for example
`pet://Pet/pet/{petId}`.

## Transports

| Flag | Transport | Endpoint |
|---|---|---|
| `--transport stdio` (default) | STDIO | |
| `--transport http` | Streamable HTTP with an event store for resumable streams | `http://<host>:<port>/mcp` |

`--host` defaults to `0.0.0.0` and `--port` to `8000`. Servers whose spec declares security
schemes also accept `--validate-tokens`; see [Authentication](authentication.md).

## Target FastMCP version

`--fastmcp-target` selects the FastMCP major the server is written for. The differences are
kept in `mcp_generator/fastmcp_target.py`.

| | Target 4 (default) | Target 3 |
|---|---|---|
| `fastmcp` requirement | `>=4.0.2,<5.0.0` | `>=3.2.4,<4.0.0` |
| `pydantic` requirement | `>=2.12,<3.0.0` | `>=2.10.3,<3.0.0` |
| Missing required parameters | Returned to the caller | `ctx.elicit()` |
| API error recovery | Error raised as is | `ctx.sample()` hint |
| HTTP client for token introspection | `httpx2` | `httpx` |

## Middleware and runtime features

The middleware stack and the switches in `fastmcp.json` are described in
[Middleware](middleware.md) and [Configuration](configuration.md).
