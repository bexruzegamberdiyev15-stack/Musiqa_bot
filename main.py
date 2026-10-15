import os
import telebot
from yt_dlp import YoutubeDL

# BotFather bergan maxfiy tokeningizni shu yerga qo'ying
BOT_TOKEN = "8855476362:AAGMcbfTg45uQaVuv-1yxSPTK7..." 

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Salom! Menga musiqa nomini yuboring, men uni YouTube'dan avtomatik qidirib, yuklab beraman! 🎵")

@bot.message_handler(func=lambda message: True)
def search_and_download(message):
    query = message.text
    status_msg = bot.reply_to(message, "YouTube'dan qidirilmoqda... 🔍")
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'default_search': 'ytsearch1',
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True
    }
    
    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(query, download=True)
            video_info = info['entries'] if 'entries' in info else info
            title = video_info.get('title', 'music')
            filename = ydl.prepare_filename(video_info).replace('.webm', '.mp3').replace('.m4a', '.mp3')
            
            bot.edit_message_text("Musiqa topildi! Telegramga yuklanmoqda... 📤", message.chat.id, status_msg.message_id)
            with open(filename, 'rb') as audio:
                bot.send_audio(message.chat.id, audio, title=title)
                
            os.remove(filename)
            bot.delete_message(message.chat.id, status_msg.message_id)
            
    except Exception as e:
        bot.edit_message_text("Uzr, musiqani topishda xatolik yuz berdi. ❌", message.chat.id, status_msg.message_id)

import threading
from flask import Flask
app = Flask('')
@app.route('/')
def home(): return "Bot is running!"
def run(): app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 80)))
threading.Thread(target=run).start()

print("Bot ishga tushdi...")
bot.infinity_polling()
