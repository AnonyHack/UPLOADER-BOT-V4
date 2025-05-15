# ©️ LISA-KOREA | @LISA_FAN_LK | NT_BOT_CHANNEL | @NT_BOTS_SUPPORT | LISA-KOREA/UPLOADER-BOT-V4

# [⚠️ Do not change this repo link ⚠️] :- https://github.com/LISA-KOREA/UPLOADER-BOT-V4


import os
from plugins.config import Config
from pyrogram import Client
from pyrogram.types import Message
from pyrogram import filters
from plugins.database.database import db  # Import database for user access

if __name__ == "__main__" :
    
    if not os.path.isdir(Config.DOWNLOAD_LOCATION):
        os.makedirs(Config.DOWNLOAD_LOCATION)
    plugins = dict(root="plugins")
    Client = Client("@Urluploader4GBbot",
    bot_token=Config.BOT_TOKEN,
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    sleep_threshold=300,
    plugins=plugins)
    print("🎊 I AM ALIVE 🎊  • Support @MEGAHUBBOTS")
    Client.run()

@Client.on_message(filters.command('broadcast2') & filters.user(Config.OWNER_ID))
async def broadcast2_handler(client, message: Message):
    if len(message.command) < 2:
        await message.reply_text("Usage: /broadcast2 <message>", quote=True)
        return
    
    broadcast_message = message.text.split(None, 1)[1]
    total_users = 0
    sent_count = 0
    failed_count = 0

    async for user in db.get_all_users():
        total_users += 1
        try:
            await client.send_message(chat_id=user['id'], text=broadcast_message)
            sent_count += 1
        except Exception:
            failed_count += 1

    await message.reply_text(
        text=f"Broadcast2 completed.\n\n"
             f"**Total Users:** {total_users}\n"
             f"**Messages Sent:** {sent_count}\n"
             f"**Failed:** {failed_count}",
        quote=True
    )
