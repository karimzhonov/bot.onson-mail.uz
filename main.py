from fastapi import FastAPI
from contextlib import asynccontextmanager
from bot import set_webhook, delete_webhook, send_message
from schemas import MessageSchema

app = FastAPI()


@asynccontextmanager
async def bot_lifespan(app_instance: FastAPI):
    await set_webhook()    
    yield
    await delete_webhook()  


@app.get("/ping")
async def ping():
    return {"status": "ok"}


@app.post("/message")
async def message(data: MessageSchema):
    return await send_message(data)
