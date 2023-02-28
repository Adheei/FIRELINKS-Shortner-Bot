# Made with python3
# (C) @trtechguide
# Copyright permission under MIT License
# All rights reserved by TRTECHGUIDE
# License -> https://github.com/TR-TECH-GUIDE/URL-Shortner-Bot/blob/main/LICENSE

import os
import aiohttp
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InlineQueryResultArticle, InputTextMessageContent
from pyshorteners import Shortener

FIRELINKS_API = os.environ.get("FIRELINKS_API", "4b4ee8f8717d775262ef74432e202b8be8597b62")

BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton(text='⚙ Join Updates Channel ⚙', url='https://telegram.me/Lmcbots')
        ]]
    )

@Client.on_message(filters.private & filters.regex(r'https?://[^\s]+'))
async def reply_shortens(bot, update):
    message = await update.reply_text(
        text="`Analysing your link...`",
        disable_web_page_preview=True,
        quote=True
    )
    link = update.matches[0].group(0)
    shorten_urls = await short(link)
    await message.edit_text(
        text=shorten_urls,
        reply_markup=BUTTONS,
        disable_web_page_preview=True
    )

@Client.on_inline_query(filters.regex(r'https?://[^\s]+'))
async def inline_short(bot, update):
    link = update.matches[0].group(0)
    shorten_urls = await short(link)
    answers = [
        InlineQueryResultArticle(
            title="Short Links",
            description=update.query,
            input_message_content=InputTextMessageContent(
                message_text=shorten_urls,
                disable_web_page_preview=True
            ),
            reply_markup=BUTTONS
        )
    ]
    await bot.answer_inline_query(
        inline_query_id=update.id,
        results=answers
    )

async def short(link):
    shorten_urls = "**--Shorted URLs--**\n"
  
    # FireLinks shorten
    try:
        api_url = "https://fire-links.in/api"
        params = {'api': FIRELINKS_API, 'url': link}
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url, params=params, raise_for_status=True) as response:
                data = await response.json()
                url = data["shortenedUrl"]
                shorten_urls += f"\n**fire-Links.in :-** {url}"
    except Exception as error:
        print(f"FireLinks error :- {error}")
    
    # Send the text
    try:
        shorten_urls += "\n\nMade by @Lmcbots"
        return shorten_urls
    except Exception as error:
        return error
