from aiogram import Bot, Dispatcher
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.exceptions import AiogramError
from config import BOT_TOKEN, WEBHOOK_URL, BASE_SITE
from schemas import MessageSchema
from logger import logging

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())


@dp.message()
async def handle_any_message(message: Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="🌐 Перейти в личный кабинет",
                web_app=WebAppInfo(url=BASE_SITE)
            )
        ]
    ])

    await message.answer(
        "*Добро пожаловать в Onson Mail!*\n\n"
        "📦 Карго | ✈️ Туризм",
        reply_markup=kb
    )


async def set_webhook():
    await bot.set_webhook(
        WEBHOOK_URL, 
        allowed_updates=dp.resolve_used_update_types(),
        drop_pending_updates=True
    )
    logging.info(f"Webhook установлен: {WEBHOOK_URL}")


async def delete_webhook():
    await bot.delete_webhook()
    logging.info("Webhook удалён")


async def send_message(message: MessageSchema):
    try:
        await bot.send_message(chat_id=message.chat_id, text=message.text)
        return {'status': 'ok'}
    except AiogramError as e:
        logging.error(f"Ошибка при отправке сообщения: {e}")
        return {'status': 'error'}
