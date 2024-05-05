import uvicorn
from fastapi import FastAPI
from api.routers import all_routers
from services import telegram_bot
import config
import asyncio

app = FastAPI(
    title="Куфар парсинг-бот с оповещением в тг"
)


for router in all_routers:
    app.include_router(router)


if __name__ == "__main__":
    telegram_bot = telegram_bot.bot.tg_bot
    asyncio.run(telegram_bot.start())
    uvicorn.run(app="main:app", reload=True)
