"""Command-line argument definitions."""

import argparse

from ..config import DEFAULT_FASTMCP_TARGET, DEFAULT_SCHEMA_DEPTH, PROJECT_DOCS_URL
from ..fastmcp_target import SUPPORTED_TARGETS


def build_parser() -> argparse.ArgumentParser:
    """Build the generate-mcp argument parser."""
    parser = argparse.ArgumentParser(
        prog="generate-mcp",
        description="Generate a FastMCP server from an OpenAPI or Swagger specification.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
Examples:
  # Basic generation (minimal server)
  generate-mcp

  # With custom OpenAPI file
  generate-mcp --file ./my-api-spec.yaml

  # Download from URL
  generate-mcp --url https://petstore3.swagger.io/api/v3/openapi.json

  # With optional features
  generate-mcp --enable-storage --enable-caching
  generate-mcp --enable-resources
  generate-mcp --enable-apps
  generate-mcp --enable-apps --generate-ui

  # Enrich descriptions with an overlay or auto-enhance
  generate-mcp --overlay ./my-overlay.yaml
  generate-mcp --overlay fhir --schema-depth 5
  generate-mcp --auto-overlay

  # Generate A2A agent adapter
  generate-mcp --enable-a2a

Documentation: {PROJECT_DOCS_URL}
        """,
    )

    parser.add_argument(
        "--file",
        type=str,
        default="./openapi.json",
        help="Path to OpenAPI specification file (default: ./openapi.json)",
    )

    parser.add_argument(
        "--url",
        type=str,
        default=None,
        help="URL to download OpenAPI specification from (overrides --file)",
    )

    parser.add_argument(
        "--enable-storage",
        action="store_true",
        default=False,
        help="Enable persistent storage backend (for OAuth tokens, session state, user data)",
    )

    parser.add_argument(
        "--enable-caching",
        action="store_true",
        default=False,
        help="Generate cache.py, a TTL cache decorator for tool functions (requires --enable-storage)",
    )

    parser.add_argument(
        "--enable-resources",
        action="store_true",
        default=False,
        help="Generate MCP resource templates from GET endpoints (exposes API data as resources)",
    )

    parser.add_argument(
        "--enable-apps",
        action="store_true",
        default=False,
        help="Generate MCP Apps display tools (interactive tables, charts, forms) and optional GenerativeUI",
    )

    parser.add_argument(
        "--generate-ui",
        action="store_true",
        default=False,
        help="Generate API-specific display tools from OpenAPI response schemas (requires --enable-apps)",
    )

    parser.add_argument(
        "--schema-depth",
        type=int,
        default=DEFAULT_SCHEMA_DEPTH,
        help=(
            "Max nesting depth for response schema parsing used by --generate-ui "
            f"(default: {DEFAULT_SCHEMA_DEPTH}, increase for deeply nested APIs)"
        ),
    )

    parser.add_argument(
        "--overlay",
        type=str,
        default=None,
        help="Overlay name or path. Bundled: 'fhir'. Or a path to an Overlay 1.0.0 file",
    )

    parser.add_argument(
        "--auto-overlay",
        action="store_true",
        default=False,
        help="Auto-generate a rule-based overlay to enhance API descriptions for AI agents",
    )

    parser.add_argument(
        "--enable-a2a",
        action="store_true",
        default=False,
        help="Generate A2A (Agent-to-Agent) adapter and AgentCard for multi-agent orchestration",
    )

    parser.add_argument(
        "--fastmcp-target",
        type=int,
        choices=SUPPORTED_TARGETS,
        default=DEFAULT_FASTMCP_TARGET,
        help=(
            "FastMCP major version the generated server targets "
            f"(default: {DEFAULT_FASTMCP_TARGET}). Target 4 drops server-side sampling "
            "and reports missing parameters back to the caller instead of eliciting them"
        ),
    )

    return parser
