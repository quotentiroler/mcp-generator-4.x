"""Central generator settings: tool naming, defaults and project identity."""

from pathlib import Path

TEMPLATES_DIR = Path(__file__).parent / "templates"

# Applied only to names longer than MAX_TOOL_NAME_LENGTH.
TOOL_NAME_ABBREVIATIONS: dict[str, str] = {}

# Client method name (snake case operation ID) -> tool name.
TOOL_NAME_OVERRIDES: dict[str, str] = {}

MAX_TOOL_NAME_LENGTH = 64

DEFAULT_SCHEMA_DEPTH = 3

# Version matrix lives in fastmcp_target.py.
DEFAULT_FASTMCP_TARGET = 4

PROJECT_REPO_URL = "https://github.com/quotentiroler/mcp-generator-4.x"
PROJECT_ISSUES_URL = f"{PROJECT_REPO_URL}/issues"
PROJECT_DOCS_URL = "https://quotentiroler.github.io/mcp-generator-4.x/"

# Endpoint the generated test suite targets unless MCP_SERVER_URL overrides it.
DEFAULT_GENERATED_MCP_URL = "http://localhost:8000/mcp"

# Handlers that read the API client from state; the auth middleware skips other methods.
CLIENT_REQUIRED_MCP_METHODS: tuple[str, ...] = (
    "tools/call",
    "resources/read",
)

# Scopes used when the spec declares no global security requirement.
DEFAULT_FALLBACK_SCOPES: list[str] = []
