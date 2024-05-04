from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from db.db import Base
from schemas.users import UserSchema


class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    search_interval: Mapped[int]

    def to_read_model(self) -> UserSchema:
        return UserSchema(
            id=self.id,
            name=self.name,
            search_interval=self.search_interval,
        )
