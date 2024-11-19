from pyrogram import Client, filters
from info import CHANNELS
from database.ia_filterdb import save_file, save_filea, check_file
from utils import get_poster
from pyrogram.types import *
import re

TO_CHANNEL = -1002247041357

media_filter = filters.document | filters.video | filters.audio

@Client.on_message(filters.chat(CHANNELS) & media_filter)
async def media(bot, message):
    """Media Handler"""
    
    def clean_file_name(file_name: str) -> str:
        file_name = file_name.lower().replace('_', ' ').replace('[', '').replace(']', '')

        while '@' in file_name or '#' in file_name:
            start_at = file_name.find('@') if file_name.find('@') != -1 else file_name.find('#')
            end_at = file_name.find(' ', start_at)
            end_at = end_at if end_at != -1 else len(file_name)
            file_name = file_name[:start_at] + file_name[end_at:].strip()

        for keyword in ['s', 'season', 'chapter']:
            file_name = file_name.split(f"{keyword}")[0]  

        return ' '.join(file_name.strip().split()[:4])

    media = None
    for file_type in ("document", "video", "audio"):
        media = getattr(message, file_type, None)
        if media is not None:
            media.file_type = file_type
            break
    else:
        return  

    media.caption = message.caption
    hu = clean_file_name(media.file_name)
    imdbk = await get_poster(hu)
    po = hu.replace(" ", "-")
    name = re.sub("_", " ", media.file_name)
    quality_match = re.search(r"\d{1,4}p", name)
    if quality_match:
        quality = quality_match.group()
        name = re.sub(quality, "", name)
    else:
        quality = "N/A"

    langs = ["tamil", "english", "malayalam", "hindi", "Tamil", "Malyalam", "English", "Hindi", "Telugu", "telugu", "Kannada", "kannada"]
    specified_lang = [word for word in langs if word in name.lower()]
    lang = specified_lang[0] if specified_lang else "N/A"

    btn = [
        [InlineKeyboardButton('📤 Dᴏᴡɴʟᴏᴀᴅ Lɪɴᴋ 📤', url=f'https://t.me/{bot.me.username}?start=getfile-{po}')]
    ]
    reply_markup = InlineKeyboardMarkup(btn)

    tru = await check_file(media)
    if tru == "okda":
        if message.id % 2 == 0:
            await save_file(media)
        else:
            await save_filea(media)
        
        await bot.send_message(chat_id=TO_CHANNEL, text=f"<b>🎬 Title : {imdbk['title']}\n🗓 Year : {imdbk['year']}\n💿 Quality : {quality}\n🔊 Language : {lang}\n\nമൂവി വേണ്ടവർ Dᴏᴡɴʟᴏᴀᴅ Lɪɴᴋ ക്ലിക്ക് ചെയ്യുക..!!!</b>", reply_markup=reply_markup)
    else:
        print("Skipped duplicate file from saving to db 😌")
