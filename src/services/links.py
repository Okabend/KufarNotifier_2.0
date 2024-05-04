from schemas.links import LinkSchemaAdd
from utils.repository import AbstractRepository


class LinksService:
    def __init__(self, links_repo: AbstractRepository):
        self.links_repo: AbstractRepository = links_repo()

    async def add_link(self, link: LinkSchemaAdd):
        links_dict = link.model_dump()
        link_id = await self.links_repo.add_one(links_dict)
        return link_id

    async def get_links(self):
        links = await self.links_repo.find_all()
        return links
