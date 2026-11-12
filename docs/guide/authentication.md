# Authentication

A generated server handles two separate concerns:

- **Backend credentials**: the token the server sends to the REST API it wraps.
- **Client authentication**: optional validation of the token an MCP client presents to the
  server over HTTP.

## Backend credentials

`ApiClientContextMiddleware` (in `middleware/authentication.py`) attaches an API client to
every `tools/call` and `resources/read` request. The token on that client depends on the
transport:

| Transport | Token sent to the backend |
|---|---|
| STDIO | The `API_TOKEN` environment variable |
| HTTP | The `Authorization: Bearer <token>` header of the incoming MCP request |

The backend base URL is the first server URL in the spec. Set `API_BASE_URL` to override it at
runtime.

```bash
export API_TOKEN="your-backend-token"
export API_BASE_URL="https://staging.example.com/api/v3"   # optional
python generated_mcp/<title>_mcp_generated.py
```

## JWT validation over HTTP

Servers generated from a spec that declares security schemes accept `--validate-tokens`. With
it, the HTTP app validates the bearer token before a request reaches MCP:

```bash
python generated_mcp/<title>_mcp_generated.py --transport http --validate-tokens
```

To make validation the default, set it in `fastmcp.json`:

```json
{
  "middleware": {
    "config": {
      "authentication": {
        "validate_tokens": true
      }
    }
  }
}
```

The verifier is FastMCP's `JWTVerifier`. It checks the signature against the JWKS, the
issuer, the audience and the expiry, and answers invalid tokens with HTTP 401. In STDIO mode
the flag is ignored with a warning.

The JWKS URI, issuer and audience are fixed at generation time. They come from top-level
extensions in the spec, with these fallbacks:

| Setting | Spec extension | Fallback |
|---|---|---|
| JWKS URI | `x-jwks-uri` | `<backend URL>/.well-known/jwks.json` |
| Issuer | `x-issuer` | `<backend URL>` |
| Audience | `x-audience` | `backend-api` |

To change them, edit the spec and regenerate, or edit `create_jwt_verifier()` in
`middleware/oauth_provider.py`.

The default verifier requires no scopes. `middleware/oauth_provider.py` also contains
`RequireScopesMiddleware`, an ASGI middleware that answers 403 when a required scope is
missing, for servers that need scope enforcement at the HTTP layer.

## OAuth2 metadata from the spec

For each `oauth2` security scheme, the generator reads the `authorizationCode`, `implicit`,
`password` and `clientCredentials` flows with their URLs and scopes. Scopes listed in the
spec's global `security` requirement become the server's default scopes. This information is
written as comments into `middleware/authentication.py` and drives the generated auth tests.

## Auth providers in `fastmcp.json`

With `--validate-tokens`, the server builds its verifier from the first enabled entry in this
order. If none is enabled, it uses the single `JWTVerifier` described above.

| Key | Effect | Settings |
|---|---|---|
| `features.propelauth` | FastMCP PropelAuth provider | `auth_url`, `introspection_client_id`, `introspection_client_secret`, `base_url`, `required_scopes` |
| `features.keycloak` | FastMCP Keycloak provider with dynamic client registration | `realm_url`, `required_scopes`, `audience` |
| `features.multi_auth` | FastMCP `MultiAuth`: the default verifier plus one `JWTVerifier` per entry in `providers` | each provider: `jwks_uri`, `issuer`, `audience`, `required_scopes` |

`features.oauth_proxy` is applied independently. When enabled, the HTTP app uses FastMCP's
`OAuthProxy` as its auth provider, which bridges identity providers without dynamic client
registration. Its settings are `upstream_authorization_endpoint`, `upstream_token_endpoint`,
`upstream_client_id`, `upstream_client_secret`, `upstream_revocation_endpoint`, `base_url`,
`redirect_path`, `valid_scopes` and `forward_pkce`.

Example with two token issuers:

```json
{
  "features": {
    "multi_auth": {
      "enabled": true,
      "providers": [
        {
          "jwks_uri": "https://partner.example.com/.well-known/jwks.json",
          "issuer": "https://partner.example.com",
          "audience": "petstore-mcp",
          "required_scopes": []
        }
      ]
    }
  }
}
```

## Dynamic component visibility

`features.dynamic_visibility.enabled` logs that per-session visibility is on. The hook point is
in `ApiClientContextMiddleware.on_request`, after a token has been validated: the generated
code reads the token's scopes and leaves the policy to you. Call
`await ctx.enable_components(...)` or `await ctx.disable_components(...)` there to show or hide
tools per session.

## Token persistence

With `--enable-storage`, `middleware/oauth_provider.py` can persist OAuth tokens through
`OAuthTokenManager` and the generated `storage.py`. See
[Optional features](features.md#storage-and-caching).
