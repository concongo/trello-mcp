"""Integration tests for MCP tools using fastmcp.Client."""

from unittest.mock import AsyncMock

import pytest
from fastmcp import Client

from tests.conftest import SAMPLE_BOARDS, SAMPLE_CARDS, SAMPLE_LISTS
from trello_mcp.models import TrelloBoard, TrelloCard, TrelloList
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
    set_client(client)
    yield client
    set_client(None)


def assert_tool_success(result):
    """Assert a tool call returned successfully with content."""
    assert not result.is_error
    assert len(result.content) > 0


async def test_list_boards_tool(mock_trello):
    async with Client(mcp) as c:
        result = await c.call_tool("list_boards", {})
        assert_tool_success(result)
        mock_trello.list_boards.assert_awaited_once()


async def test_list_lists_tool(mock_trello):
    async with Client(mcp) as c:
        result = await c.call_tool("list_lists", {"board_id": "board1"})
        assert_tool_success(result)
        mock_trello.list_lists.assert_awaited_once_with("board1")


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


async def test_search_board_tool(mock_trello):
    async with Client(mcp) as c:
        result = await c.call_tool("search_board", {"query": "alpha"})
        assert_tool_success(result)


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
