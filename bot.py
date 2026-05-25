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

@bot.message_handler(content_types=['text', 'photo'])
def handle_post(message):

    pending_posts[message.message_id] = message

    keyboard = InlineKeyboardMarkup()

    keyboard.row(
        InlineKeyboardButton(
            "✅ Approve",
            callback_data=f"approve_{message.message_id}"
        ),
        InlineKeyboardButton(
            "❌ Reject",
            callback_data=f"reject_{message.message_id}"
        )
    )

    if message.content_type == "text":

        bot.send_message(
            MOD_GROUP_ID,
            f"👤 {message.from_user.first_name}\n"
            f"@{message.from_user.username}\n"
            f"🆔 {message.from_user.id}\n\n"
            f"{message.text}",
            reply_markup=keyboard
        )

    elif message.content_type == "photo":

        caption = (
            f"👤 {message.from_user.first_name}\n"
            f"@{message.from_user.username}\n"
            f"🆔 {message.from_user.id}\n\n"
            f"{message.caption if message.caption else ''}"
        )

        bot.send_photo(
            MOD_GROUP_ID,
            message.photo[-1].file_id,
            caption=caption,
            reply_markup=keyboard
        )

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):

    data = call.data

    if data.startswith("approve_"):

        msg_id = int(data.split("_")[1])

        if msg_id in pending_posts:

            msg = pending_posts[msg_id]

            if msg.content_type == "text":

                bot.send_message(
                    CHANNEL_ID,
                    f"{msg.text}\n\n"
                    f"(Gönderen: {msg.from_user.first_name})"
                )

            elif msg.content_type == "photo":

                caption = (
                    f"{msg.caption if msg.caption else ''}\n\n"
                    f"(Gönderen: {msg.from_user.first_name})"
                )

                bot.send_photo(
                    CHANNEL_ID,
                    msg.photo[-1].file_id,
                    caption=caption
                )

            bot.answer_callback_query(
                call.id,
                "Onaylandı ✅"
            )

            bot.send_message(
                msg.chat.id,
                "Gönderiniz H.O.F 🦁 Başarı Duvarı’nda paylaşıldı 🔥\n\n"
                "Paylaşımlarınıza devam etmeyi ve başarı duvarında beğendiğiniz gönderilere emoji bırakarak topluluk kültürümüzü güçlendirmeyi unutmayın 🦁📈"
            )

            bot.edit_message_reply_markup(
                call.message.chat.id,
                call.message.message_id,
                reply_markup=None
            )

    elif data.startswith("reject_"):

        bot.answer_callback_query(
            call.id,
            "Reddedildi ❌"
        )

        bot.edit_message_reply_markup(
            call.message.chat.id,
            call.message.message_id,
            reply_markup=None
        )

print("Bot çalışıyor...")

bot.infinity_polling()
