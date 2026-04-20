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


@app.command()
def scan(once: bool = typer.Option(False, "--once")) -> None:
    """run the live scanner."""
    Console().print("scan stub")


@app.command()
def investigate(target: str = typer.Argument(...)) -> None:
    """investigate a tx hash or block number."""
    Console().print(f"investigate stub: {target}")


if __name__ == "__main__":
    app()
