"""Tests for Pydantic models."""

from trello_mcp.models import (
    TrelloBoard,
    TrelloCard,
    TrelloCheckItem,
    TrelloChecklist,
    TrelloCustomField,
    TrelloLabel,
    TrelloList,
)


class TestTrelloBoard:
    def test_from_api_response(self):
        board = TrelloBoard(
            id="b1", name="My Board", desc="A board", url="https://trello.com/b/b1"
        )
        assert board.id == "b1"
        assert board.name == "My Board"
        assert board.closed is False

    def test_defaults(self):
        board = TrelloBoard(id="b1", name="X")
        assert board.desc == ""
        assert board.url == ""
        assert board.closed is False


class TestTrelloList:
    def test_from_api_response_with_alias(self):
        lst = TrelloList(id="l1", name="To Do", idBoard="b1")
        assert lst.id_board == "b1"

    def test_populate_by_name(self):
        lst = TrelloList(id="l1", name="To Do", id_board="b1")
        assert lst.id_board == "b1"


class TestTrelloCard:
    def test_from_api_response(self):
        card = TrelloCard(id="c1", name="Task", idList="l1", idBoard="b1")
        assert card.id_list == "l1"
        assert card.id_board == "b1"
        assert card.labels == []

    def test_model_dump(self):
        card = TrelloCard(id="c1", name="Task", desc="Do it", idList="l1")
        data = card.model_dump()
        assert data["id"] == "c1"
        assert data["id_list"] == "l1"

    def test_due_fields_defaults(self):
        card = TrelloCard(id="c1", name="Task")
        assert card.due is None
        assert card.due_complete is False

    def test_due_fields_from_api(self):
        card = TrelloCard(id="c1", name="Task", due="2025-12-31T12:00:00.000Z", dueComplete=True)
        assert card.due == "2025-12-31T12:00:00.000Z"
        assert card.due_complete is True


class TestTrelloCheckItem:
    def test_from_api_response(self):
        item = TrelloCheckItem(id="ci1", name="Step 1", state="incomplete", idChecklist="cl1")
        assert item.id_checklist == "cl1"
        assert item.state == "incomplete"

    def test_defaults(self):
        item = TrelloCheckItem(id="ci1", name="Step 1")
        assert item.state == "incomplete"
        assert item.id_checklist == ""


class TestTrelloChecklist:
    def test_from_api_response(self):
        cl = TrelloChecklist(
            id="cl1",
            name="Tasks",
            idCard="card1",
            checkItems=[
                {"id": "ci1", "name": "Step 1", "state": "incomplete", "idChecklist": "cl1"}
            ],
        )
        assert cl.id_card == "card1"
        assert len(cl.check_items) == 1
        assert cl.check_items[0].name == "Step 1"

    def test_defaults(self):
        cl = TrelloChecklist(id="cl1", name="Tasks")
        assert cl.id_card == ""
        assert cl.check_items == []


class TestTrelloLabel:
    def test_from_api_response(self):
        label = TrelloLabel(id="lbl1", name="Bug", color="red", idBoard="board1")
        assert label.id_board == "board1"
        assert label.color == "red"

    def test_defaults(self):
        label = TrelloLabel(id="lbl1")
        assert label.name == ""
        assert label.color is None
        assert label.id_board == ""


class TestTrelloCustomField:
    def test_from_api_response(self):
        cf = TrelloCustomField(id="cf1", name="Priority", type="list", idModel="board1")
        assert cf.id_model == "board1"
        assert cf.type == "list"

    def test_defaults(self):
        cf = TrelloCustomField(id="cf1", name="Priority")
        assert cf.type == ""
        assert cf.id_model == ""
