"""Integration tests for MCP tools using fastmcp.Client."""

from unittest.mock import AsyncMock

import pytest
from fastmcp import Client

from tests.conftest import SAMPLE_BOARDS, SAMPLE_CARDS, SAMPLE_LISTS
from trello_mcp.models import (
    TrelloBoard,
    TrelloCard,
    TrelloCheckItem,
    TrelloChecklist,
    TrelloCustomField,
    TrelloLabel,
    TrelloList,
)
from trello_mcp.server import mcp, set_client


@pytest.fixture
def mock_trello():
    """Create a mock TrelloClient and inject it into the server."""
    client = AsyncMock()
    client.list_boards.return_value = [TrelloBoard(**b) for b in SAMPLE_BOARDS]
    client.list_lists.return_value = [TrelloList(**lst) for lst in SAMPLE_LISTS]
    client.list_cards.return_value = [TrelloCard(**c) for c in SAMPLE_CARDS]
    client.get_board_cards.return_value = [TrelloCard(**c) for c in SAMPLE_CARDS]
    client.create_card.return_value = TrelloCard(
        id="card3", name="New", desc="", idList="list1", idBoard="board1"
    )
    client.move_card.return_value = TrelloCard(
        id="card1", name="Task 1", idList="list2", idBoard="board1"
    )
    client.update_card.return_value = TrelloCard(
        id="card1", name="Updated", desc="New desc", idList="list1", idBoard="board1"
    )
    client.add_comment.return_value = {"id": "action1", "data": {"text": "Hi"}}
    client.archive_card.return_value = TrelloCard(
        id="card1", name="Task 1", idList="list1", idBoard="board1", closed=True
    )
    client.search_board.return_value = [TrelloBoard(**SAMPLE_BOARDS[0])]
    # Lists management
    client.create_list.return_value = TrelloList(id="list3", name="Done", idBoard="board1")
    client.update_list.return_value = TrelloList(id="list1", name="Renamed", idBoard="board1")
    client.archive_list.return_value = TrelloList(
        id="list1", name="To Do", idBoard="board1", closed=True
    )
    # Due dates
    client.set_due_date.return_value = TrelloCard(
        id="card1", name="Task 1", idList="list1", due="2025-12-31T12:00:00.000Z"
    )
    client.mark_due_complete.return_value = TrelloCard(
        id="card1", name="Task 1", idList="list1", dueComplete=True
    )
    # Checklists
    client.get_checklists.return_value = [
        TrelloChecklist(id="cl1", name="Tasks", idCard="card1", checkItems=[])
    ]
    client.create_checklist.return_value = TrelloChecklist(id="cl2", name="New CL", idCard="card1")
    client.delete_checklist.return_value = None
    client.add_check_item.return_value = TrelloCheckItem(
        id="ci3", name="Step 3", idChecklist="cl1"
    )
    client.update_check_item.return_value = TrelloCheckItem(
        id="ci1", name="Step 1", state="complete", idChecklist="cl1"
    )
    client.delete_check_item.return_value = None
    # Labels
    client.get_board_labels.return_value = [
        TrelloLabel(id="lbl1", name="Bug", color="red", idBoard="board1")
    ]
    client.create_label.return_value = TrelloLabel(
        id="lbl3", name="Urgent", color="orange", idBoard="board1"
    )
    client.add_label_to_card.return_value = None
    client.remove_label_from_card.return_value = None
    # Custom fields
    client.get_custom_fields.return_value = [
        TrelloCustomField(id="cf1", name="Priority", type="list", idModel="board1")
    ]
    client.set_card_custom_field.return_value = {"id": "cf1", "value": {"number": "5"}}
    set_client(client)
    yield client
    set_client(None)


def assert_tool_success(result):
    """Assert a tool call returned successfully with content."""
    assert not result.is_error
    assert len(result.content) > 0


# --- Board tools ---


async def test_list_boards_tool(mock_trello):
    async with Client(mcp) as c:
        result = await c.call_tool("list_boards", {})
        assert_tool_success(result)
        mock_trello.list_boards.assert_awaited_once()


