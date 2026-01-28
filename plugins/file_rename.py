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
import re

UPLOAD_TEXT = """Uploading Started...."""
DOWNLOAD_TEXT = """Download Started..."""

app = Client("4gb_FileRenameBot", api_id=Config.API_ID, api_hash=Config.API_HASH, session_string=Config.STRING_SESSION)

renamer = EnhancedAutoRenamer()

# --- GLOBAL QUEUES ---
# Input Queue: Stores incoming messages
USER_QUEUE = {} 
# Upload Queue: Stores downloaded files ready for upload
UPLOAD_QUEUE = {}
# Workers: Stores the async tasks
WORKERS = {}
# ---------------------

@Client.on_message(filters.private & (filters.audio | filters.document | filters.video))
async def rename_start(client, message):
    user_id = message.from_user.id

    # 1. Initialize Queue for User
    if user_id not in USER_QUEUE:
        USER_QUEUE[user_id] = []
    
    # 2. Add Message to Queue
    USER_QUEUE[user_id].append(message)
    
    # 3. Check if Workers are already running
    if user_id in WORKERS:
        # Worker is running, so this is just queued
        pos = len(USER_QUEUE[user_id])
        await message.reply_text(f"✅ **Added to Queue!**\nPosition: {pos}", quote=True)
        return

    # 4. Start Workers (Download & Upload run in parallel)
    if user_id not in UPLOAD_QUEUE:
        UPLOAD_QUEUE[user_id] = asyncio.Queue()
        
    # Create background tasks
    dl_task = asyncio.create_task(download_worker(client, user_id))
    ul_task = asyncio.create_task(upload_worker(client, user_id))
    WORKERS[user_id] = {'dl': dl_task, 'ul': ul_task}

