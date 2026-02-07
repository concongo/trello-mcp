"""Tests for TrelloClient with mocked HTTP."""

import httpx
import pytest
import respx

from tests.conftest import (
    SAMPLE_BOARDS,
    SAMPLE_CARDS,
    SAMPLE_CHECKLISTS,
    SAMPLE_CUSTOM_FIELDS,
    SAMPLE_LABELS,
    SAMPLE_LISTS,
)
from trello_mcp.client import TrelloClient


@pytest.fixture
def mock_client():
    client = TrelloClient(api_key="key", token="tok", base_url="https://api.trello.com/1")
    return client


BASE = "https://api.trello.com/1"


# --- Boards ---


@respx.mock
async def test_list_boards(mock_client):
    respx.get(f"{BASE}/members/me/boards").mock(
        return_value=httpx.Response(200, json=SAMPLE_BOARDS)
    )
    boards = await mock_client.list_boards()
    assert len(boards) == 2
    assert boards[0].name == "Project Alpha"


@respx.mock
async def test_search_board(mock_client):
    respx.get(f"{BASE}/members/me/boards").mock(
        return_value=httpx.Response(200, json=SAMPLE_BOARDS)
    )
    results = await mock_client.search_board("alpha")
    assert len(results) == 1
    assert results[0].name == "Project Alpha"


# --- Lists ---


@respx.mock
async def test_list_lists(mock_client):
    respx.get(f"{BASE}/boards/board1/lists").mock(
        return_value=httpx.Response(200, json=SAMPLE_LISTS)
    )
    lists = await mock_client.list_lists("board1")
    assert len(lists) == 2
    assert lists[0].name == "To Do"


@respx.mock
async def test_create_list(mock_client):
    new_list = {"id": "list3", "name": "Done", "idBoard": "board1", "closed": False}
    respx.post(f"{BASE}/lists").mock(return_value=httpx.Response(200, json=new_list))
    lst = await mock_client.create_list("board1", "Done")
    assert lst.id == "list3"
    assert lst.name == "Done"


@respx.mock
async def test_update_list(mock_client):
    updated = {"id": "list1", "name": "Renamed", "idBoard": "board1", "closed": False}
    respx.put(f"{BASE}/lists/list1").mock(return_value=httpx.Response(200, json=updated))
    lst = await mock_client.update_list("list1", name="Renamed")
    assert lst.name == "Renamed"


@respx.mock
async def test_archive_list(mock_client):
    archived = {"id": "list1", "name": "To Do", "idBoard": "board1", "closed": True}
    respx.put(f"{BASE}/lists/list1").mock(return_value=httpx.Response(200, json=archived))
    lst = await mock_client.archive_list("list1")
    assert lst.closed is True


# --- Cards ---


@respx.mock
async def test_list_cards(mock_client):
    respx.get(f"{BASE}/lists/list1/cards").mock(
        return_value=httpx.Response(200, json=SAMPLE_CARDS)
    )
    cards = await mock_client.list_cards("list1")
    assert len(cards) == 2
    assert cards[0].name == "Task 1"


