from repositories.ads import AdsRepository
from services.ads import AdsService
from repositories.users import UsersRepository
from services.users import UsersService
from repositories.links import LinksRepository
from services.links import LinksService


def ads_service():
    return AdsService(AdsRepositoryd)


def users_service():
    return UsersService(UsersRepository)


def links_service():
    return LinksService(LinksRepository)
