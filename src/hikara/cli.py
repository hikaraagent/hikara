"""hikara command-line interface.

four command groups:
  scan        run live scanner against configured rpc / geyser.
  investigate dive into a single signature or slot.
  demo        scripted offline demos.
  version     print version + build info.
"""

from __future__ import annotations

import typer
from rich.console import Console

from hikara import __version__
from hikara.config import load
from hikara.demo.investigate import run_demo_investigate
from hikara.demo.replay import run_demo_replay
from hikara.demo.scan import run_demo_scan

app = typer.Typer(
    name="hikara",
    add_completion=False,
    help="solana mev forensics agent. read-only by design.",
    no_args_is_help=True,
)

demo_app = typer.Typer(
    name="demo", help="scripted offline demos. zero network.", no_args_is_help=True
)
app.add_typer(demo_app, name="demo")


def _version_callback(value: bool) -> None:
    if value:
        Console().print(f"hikara {__version__}")
        raise typer.Exit()


@app.callback()
def _main(
    version: bool = typer.Option(
        None,
        "--version",
        "-V",
        callback=_version_callback,
        is_eager=True,
        help="print version and exit.",
    ),
) -> None:
    """solana mev forensics agent. read-only by design."""
    _ = version


@app.command()
def version() -> None:
    """print version + build info."""
    console = Console()
    settings = load()
    console.print(f"hikara {__version__}")
    console.print(f"  trace_mode: {settings.trace_mode}")
    console.print(f"  rpc:        {'set' if settings.has_rpc else 'unset'}")
    console.print(f"  stream:     {'set' if settings.has_stream else 'unset'}")
    console.print(f"  ai:         {'set' if settings.has_ai else 'unset'}")
    console.print(f"  sink:       {settings.sink}")


@app.command()
def scan(
    once: bool = typer.Option(
        False, "--once", help="exit after first slot (smoke test)."
    ),
) -> None:
    """run the live scanner. requires HIKARA_RPC_HTTP_URL or a stream endpoint."""
    settings = load()
    console = Console()
    if not settings.has_rpc and not settings.has_stream:
        console.print(
            "[yellow]no rpc or stream configured. set HIKARA_RPC_HTTP_URL "
            "or HIKARA_GEYSER_GRPC_URL.[/yellow]"
        )
        console.print("falling back to demo scan.")
        run_demo_scan()
        return
    console.print("[yellow]live scan stub. ingest-rs wiring lands in a future minor.[/yellow]")
    target = settings.geyser_grpc_url or settings.rpc_http_url or settings.rpc_ws_url
    console.print(f"would connect to: {target}")
    console.print(f"once={once}")


@app.command()
def investigate(
    target: str = typer.Argument(..., help="signature or slot number."),
) -> None:
    """investigate a signature or slot number."""
    settings = load()
    console = Console()
    if not settings.has_rpc:
        console.print(
            f"[yellow]no rpc. running offline demo for target={target}.[/yellow]"
        )
        run_demo_investigate()
        return
    console.print(f"[yellow]investigate stub. target={target}.[/yellow]")


@demo_app.command("scan")
def demo_scan() -> None:
    """canned scan of a synthetic slot. emits to stdout."""
    run_demo_scan()


@demo_app.command("investigate")
def demo_investigate() -> None:
    """walk the full pipeline on a synthetic sandwich slot."""
    run_demo_investigate()


@demo_app.command("replay")
def demo_replay(
    slot_id: str = typer.Argument(..., help="fixture slot id."),
) -> None:
    """replay a recorded slot fixture."""
    run_demo_replay(slot_id)


if __name__ == "__main__":
    app()
