# Examples

The [`examples/`](https://github.com/quotentiroler/mcp-generator-4.x/tree/main/examples)
directory holds input specs only. CI regenerates a server from each one and runs its test suite
(`.github/workflows/test-examples.yml`).

| Directory | Spec version | Paths | Notes |
|---|---|---|---|
| `minimal` | OpenAPI 3.0.0 | 2 | Smallest working input |
| `petstore-openapi-3-0-4` | OpenAPI 3.0.4 | 13 | Swagger Petstore with OAuth2 (implicit flow) and API key |
| `petstore-openapi-3-1-0` | OpenAPI 3.1.0 | 2 | OpenAPI 3.1 input |
| `petstore-swagger-2-0` | Swagger 2.0 | 14 | Swagger 2.0 input |
| `proxy-smart` | OpenAPI 3.0.3 | 139 | Proxy Smart backend API, a larger spec |

## Generate and test an example

```bash
cd examples/petstore-openapi-3-0-4
generate-mcp --enable-storage --enable-caching --enable-resources
python test/run_tests.py
```

`generate-mcp` reads `openapi.json` from the current directory and writes
`generated_openapi/`, `generated_mcp/` and `test/` next to it. These outputs are ignored by
git.

To regenerate and test every example from the repository root:

```bash
uv run python scripts/test_examples.py
# Only examples whose directory name contains the given text
uv run python scripts/test_examples.py --example swagger-2-0
```

## Output for the Petstore example

```text
generated_mcp/
├── swagger_petstore_openapi_mcp_generated.py   main server, mounts the sub-servers
├── servers/
│   ├── pet_server.py                            8 tools
│   ├── store_server.py                          4 tools
│   └── user_server.py                           7 tools
├── middleware/
│   ├── authentication.py
│   ├── oauth_provider.py
│   └── event_store.py
├── fastmcp.json
├── pyproject.toml
├── README.md
├── Dockerfile
└── docker-compose.yml
```

Tool names carry the sub-server namespace, for example `Pet_add_pet` and
`Store_place_order`.
