# CLI reference

The package installs three commands. The help text on this page is rendered from the
commands' argument parsers each time the documentation is built.

## generate-mcp

Generates a server from a spec. All output goes to the current working directory; see
[Architecture](architecture.md#generated-layout) for the layout.

<!-- cli-help: generate-mcp -->

Notes:

- `--url` saves the download as `openapi.json`, or `openapi.yaml` when the URL ends in
  `.yaml` or `.yml`, in the current directory.
- `--enable-caching` has no effect without `--enable-storage`, and `--generate-ui` has no
  effect without `--enable-apps`. The generator prints a warning and skips them.
- `--overlay fhir` applies the overlay bundled in `mcp_generator/overlays/fhir.overlay.yaml`.
- After a run, the generator prints the optional flags that were not used, with a command to
  regenerate with them.

The flags are described in [Optional features](features.md).

## register-mcp

Keeps a local registry of generated servers for `run-mcp`. A path given without a subcommand
is treated as `add`, so `register-mcp ./generated_mcp` and `register-mcp add ./generated_mcp`
are equivalent.

<!-- cli-help: register-mcp -->

`add` reads the server name and entry point from the
`[project.entry-points."mcp_servers"]` table of the server's `pyproject.toml`. `export` writes
a `server.json` draft for a registered server. Its publisher, source URL, homepage and license
fields are `TODO` placeholders to fill in before publishing to an MCP registry.

### Registry location

The first match wins:

1. `MCP_REGISTRY_PATH`, a full path to the registry file
2. `$XDG_DATA_HOME/mcp-generator/servers.json`
3. `~/.mcp-generator/servers.json`

## run-mcp

Starts a registered server by name.

<!-- cli-help: run-mcp -->

`run-mcp` imports the server's entry point and calls it with `--transport`. In HTTP mode it
also passes `--host`, `--port` and, when set, `--validate-tokens`. Only servers generated from
a spec with security schemes accept `--validate-tokens`.

## Generated server

The main module of a generated server has its own command line:

```bash
python generated_mcp/<title>_mcp_generated.py [--transport {stdio,http}] [--host HOST] [--port PORT] [--validate-tokens]
```

| Option | Default | Description |
|---|---|---|
| `--transport` | `stdio` | `stdio` or `http` (Streamable HTTP at `/mcp`) |
| `--host` | `0.0.0.0` | Bind address for HTTP |
| `--port` | `8000` | Port for HTTP |
| `--validate-tokens` | `middleware.config.authentication.validate_tokens` in `fastmcp.json` | Validate JWTs on HTTP requests. Present only when the spec declares security schemes. |

## Helper scripts

These modules ship with the package and run with `python -m`:

| Command | Purpose |
|---|---|
| `python -m mcp_generator.scripts.validate_openapi [--spec PATH] [--strict]` | Checks a JSON spec for problems that affect generation |
| `python -m mcp_generator.scripts.generate_jwt_keypair` | Writes an RSA key pair and a JWKS file to a `keys/` directory inside the installed `mcp_generator` package, for local JWT testing |
