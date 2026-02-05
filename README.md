# Trello MCP Server

MCP server exposing Trello board, list, and card operations as tools.

## Setup

```bash
uv venv && uv pip install -e ".[dev]"
cp .env.example .env  # Fill in your Trello API key and token
```

## Usage

```bash
# stdio transport (default, for MCP clients like Claude Code)
trello-mcp run

# SSE transport (for network access)
trello-mcp run --transport sse --port 8000
```

## Docker

```bash
docker compose up --build
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
| `add_comment` | Add a comment to a card |
| `archive_card` | Archive (close) a card |
| `search_board` | Find a board by name substring |

## Development

```bash
pytest --cov
ruff check . && ruff format --check .
```
