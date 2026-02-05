"""CLI for running the Trello MCP server."""

import click


@click.group()
def cli():
    """Trello MCP Server CLI."""


@cli.command()
@click.option("--transport", default="stdio", type=click.Choice(["stdio", "sse"]))
@click.option("--port", default=8000, type=int, help="Port for SSE transport")
def run(transport: str, port: int):
    """Start the Trello MCP server."""
    from trello_mcp.server import mcp

    if transport == "sse":
        mcp.run(transport="sse", port=port)
    else:
        mcp.run(transport="stdio")


if __name__ == "__main__":
    cli()
