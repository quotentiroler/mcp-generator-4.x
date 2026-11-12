"""
Global run-mcp CLI command.

This is a dispatcher that can run any registered MCP server by name.
Servers are registered via the local registry file at ~/.mcp-generator/servers.json
Use 'register-mcp' to add servers to the registry.
"""

import argparse
import sys
from pathlib import Path

from .register_mcp import get_registry_path, load_registry


def build_parser() -> argparse.ArgumentParser:
    """Build the run-mcp argument parser."""
    parser = argparse.ArgumentParser(
        prog="run-mcp",
        description="Run a registered MCP server",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "server_name",
        nargs="?",
        help="Name of the MCP server to run (use --list to see available servers)",
    )
    parser.add_argument("--list", action="store_true", help="List all registered MCP servers")
    parser.add_argument(
        "--mode",
        "--transport",
        dest="transport",
        choices=["stdio", "http"],
        default="stdio",
        help="Transport protocol to use (default: stdio)",
    )
    parser.add_argument(
        "--host", default="0.0.0.0", help="Host to bind to for HTTP transport (default: 0.0.0.0)"
    )
    parser.add_argument(
        "--port", type=int, default=8000, help="Port to bind to for HTTP transport (default: 8000)"
    )
    parser.add_argument(
        "--validate-tokens",
        action="store_true",
        help="Enable JWT token validation for HTTP transport",
    )
    return parser


def main() -> int:
    """Main entry point for run-mcp CLI."""
    parser = build_parser()
    args = parser.parse_args()

    servers = load_registry(create_dirs=False)

    # Handle --list flag
    if args.list:
        if not servers:
            print("No MCP servers registered.")
            print(f"\nRegistry location: {get_registry_path(create_dirs=False)}")
            print("\nTo register a server:")
            print("  register-mcp /path/to/server")
            return 0

        print("Registered MCP Servers:")
        print("=" * 70)
        for name, info in sorted(servers.items()):
            print(f"\n  • {name}")
            print(f"    Path: {info['path']}")
            print(f"    Entry point: {info['entry_point']}")
            if info.get("description"):
                print(f"    Description: {info['description']}")
        print(f"\n{'=' * 70}")
        print(f"Registry location: {get_registry_path(create_dirs=False)}")
        print("\nUsage: run-mcp <server_name> [options]")
        return 0

    # Require server name if not listing
    if not args.server_name:
        parser.error("server_name is required (use --list to see available servers)")

    # Check if server exists
    if args.server_name not in servers:
        print(f"❌ Error: Server '{args.server_name}' not found.")
        print("\nAvailable servers:")
        if servers:
            for name in sorted(servers.keys()):
                print(f"  • {name}")
        else:
            print("  (none registered)")
        print("\nUsage: run-mcp <server_name> [options]")
        print("       run-mcp --list")
        print("       register-mcp /path/to/server")
        return 1

    # Load and run the server
    try:
        print(f"🚀 Loading MCP server: {args.server_name}")
        info = servers[args.server_name]
        server_path = Path(info["path"])
        entry_point = info["entry_point"]  # e.g. "module_name:main"

        # Add server path to sys.path
        if str(server_path) not in sys.path:
            sys.path.insert(0, str(server_path))

        # Import and get the main function
        module_name, func_name = entry_point.split(":")
        module = __import__(module_name)
        server_main = getattr(module, func_name)

        # Set up sys.argv for the server's argument parser
        sys.argv = ["run-mcp", "--transport", args.transport]

        if args.transport == "http":
            sys.argv.extend(["--host", args.host, "--port", str(args.port)])
            if args.validate_tokens:
                sys.argv.append("--validate-tokens")

        # Run the server's main function
        server_main()
        return 0

    except Exception as e:
        print(f"❌ Error loading/running server '{args.server_name}': {e}")
        import traceback

        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
