import re, os, time
id_pattern = re.compile(r'^.\d+$') 

class Config(object):
    # digital_botz client config
    API_ID = os.environ.get("API_ID", "rdl")
    API_HASH = os.environ.get("API_HASH", "rdl")
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "rdl") 
    BOT = None

    # premium account string session required 😢 
    STRING_SESSION = os.environ.get("STRING_SESSION", "rdl")
    
    # database config
    DB_NAME = os.environ.get("DB_NAME","DiAuto")     
    DB_URL = os.environ.get("DB_URL","rdl")
 
    # other configs
    RKN_PIC = os.environ.get("RKN_PIC", "https://i.ibb.co/fzgHjXQn/1752254564132.png")
    ADMIN = [int(admin) if id_pattern.search(admin) else admin for admin in os.environ.get('ADMIN', '6318135266').split()]
    LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", "-1001925329161"))

    # free upload limit 
    FREE_UPLOAD_LIMIT = 6442450944 # calculation 6*1024*1024*1024=results

    # premium mode feature ✅
    UPLOAD_LIMIT_MODE = True 
    PREMIUM_MODE = True 
    
    #force subs
    try:
        FORCE_SUB = int(os.environ.get("FORCE_SUB", "")) 
    except:
        FORCE_SUB = os.environ.get("FORCE_SUB", "OtherBs")
        
    # wes response configuration     
    PORT = int(os.environ.get("PORT", "8720"))
    BOT_UPTIME = time.time()

class rkn(object):
    # part of text configuration
    START_TXT = """👋 <b>Hello, {}!</b>

<b>Welcome to the Fast and simple file renaming Bot.</b>

Send a file to get started.

🛠 <b>Key features:</b>
• Quick Auto Rename files  
• Custom captions  
• Convert videos & documents  
• Customize thumbnails  

🌟 <i>Lightning-fast with premium enchantments!</i>

🛸 <i>Powered By</i> <a href="https://t.me/xspes">NAm</a> <b>|</b> 🪄 <i>Spell Weaver</i>"""

    ABOUT_TXT = """🪄 <b>BOT PROFILE</b> 🔮

├ 🎯 <b>Name:</b> {}
├ 🛠️ <b>Developers:</b> {}
├ 💻 <b>Programer:</b> {}
├ 📦 <b>Library:</b> {}
├ 🐍 <b>Language:</b> {}
├ 🗃️ <b>Data Base:</b> {}
├ ☁️ <b>Server:</b> <a href='https://deluxhost.net//'>DeluxHost</a>
├ 👨‍💻 <b>Wizard:</b> <a href='https://t.me/xspes'>NAm</a>
└ 🆕 <b>Version:</b> <a href='https://github.com/yuIlariy/Digital-Auto-Rename-Bot'>{}</a>

✨ <i>Where files transform with magical precision!</i>"""

    HELP_TXT = """
<b>•></b> 𝚂𝚎𝚗𝚍 /autorename 𝙵𝚘𝚛 𝚊𝚞𝚝𝚘 𝚁𝚎𝚗𝚊𝚖𝚎 𝚑𝚎𝚕𝚙 𝙰𝚗𝚍 𝚜𝚎𝚝𝚝𝚒𝚗𝚐 𝚊𝚞𝚝𝚘 𝚛𝚎𝚗𝚊𝚖𝚎.

✏️ <b><u>Hᴏᴡ Tᴏ Rᴇɴᴀᴍᴇ A Fɪʟᴇ</u></b>
<b>•></b> Sᴇɴᴅ Aɴy Fɪʟᴇ\nAɴᴅ 𝚂ᴇʟᴇᴄᴛ Tʜᴇ Fᴏʀᴍᴀᴛ [ document, video, audio ].           
ℹ️ 𝗔𝗻𝘆 𝗢𝘁𝗵𝗲𝗿 𝗛𝗲𝗹𝗽 𝗖𝗼𝗻𝘁𝗮𝗰𝘁 :- <a href=https://t.me/DigitalBotz_Support>𝑺𝑼𝑷𝑷𝑶𝑹𝑻 𝑮𝑹𝑶𝑼𝑷</a>
"""

    
    
    THUMBNAIL = """
🌌 <b><u>Hᴏᴡ Tᴏ Sᴇᴛ Tʜᴜᴍʙɴɪʟᴇ</u></b>

<b>•></b> Sᴇɴᴅ Aɴy Pʜᴏᴛᴏ Tᴏ Aᴜᴛᴏᴍᴀᴛɪᴄᴀʟʟy Sᴇᴛ Tʜᴜᴍʙɴɪʟᴇ.
<b>•></b> /del_thumb Uꜱᴇ Tʜɪꜱ Cᴏᴍᴍᴀɴᴅ Tᴏ Dᴇʟᴇᴛᴇ Yᴏᴜʀ Oʟᴅ Tʜᴜᴍʙɴɪʟᴇ.
<b>•></b> /view_thumb Uꜱᴇ Tʜɪꜱ Cᴏᴍᴍᴀɴᴅ Tᴏ Vɪᴇᴡ Yᴏᴜʀ Cᴜʀʀᴇɴᴛ Tʜᴜᴍʙɴɪʟᴇ.
"""
    CAPTION= """
📑 <b><u>Hᴏᴡ Tᴏ Sᴇᴛ Cᴜꜱᴛᴏᴍ Cᴀᴩᴛɪᴏɴ</u></b>

<b>•></b> /set_caption - Uꜱᴇ Tʜɪꜱ Cᴏᴍᴍᴀɴᴅ Tᴏ Sᴇᴛ ᴀ Cᴜꜱᴛᴏᴍ Cᴀᴩᴛɪᴏɴ
<b>•></b> /see_caption - Uꜱᴇ Tʜɪꜱ Cᴏᴍᴍᴀɴᴅ Tᴏ Vɪᴇᴡ Yᴏᴜʀ Cᴜꜱᴛᴏᴍ Cᴀᴩᴛɪᴏɴ
<b>•></b> /del_caption - Uꜱᴇ Tʜɪꜱ Cᴏᴍᴍᴀɴᴅ Tᴏ Dᴇʟᴇᴛᴇ Yᴏᴜʀ Cᴜꜱᴛᴏᴍ Cᴀᴩᴛɪᴏɴ

Exᴀᴍᴩʟᴇ:- `/set_caption 📕 Fɪʟᴇ Nᴀᴍᴇ: {filename}
💾 Sɪᴢᴇ: {filesize}
⏰ Dᴜʀᴀᴛɪᴏɴ: {duration}`
"""
    BOT_STATUS = """
⚡️ ʙᴏᴛ sᴛᴀᴛᴜs ⚡️

⌚️ ʙᴏᴛ ᴜᴩɪᴍᴇ: `{}`
👭 ᴛᴏᴛᴀʟ ᴜsᴇʀꜱ: `{}`
💸 ᴛᴏᴛᴀʟ ᴘʀᴇᴍɪᴜᴍ ᴜsᴇʀs: `{}`
֍ ᴜᴘʟᴏᴀɪᴏ: `{}`
⊙ ᴅᴏᴡɴʟᴏᴀᴅ: `{}`
"""
    LIVE_STATUS = """
⚡ ʟɪᴠᴇ sᴇʀᴠᴇʀ sᴛᴀᴛᴜs ⚡

⏰ ᴜᴘᴛɪᴍᴇ: `{}`
🔥 ᴄᴘᴜ: `{}%`
📊 ʀᴀᴍ: `{}%` 
💾 ᴛᴏᴛᴀʟ ᴅɪsᴋ: `{}`
📉 ᴜsᴇᴅ sᴘᴀᴄᴇ: `{} {}%`
📁 ғʀᴇᴇ sᴘᴀᴄᴇ: `{}`
📤 ᴜᴘᴏ: `{}`
📥 ᴅᴏᴡɴʟᴏᴀᴅ: `{}`
🧩 V𝟹.𝟷.𝟶 [STABLE]
"""
    
    
    #⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️
