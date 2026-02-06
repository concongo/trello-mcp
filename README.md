# Trello MCP Server

MCP server exposing Trello board, list, and card operations as tools.

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
uv run pytest --cov
uv run ruff check . && uv run ruff format --check .
```