@respx.mock
async def test_get_board_cards(mock_client):
    respx.get(f"{BASE}/boards/board1/cards").mock(
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
    respx.post(f"{BASE}/cards").mock(return_value=httpx.Response(200, json=new_card))
    card = await mock_client.create_card("list1", "New Task", "Details")
    assert card.id == "card3"
    assert card.name == "New Task"


@respx.mock
async def test_move_card(mock_client):
    moved = {**SAMPLE_CARDS[0], "idList": "list2"}
    respx.put(f"{BASE}/cards/card1").mock(return_value=httpx.Response(200, json=moved))
    card = await mock_client.move_card("card1", "list2")
    assert card.id_list == "list2"


@respx.mock
async def test_update_card(mock_client):
    updated = {**SAMPLE_CARDS[0], "name": "Updated", "desc": "New desc"}
    respx.put(f"{BASE}/cards/card1").mock(return_value=httpx.Response(200, json=updated))
    card = await mock_client.update_card("card1", name="Updated", desc="New desc")
    assert card.name == "Updated"


@respx.mock
async def test_add_comment(mock_client):
    comment_resp = {"id": "action1", "type": "commentCard", "data": {"text": "Hello"}}
    respx.post(f"{BASE}/cards/card1/actions/comments").mock(
        return_value=httpx.Response(200, json=comment_resp)
    )
    result = await mock_client.add_comment("card1", "Hello")
    assert result["data"]["text"] == "Hello"


@respx.mock
async def test_archive_card(mock_client):
    archived = {**SAMPLE_CARDS[0], "closed": True}
    respx.put(f"{BASE}/cards/card1").mock(return_value=httpx.Response(200, json=archived))
    card = await mock_client.archive_card("card1")
    assert card.closed is True


# --- Card Due Dates ---


@respx.mock
async def test_set_due_date(mock_client):
    updated = {**SAMPLE_CARDS[0], "due": "2025-12-31T12:00:00.000Z"}
    respx.put(f"{BASE}/cards/card1").mock(return_value=httpx.Response(200, json=updated))
    card = await mock_client.set_due_date("card1", "2025-12-31T12:00:00.000Z")
    assert card.due == "2025-12-31T12:00:00.000Z"


@respx.mock
async def test_mark_due_complete(mock_client):
    updated = {**SAMPLE_CARDS[0], "dueComplete": True}
    respx.put(f"{BASE}/cards/card1").mock(return_value=httpx.Response(200, json=updated))
    card = await mock_client.mark_due_complete("card1", True)
    assert card.due_complete is True


# --- Checklists ---


@respx.mock
async def test_get_checklists(mock_client):
    respx.get(f"{BASE}/cards/card1/checklists").mock(
        return_value=httpx.Response(200, json=SAMPLE_CHECKLISTS)
    )
    checklists = await mock_client.get_checklists("card1")
    assert len(checklists) == 1
    assert checklists[0].name == "Tasks"
    assert len(checklists[0].check_items) == 2


@respx.mock
async def test_create_checklist(mock_client):
    new_cl = {"id": "cl2", "name": "New CL", "idCard": "card1", "checkItems": []}
    respx.post(f"{BASE}/cards/card1/checklists").mock(
        return_value=httpx.Response(200, json=new_cl)
    )
    cl = await mock_client.create_checklist("card1", "New CL")
    assert cl.id == "cl2"
    assert cl.name == "New CL"


@respx.mock
async def test_delete_checklist(mock_client):
    respx.delete(f"{BASE}/checklists/cl1").mock(return_value=httpx.Response(200))
    await mock_client.delete_checklist("cl1")


@respx.mock
async def test_add_check_item(mock_client):
    new_item = {"id": "ci3", "name": "Step 3", "state": "incomplete", "idChecklist": "cl1"}
    respx.post(f"{BASE}/checklists/cl1/checkItems").mock(
        return_value=httpx.Response(200, json=new_item)
    )
    item = await mock_client.add_check_item("cl1", "Step 3")
    assert item.id == "ci3"
    assert item.name == "Step 3"


@respx.mock
async def test_update_check_item(mock_client):
    updated = {"id": "ci1", "name": "Step 1", "state": "complete", "idChecklist": "cl1"}
    respx.put(f"{BASE}/cards/card1/checklist/cl1/checkItem/ci1").mock(
        return_value=httpx.Response(200, json=updated)
    )
    item = await mock_client.update_check_item("card1", "cl1", "ci1", state="complete")
    assert item.state == "complete"


@respx.mock
async def test_delete_check_item(mock_client):
    respx.delete(f"{BASE}/checklists/cl1/checkItems/ci1").mock(return_value=httpx.Response(200))
    await mock_client.delete_check_item("cl1", "ci1")


# --- Labels ---


@respx.mock
async def test_get_board_labels(mock_client):
    respx.get(f"{BASE}/boards/board1/labels").mock(
        return_value=httpx.Response(200, json=SAMPLE_LABELS)
    )
    labels = await mock_client.get_board_labels("board1")
    assert len(labels) == 2
    assert labels[0].name == "Bug"


@respx.mock
async def test_create_label(mock_client):
    new_label = {"id": "lbl3", "name": "Urgent", "color": "orange", "idBoard": "board1"}
    respx.post(f"{BASE}/labels").mock(return_value=httpx.Response(200, json=new_label))
    label = await mock_client.create_label("board1", "Urgent", "orange")
    assert label.id == "lbl3"
    assert label.color == "orange"


@respx.mock
async def test_add_label_to_card(mock_client):
    respx.post(f"{BASE}/cards/card1/idLabels").mock(
        return_value=httpx.Response(200, json=[{"id": "lbl1"}])
    )
    await mock_client.add_label_to_card("card1", "lbl1")


@respx.mock
async def test_remove_label_from_card(mock_client):
    respx.delete(f"{BASE}/cards/card1/idLabels/lbl1").mock(return_value=httpx.Response(200))
    await mock_client.remove_label_from_card("card1", "lbl1")


# --- Custom Fields ---


@respx.mock
async def test_get_custom_fields(mock_client):
    respx.get(f"{BASE}/boards/board1/customFields").mock(
        return_value=httpx.Response(200, json=SAMPLE_CUSTOM_FIELDS)
    )
    fields = await mock_client.get_custom_fields("board1")
    assert len(fields) == 2
    assert fields[0].name == "Priority"


@respx.mock
async def test_set_card_custom_field(mock_client):
    resp_data = {"id": "cf1", "value": {"number": "5"}}
    respx.put(f"{BASE}/cards/card1/customField/cf1/item").mock(
        return_value=httpx.Response(200, json=resp_data)
    )
    result = await mock_client.set_card_custom_field("card1", "cf1", {"number": "5"})
    assert result["value"]["number"] == "5"


# --- Error handling ---


@respx.mock
async def test_http_error_raises(mock_client):
    respx.get(f"{BASE}/members/me/boards").mock(
        return_value=httpx.Response(401, json={"error": "unauthorized"})
    )
    with pytest.raises(httpx.HTTPStatusError):
        await mock_client.list_boards()


@respx.mock
async def test_delete_error_raises(mock_client):
    respx.delete(f"{BASE}/checklists/bad").mock(
        return_value=httpx.Response(404, json={"error": "not found"})
    )
    with pytest.raises(httpx.HTTPStatusError):
        await mock_client.delete_checklist("bad")
