import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import os

TOKEN = os.getenv("BOT_TOKEN")

MOD_GROUP_ID = "-1003984397622"
CHANNEL_ID = "-1003934780486"

bot = telebot.TeleBot(TOKEN)

pending_posts = {}

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "🏆 HOF Başarı Botu aktif.")

@bot.message_handler(content_types=['text', 'photo'])
def receive_post(message):

    keyboard = InlineKeyboardMarkup()

    approve_btn = InlineKeyboardButton(
        "✅ Approve",
        callback_data=f"approve_{message.message_id}"
    )

    reject_btn = InlineKeyboardButton(
        "❌ Reject",
        callback_data=f"reject_{message.message_id}"
    )

    keyboard.add(approve_btn, reject_btn)

    pending_posts[message.message_id] = message

    if message.content_type == "text":

        sent = bot.send_message(
            MOD_GROUP_ID,
            f"🏆 Yeni HOF Gönderisi\n\n{message.text}",
            reply_markup=keyboard
        )

    elif message.content_type == "photo":

        sent = bot.send_photo(
            MOD_GROUP_ID,
            message.photo[-1].file_id,
            caption="🏆 Yeni HOF Gönderisi",
            reply_markup=keyboard
        )

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):

    data = call.data

    if data.startswith("approve_"):

        msg_id = int(data.split("_")[1])

        if msg_id in pending_posts:

            original_message = pending_posts[msg_id]

            if original_message.content_type == "text":

                bot.send_message(
                    CHANNEL_ID,
                    f"🏆 H.O.F 🦁 Başarı Duvarı\n\n{original_message.text}"
                )

            elif original_message.content_type == "photo":

                bot.send_photo(
                    CHANNEL_ID,
                    original_message.photo[-1].file_id,
                    caption="🏆 H.O.F 🦁 Başarı Duvarı"
                )

            bot.answer_callback_query(
                call.id,
                "Gönderi onaylandı ✅"
            )

    elif data.startswith("reject_"):

        bot.answer_callback_query(
            call.id,
            "Gönderi reddedildi ❌"
        )

print("Bot çalışıyor...")

bot.infinity_polling()
