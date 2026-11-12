# Contributing to MCP Generator 4.x

Bug reports, feature requests, documentation fixes and code changes are welcome. Open an
[issue](https://github.com/quotentiroler/mcp-generator-4.x/issues) first for larger changes so
the approach can be discussed before you start.

## Development setup

Requirements: Python 3.11 or later, [uv](https://docs.astral.sh/uv/) and Git.

```bash
git clone https://github.com/YOUR_USERNAME/mcp-generator-4.x.git
cd mcp-generator-4.x
git remote add upstream https://github.com/quotentiroler/mcp-generator-4.x.git

uv sync --group dev                    # add --group docs to build the documentation
git config core.hooksPath .githooks    # optional: ruff format and ruff check on commit
```

On Linux and macOS, make the hook executable with `chmod +x .githooks/pre-commit`.

## Branches and releases

| Branch | Role |
|---|---|
| `dev/<topic>` | Feature and fix branches, created from `develop` |
| `develop` | Integration branch |
| `test` | Beta channel: merging into it publishes a pre-release |
| `main` | Stable channel: merging into it publishes a release |

A push to a `dev/**` branch opens a pull request into `develop`. Changes then move
`develop` to `test` to `main` through promotion pull requests that the workflows open. Open
your own pull requests against `develop`, never against `test` or `main`.

```bash
git fetch upstream
git checkout -b dev/my-change upstream/develop
# edit, test, commit
git push origin dev/my-change
```

## Checks

CI (`.github/workflows/tests.yml`) runs these on Ubuntu and Windows with Python 3.11 and 3.12.
Run them before pushing:

```bash
uv run ruff check .
uv run ruff format --check .
uv run mypy mcp_generator/
uv run pytest test/ --ignore=test/generated
```

`.github/workflows/test-examples.yml` regenerates every spec in `examples/` and runs the
generated test suites. To do the same locally:

```bash
uv run python scripts/test_examples.py
```

When you change the documentation, build it with strict checking:

```bash
uv sync --group docs
uv run mkdocs build --strict
```

The CLI reference renders each command's `--help` output at build time
(`scripts/mkdocs_hooks.py`), so option changes in the argument parsers show up there without
editing the page.

## Code style

- Ruff formatting and linting with a line length of 100
- Type hints on all functions; `mypy mcp_generator/` must pass
- Docstrings on public functions
- Tests for new behavior in `test/`

## Commit messages

Use [Conventional Commits](https://www.conventionalcommits.org/): `feat:`, `fix:`, `docs:`,
`test:`, `refactor:`, `ci:` or `chore:`, followed by a short summary. The changelog is built
from these messages.

## Pull requests

- Keep each pull request to one change.
- Describe what changed and why, and link the related issue.
- Update the documentation in `docs/` when behavior or options change.
- Make sure the checks above pass.

## Reporting bugs

Include:

- The OpenAPI spec, reduced to a minimal example and stripped of private data
- The full command and its output, including any stack trace
- Expected and actual behavior
- Operating system, Python version and `mcp-generator` version

The issue templates in `.github/ISSUE_TEMPLATE/` list the same fields.

## Code of conduct

This project follows the [Code of Conduct](CODE_OF_CONDUCT.md).

## License

By contributing, you agree that your contributions are licensed under the
[Apache License 2.0](LICENSE).