async def download_worker(client, user_id):
    """
    Worker 1: Downloads files, extracts info, puts them in Upload Queue.
    Starts next download immediately after finishing the current one.
    """
    try:
        while user_id in USER_QUEUE and USER_QUEUE[user_id]:
            # --- SORTING LOGIC ---
            def get_sort_key(msg):
                try:
                    file_val = getattr(msg, msg.media.value)
                    fname = file_val.file_name or ""
                    info = renamer.extract_all_info(fname)
                    
                    season = int(info['season'].upper().replace("S", "")) if info.get('season') else 0
                    episode = int(info['episode'].upper().replace("E", "")) if info.get('episode') else 0
                    return (season, episode)
                except:
                    return (999, 999)

            # Sort Queue
            USER_QUEUE[user_id].sort(key=get_sort_key)
            
            # Pop First Message
            message = USER_QUEUE[user_id].pop(0)
            
            # --- PROCESS DOWNLOAD ---
            try:
                # Basic Checks
                rkn_file = getattr(message, message.media.value)
                if not Config.STRING_SESSION:
                    if rkn_file.file_size > 2000 * 1024 * 1024:
                        await message.reply_text("Sᴏʀʀy Bʀᴏ Tʜɪꜱ Bᴏᴛ Iꜱ Dᴏᴇꜱɴ'ᴛ Sᴜᴩᴩᴏʀᴛ Uᴩʟᴏᴀᴅɪɴɢ Fɪʟᴇꜱ Bɪɢɢᴇʀ Tʜᴀɴ 2Gʙ+")
                        continue

                filename = rkn_file.file_name or "unknown_file"
                if "." in filename:
                    extn = filename.rsplit('.', 1)[-1]
                else:
                    extn = "mkv"
                    filename = filename + "." + extn
                
                # Emojis & Text
                filesize = humanbytes(rkn_file.file_size)
                mime_type = rkn_file.mime_type
                extension_type = mime_type.split('/')[0]
                file_ext = filename.split('.')[-1].lower() if "." in filename else "unknown"

                FILE_TYPE_EMOJIS = {
                    "audio": "🎵", "video": "🎬", "image": "🖼️", "application": "📦", "default": "📁"
                }
                EXTENSION_EMOJIS = {
                    "mkv": "📽️", "mp4": "🎥", "zip": "🗜️", "rar": "📚", "pdf": "📕", "txt": "📝", "py": "🐍", "jpg": "🖼️"
                }
                emoji = EXTENSION_EMOJIS.get(file_ext) or FILE_TYPE_EMOJIS.get(extension_type, FILE_TYPE_EMOJIS["default"])

                # Send Status
                rkn_processing = await message.reply_text(
                    text=f"**🔄 Aᴜᴛᴏ-Rᴇɴᴀᴍᴇ Sᴛᴀʀᴛᴇᴅ...**\n\n"
                         f"**__{emoji} Fɪʟᴇ Iɴꜰᴏ:__**\n"
                         f"🗃️ Oʀɪɢɪɴᴀʟ: `{filename}`\n"
                         f"💾 Sɪᴢᴇ: `{filesize}`\n"
                         f"🧬 Tyᴩᴇ: `{mime_type}`\n\n"
                         f"⏳ **Pʀᴏᴄᴇꜱꜱɪɴɢ...**"
                )

                # Rename Logic
                info = renamer.extract_all_info(filename)
                user_data = await digital_botz.get_user_data(user_id)
                format_template = user_data.get('format_template', "{original}.{ext}")
                new_name = renamer.apply_format_template(info, format_template)
                
                if not new_name.endswith(f".{info['extension']}"):
                    new_name += f".{info['extension']}"
                new_filename = new_name.replace("/", "_").replace("\\", "_")
                
                if not os.path.isdir("Renames"): os.makedirs("Renames", exist_ok=True)
                file_path = f"Renames/{new_filename}"

                # Download
                await rkn_processing.edit(f"📥 **Dᴏᴡɴʟᴏᴀᴅɪɴɢ:**\n`{new_filename}`")
                dl_path = await client.download_media(
                    message=message, 
                    file_name=file_path, 
                    progress=progress_for_pyrogram, 
                    progress_args=(DOWNLOAD_TEXT, rkn_processing, time.time())
                )

                # Metadata & Thumbnail
                duration = 0
                try:
                    parser = createParser(file_path)
                    metadata = extractMetadata(parser)
                    if metadata and metadata.has("duration"):
                        duration = metadata.get('duration').seconds
                    if parser: parser.close()
                except: pass
                
                ph_path = None
                c_caption = user_data.get('caption', None)
                c_thumb = user_data.get('file_id', None)
                
                caption = f"**{new_filename}**"
                if c_caption:
                    try:
                        caption = c_caption.format(filename=new_filename, filesize=filesize, duration=convert(duration))
                    except: pass
                
                media_thumbs = getattr(rkn_file, 'thumbs', None)
                if (media_thumbs or c_thumb):
                    try:
                        thumb_to_dl = c_thumb if c_thumb else media_thumbs[0].file_id
                        ph_path = await client.download_media(thumb_to_dl)
                        if ph_path and os.path.exists(ph_path):
                            Image.open(ph_path).convert("RGB").save(ph_path)
                            img = Image.open(ph_path)
                            img.resize((320, 320))
                            img.save(ph_path, "JPEG")
                    except: ph_path = None

                # Determine Type
                upload_type = "document"
                if message.media == MessageMediaType.VIDEO: upload_type = "video"
                elif message.media == MessageMediaType.AUDIO: upload_type = "audio"

                # Update Status and Push to Upload Queue
                await rkn_processing.edit("⏳ **Rᴇᴀᴅy ᴛᴏ Uᴩʟᴏᴀᴅ...**")
                
                upload_data = {
                    'message': message,
                    'file_path': file_path,
                    'ph_path': ph_path,
                    'caption': caption,
                    'duration': duration,
                    'rkn_processing': rkn_processing,
                    'upload_type': upload_type,
                    'file_size': rkn_file.file_size
                }
                
                await UPLOAD_QUEUE[user_id].put(upload_data)
                
            except Exception as e:
                print(f"Download Error: {e}")
                try: await rkn_processing.edit(f"⚠️ Error: {e}")
                except: pass

            # Loop continues immediately to download the NEXT file
            await asyncio.sleep(1)

    except Exception as e:
        print(f"DL Worker Error: {e}")
    finally:
        # Signal Upload Worker to stop
        await UPLOAD_QUEUE[user_id].put(None)

