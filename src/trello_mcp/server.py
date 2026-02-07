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


# --- Board tools ---


@mcp.tool()
async def list_boards() -> list[dict]:
    """List all boards for the authenticated Trello user."""
    boards = await get_client().list_boards()
    return [b.model_dump() for b in boards]


@mcp.tool()
async def search_board(query: str) -> list[dict]:
    """Find a board by name substring."""
    boards = await get_client().search_board(query)
    return [b.model_dump() for b in boards]


# --- List tools ---


@mcp.tool()
async def list_lists(board_id: str) -> list[dict]:
    """List all lists in a Trello board."""
    lists = await get_client().list_lists(board_id)
    return [lst.model_dump() for lst in lists]


@mcp.tool()
async def create_list(board_id: str, name: str) -> dict:
    """Create a new list on a Trello board."""
    lst = await get_client().create_list(board_id, name)
    return lst.model_dump()


@mcp.tool()
async def update_list(list_id: str, name: str | None = None, closed: bool | None = None) -> dict:
    """Update a list's name and/or closed status."""
    lst = await get_client().update_list(list_id, name=name, closed=closed)
    return lst.model_dump()


@mcp.tool()
async def archive_list(list_id: str) -> dict:
    """Archive (close) a Trello list."""
    lst = await get_client().archive_list(list_id)
    return lst.model_dump()


# --- Card tools ---


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


# --- Card Due Date tools ---


@mcp.tool()
async def set_due_date(card_id: str, due: str) -> dict:
    """Set a due date on a card. Use ISO 8601 format (e.g. '2025-12-31T12:00:00Z')."""
    card = await get_client().set_due_date(card_id, due)
    return card.model_dump()


@mcp.tool()
async def mark_due_complete(card_id: str, complete: bool) -> dict:
    """Mark a card's due date as complete or incomplete."""
    card = await get_client().mark_due_complete(card_id, complete)
    return card.model_dump()


# --- Checklist tools ---


@mcp.tool()
async def get_checklists(card_id: str) -> list[dict]:
    """Get all checklists on a card."""
    checklists = await get_client().get_checklists(card_id)
    return [cl.model_dump() for cl in checklists]


@mcp.tool()
async def create_checklist(card_id: str, name: str) -> dict:
    """Create a new checklist on a card."""
    cl = await get_client().create_checklist(card_id, name)
    return cl.model_dump()


@mcp.tool()
async def delete_checklist(checklist_id: str) -> dict:
    """Delete a checklist."""
    await get_client().delete_checklist(checklist_id)
    return {"deleted": True}


@mcp.tool()
async def add_check_item(checklist_id: str, name: str) -> dict:
    """Add an item to a checklist."""
    item = await get_client().add_check_item(checklist_id, name)
    return item.model_dump()


@mcp.tool()
async def update_check_item(
    card_id: str,
    checklist_id: str,
    check_item_id: str,
    state: str | None = None,
    name: str | None = None,
) -> dict:
    """Update a check item's state ('complete'/'incomplete') or name."""
    item = await get_client().update_check_item(
        card_id, checklist_id, check_item_id, state=state, name=name
    )
    return item.model_dump()


@mcp.tool()
async def delete_check_item(checklist_id: str, check_item_id: str) -> dict:
    """Delete a check item from a checklist."""
    await get_client().delete_check_item(checklist_id, check_item_id)
    return {"deleted": True}


# --- Label tools ---


@mcp.tool()
async def get_board_labels(board_id: str) -> list[dict]:
    """Get all labels on a board."""
    labels = await get_client().get_board_labels(board_id)
    return [lbl.model_dump() for lbl in labels]


@mcp.tool()
async def create_label(board_id: str, name: str, color: str) -> dict:
    """Create a new label on a board."""
    label = await get_client().create_label(board_id, name, color)
    return label.model_dump()


@mcp.tool()
async def add_label_to_card(card_id: str, label_id: str) -> dict:
    """Add a label to a card."""
    await get_client().add_label_to_card(card_id, label_id)
    return {"added": True}


@mcp.tool()
async def remove_label_from_card(card_id: str, label_id: str) -> dict:
    """Remove a label from a card."""
    await get_client().remove_label_from_card(card_id, label_id)
    return {"removed": True}


# --- Custom Field tools ---


@mcp.tool()
async def get_custom_fields(board_id: str) -> list[dict]:
    """Get all custom field definitions on a board."""
    fields = await get_client().get_custom_fields(board_id)
    return [f.model_dump() for f in fields]


@mcp.tool()
async def set_card_custom_field(card_id: str, field_id: str, value: dict) -> dict:
    """Set a custom field value on a card. Value format depends on field type."""
    return await get_client().set_card_custom_field(card_id, field_id, value)
