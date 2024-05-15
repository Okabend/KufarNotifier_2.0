import uvicorn
from fastapi import FastAPI
from api.routers import all_routers
from services import telegram_bot
import config
import asyncio
from loguru import logger

app = FastAPI(
    title="Куфар парсинг-бот с оповещением в тг"
)


@app.on_event("startup")
async def startup_event():
    """actions on start app"""
    logger.info('Start')


@app.on_event("shutdown")
def shutdown_event():
    """actions on shutdown app"""
    logger.info('Finish')


for router in all_routers:
    app.include_router(router)


if __name__ == "__main__":
    telegram_bot = telegram_bot.bot.tg_bot
    asyncio.run(telegram_bot.start())
    uvicorn.run(app="main:app", reload=True)
