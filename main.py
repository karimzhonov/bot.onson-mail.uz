from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
from config import  DEBUG
from bot import set_webhook, delete_webhook, send_message, feed_update
from schemas import MessageSchema
from logger import logging
from db.utils import register_tortoise

@asynccontextmanager
async def lifespan(app_instance: FastAPI):
    if not DEBUG:
        await set_webhook()
    yield
    if not DEBUG:
        await delete_webhook()


app = FastAPI(
    lifespan=lifespan
)
register_tortoise(app)

@app.get("/ping")
async def ping():
    return {"status": "ok"}


@app.post("/webhook")
async def webhook(request: Request) -> None:
    logging.info("Received webhook request")
    update = await request.json()  # Получаем данные из запроса
    # Обрабатываем обновление через диспетчер (dp) и передаем в бот
    await feed_update(update)
    logging.info("Update processed")


@app.post("/message")
async def message(data: MessageSchema):
    return await send_message(data)
