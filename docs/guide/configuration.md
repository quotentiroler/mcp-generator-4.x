# Configuration

A generated server reads its runtime settings from `generated_mcp/fastmcp.json` and from
environment variables. Generator behavior is set by command-line flags (see the
[CLI reference](cli.md)) and, for source checkouts, by `mcp_generator/config.py`.

## fastmcp.json

The server loads `fastmcp.json` from its own directory at startup. Edit the file and restart
the server to apply changes; no regeneration is needed. The generator writes it from
`mcp_generator/templates/fastmcp_template.json`.

### Read at runtime

| Key | Default | Effect |
|---|---|---|
| `middleware.config.authentication.validate_tokens` | `false` | Default for `--validate-tokens` |
| `features.search_tools.enabled` | `false` | Adds FastMCP's `BM25SearchTransform`, which lets clients search the tool catalog |
| `features.search_tools.serializer` | `null` | Search result format: `null`, `"markdown"` or `"json"` |
| `features.code_mode.enabled` | `false` | Adds FastMCP's experimental `CodeMode` transform, which replaces the catalog with search, inspect and execute meta-tools |
| `features.version_filter.enabled` | `false` | Adds FastMCP's `VersionFilter` transform |
| `features.version_filter.version_gte`, `version_lt` | `null` | Version bounds for the filter |
| `features.version_filter.include_unversioned` | `true` | Keep tools without a version |
| `features.response_limiting.enabled` | `true` | Adds `ResponseLimitingMiddleware` |
| `features.response_limiting.max_size_bytes` | `1048576` | Response size limit |
| `features.ping_middleware.enabled` | `true` | Adds `PingMiddleware` |
| `features.rate_limiting.enabled` | `false` | Adds `RateLimitingMiddleware` |
| `features.rate_limiting.max_requests_per_second` | `10.0` | Token refill rate |
| `features.rate_limiting.burst_capacity` | `20` | Bucket size |
| `features.rate_limiting.global_limit` | `false` | One bucket for all clients instead of one per client |
| `features.opentelemetry.enabled` | `false` | Installs an OpenTelemetry tracer provider |
| `features.opentelemetry.service_name` | API title | Service name for traces |
| `features.dynamic_visibility.enabled` | `false` | Logs that per-session visibility is on; see [Authentication](authentication.md#dynamic-component-visibility) |
| `features.multi_auth`, `features.propelauth`, `features.keycloak`, `features.oauth_proxy` | disabled | Auth providers; see [Authentication](authentication.md#auth-providers-in-fastmcpjson) |
| `features.apps.generative_ui` | `false` | With `--enable-apps`, adds FastMCP's `GenerativeUI` provider |

### Informational keys

These keys describe choices made at generation time. The server does not read them, and
changing them has no effect:

| Key | Generated behavior |
|---|---|
| `composition.strategy`, `composition.resource_prefix_format` | Sub-servers are always mounted with a namespace |
| `features.tool_tags` | Every tool is tagged with its module's tag |
| `features.tool_timeouts` | Every tool has a 30 second timeout |
| `features.component_versioning` | Deprecated operations get `version="deprecated"` |
| `features.validate_output` | Tools keep FastMCP's default output validation |
| `features.apps.enabled`, `features.apps.display_tools` | Display tools exist when generated with `--enable-apps` |

## Environment variables

### Generated server

| Variable | Used by | Purpose |
|---|---|---|
| `API_TOKEN` | Server, STDIO mode | Token sent to the backend API |
| `API_BASE_URL` | Server | Overrides the backend URL taken from the spec |
| `OTEL_EXPORTER_OTLP_ENDPOINT` | Server | OTLP endpoint for traces; console output when unset |
| `MCP_RESOURCE_URL` | `create_remote_auth_provider()` | Resource URL for RFC 8707 audience binding |
| `MCP_SERVER_URL` | Generated tests | Server URL the tests call (default `http://localhost:8000/mcp`) |
| `MCP_SERVER_PORT` | `test/run_tests.py` | Port the runner starts the server on (default `8000`) |
| `A2A_HOST`, `A2A_PORT` | `a2a_adapter.py` | Bind address of the A2A adapter |

### Generator tools

| Variable | Used by | Purpose |
|---|---|---|
| `MCP_REGISTRY_PATH` | `register-mcp`, `run-mcp` | Registry file location |
| `XDG_DATA_HOME` | `register-mcp`, `run-mcp` | Registry under `$XDG_DATA_HOME/mcp-generator/` when `MCP_REGISTRY_PATH` is unset |

## Generator settings in config.py

In a source checkout, `mcp_generator/config.py` holds settings that have no CLI flag:

| Setting | Default | Purpose |
|---|---|---|
| `TOOL_NAME_OVERRIDES` | `{}` | Map of client method name (snake case operation ID) to tool name |
| `MAX_TOOL_NAME_LENGTH` | `64` | Length above which abbreviations apply |
| `TOOL_NAME_ABBREVIATIONS` | `{}` | Word replacements applied to names longer than `MAX_TOOL_NAME_LENGTH` |
| `DEFAULT_SCHEMA_DEPTH` | `3` | Default for `--schema-depth` |
| `DEFAULT_FASTMCP_TARGET` | `4` | Default for `--fastmcp-target` |
| `DEFAULT_FALLBACK_SCOPES` | `[]` | Scopes used when the spec's global `security` lists none |

Example:

```python
TOOL_NAME_ABBREVIATIONS = {"healthcare": "hc", "organization": "org"}
TOOL_NAME_OVERRIDES = {"create_smart_app_registration": "register_smart_app"}
```