#⚠️ Dᴏɴ'ᴛ Rᴇᴍᴏᴠᴇ Oᴜʀ Cʀᴇᴅɪᴛꜱ @RknDeveloper🙏🥲
    # ᴡʜᴏᴇᴠᴇʀ ɪs ᴅᴇᴘʟᴏʏɪɴɢ ᴛʜɪs ʀᴇᴘᴏ ɪs ᴡᴀʀɴᴇᴅ ⚠️ ᴅᴏ ɴᴏᴛ ʀᴇᴍᴏᴠᴇ ᴄʀᴇᴅɪᴛs ɢɪᴠᴇɴ ɪɴ ᴛʜɪs ʀᴇᴘᴏ #ғɪʀsᴛ ᴀɴᴅ ʟᴀsᴛ ᴡᴀʀɴɪɴɢ ⚠️
    DEV_TXT = """<b><u>Sᴩᴇᴄɪᴀʟ Tʜᴀɴᴋꜱ & Dᴇᴠᴇʟᴏᴩᴇʀꜱ</b></u>
    
» 𝗦𝗢𝗨𝗥𝗖𝗘 𝗖𝗢𝗗𝗘 : <a href=https://github.com/DigitalBotz/Digital-Auto-Rename-Bot>Digital-Auto-Rename-Bot</a>

• ❣️ <a href=https://github.com/RknDeveloper>RknDeveloper</a>
• ❣️ <a href=https://github.com/DigitalBotz>DigitalBotz</a>
• ❣️ <a href=https://github.com/JayMahakal98>Jay Mahakal</a> """
    # ⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️

    # Premium plans list
    UPGRADE_PREMIUM = """
•⪼ ★𝘗𝘳𝘭𝘢𝘯𝘴    -  ⏳𝘋𝘢𝘵𝘦 - 💸𝘗𝘳𝘪𝘤𝘦  
•⪼ 🥉𝘉𝘳𝘰𝘯𝘻𝘦   -   3𝘥𝘢𝘺𝘴   -   $0.47  
•⪼ 🥈𝘚𝘪𝘭𝘷𝘦𝘳   -   7𝘥𝘢𝘺𝘴   -   $0.71  
•⪼ 🥇𝘎𝘰𝘭𝘥    -  15𝘥𝘢𝘺𝘴  -   $1.15  
•⪼ 🏆𝘗𝘭𝘢𝘵𝘪𝘯𝘶𝘮 -  1𝘮𝘰𝘯𝘵𝘩  -   $2.11  
•⪼ 💎𝘋𝘪𝘢𝘮𝘰𝘯𝘥  -  2𝘮𝘰𝘯𝘵𝘩  -   $3.00  

🚀 Daily Upload Limit: Unlimited  
🎁 Discount All Plans: $0.11  
"""