async def test_search_board_tool(mock_trello):
    async with Client(mcp) as c:
        result = await c.call_tool("search_board", {"query": "alpha"})
        assert_tool_success(result)


# --- List tools ---


async def test_list_lists_tool(mock_trello):
    async with Client(mcp) as c:
        result = await c.call_tool("list_lists", {"board_id": "board1"})
        assert_tool_success(result)
        mock_trello.list_lists.assert_awaited_once_with("board1")


async def test_create_list_tool(mock_trello):
    async with Client(mcp) as c:
        result = await c.call_tool("create_list", {"board_id": "board1", "name": "Done"})
        assert_tool_success(result)
        mock_trello.create_list.assert_awaited_once_with("board1", "Done")


async def test_update_list_tool(mock_trello):
    async with Client(mcp) as c:
        result = await c.call_tool("update_list", {"list_id": "list1", "name": "Renamed"})
        assert_tool_success(result)
        mock_trello.update_list.assert_awaited_once_with("list1", name="Renamed", closed=None)


async def test_archive_list_tool(mock_trello):
    async with Client(mcp) as c:
        result = await c.call_tool("archive_list", {"list_id": "list1"})
        assert_tool_success(result)
        mock_trello.archive_list.assert_awaited_once_with("list1")


# --- Card tools ---


async def test_list_cards_tool(mock_trello):
    async with Client(mcp) as c:
        result = await c.call_tool("list_cards", {"list_id": "list1"})
        assert_tool_success(result)
        mock_trello.list_cards.assert_awaited_once_with("list1")


async def test_get_board_cards_tool(mock_trello):
    async with Client(mcp) as c:
        result = await c.call_tool("get_board_cards", {"board_id": "board1"})
        assert_tool_success(result)


async def test_create_card_tool(mock_trello):
    async with Client(mcp) as c:
        result = await c.call_tool("create_card", {"list_id": "list1", "name": "New"})
        assert_tool_success(result)
        mock_trello.create_card.assert_awaited_once_with("list1", "New", "")


async def test_move_card_tool(mock_trello):
    async with Client(mcp) as c:
        result = await c.call_tool("move_card", {"card_id": "card1", "list_id": "list2"})
        assert_tool_success(result)


async def test_update_card_tool(mock_trello):
    async with Client(mcp) as c:
        result = await c.call_tool(
            "update_card", {"card_id": "card1", "name": "Updated", "desc": "New desc"}
        )
        assert_tool_success(result)
        mock_trello.update_card.assert_awaited_once_with("card1", name="Updated", desc="New desc")


async def test_add_comment_tool(mock_trello):
    async with Client(mcp) as c:
        result = await c.call_tool("add_comment", {"card_id": "card1", "text": "Hi"})
        assert_tool_success(result)


async def test_archive_card_tool(mock_trello):
    async with Client(mcp) as c:
        result = await c.call_tool("archive_card", {"card_id": "card1"})
        assert_tool_success(result)


# --- Card Due Date tools ---


async def test_set_due_date_tool(mock_trello):
    async with Client(mcp) as c:
        result = await c.call_tool(
            "set_due_date", {"card_id": "card1", "due": "2025-12-31T12:00:00.000Z"}
        )
        assert_tool_success(result)
        mock_trello.set_due_date.assert_awaited_once_with("card1", "2025-12-31T12:00:00.000Z")


async def test_mark_due_complete_tool(mock_trello):
    async with Client(mcp) as c:
        result = await c.call_tool("mark_due_complete", {"card_id": "card1", "complete": True})
        assert_tool_success(result)
        mock_trello.mark_due_complete.assert_awaited_once_with("card1", True)


# --- Checklist tools ---


async def test_get_checklists_tool(mock_trello):
    async with Client(mcp) as c:
        result = await c.call_tool("get_checklists", {"card_id": "card1"})
        assert_tool_success(result)
        mock_trello.get_checklists.assert_awaited_once_with("card1")


