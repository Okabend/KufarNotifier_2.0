from schemas.ads import AdSchemaAdd
from utils.repository import AbstractRepository


class AdsService:
    def __init__(self, ads_repo: AbstractRepository):
        self.ads_repo: AbstractRepository = ads_repo()

    async def add_ads(self, ad: AdSchemaAdd):
        ads_dict = ad.model_dump()
        ad_id = await self.ads_repo.add_one(ads_dict)
        return ad_id

    async def get_ads(self):
        ads = await self.ads_repo.find_all()
        return ads
