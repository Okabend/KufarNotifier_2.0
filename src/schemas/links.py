from pydantic import BaseModel
from datetime import datetime


class LinkSchema(BaseModel):
    id: int
    url: str
    user_id: int
    added_at: datetime
    link_tag: str

    class Config:
        from_attributes = True


class LinkSchemaAdd(BaseModel):
    pass