async def test_create_checklist_tool(mock_trello):
    async with Client(mcp) as c:
        result = await c.call_tool("create_checklist", {"card_id": "card1", "name": "New CL"})
        assert_tool_success(result)
        mock_trello.create_checklist.assert_awaited_once_with("card1", "New CL")


async def test_delete_checklist_tool(mock_trello):
    async with Client(mcp) as c:
        result = await c.call_tool("delete_checklist", {"checklist_id": "cl1"})
        assert_tool_success(result)
        mock_trello.delete_checklist.assert_awaited_once_with("cl1")


async def test_add_check_item_tool(mock_trello):
    async with Client(mcp) as c:
        result = await c.call_tool("add_check_item", {"checklist_id": "cl1", "name": "Step 3"})
        assert_tool_success(result)
        mock_trello.add_check_item.assert_awaited_once_with("cl1", "Step 3")


async def test_update_check_item_tool(mock_trello):
    async with Client(mcp) as c:
        result = await c.call_tool(
            "update_check_item",
            {
                "card_id": "card1",
                "checklist_id": "cl1",
                "check_item_id": "ci1",
                "state": "complete",
            },
        )
        assert_tool_success(result)
        mock_trello.update_check_item.assert_awaited_once_with(
            "card1", "cl1", "ci1", state="complete", name=None
        )


async def test_delete_check_item_tool(mock_trello):
    async with Client(mcp) as c:
        result = await c.call_tool(
            "delete_check_item", {"checklist_id": "cl1", "check_item_id": "ci1"}
        )
        assert_tool_success(result)
        mock_trello.delete_check_item.assert_awaited_once_with("cl1", "ci1")


# --- Label tools ---


async def test_get_board_labels_tool(mock_trello):
    async with Client(mcp) as c:
        result = await c.call_tool("get_board_labels", {"board_id": "board1"})
        assert_tool_success(result)
        mock_trello.get_board_labels.assert_awaited_once_with("board1")


async def test_create_label_tool(mock_trello):
    async with Client(mcp) as c:
        result = await c.call_tool(
            "create_label", {"board_id": "board1", "name": "Urgent", "color": "orange"}
        )
        assert_tool_success(result)
        mock_trello.create_label.assert_awaited_once_with("board1", "Urgent", "orange")


async def test_add_label_to_card_tool(mock_trello):
    async with Client(mcp) as c:
        result = await c.call_tool("add_label_to_card", {"card_id": "card1", "label_id": "lbl1"})
        assert_tool_success(result)
        mock_trello.add_label_to_card.assert_awaited_once_with("card1", "lbl1")


async def test_remove_label_from_card_tool(mock_trello):
    async with Client(mcp) as c:
        result = await c.call_tool(
            "remove_label_from_card", {"card_id": "card1", "label_id": "lbl1"}
        )
        assert_tool_success(result)
        mock_trello.remove_label_from_card.assert_awaited_once_with("card1", "lbl1")


# --- Custom Field tools ---


async def test_get_custom_fields_tool(mock_trello):
    async with Client(mcp) as c:
        result = await c.call_tool("get_custom_fields", {"board_id": "board1"})
        assert_tool_success(result)
        mock_trello.get_custom_fields.assert_awaited_once_with("board1")


async def test_set_card_custom_field_tool(mock_trello):
    async with Client(mcp) as c:
        result = await c.call_tool(
            "set_card_custom_field",
            {"card_id": "card1", "field_id": "cf1", "value": {"number": "5"}},
        )
        assert_tool_success(result)
        mock_trello.set_card_custom_field.assert_awaited_once_with("card1", "cf1", {"number": "5"})


# --- Resources ---


async def test_resources_are_registered():
    async with Client(mcp) as c:
        resources = await c.list_resources()
        uris = {str(r.uri) for r in resources}
        assert "trello://docs/api-introduction" in uris
        assert "trello://docs/object-definitions" in uris
        assert "trello://docs/status-codes" in uris
        assert len(uris) == 8


async def test_resource_content_readable():
    async with Client(mcp) as c:
        result = await c.read_resource("trello://docs/api-introduction")
        text = result[0].content if hasattr(result[0], "content") else str(result[0])
        assert "Trello API Introduction" in text
