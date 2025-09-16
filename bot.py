import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo, Update
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.exceptions import AiogramError
from db.utils import init_tortoise
from db.models.telegram import ReferralLink
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
                text="Открыть",
                web_app=WebAppInfo(url=BASE_SITE)
            )
        ]
    ])

    args = message.text.split()

    if len(args) > 1:
        ref_id = args[1]
        ref_exists = await ReferralLink.filter(user_id=message.from_user.id).exists()
        if not ref_exists:
            await ReferralLink.create(
                owner_id=ref_id,
                user_id=message.from_user.id
            )

    await message.answer(
        """Onson Mail Group - это динамично развивающаяся компания, предоставляющая профессиональные услуги в сфере грузоперевозок, туризма и консалтинга. Мы стремимся к совершенству, предлагая надежные решения, ориентированные на потребности наших клиентов. Присоединитесь к нам!!!""",
        reply_markup=kb
    )


async def feed_update(data):
    update = Update(**data)
    await dp.feed_update(bot, update)


async def set_webhook():
    info = await bot.get_webhook_info()
    if info.url == WEBHOOK_URL:
        return
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


async def main():
    await init_tortoise()
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
