# Middleware

`main()` in the generated server adds FastMCP middleware in this order:

| Order | Middleware | Added when |
|---|---|---|
| 1 | `ErrorHandlingMiddleware(include_traceback=True)` | Always |
| 2 | `ApiClientContextMiddleware` | Always |
| 3 | `DetailedTimingMiddleware` | Always |
| 4 | `LoggingMiddleware(include_payloads=False)` | Always |
| 5 | `ResponseLimitingMiddleware(max_size=...)` | `features.response_limiting.enabled` (default `true`) |
| 6 | `PingMiddleware` | `features.ping_middleware.enabled` (default `true`) |
| 7 | `RateLimitingMiddleware(...)` | `features.rate_limiting.enabled` (default `false`) |

The `features.*` keys live in `generated_mcp/fastmcp.json`; see
[Configuration](configuration.md).

## What each one does

- **Error handling** converts exceptions raised by tools into MCP errors that include the
  traceback.
- **ApiClientContextMiddleware** builds the backend API client for `tools/call` and
  `resources/read` and stores it in the request context. It passes every other MCP method
  through unchanged. See [Authentication](authentication.md#backend-credentials).
- **Timing** records the duration of each request.
- **Logging** logs requests and responses without payloads.
- **Response limiting** truncates tool responses larger than
  `features.response_limiting.max_size_bytes` (default 1,048,576 bytes) at a UTF-8 boundary.
- **Ping** sends keepalive pings on long-lived HTTP connections.
- **Rate limiting** applies a token bucket with `max_requests_per_second` (default 10),
  `burst_capacity` (default 20) and `global_limit` (default `false`, which limits per
  client).

JWT validation runs earlier, as ASGI middleware on the HTTP app, when the server starts with
`--validate-tokens`.

## OpenTelemetry

With `features.opentelemetry.enabled`, the server installs an OpenTelemetry tracer provider
named after `features.opentelemetry.service_name`. Spans go to the console unless
`OTEL_EXPORTER_OTLP_ENDPOINT` is set, in which case they go to that OTLP gRPC endpoint.

The OpenTelemetry packages are an optional dependency group of the generated package:

```bash
pip install -e "./generated_mcp[telemetry]"
export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317
python generated_mcp/<title>_mcp_generated.py --transport http
```

If the packages are missing, the server logs a warning and starts without tracing.

## Adding middleware

The generated files are regular Python. Add middleware in `main()` of the main module, or
extend `ApiClientContextMiddleware` in `middleware/authentication.py`. Regenerating overwrites
both files, so keep a patch or a wrapper module if you regenerate often.
