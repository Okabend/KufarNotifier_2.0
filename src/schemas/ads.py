from pydantic import BaseModel


class AdSchema(BaseModel):
    id: int
    url: str
    header: str
    address: str
    price: str
    photo_url: str
    link_id: int

    class Config:
        from_attributes = True


class AdSchemaAdd(BaseModel):
    pass
