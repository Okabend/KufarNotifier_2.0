from typing import Annotated
from fastapi import APIRouter, Depends, Header
from loguru import logger
from api.dependencies import users_service, ads_service, links_service
from aiogram import types
from services.telegram_bot.bot import tg_bot
import config

router = APIRouter(
    prefix="",
    tags=["Telegram"],
)


@router.post(config.TG_WEBHOOK_PATH)
async def bot_webhook(update: dict,
                      x_telegram_bot_api_secret_token: Annotated[str | None, Header()] = None) -> None | dict:
    """ Register webhook endpoint for telegram bot"""
    if x_telegram_bot_api_secret_token != config.TG_MY_TOKEN:
        logger.error("Wrong secret token !")
        return {"status": "error", "message": "Wrong secret token !"}
    telegram_update = types.Update(**update)
    telegram_bot = tg_bot

    await telegram_bot.dp.feed_webhook_update(bot=telegram_bot.bot, update=telegram_update)