async def upload_worker(client, user_id):
    """
    Worker 2: Uploads files sequentially from the queue.
    """
    try:
        while True:
            data = await UPLOAD_QUEUE[user_id].get()
            
            if data is None:
                # Sentinel value received, stop worker
                break
                
            # Extract Data
            message = data['message']
            file_path = data['file_path']
            ph_path = data['ph_path']
            caption = data['caption']
            duration = data['duration']
            rkn_processing = data['rkn_processing']
            upload_type = data['upload_type']
            file_size = data['file_size']
            
            # Start Upload
            await rkn_processing.edit("📤 **Uᴩʟᴏᴀᴅɪɴɢ...**")
            
            # Choose correct client (Bot vs Session)
            uploader = app if (Config.STRING_SESSION and file_size > 2000 * 1024 * 1024) else client
            
            try:
                filw, error = await upload_files(
                    uploader, 
                    Config.LOG_CHANNEL if uploader == app else message.chat.id, 
                    upload_type, 
                    file_path, 
                    ph_path, 
                    caption, 
                    duration, 
                    rkn_processing
                )

                if error:
                    await rkn_processing.edit(f"⚠️ Upload Error: {error}")
                else:
                    # If uploaded via Session, forward to user
                    if uploader == app:
                        await asyncio.sleep(2)
                        await client.copy_message(message.from_user.id, filw.chat.id, filw.id)
                    
                    # Success
                    await rkn_processing.edit("✅ **Uᴩʟᴏᴀᴅᴇᴅ Sᴜᴄᴄᴇꜱꜱꜰᴜʟʟy!**")
                    await asyncio.sleep(2)
                    await rkn_processing.delete()

            except Exception as e:
                await rkn_processing.edit(f"⚠️ Error: {e}")
            finally:
                # Cleanup Files
                await remove_path(ph_path, file_path)
            
            # Loop continues to next upload
            
    except Exception as e:
        print(f"UL Worker Error: {e}")
    finally:
        # Cleanup Globals
        if user_id in WORKERS: del WORKERS[user_id]
        if user_id in UPLOAD_QUEUE: del UPLOAD_QUEUE[user_id]
        if user_id in USER_QUEUE: del USER_QUEUE[user_id]

async def upload_files(bot, sender_id, upload_type, file_path, ph_path, caption, duration, rkn_processing):
    try:
        if not os.path.exists(file_path):
            return None, f"File not found: {file_path}"
            
        if upload_type == "document":
            filw = await bot.send_document(
                sender_id, document=file_path, thumb=ph_path, caption=caption,
                progress=progress_for_pyrogram, progress_args=(UPLOAD_TEXT, rkn_processing, time.time()))
        
        elif upload_type == "video":
            filw = await bot.send_video(
                sender_id, video=file_path, caption=caption, thumb=ph_path, duration=duration,
                progress=progress_for_pyrogram, progress_args=(UPLOAD_TEXT, rkn_processing, time.time()))
        
        elif upload_type == "audio":
            filw = await bot.send_audio(
                sender_id, audio=file_path, caption=caption, thumb=ph_path, duration=duration,
                progress=progress_for_pyrogram, progress_args=(UPLOAD_TEXT, rkn_processing, time.time()))
        else:
            return None, f"Unknown upload type: {upload_type}"
        
        return filw, None
        
    except Exception as e:
        return None, str(e)
