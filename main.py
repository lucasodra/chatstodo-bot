import asyncio
from pyrogram import Client, filters

import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

app = Client("chats_todo_bot")


@app.on_message(filters.text & filters.private)
async def echo(client, message):
    await message.reply(message.text)


app.run()
