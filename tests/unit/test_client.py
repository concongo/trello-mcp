"""Tests for TrelloClient with mocked HTTP."""

import httpx
import pytest
import respx

from tests.conftest import SAMPLE_BOARDS, SAMPLE_CARDS, SAMPLE_LISTS
from trello_mcp.client import TrelloClient


@pytest.fixture
def mock_client():
    client = TrelloClient(api_key="key", token="tok", base_url="https://api.trello.com/1")
    return client


@respx.mock
async def test_list_boards(mock_client):
    respx.get("https://api.trello.com/1/members/me/boards").mock(
        return_value=httpx.Response(200, json=SAMPLE_BOARDS)
    )
    boards = await mock_client.list_boards()
    assert len(boards) == 2
    assert boards[0].name == "Project Alpha"


@respx.mock
async def test_list_lists(mock_client):
    respx.get("https://api.trello.com/1/boards/board1/lists").mock(
        return_value=httpx.Response(200, json=SAMPLE_LISTS)
    )
    lists = await mock_client.list_lists("board1")
    assert len(lists) == 2
    assert lists[0].name == "To Do"


@respx.mock
async def test_list_cards(mock_client):
    respx.get("https://api.trello.com/1/lists/list1/cards").mock(
        return_value=httpx.Response(200, json=SAMPLE_CARDS)
    )
    cards = await mock_client.list_cards("list1")
    assert len(cards) == 2
    assert cards[0].name == "Task 1"


@respx.mock
async def test_get_board_cards(mock_client):
    respx.get("https://api.trello.com/1/boards/board1/cards").mock(
        return_value=httpx.Response(200, json=SAMPLE_CARDS)
    )
    cards = await mock_client.get_board_cards("board1")
    assert len(cards) == 2


@respx.mock
async def test_create_card(mock_client):
    new_card = {
        "id": "card3",
        "name": "New Task",
        "desc": "Details",
        "idList": "list1",
        "idBoard": "board1",
        "url": "",
        "closed": False,
        "labels": [],
    }
    respx.post("https://api.trello.com/1/cards").mock(
        return_value=httpx.Response(200, json=new_card)
    )
    card = await mock_client.create_card("list1", "New Task", "Details")
    assert card.id == "card3"
    assert card.name == "New Task"


@respx.mock
async def test_move_card(mock_client):
    moved = {**SAMPLE_CARDS[0], "idList": "list2"}
    respx.put("https://api.trello.com/1/cards/card1").mock(
        return_value=httpx.Response(200, json=moved)
    )
    card = await mock_client.move_card("card1", "list2")
    assert card.id_list == "list2"


@respx.mock
async def test_add_comment(mock_client):
    comment_resp = {"id": "action1", "type": "commentCard", "data": {"text": "Hello"}}
    respx.post("https://api.trello.com/1/cards/card1/actions/comments").mock(
        return_value=httpx.Response(200, json=comment_resp)
    )
    result = await mock_client.add_comment("card1", "Hello")
    assert result["data"]["text"] == "Hello"


@respx.mock
async def test_archive_card(mock_client):
    archived = {**SAMPLE_CARDS[0], "closed": True}
    respx.put("https://api.trello.com/1/cards/card1").mock(
        return_value=httpx.Response(200, json=archived)
    )
    card = await mock_client.archive_card("card1")
    assert card.closed is True


@respx.mock
async def test_search_board(mock_client):
    respx.get("https://api.trello.com/1/members/me/boards").mock(
        return_value=httpx.Response(200, json=SAMPLE_BOARDS)
    )
    results = await mock_client.search_board("alpha")
    assert len(results) == 1
    assert results[0].name == "Project Alpha"


@respx.mock
async def test_http_error_raises(mock_client):
    respx.get("https://api.trello.com/1/members/me/boards").mock(
        return_value=httpx.Response(401, json={"error": "unauthorized"})
    )
    with pytest.raises(httpx.HTTPStatusError):
        await mock_client.list_boards()
