import os
from os.path import join, dirname
from dotenv import load_dotenv

import asyncio
from pyrogram import Client, filters
from pyrogram.types import BotCommand


dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

app = Client("chats_todo_bot")


@app.on_message(filters.command("start"))
async def handle_start(client, message):
    await message.reply_text(f"Hello, {message.from_user.first_name}! How can I help you today?")


@app.on_message(filters.command("help"))
async def handle_help(client, message):
    await message.reply_text(f"help")


@app.on_message(filters.command("viewgroups"))
async def handle_view_groups(client, message):
    await message.reply_text(f"view groups connected to")


@app.on_message(filters.command("addgroup"))
async def handle_add_group(client, message):
    await message.reply_text(f"add a group to track")


@app.on_message(filters.command("deletegroup"))
async def handle_delete_group(client, message):
    await message.reply_text(f"delete a group from tracking")


@app.on_message(filters.command("all"))
async def handle_do_all_actions(client, message):
    await message.reply_text(f"summary, todo, events")


@app.on_message(filters.command("summary"))
async def handle_do_summary(client, message):
    await message.reply_text(f"summary")


@app.on_message(filters.command("todo"))
async def handle_do_todo(client, message):
    await message.reply_text(f"to dos")


@app.on_message(filters.command("event"))
async def handle_do_event(client, message):
    await message.reply_text(f"events")


@app.on_message(filters.command("feedback"))
async def handle_do_event(client, message):
    await message.reply_text(f"feedback")


async def set_commands():
    await app.set_bot_commands([
        BotCommand("start", "Start interacting with the bot"),
        BotCommand("help", "Get help and instructions on how to use the bot"),
        BotCommand("all", "Get summary, todo and event"),
        BotCommand("viewgroups", "View groups that I am connected to"),
        BotCommand("addgroup", "Add groups to track"),
        BotCommand("deletegroup", "Delete groups from my tracking"),
        BotCommand("summary", "Get summary of group(s)"),
        BotCommand("todo", "Get todo of group(s) "),
        BotCommand("event", "Get event of group(s)"),
        BotCommand("feedback", "Let us know how we can better serve you")
    ])


async def main():
    async with app:
        await set_commands()  # Set bot commands
        print("Bot is running...")
        await asyncio.get_event_loop().create_future()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
