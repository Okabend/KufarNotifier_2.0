from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from db.db import Base
from schemas.links import LinkSchema


class Links(Base):
    __tablename__ = "links"

    id: Mapped[int] = mapped_column(primary_key=True)
    url: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    added_at: Mapped[datetime]
    link_tag: Mapped[Optional[str]]

    def to_read_model(self) -> LinkSchema:
        return LinkSchema(
            id=self.id,
            url=self.url,
            user_id=self.user_id,
            added_at=self.added_at,
            link_tag=self.link_tag,
        )
