import telebot
import os

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_CHAT_ID = "-1003984397622"

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "🏆 HOF Başarı Botu aktif.")

@bot.message_handler(func=lambda message: True, content_types=['text', 'photo', 'document'])
def forward(message):
    bot.forward_message(
        ADMIN_CHAT_ID,
        message.chat.id,
        message.message_id
    )

print("Bot çalışıyor...")

bot.infinity_polling()
