from typing import Annotated

from fastapi import APIRouter, Depends

from api.dependencies import users_service, ads_service, links_service

router = APIRouter(
    prefix="/telegram",
    tags=["Users"],
)
