from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
from bot import set_webhook, delete_webhook, send_message, feed_update
from schemas import MessageSchema
from logger import logging

@asynccontextmanager
async def lifespan(app_instance: FastAPI):
    await set_webhook()    
    yield
    await delete_webhook()  


app = FastAPI(
    lifespan=lifespan
)

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
