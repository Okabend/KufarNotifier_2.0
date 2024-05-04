from models.links import Links
from utils.repository import SQLAlchemyRepository


class LinksRepository(SQLAlchemyRepository):
    model = Links
