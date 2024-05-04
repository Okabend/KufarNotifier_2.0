from pydantic import BaseModel


class UserSchema(BaseModel):
    id: int
    name: str
    search_interval: int

    class Config:
        from_attributes = True


class UserSchemaAdd(BaseModel):
    id: int
    name: str
    search_interval: int
