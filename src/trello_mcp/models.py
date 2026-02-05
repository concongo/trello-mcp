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

    model_config = {"populate_by_name": True}
