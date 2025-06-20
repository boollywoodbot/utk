
import os
import requests
from pyrogram import Client, filters
from pyrogram.types import Message

API_ID = int(os.getenv("21905616"))
API_HASH = os.getenv("0506d1a8b04f4c580c369b47c885bbd4")
BOT_TOKEN = os.getenv("7735934554:AAGDkofvouEZa2--j66oX5v3tAJ6UAyx9w0")

app = Client("utkarsh_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

def download_video(url):
    filename = url.split("/")[-2] + ".mp4"
    filepath = os.path.join(DOWNLOAD_FOLDER, filename)
    r = requests.get(url, stream=True)
    r.raise_for_status()
    with open(filepath, "wb") as f:
        for chunk in r.iter_content(chunk_size=1024*1024):
            if chunk:
                f.write(chunk)
    return filepath

@app.on_message(filters.document & filters.private)
async def handle_txt_file(client, message: Message):
    file = await message.download()
    await message.reply("📥 .txt फ़ाइल मिली — वीडियो लिंक पढ़ रहा हूँ...")

    with open(file, "r") as f:
        lines = f.readlines()

    total = 0
    for line in lines:
        if "enc_plain_mp4" in line and ".mp4" in line:
            url = line.strip().split()[-1]
            try:
                await message.reply(f"⬇️ Downloading: {url}")
                video_path = download_video(url)
                await message.reply_video(video=video_path)
                total += 1
            except Exception as e:
                await message.reply(f"❌ Error downloading video: {e}")

    await message.reply(f"✅ {total} वीडियो भेज दिए गए।")

app.run()
