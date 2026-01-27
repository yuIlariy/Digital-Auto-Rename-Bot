# (c) @RknDeveloperr
# Rkn Developer 
# Don't Remove Credit 😔
# Telegram Channel @RknDeveloper & @Rkn_Botz
# Developer @RknDeveloperr
# Special Thanks To @ReshamOwner
# Update Channel @Digital_Botz & @DigitalBotz_Support
"""
Apache License 2.0
Copyright (c) 2025 @Digital_Botz
"""

# pyrogram imports
from pyrogram import Client, filters
from pyrogram.enums import MessageMediaType
from pyrogram.errors import FloodWait
from pyrogram.file_id import FileId
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ForceReply

# hachoir imports
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from PIL import Image

# bots imports
from helper.utils import progress_for_pyrogram, convert, humanbytes, add_prefix_suffix, remove_path
from helper.database import digital_botz
from config import Config
from plugins.auto_rename import EnhancedAutoRenamer

# extra imports
from asyncio import sleep
import os, time, asyncio

UPLOAD_TEXT = """Uploading Started...."""
DOWNLOAD_TEXT = """Download Started..."""

app = Client("4gb_FileRenameBot", api_id=Config.API_ID, api_hash=Config.API_HASH, session_string=Config.STRING_SESSION)

renamer = EnhancedAutoRenamer()

