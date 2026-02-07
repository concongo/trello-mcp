# Trello MCP Server

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![CI](https://github.com/concongo/trello-mcp/actions/workflows/ci.yml/badge.svg)](https://github.com/concongo/trello-mcp/actions/workflows/ci.yml)

An [MCP](https://modelcontextprotocol.io/) server that exposes Trello board, list, and card operations as tools — so AI assistants like Claude can manage your Trello boards directly.

Built with [FastMCP](https://github.com/jlowin/fastmcp), [httpx](https://www.python-httpx.org/), and [Pydantic](https://docs.pydantic.dev/).

## Features

- List, create, update, move, and archive Trello cards
- Browse boards and lists
- Search boards by name
- Add comments to cards
- Bundled Trello API documentation as MCP resources
- Supports **stdio** and **SSE** transports
- Docker ready

## Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) package manager
- A Trello account with API credentials

### Getting Trello API Credentials

1. Go to https://trello.com/power-ups/admin and log in
2. Create a new Power-Up (or use an existing one)
3. Copy your **API Key** from the Power-Up settings
4. Generate a **Token** by clicking the token link on the same page and authorizing access

## Setup

```bash
uv sync --extra dev
cp .env.example .env  # Fill in your Trello API key and token
```

## Usage

```bash
# stdio transport (default, for MCP clients like Claude Code)
uv run trello-mcp run

# SSE transport (for network access)
uv run trello-mcp run --transport sse --port 8000
```

## Docker

```bash
docker compose up --build
```

## Client Configuration

### stdio (local clients)

The client spawns the server as a subprocess. Use this for Claude Code, Cursor, Windsurf, and similar tools.

**Claude Code** — add to `.mcp.json` (project) or `~/.claude.json` (global), or use the CLI:

```bash
claude mcp add --transport stdio trello -- \
  uv --directory /absolute/path/to/trello-mcp run trello-mcp run
```

Or manually add to `.mcp.json`:

```json
{
  "mcpServers": {
    "trello": {
      "type": "stdio",
      "command": "uv",
      "args": ["--directory", "/absolute/path/to/trello-mcp", "run", "trello-mcp", "run"],
      "env": {
        "TRELLO_API_KEY": "${TRELLO_API_KEY}",
        "TRELLO_TOKEN": "${TRELLO_TOKEN}"
      }
    }
  }
}
```

**Cursor** — add to `.cursor/mcp.json` in your project root:

```json
{
  "mcpServers": {
    "trello": {
      "command": "uv",
      "args": ["--directory", "/absolute/path/to/trello-mcp", "run", "trello-mcp", "run"],
      "env": {
        "TRELLO_API_KEY": "your-api-key",
        "TRELLO_TOKEN": "your-token"
      }
    }
  }
}
```

**OpenCode** — add an `opencode.json` (project config) in your repo root:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "trello": {
      "type": "local",
      "command": ["uv", "--directory", "/absolute/path/to/trello-mcp", "run", "trello-mcp", "run"],
      "enabled": true,
      "environment": {
        "TRELLO_API_KEY": "{env:TRELLO_API_KEY}",
        "TRELLO_TOKEN": "{env:TRELLO_TOKEN}"
      }
    }
  }
}
```

### SSE (network clients)

Start the server first, then point your client to the SSE endpoint.

```bash
# Start the server (or use docker compose up --build)
uv run trello-mcp run --transport sse --port 8000
```

Then configure your client to connect to `http://localhost:8000/sse`.

**Claude Code** — add to `.mcp.json` or use the CLI:

```bash
claude mcp add --transport sse trello http://localhost:8000/sse
```

Or manually:

```json
{
  "mcpServers": {
    "trello": {
      "type": "sse",
      "url": "http://localhost:8000/sse"
    }
  }
}
```

**Cursor** — add to `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "trello": {
      "url": "http://localhost:8000/sse"
    }
  }
}
```

## Tools

| Tool | Description |
|------|-------------|
| `list_boards` | List all boards for the authenticated user |
| `list_lists` | List all lists in a board |
| `list_cards` | List all cards in a list |
| `get_board_cards` | Get all cards on a board |
| `create_card` | Create a new card in a list |
| `move_card` | Move a card to another list |
| `update_card` | Update a card's name and/or description |
| `add_comment` | Add a comment to a card |
| `archive_card` | Archive (close) a card |
| `search_board` | Find a board by name substring |

## Development

```bash
uv sync --extra dev
uv run pre-commit install
uv run pytest --cov
uv run ruff check . && uv run ruff format --check .
```

## License

[MIT](LICENSE)
