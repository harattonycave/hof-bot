import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import os
import json

TOKEN = os.getenv("BOT_TOKEN")

MOD_GROUP_ID = -1003984397622
CHANNEL_ID = -1003934780486

bot = telebot.TeleBot(TOKEN)

pending_posts = {}

if os.path.exists("users.json"):
    with open("users.json", "r") as f:
        users = json.load(f)
else:
    users = {}

if os.path.exists("posts.json"):
    with open("posts.json", "r") as f:
        posts = json.load(f)
else:
    posts = {}


@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "🏆 HOF Başarı Botu aktif.")


@bot.message_handler(commands=['elite'])
def make_elite(message):

    admin_id = message.from_user.id

    allowed_admins = [
        519641863
    ]

    if admin_id not in allowed_admins:
        return

    try:

        hof_number = int(message.text.split()[1])

        for user_id, data in users.items():

            if data["hof_id"] == hof_number:

                data["rank"] = "Elite Trader"

                with open("users.json", "w") as f:
                    json.dump(users, f)

                bot.reply_to(
                    message,
                    f"HOF Trader #{hof_number} artık Elite Trader oldu 🦁"
                )

                return

        bot.reply_to(message, "Trader bulunamadı.")

    except:
        bot.reply_to(message, "Kullanım: /elite 184")


@bot.message_handler(commands=['legend'])
def make_legend(message):

    admin_id = message.from_user.id

    allowed_admins = [
        519641863
    ]

    if admin_id not in allowed_admins:
        return

    try:

        hof_number = int(message.text.split()[1])

        for user_id, data in users.items():

            if data["hof_id"] == hof_number:

                data["rank"] = "Legend Trader"

                with open("users.json", "w") as f:
                    json.dump(users, f)

                bot.reply_to(
                    message,
                    f"HOF Trader #{hof_number} artık Legend Trader oldu 👑"
                )

                return

        bot.reply_to(message, "Trader bulunamadı.")

    except:
        bot.reply_to(message, "Kullanım: /legend 184")


@bot.message_handler(commands=['trader'])
def remove_elite(message):

    admin_id = message.from_user.id

    allowed_admins = [
        519641863
    ]

    if admin_id not in allowed_admins:
        return

    try:

        hof_number = int(message.text.split()[1])

        for user_id, data in users.items():

            if data["hof_id"] == hof_number:

                data["rank"] = "Trader"

                with open("users.json", "w") as f:
                    json.dump(users, f)

                bot.reply_to(
                    message,
                    f"HOF Trader #{hof_number} normal Trader seviyesine döndürüldü."
                )

                return

        bot.reply_to(message, "Trader bulunamadı.")

    except:
        bot.reply_to(message, "Kullanım: /trader 184")


@bot.message_handler(commands=['stats'])
def show_stats(message):

    try:

        hof_number = int(message.text.split()[1])

        for user_id, data in users.items():

            if data["hof_id"] == hof_number:

                bot.reply_to(
                    message,
                    f"🏷️ HOF {data['rank']} #{data['hof_id']}\n\n"
                    f"📈 Toplam Puan: {data['points']}\n"
                    f"🔥 Approved Paylaşım: {data['approved_posts']}"
                )

                return

        bot.reply_to(message, "Trader bulunamadı.")

    except:
        bot.reply_to(message, "Kullanım: /stats 184")


@bot.message_handler(commands=['mystats'])
def my_stats(message):

    user_id = str(message.from_user.id)

    if user_id not in users:

        bot.reply_to(message, "Henüz sistemde kaydınız yok.")
        return

    data = users[user_id]

    bot.reply_to(
        message,
        f"🏷️ HOF {data['rank']} #{data['hof_id']}\n\n"
        f"📈 Toplam Puanınız: {data['points']}\n"
        f"🔥 Approved Paylaşımınız: {data['approved_posts']}"
    )


@bot.message_handler(commands=['leaderboard'])
def leaderboard(message):

    sorted_users = sorted(
        users.values(),
        key=lambda x: x["points"],
        reverse=True
    )

    text = "🏆 HOF Leaderboard\n\n"

    medals = ["🥇", "🥈", "🥉"]

    for index, user in enumerate(sorted_users[:10]):

        medal = medals[index] if index < 3 else "🏅"

        text += (
            f"{medal} HOF {user['rank']} "
            f"#{user['hof_id']} — "
            f"{user['points']} puan\n"
        )

    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', 'photo'])
def handle_post(message):

    user_id = str(message.from_user.id)

    if user_id not in users:

        hof_number = len(users) + 101

        users[user_id] = {
            "hof_id": hof_number,
            "rank": "Trader",
            "points": 0,
            "approved_posts": 0
        }

        with open("users.json", "w") as f:
            json.dump(users, f)

        bot.send_message(
            message.chat.id,
            f"🏷️ HOF Trader #{hof_number} olarak sisteme katıldınız 🦁\n\n"
            f"Başarı paylaşımlarınız artık H.O.F ekosisteminde yer alabilir.\n"
            f"Disiplinli kalın, gelişmeye devam edin ve kültürü birlikte büyütelim 📈"
        )

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

    hof_tag = f"HOF {users[user_id]['rank']} #{users[user_id]['hof_id']}"

    username_line = (
        f"@{message.from_user.username}\n"
        if message.from_user.username else ""
    )

    if message.content_type == "text":

        bot.send_message(
            MOD_GROUP_ID,
            f"👤 {message.from_user.first_name}\n"
            f"{username_line}"
            f"🆔 {message.from_user.id}\n"
            f"🏷️ {hof_tag}\n\n"
            f"{message.text}",
            reply_markup=keyboard
        )

    elif message.content_type == "photo":

        caption = (
            f"👤 {message.from_user.first_name}\n"
            f"{username_line}"
            f"🆔 {message.from_user.id}\n"
            f"🏷️ {hof_tag}\n\n"
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

            user_id = str(msg.from_user.id)

            hof_tag = f"HOF {users[user_id]['rank']} #{users[user_id]['hof_id']}"

            users[user_id]["approved_posts"] += 1
            users[user_id]["points"] += 3

            with open("users.json", "w") as f:
                json.dump(users, f)

            if msg.content_type == "text":

                sent_message = bot.send_message(
                    CHANNEL_ID,
                    f"{msg.text}\n\n"
                    f"(Gönderen: {hof_tag})"
                )

            elif msg.content_type == "photo":

                caption = (
                    f"{msg.caption if msg.caption else ''}\n\n"
                    f"(Gönderen: {hof_tag})"
                )

                sent_message = bot.send_photo(
                    CHANNEL_ID,
                    msg.photo[-1].file_id,
                    caption=caption
                )

            posts[str(sent_message.message_id)] = {
                "owner_id": user_id,
                "hof_id": users[user_id]["hof_id"],
                "rank": users[user_id]["rank"],
                "reactions": 0,
                "rewarded_10": False
            }

            with open("posts.json", "w") as f:
                json.dump(posts, f)

            bot.answer_callback_query(
                call.id,
                "Onaylandı ✅"
            )

            bot.send_message(
                msg.chat.id,
                f"Gönderiniz H.O.F 🦁 Başarı Duvarı’nda paylaşıldı 🔥\n\n"
                f"Toplam approved paylaşımınız: {users[user_id]['approved_posts']}\n"
                f"Toplam puanınız: {users[user_id]['points']} 📈\n\n"
                f"Paylaşımlarınıza devam etmeyi ve başarı duvarında beğendiğiniz gönderilere emoji bırakarak topluluk kültürümüzü güçlendirmeyi unutmayın 🦁"
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
