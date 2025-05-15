import shutil
import psutil
from pyrogram import filters
from pyrogram.types import (
    Message
)
from plugins.config import Config
from pyrogram import Client, enums
from plugins.database.database import db
from plugins.functions.display_progress import humanbytes
from pyrogram import Client

@Client.on_message(filters.private & filters.command('total'))
async def sts(c, m):
    if m.from_user.id != Config.OWNER_ID:
        return 
    total_users = await db.total_users_count()
    await m.reply_text(text=f"<b>Total users:</b> {total_users}", quote=True)


@Client.on_message(filters.command('status') & filters.user(Config.OWNER_ID))
async def status_handler(_, m: Message):
    total, used, free = shutil.disk_usage(".")
    total = humanbytes(total)
    used = humanbytes(used)
    free = humanbytes(free)
    cpu_usage = psutil.cpu_percent()
    ram_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent
    total_users = await db.total_users_count()
    await m.reply_text(
        text=f"**Total Disk Space:** {total} \n"
             f"**Used Space:** {used}({disk_usage}%) \n"
             f"**Free Space:** {free} \n"
             f"**CPU Usage:** {cpu_usage}% \n"
             f"**RAM Usage:** {ram_usage}%\n\n"
             f"**Total Users in DB:** `{total_users}`",
        quote=True
    )


@Client.on_message(filters.command('broadcast') & filters.user(Config.OWNER_ID))
async def broadcast_handler(client, message: Message):
    if len(message.command) < 2:
        await message.reply_text("Usage: /broadcast <message>", quote=True)
        return
    
    broadcast_message = message.text.split(None, 1)[1]
    total_users = await db.total_users_count()
    sent_count = 0
    failed_count = 0

    async for user in db.get_all_users():
        try:
            await client.send_message(chat_id=user['id'], text=broadcast_message)
            sent_count += 1
        except Exception:
            failed_count += 1

    await message.reply_text(
        text=f"Broadcast completed.\n\n"
             f"**Total Users:** {total_users}\n"
             f"**Messages Sent:** {sent_count}\n"
             f"**Failed:** {failed_count}",
        quote=True
    )
