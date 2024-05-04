import uvicorn
from fastapi import FastAPI

from api.routers import all_routers


app = FastAPI(
    title="Куфар парсинг-бот с оповещением в тг"
)


for router in all_routers:
    app.include_router(router)


if __name__ == "__main__":
    uvicorn.run(app="main:app", reload=True)