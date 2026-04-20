"""hakiri command-line interface."""

from __future__ import annotations

import typer
from rich.console import Console

from hakiri import __version__

app = typer.Typer(
    name="hakiri",
    add_completion=False,
    help="ethereum mev forensics agent. read-only by design.",
    no_args_is_help=True,
)


@app.command()
def version() -> None:
    """print version + build info."""
    Console().print(f"hakiri {__version__}")


if __name__ == "__main__":
    app()
