"""CLI entry point for the generated project."""

import asyncio

import typer

from harness_agent.agent import chat_loop

app = typer.Typer()


@app.command()
def hello(name: str = typer.Argument("World")) -> None:
    """Print a greeting message."""
    typer.echo(f"Hello, {name}!")


@app.command()
def chat(session_id: str = typer.Argument("default")) -> None:
    """Start interactive chat with Architect agent."""
    typer.echo(f"Starting chat session: {session_id}")
    asyncio.run(chat_loop(session_id))


def version_callback(value: bool) -> None:
    """Print version and exit."""
    if value:
        typer.echo("harness_agent 0.1.0")
        raise typer.Exit()


@app.callback()
def main(
    version: bool = typer.Option(
        False,
        "--version",
        "-v",
        help="Show version and exit.",
        is_eager=True,
        callback=version_callback,
    ),
) -> None:
    """harness-agent CLI."""


def cli() -> None:
    """Entry point for setuptools console script."""
    app()


if __name__ == "__main__":
    cli()
