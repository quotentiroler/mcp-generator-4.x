# Quick start

This page takes an OpenAPI spec to a running MCP server connected to a client. It uses the
public Swagger Petstore spec; replace it with your own.

## 1. Generate

Run the generator in an empty working directory:

=== "From a URL"

    ```bash
    generate-mcp --url https://petstore3.swagger.io/api/v3/openapi.json
    ```

=== "From a file"

    ```bash
    # Reads ./openapi.json when --file is omitted
    generate-mcp --file ./my-api.yaml
    ```

The generator writes everything relative to the current directory:

| Path | Contents |
|---|---|
| `generated_openapi/` | Python API client and the resolved spec (`openapi.json`) |
| `generated_mcp/` | The MCP server package |
| `test/generated/` | Generated pytest suite |
| `test/run_tests.py` | Starts the server over HTTP and runs the suite |

`generated_mcp/` imports the client from `../generated_openapi`, so keep both directories side
by side. [Architecture](../guide/architecture.md) describes the files inside `generated_mcp/`,
and [Optional features](../guide/features.md) lists the flags that add more.

## 2. Install the server's dependencies

```bash
pip install -e ./generated_mcp
```

## 3. Run

The main module is named after the API title: `<title>_mcp_generated.py`.

=== "STDIO"

    ```bash
    export API_TOKEN="your-backend-token"   # PowerShell: $env:API_TOKEN = "..."
    python generated_mcp/swagger_petstore_openapi_mcp_generated.py
    ```

=== "HTTP"

    ```bash
    python generated_mcp/swagger_petstore_openapi_mcp_generated.py --transport http --port 8000
    ```

    The MCP endpoint is `http://localhost:8000/mcp` (Streamable HTTP).

Start the server through its own `main()` as shown, or through `run-mcp` (step 4). Loading
`create_server` with the FastMCP CLI (`fastmcp run file.py:create_server`) registers the tools
but skips the middleware that `main()` adds, so tool calls fail with "API client not
available".

In STDIO mode the server sends `API_TOKEN` to the backend API. In HTTP mode it forwards the
`Authorization: Bearer` header of each MCP request. See
[Authentication](../guide/authentication.md).

## 4. Register (optional)

`register-mcp` records the server in a local registry so that `run-mcp` can start it by name:

```bash
register-mcp ./generated_mcp
run-mcp --list
run-mcp swagger_petstore_openapi --mode http --port 8000
```

The registry name comes from the `[project.entry-points."mcp_servers"]` table in
`generated_mcp/pyproject.toml`. See the [CLI reference](../guide/cli.md#register-mcp).

## 5. Connect a client

For a client that launches servers over STDIO, such as Claude Desktop, add an entry to its MCP
configuration file:

```json
{
  "mcpServers": {
    "petstore": {
      "command": "python",
      "args": ["/absolute/path/to/generated_mcp/swagger_petstore_openapi_mcp_generated.py"],
      "env": {
        "API_TOKEN": "your-backend-token"
      }
    }
  }
}
```

Use the Python interpreter of the environment where you installed the server's dependencies.
Clients that speak Streamable HTTP connect to `http://localhost:8000/mcp` instead.

## 6. Test

From the directory where you ran `generate-mcp`:

```bash
python test/run_tests.py
```

See [Testing](../guide/testing.md) for the MCP Inspector and the generated test suite.
