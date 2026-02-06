"""FastMCP server exposing Trello operations as tools."""

from importlib import resources as pkg_resources

from fastmcp import FastMCP

from trello_mcp.client import TrelloClient
from trello_mcp.models import Settings

mcp = FastMCP("Trello MCP Server")

# --- Resources: Trello API documentation ---

_RESOURCES = {
    "api-introduction": "API Introduction — core concepts, endpoints, and first requests",
    "nested-resources": "Nested Resources — accessing hierarchical data",
    "object-definitions": "Object Definitions — Board, Card, List, Member, Action fields",
    "limits": "Limits — board and card object limits and thresholds",
    "rate-limits": "Rate Limits — request quotas, error responses, and best practices",
    "custom-fields": "Custom Fields — creating, reading, updating custom field values on cards",
    "authorization": "Authorization — API keys, tokens, OAuth, scopes, and security",
    "status-codes": "Status Codes — HTTP response codes returned by the API",
}


def _load_resource(name: str) -> str:
    filename = name.replace("-", "_")
    ref = pkg_resources.files("trello_mcp").joinpath(f"resources/{filename}.md")
    return ref.read_text(encoding="utf-8")


def _register_resources():
    from fastmcp.resources.resource import FunctionResource

    for slug, desc in _RESOURCES.items():

        def _reader(s=slug) -> str:
            return _load_resource(s)

        resource = FunctionResource(
            uri=f"trello://docs/{slug}",
            name=slug,
            description=desc,
            mime_type="text/markdown",
            fn=_reader,
        )
        mcp.add_resource(resource)


_register_resources()


_client: TrelloClient | None = None


def get_client() -> TrelloClient:
    global _client
    if _client is None:
        settings = Settings()
        _client = TrelloClient(
            api_key=settings.trello_api_key,
            token=settings.trello_token,
            base_url=settings.trello_base_url,
        )
    return _client


def set_client(client: TrelloClient):
    """Inject a client instance (for testing)."""
    global _client
    _client = client


@mcp.tool()
async def list_boards() -> list[dict]:
    """List all boards for the authenticated Trello user."""
    boards = await get_client().list_boards()
    return [b.model_dump() for b in boards]


@mcp.tool()
async def list_lists(board_id: str) -> list[dict]:
    """List all lists in a Trello board."""
    lists = await get_client().list_lists(board_id)
    return [lst.model_dump() for lst in lists]


@mcp.tool()
async def list_cards(list_id: str) -> list[dict]:
    """List all cards in a Trello list."""
    cards = await get_client().list_cards(list_id)
    return [c.model_dump() for c in cards]


@mcp.tool()
async def get_board_cards(board_id: str) -> list[dict]:
    """Get all cards on a Trello board."""
    cards = await get_client().get_board_cards(board_id)
    return [c.model_dump() for c in cards]


@mcp.tool()
async def create_card(list_id: str, name: str, desc: str = "") -> dict:
    """Create a new card in a Trello list."""
    card = await get_client().create_card(list_id, name, desc)
    return card.model_dump()


@mcp.tool()
async def move_card(card_id: str, list_id: str) -> dict:
    """Move a card to another list."""
    card = await get_client().move_card(card_id, list_id)
    return card.model_dump()


@mcp.tool()
async def update_card(card_id: str, name: str | None = None, desc: str | None = None) -> dict:
    """Update a card's name and/or description."""
    card = await get_client().update_card(card_id, name=name, desc=desc)
    return card.model_dump()


@mcp.tool()
async def add_comment(card_id: str, text: str) -> dict:
    """Add a comment to a Trello card."""
    return await get_client().add_comment(card_id, text)


@mcp.tool()
async def archive_card(card_id: str) -> dict:
    """Archive (close) a Trello card."""
    card = await get_client().archive_card(card_id)
    return card.model_dump()


@mcp.tool()
async def search_board(query: str) -> list[dict]:
    """Find a board by name substring."""
    boards = await get_client().search_board(query)
    return [b.model_dump() for b in boards]
