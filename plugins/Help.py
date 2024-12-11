from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

@Client.on_message(filters.command("link"))
async def generate_link(client, message):
    command_text = message.text.split(maxsplit=1)
    if len(command_text) < 2:
        await message.reply("❗️How to Search Movies Here❓/n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n1. Just Send Movie Name and Movie Released Year Correctly.\n<blockquote>(Check Google for Correct Movie Spelling and Movie Released Year)</blockquote>/n/n")
        return
