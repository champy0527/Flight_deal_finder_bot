import asyncio
from telegram import Bot
import os
from dotenv import load_dotenv

BOT_TOKEN = os.getenv("TLGRM_BOT_TOKEN")
bot_chat_id = os.getenv("TLGRM_CHAT_ID")


async def telegram_bot_sendtext(bot_message):
    bot = Bot(token=BOT_TOKEN)
    await bot.send_message(chat_id=bot_chat_id, text=bot_message)


async def notify_lowest_price(bot_message):
    await telegram_bot_sendtext(bot_message)
