# Examples

Each directory holds an `openapi.json` input spec. CI regenerates a server from every
directory and runs its test suite.

| Directory | Spec version |
|---|---|
| `minimal` | OpenAPI 3.0.0 |
| `petstore-openapi-3-0-4` | OpenAPI 3.0.4 |
| `petstore-openapi-3-1-0` | OpenAPI 3.1.0 |
| `petstore-swagger-2-0` | Swagger 2.0 |
| `proxy-smart` | OpenAPI 3.0.3 |

```bash
cd examples/petstore-openapi-3-0-4
generate-mcp
python test/run_tests.py
```

See [Examples](https://quotentiroler.github.io/mcp-generator-4.x/getting-started/examples/) in
the documentation for the generated layout and the script that tests all examples.

To add an example, create a directory with an `openapi.json`. CI picks up every directory that
contains one.