@Client.on_message(filters.private & (filters.audio | filters.document | filters.video))
async def rename_start(client, message):
    # 1. Check File Size for Non-Premium/Non-Session users
    rkn_file = getattr(message, message.media.value)
    if not Config.STRING_SESSION:
        if rkn_file.file_size > 2000 * 1024 * 1024:
             return await message.reply_text("Sᴏʀʀy Bʀᴏ Tʜɪꜱ Bᴏᴛ Iꜱ Dᴏᴇꜱɴ'ᴛ Sᴜᴩᴩᴏʀᴛ Uᴩʟᴏᴀᴅɪɴɢ Fɪʟᴇꜱ Bɪɢɢᴇʀ Tʜᴀɴ 2Gʙ+")

    # 2. Gather File Info & Emojis
    filename = rkn_file.file_name
    # Default fallback for filename if missing
    if not filename:
        filename = "unknown_file"
        
    if not "." in filename:
        if "." in filename:
            extn = filename.rsplit('.', 1)[-1]
        else:
            extn = "mkv"
        filename = filename + "." + extn
        
    filesize = humanbytes(rkn_file.file_size)
    mime_type = rkn_file.mime_type
    dcid = FileId.decode(rkn_file.file_id).dc_id
    extension_type = mime_type.split('/')[0]

    # --- EMOJI LOGIC ---
    file_ext = filename.split('.')[-1].lower() if "." in filename else "unknown"

    FILE_TYPE_EMOJIS = {
        "audio": "🎵",
        "video": "🎬",
        "image": "🖼️",
        "application": "📦",
        "text": "📄",
        "font": "🔤",
        "message": "💬",
        "multipart": "🧩",
        "default": "📁"
    }

    EXTENSION_EMOJIS = {
        "zip": "🗜️", "rar": "📚", "7z": "🧳", "tar": "🗂️", "gz": "🧪", "xz": "🧬",
        "pdf": "📕", "apk": "🤖", "exe": "💻", "msi": "🛠️",
        "doc": "📄", "docx": "📄", "ppt": "📊", "pptx": "📊",
        "xls": "📈", "xlsx": "📈", "csv": "📑", "txt": "📝",
        "json": "🧾", "xml": "🧬", "html": "🌐",
        "py": "🐍", "js": "📜", "ts": "📜", "java": "☕", "c": "🔧", "cpp": "🔩",
        "mp3": "🎶", "wav": "🔊", "flac": "🎼",
        "mp4": "🎥", "mkv": "📽️", "mov": "🎞️", "webm": "🌐",
        "jpg": "🖼️", "jpeg": "🖼️", "png": "🖼️", "gif": "🌀", "svg": "📐",
        "ttf": "🔤", "otf": "🔤", "woff": "🔤", "eot": "🔤"
    }

    emoji = EXTENSION_EMOJIS.get(file_ext) or FILE_TYPE_EMOJIS.get(extension_type, FILE_TYPE_EMOJIS["default"])
    # -------------------

    # 3. Send Initial Status Message (Auto-Rename Triggered)
    rkn_processing = await message.reply_text(
        text=f"**🔄 Aᴜᴛᴏ-Rᴇɴᴀᴍᴇ Sᴛᴀʀᴛᴇᴅ...**\n\n"
             f"**__{emoji} Fɪʟᴇ Iɴꜰᴏ:__**\n"
             f"🗃️ Oʀɪɢɪɴᴀʟ: `{filename}`\n"
             f"💾 Sɪᴢᴇ: `{filesize}`\n"
             f"🧬 Tyᴩᴇ: `{mime_type}`\n\n"
             f"⏳ **Pʀᴏᴄᴇꜱꜱɪɴɢ...**"
    )

    user_id = message.from_user.id
    
    # 4. Generate New Filename
    # Extract info from filename
    info = renamer.extract_all_info(filename)

    # Get user's format template (or default)
    user_data = await digital_botz.get_user_data(user_id)
    format_template = user_data.get('format_template', None)
    
    if not format_template:
        format_template = "{original}.{ext}"

    # Apply template
    new_name = renamer.apply_format_template(info, format_template)
    
    # Ensure extension is correct
    if not new_name.endswith(f".{info['extension']}"):
        new_name += f".{info['extension']}"
    
    # Sanitize filename (Fix for 'No such file' errors)
    new_filename = new_name.replace("/", "_").replace("\\", "_")
    
    # 5. Create Directory & Paths
    if not os.path.isdir("Renames"):
        os.makedirs("Renames", exist_ok=True)
        
    file_path = f"Renames/{new_filename}"
    
    # 6. Download
    await rkn_processing.edit(f"📥 **Dᴏᴡɴʟᴏᴀᴅɪɴɢ:**\n`{new_filename}`")
    try:            
        dl_path = await client.download_media(
            message=message, 
            file_name=file_path, 
            progress=progress_for_pyrogram, 
            progress_args=(DOWNLOAD_TEXT, rkn_processing, time.time())
        )                    
    except Exception as e:        
        return await rkn_processing.edit(f"⚠️ Download Error: {e}")
    
    # 7. Extract Duration (Metadata)
    duration = 0
    try:
        parser = createParser(file_path)
        metadata = extractMetadata(parser)
        if metadata and metadata.has("duration"):
            duration = metadata.get('duration').seconds
        if parser:
            parser.close()
    except:
        pass
        
    # 8. Handle Thumbnail & Caption
    ph_path = None
    c_caption = user_data.get('caption', None)
    c_thumb = user_data.get('file_id', None)

    if c_caption:
         try:
             caption = c_caption.format(filename=new_filename, filesize=filesize, duration=convert(duration))
         except Exception as e:             
             caption = f"**{new_filename}**"          
    else:
         caption = f"**{new_filename}**"
 
    # Download Thumbnail if available
    media_thumbs = getattr(rkn_file, 'thumbs', None)
    if (media_thumbs or c_thumb):
         try:
             if c_thumb:
                 ph_path = await client.download_media(c_thumb) 
             else:
                 ph_path = await client.download_media(media_thumbs[0].file_id)
             
             if ph_path and os.path.exists(ph_path):
                 Image.open(ph_path).convert("RGB").save(ph_path)
                 img = Image.open(ph_path)
                 img.resize((320, 320))
                 img.save(ph_path, "JPEG")
         except Exception as e:
             ph_path = None

    # 9. Determine Upload Type
    upload_type = "document" # Default
    if message.media == MessageMediaType.VIDEO:
        upload_type = "video"
    elif message.media == MessageMediaType.AUDIO:
        upload_type = "audio"
    
    await rkn_processing.edit("📤 **Uᴩʟᴏᴀᴅɪɴɢ...**")
    
    # 10. Upload Logic (Auto-Handling Large Files)
    if rkn_file.file_size > 2000 * 1024 * 1024:
        # Large File Logic (Using Session String Client 'app')
        filw, error = await upload_files(
            app, Config.LOG_CHANNEL, upload_type, file_path, 
            ph_path, caption, duration, rkn_processing
        )
        if error:            
            await remove_path(ph_path, file_path, dl_path)
            return await rkn_processing.edit(f"⚠️ Upload Error: {error}")
        
        # Forward to user from Log Channel
        from_chat = filw.chat.id
        mg_id = filw.id
        await asyncio.sleep(2)
        await client.copy_message(message.from_user.id, from_chat, mg_id)     
    else:
        # Regular File Logic (Using Bot Client)
        filw, error = await upload_files(
            client, message.chat.id, upload_type, file_path, 
            ph_path, caption, duration, rkn_processing
        )
        if error:            
            await remove_path(ph_path, file_path, dl_path)
            return await rkn_processing.edit(f"⚠️ Upload Error: {error}")        

    # 11. Cleanup, Success Message & Auto-Delete
    await remove_path(ph_path, file_path, dl_path)
    await rkn_processing.edit("✅ **Uᴩʟᴏᴀᴅᴇᴅ Sᴜᴄᴄᴇꜱꜱꜰᴜʟʟy!**")
    await asyncio.sleep(2) 
    await rkn_processing.delete()
    return

async def upload_files(bot, sender_id, upload_type, file_path, ph_path, caption, duration, rkn_processing):
    """
    Unified function to upload files based on type
    """
    try:
        if not os.path.exists(file_path):
            return None, f"File not found: {file_path}"
            
        if upload_type == "document":
            filw = await bot.send_document(
                sender_id,
                document=file_path,
                thumb=ph_path,
                caption=caption,
                progress=progress_for_pyrogram,
                progress_args=(UPLOAD_TEXT, rkn_processing, time.time()))
        
        elif upload_type == "video":
            filw = await bot.send_video(
                sender_id,
                video=file_path,
                caption=caption,
                thumb=ph_path,
                duration=duration,
                progress=progress_for_pyrogram,
                progress_args=(UPLOAD_TEXT, rkn_processing, time.time()))
        
        elif upload_type == "audio":
            filw = await bot.send_audio(
                sender_id,
                audio=file_path,
                caption=caption,
                thumb=ph_path,
                duration=duration,
                progress=progress_for_pyrogram,
                progress_args=(UPLOAD_TEXT, rkn_processing, time.time()))
        else:
            return None, f"Unknown upload type: {upload_type}"
        
        return filw, None
        
    except Exception as e:
        return None, str(e)
