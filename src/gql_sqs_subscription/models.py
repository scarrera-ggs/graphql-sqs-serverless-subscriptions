from pydantic import BaseModel, HttpUrl


class CustomBaseModel(BaseModel):
    """Custom class config for data models."""

    class Config:  # noqa
        # Make objects immutable
        frozen = True
        # allow to use aliases and field names when creating a new object
        populate_by_name = True


class ConcertoRequest(CustomBaseModel):
    """Data model for Concerto API Request."""

    method: str
    url: HttpUrl
    headers: dict
    data: dict
    message_attributes: dict
