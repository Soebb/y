from os import environ
from yun import Yun
from pyrogram import Client, filters
import requests

API_ID = environ.get('API_ID')
API_HASH = environ.get('API_HASH')
BOT_TOKEN = environ.get('BOT_TOKEN')

bot = Client('bot',
             api_id=API_ID,
             api_hash=API_HASH,
             bot_token=BOT_TOKEN,
             workers=50,
             sleep_threshold=10)


@bot.on_message(filters.command('start') & filters.private)
async def start(bot, message):
    await message.reply(
        f"**Hi {message.chat.first_name}!**\n\n"
        "I'm a specialised bot for shortening Droplink.co links which can help you earn money by just sharing links. I am made by @ToonsHub2006.")


@bot.on_message(filters.regex(r'https?://[^\s]+') & filters.private)
async def link_handler(bot, message):
    api = Yun('509:66zjkr6vbw08csog80swgccgow8owwc')
    result = api.short('title', 'url')
    await message.reply(f'Here is your [`{result}`]({result})', quote=True)

bot.run()
