"""Async Trello API client using httpx."""

import httpx

from trello_mcp.models import (
    TrelloBoard,
    TrelloCard,
    TrelloCheckItem,
    TrelloChecklist,
    TrelloCustomField,
    TrelloLabel,
    TrelloList,
)


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

    async def _put_json(self, path: str, body: dict) -> dict:
        resp = await self._client.put(path, params=self._auth, json=body)
        resp.raise_for_status()
        return resp.json()

    async def _delete(self, path: str) -> None:
        resp = await self._client.delete(path, params=self._auth)
        resp.raise_for_status()

    # --- Boards ---

    async def list_boards(self) -> list[TrelloBoard]:
        data = await self._get("/members/me/boards", {"fields": "name,desc,url,closed"})
        return [TrelloBoard(**b) for b in data]

    async def search_board(self, query: str) -> list[TrelloBoard]:
        boards = await self.list_boards()
        q = query.lower()
        return [b for b in boards if q in b.name.lower()]

    # --- Lists ---

    async def list_lists(self, board_id: str) -> list[TrelloList]:
        data = await self._get(f"/boards/{board_id}/lists")
        return [TrelloList(**lst) for lst in data]

    async def create_list(self, board_id: str, name: str) -> TrelloList:
        data = await self._post("/lists", {"name": name, "idBoard": board_id})
        return TrelloList(**data)

    async def update_list(
        self, list_id: str, name: str | None = None, closed: bool | None = None
    ) -> TrelloList:
        params: dict = {}
        if name is not None:
            params["name"] = name
        if closed is not None:
            params["closed"] = str(closed).lower()
        data = await self._put(f"/lists/{list_id}", params)
        return TrelloList(**data)

    async def archive_list(self, list_id: str) -> TrelloList:
        return await self.update_list(list_id, closed=True)

    # --- Cards ---

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

    async def update_card(
        self, card_id: str, name: str | None = None, desc: str | None = None
    ) -> TrelloCard:
        params = {}
        if name is not None:
            params["name"] = name
        if desc is not None:
            params["desc"] = desc
        data = await self._put(f"/cards/{card_id}", params)
        return TrelloCard(**data)

    async def add_comment(self, card_id: str, text: str) -> dict:
        return await self._post(f"/cards/{card_id}/actions/comments", {"text": text})

    async def archive_card(self, card_id: str) -> TrelloCard:
        data = await self._put(f"/cards/{card_id}", {"closed": "true"})
        return TrelloCard(**data)

    # --- Card Due Dates ---

    async def set_due_date(self, card_id: str, due: str) -> TrelloCard:
        data = await self._put(f"/cards/{card_id}", {"due": due})
        return TrelloCard(**data)

    async def mark_due_complete(self, card_id: str, complete: bool) -> TrelloCard:
        data = await self._put(f"/cards/{card_id}", {"dueComplete": str(complete).lower()})
        return TrelloCard(**data)

    # --- Checklists ---

    async def get_checklists(self, card_id: str) -> list[TrelloChecklist]:
        data = await self._get(f"/cards/{card_id}/checklists")
        return [TrelloChecklist(**cl) for cl in data]

    async def create_checklist(self, card_id: str, name: str) -> TrelloChecklist:
        data = await self._post(f"/cards/{card_id}/checklists", {"name": name})
        return TrelloChecklist(**data)

    async def delete_checklist(self, checklist_id: str) -> None:
        await self._delete(f"/checklists/{checklist_id}")

    async def add_check_item(self, checklist_id: str, name: str) -> TrelloCheckItem:
        data = await self._post(f"/checklists/{checklist_id}/checkItems", {"name": name})
        return TrelloCheckItem(**data)

    async def update_check_item(
        self,
        card_id: str,
        checklist_id: str,
        check_item_id: str,
        state: str | None = None,
        name: str | None = None,
    ) -> TrelloCheckItem:
        params: dict = {}
        if state is not None:
            params["state"] = state
        if name is not None:
            params["name"] = name
        data = await self._put(
            f"/cards/{card_id}/checklist/{checklist_id}/checkItem/{check_item_id}", params
        )
        return TrelloCheckItem(**data)

    async def delete_check_item(self, checklist_id: str, check_item_id: str) -> None:
        await self._delete(f"/checklists/{checklist_id}/checkItems/{check_item_id}")

    # --- Labels ---

    async def get_board_labels(self, board_id: str) -> list[TrelloLabel]:
        data = await self._get(f"/boards/{board_id}/labels")
        return [TrelloLabel(**lbl) for lbl in data]

    async def create_label(self, board_id: str, name: str, color: str) -> TrelloLabel:
        data = await self._post("/labels", {"idBoard": board_id, "name": name, "color": color})
        return TrelloLabel(**data)

    async def add_label_to_card(self, card_id: str, label_id: str) -> None:
        await self._post(f"/cards/{card_id}/idLabels", {"value": label_id})

    async def remove_label_from_card(self, card_id: str, label_id: str) -> None:
        await self._delete(f"/cards/{card_id}/idLabels/{label_id}")

    # --- Custom Fields ---

    async def get_custom_fields(self, board_id: str) -> list[TrelloCustomField]:
        data = await self._get(f"/boards/{board_id}/customFields")
        return [TrelloCustomField(**cf) for cf in data]

    async def set_card_custom_field(self, card_id: str, field_id: str, value: dict) -> dict:
        return await self._put_json(
            f"/cards/{card_id}/customField/{field_id}/item", {"value": value}
        )
