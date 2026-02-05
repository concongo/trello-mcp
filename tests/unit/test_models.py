"""Tests for Pydantic models."""

from trello_mcp.models import TrelloBoard, TrelloCard, TrelloList


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
