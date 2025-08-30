from pydantic import BaseModel


class MessageSchema(BaseModel):
    chat_id: int
    text: str
