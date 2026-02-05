"""Async Trello API client using httpx."""

import httpx

from trello_mcp.models import TrelloBoard, TrelloCard, TrelloList


class TrelloClient:
    """Async client for the Trello REST API."""

    def __init__(self, api_key: str, token: str, base_url: str = "https://api.trello.com/1"):
        self.base_url = base_url
        self._auth = {"key": api_key, "token": token}
        self._client = httpx.AsyncClient(base_url=base_url, timeout=30.0)

    async def close(self):
        await self._client.aclose()

    async def _get(self, path: str, params: dict | None = None) -> list | dict:
        merged = {**self._auth, **(params or {})}
        resp = await self._client.get(path, params=merged)
        resp.raise_for_status()
        return resp.json()

    async def _post(self, path: str, params: dict | None = None) -> dict:
        merged = {**self._auth, **(params or {})}
        resp = await self._client.post(path, params=merged)
        resp.raise_for_status()
        return resp.json()

    async def _put(self, path: str, params: dict | None = None) -> dict:
        merged = {**self._auth, **(params or {})}
        resp = await self._client.put(path, params=merged)
        resp.raise_for_status()
        return resp.json()

    async def list_boards(self) -> list[TrelloBoard]:
        data = await self._get("/members/me/boards", {"fields": "name,desc,url,closed"})
        return [TrelloBoard(**b) for b in data]

    async def list_lists(self, board_id: str) -> list[TrelloList]:
        data = await self._get(f"/boards/{board_id}/lists")
        return [TrelloList(**lst) for lst in data]

    async def list_cards(self, list_id: str) -> list[TrelloCard]:
        data = await self._get(f"/lists/{list_id}/cards")
        return [TrelloCard(**c) for c in data]

    async def get_board_cards(self, board_id: str) -> list[TrelloCard]:
        data = await self._get(f"/boards/{board_id}/cards")
        return [TrelloCard(**c) for c in data]

    async def create_card(self, list_id: str, name: str, desc: str = "") -> TrelloCard:
        params = {"idList": list_id, "name": name}
        if desc:
            params["desc"] = desc
        data = await self._post("/cards", params)
        return TrelloCard(**data)

    async def move_card(self, card_id: str, list_id: str) -> TrelloCard:
        data = await self._put(f"/cards/{card_id}", {"idList": list_id})
        return TrelloCard(**data)

    async def add_comment(self, card_id: str, text: str) -> dict:
        return await self._post(f"/cards/{card_id}/actions/comments", {"text": text})

    async def archive_card(self, card_id: str) -> TrelloCard:
        data = await self._put(f"/cards/{card_id}", {"closed": "true"})
        return TrelloCard(**data)

    async def search_board(self, query: str) -> list[TrelloBoard]:
        boards = await self.list_boards()
        q = query.lower()
        return [b for b in boards if q in b.name.lower()]
