import asyncio
from telegram import Bot
import os


def send_telegram_message(message):
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    bot = Bot(token=bot_token)

    async def async_send_message():
        await bot.send_message(chat_id=chat_id, text=message)

    asyncio.run(async_send_message())
