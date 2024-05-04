from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from db.db import Base
from schemas.ads import AdSchema


class Ads(Base):
    __tablename__ = "ads"

    id: Mapped[int] = mapped_column(primary_key=True)
    url: Mapped[str]
    header: Mapped[str]
    address: Mapped[str]
    price: Mapped[str]
    photo_url: Mapped[Optional[str]]
    link_id: Mapped[int] = mapped_column(ForeignKey("links.id"))

    def to_read_model(self) -> AdSchema:
        return AdSchema(
            id=self.id,
            url=self.url,
            header=self.header,
            address=self.address,
            price=self.price,
            photo_url=self.photo_url,
            link_id=self.link_id,
        )
