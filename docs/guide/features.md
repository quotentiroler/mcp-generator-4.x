# Optional features

Each feature below is off by default and enabled with a `generate-mcp` flag. Flags can be
combined:

```bash
generate-mcp --enable-resources --enable-storage --enable-caching --enable-apps --generate-ui
```

## MCP resources

`--enable-resources` turns GET operations that have an `operationId` into MCP resource
templates, next to the tools. Path and query parameters become RFC 6570 template variables:

```text
pet://Pet/pet/{petId}
findbystatus://Pet/pet/findByStatus{?status}
```

## Storage and caching

`--enable-storage` writes `generated_mcp/storage.py`, a small async key-value store:

```python
from storage import get_storage

storage = get_storage("filesystem", storage_dir=".mcp_storage")  # or get_storage("memory")
await storage.set("key", "value")
value = await storage.get("key")
```

The filesystem backend encrypts values with Fernet when `cryptography` is installed. Without
an `encryption_key` argument it creates a key in `<storage_dir>/.encryption_key`. The OAuth
helpers in `middleware/oauth_provider.py` use this store to persist tokens.

`--enable-caching` (together with `--enable-storage`) writes `generated_mcp/cache.py`, a
decorator that caches function results in the store. It is opt-in per function:

```python
from storage import get_storage
from cache import get_cache_middleware

cache = get_cache_middleware(get_storage("filesystem"), default_ttl=300)

@cache.cached(ttl=600)
async def expensive_lookup(param: str) -> dict:
    ...
```

## MCP Apps display tools

`--enable-apps` mounts a `display` sub-server with eight tools that render data as interactive
UI in clients that support MCP Apps: `display_show_table`, `display_show_detail`,
`display_show_chart`, `display_show_form`, `display_show_comparison`, `display_show_metrics`,
`display_show_timeline` and `display_show_progress`. The model passes the data to show.

Rendering uses `prefab-ui`, which the generated `pyproject.toml` pulls in through
`fastmcp[apps]`. Without it, the display tools return the data as JSON.

`--generate-ui` (with `--enable-apps`) adds per-tag sub-servers built from the spec's response
and request schemas, mounted as `<tag>_ui`:

| Tool name pattern | Source operation | Renders |
|---|---|---|
| `<tag>_ui_view_<operation>_table` | GET returning an array | Table with typed columns |
| `<tag>_ui_view_<operation>_detail` | GET returning an object | Detail card |
| `<tag>_ui_form_<operation>` | POST or PUT with a request body | Input form that calls the operation |
| `<tag>_ui_action_delete_<operation>` | DELETE | Confirmation action |

`--schema-depth` (default 3) limits how deep nested schemas are expanded into columns and
fields.

Setting `features.apps.generative_ui` to `true` in `fastmcp.json` also adds FastMCP's
`GenerativeUI` provider.

## OpenAPI Overlays

`--overlay PATH` applies an [OpenAPI Overlay 1.0.0](https://spec.openapis.org/overlay/v1.0.0.html)
document (JSON or YAML) before generation. Each action has a `target` path and either an
`update` value or `remove: true`:

```yaml
overlay: 1.0.0
info:
  title: Petstore descriptions
  version: 1.0.0
actions:
  - target: "$.paths['/pet/{petId}'].get.description"
    update: Return one pet by its numeric ID.
```

`--overlay fhir` applies the overlay bundled with the package for FHIR APIs.

`--auto-overlay` builds an overlay from the spec itself, using fixed rules:

- An operation whose description is missing or shorter than the inferred one gets a
  description derived from its HTTP method and path, such as "Retrieve details of a specific
  pet." An operation without a summary gets the same text as its summary.
- A parameter without a description gets one from a list of common names (`limit`, `offset`,
  `sort`, `q` and others), or "Required string parameter." style text from its type.

No model or network call is involved.

Both options leave the original file unchanged and write the result to
`<name>_enhanced.<ext>` next to it.

## A2A adapter

`--enable-a2a` writes two files into `generated_mcp/`:

- `agent_card.json`: an [A2A](https://github.com/a2aproject/A2A) agent card with one skill per
  sub-server
- `a2a_adapter.py`: a scaffold for serving the card and forwarding A2A tasks to the MCP tools,
  which needs `pip install a2a-sdk starlette uvicorn`

The adapter is a starting point. It does not yet run unmodified against servers generated for
FastMCP 4, so expect to adapt its server import and tool calls.
