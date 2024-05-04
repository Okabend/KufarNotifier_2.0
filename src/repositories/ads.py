from models.ads import Ads
from utils.repository import SQLAlchemyRepository


class AdsRepository(SQLAlchemyRepository):
    model = Ads
