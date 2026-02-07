"""Pydantic models for Trello entities and settings."""

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    trello_api_key: str = Field(description="Trello API key")
    trello_token: str = Field(description="Trello OAuth token")
    trello_base_url: str = Field(default="https://api.trello.com/1")

    model_config = {"env_file": ".env"}


class TrelloBoard(BaseModel):
    """A Trello board."""

    id: str
    name: str
    desc: str = ""
    url: str = ""
    closed: bool = False


class TrelloList(BaseModel):
    """A list within a Trello board."""

    id: str
    name: str
    id_board: str = Field(alias="idBoard", default="")
    closed: bool = False

    model_config = {"populate_by_name": True}


class TrelloCard(BaseModel):
    """A card within a Trello list."""

    id: str
    name: str
    desc: str = ""
    id_list: str = Field(alias="idList", default="")
    id_board: str = Field(alias="idBoard", default="")
    url: str = ""
    closed: bool = False
    labels: list[dict] = Field(default_factory=list)
    due: str | None = None
    due_complete: bool = Field(alias="dueComplete", default=False)

    model_config = {"populate_by_name": True}


class TrelloCheckItem(BaseModel):
    """A check item within a checklist."""

    id: str
    name: str
    state: str = "incomplete"
    id_checklist: str = Field(alias="idChecklist", default="")

    model_config = {"populate_by_name": True}


class TrelloChecklist(BaseModel):
    """A checklist on a card."""

    id: str
    name: str
    id_card: str = Field(alias="idCard", default="")
    check_items: list[TrelloCheckItem] = Field(alias="checkItems", default_factory=list)

    model_config = {"populate_by_name": True}


class TrelloLabel(BaseModel):
    """A label on a board."""

    id: str
    name: str = ""
    color: str | None = None
    id_board: str = Field(alias="idBoard", default="")

    model_config = {"populate_by_name": True}


class TrelloCustomField(BaseModel):
    """A custom field definition on a board."""

    id: str
    name: str
    type: str = ""
    id_model: str = Field(alias="idModel", default="")

    model_config = {"populate_by_name": True}
