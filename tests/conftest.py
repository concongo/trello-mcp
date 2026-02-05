"""Shared test fixtures."""

import pytest

from trello_mcp.client import TrelloClient

SAMPLE_BOARDS = [
    {
        "id": "board1",
        "name": "Project Alpha",
        "desc": "Main project",
        "url": "https://trello.com/b/board1",
        "closed": False,
    },
    {
        "id": "board2",
        "name": "Beta Tasks",
        "desc": "",
        "url": "https://trello.com/b/board2",
        "closed": False,
    },
]

SAMPLE_LISTS = [
    {"id": "list1", "name": "To Do", "idBoard": "board1", "closed": False},
    {"id": "list2", "name": "In Progress", "idBoard": "board1", "closed": False},
]

SAMPLE_CARDS = [
    {
        "id": "card1",
        "name": "Task 1",
        "desc": "Do stuff",
        "idList": "list1",
        "idBoard": "board1",
        "url": "https://trello.com/c/card1",
        "closed": False,
        "labels": [],
    },
    {
        "id": "card2",
        "name": "Task 2",
        "desc": "",
        "idList": "list1",
        "idBoard": "board1",
        "url": "https://trello.com/c/card2",
        "closed": False,
        "labels": [],
    },
]


@pytest.fixture
def trello_client():
    """Create a TrelloClient pointed at a mock base URL."""
    return TrelloClient(
        api_key="test-key", token="test-token", base_url="https://api.trello.com/1"
    )
