"""MkDocs hooks: render each CLI's --help output into the docs at build time."""

import argparse
import functools
import re
from collections.abc import Callable

from mcp_generator.cli.args import build_parser as build_generate_parser
from mcp_generator.register_mcp import build_parser as build_register_parser
from mcp_generator.run_mcp import build_parser as build_run_parser

PARSERS: dict[str, Callable[[], argparse.ArgumentParser]] = {
    "generate-mcp": build_generate_parser,
    "register-mcp": build_register_parser,
    "run-mcp": build_run_parser,
}

HELP_PLACEHOLDER = re.compile(r"<!--\s*cli-help:\s*([\w-]+)\s*-->")
HELP_WIDTH = 88


def _format_help(parser: argparse.ArgumentParser) -> str:
    parser.formatter_class = functools.partial(
        argparse.RawDescriptionHelpFormatter, width=HELP_WIDTH
    )
    return parser.format_help().rstrip()


def _subcommand_parsers(parser: argparse.ArgumentParser) -> list[argparse.ArgumentParser]:
    return [
        subparser
        for action in parser._actions
        if isinstance(action, argparse._SubParsersAction)
        for subparser in action.choices.values()
    ]


def render_cli_help(command: str) -> str:
    """Return the help text of ``command`` and its subcommands as fenced blocks."""
    parser = PARSERS[command]()
    sections = [parser, *_subcommand_parsers(parser)]
    return "\n\n".join(f"```text\n{_format_help(section)}\n```" for section in sections)


def on_page_markdown(markdown: str, **_: object) -> str:
    return HELP_PLACEHOLDER.sub(lambda match: render_cli_help(match.group(1)), markdown)
