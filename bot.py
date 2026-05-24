import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import os

TOKEN = os.getenv("BOT_TOKEN")

MOD_GROUP_ID = -1003984397622
CHANNEL_ID = -1003934780486

bot = telebot.TeleBot(TOKEN)

pending_posts = {}

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "🏆 HOF Başarı Botu aktif.")

@bot.message_handler(content_types=['text'])
def handle_text(message):

    pending_posts[message.message_id] = message

    keyboard = InlineKeyboardMarkup()

    keyboard.row(
        InlineKeyboardButton("✅ Approve", callback_data=f"approve_{message.message_id}"),
        InlineKeyboardButton("❌ Reject", callback_data=f"reject_{message.message_id}")
    )

    bot.send_message(
        MOD_GROUP_ID,
        f"🏆 Yeni HOF Gönderisi\n\n{message.text}",
        reply_markup=keyboard
    )

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):

    data = call.data

    if data.startswith("approve_"):

        msg_id = int(data.split("_")[1])

        if msg_id in pending_posts:

            msg = pending_posts[msg_id]

            bot.send_message(
                CHANNEL_ID,
                f"🏆 H.O.F 🦁 Başarı Duvarı\n\n{msg.text}"
            )

            bot.answer_callback_query(call.id, "Onaylandı ✅")

    elif data.startswith("reject_"):

        bot.answer_callback_query(call.id, "Reddedildi ❌")

print("Bot çalışıyor...")

bot.infinity_polling()
