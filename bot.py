import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import os
import json
from datetime import datetime

TOKEN = os.getenv("BOT_TOKEN")

MOD_GROUP_ID = -1003984397622
CHANNEL_ID = -1003934780486

bot = telebot.TeleBot(TOKEN)

pending_posts = {}

# USERS

if os.path.exists("users.json"):
    with open("users.json", "r") as f:
        users = json.load(f)
else:
    users = {}

# POSTS

if os.path.exists("posts.json"):
    with open("posts.json", "r") as f:
        posts = json.load(f)
else:
    posts = {}

# MODERATION LOGS

if os.path.exists("moderation_logs.json"):
    with open("moderation_logs.json", "r") as f:
        moderation_logs = json.load(f)
else:
    moderation_logs = []


@bot.message_handler(commands=['start'])
def start(message):

    bot.reply_to(
        message,
        "🏆 HOF Başarı Botu aktif."
    )


# ELITE SYSTEM

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
                    json.dump(users, f, indent=4)

                bot.reply_to(
                    message,
                    f"HOF Trader #{hof_number} artık Elite Trader oldu 🦁"
                )

                return

        bot.reply_to(message, "Trader bulunamadı.")

    except:

        bot.reply_to(
            message,
            "Kullanım: /elite 184"
        )


# LEGEND SYSTEM

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
                    json.dump(users, f, indent=4)

                bot.reply_to(
                    message,
                    f"HOF Trader #{hof_number} artık Legend Trader oldu 👑"
                )

                return

        bot.reply_to(message, "Trader bulunamadı.")

    except:

        bot.reply_to(
            message,
            "Kullanım: /legend 184"
        )


# RESET TO TRADER

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
                    json.dump(users, f, indent=4)

                bot.reply_to(
                    message,
                    f"HOF Trader #{hof_number} normal Trader seviyesine döndürüldü."
                )

                return

        bot.reply_to(message, "Trader bulunamadı.")

    except:

        bot.reply_to(
            message,
            "Kullanım: /trader 184"
        )


# REACTION REWARD SYSTEM

@bot.message_handler(commands=['react'])
def add_reaction_points(message):

    admin_id = message.from_user.id

    allowed_admins = [
        519641863
    ]

    if admin_id not in allowed_admins:
        return

    try:

        args = message.text.split()

        hof_number = int(args[1])
        reaction_count = int(args[2])

        for user_id, data in users.items():

            if data["hof_id"] == hof_number:

                reward = 0

                if reaction_count >= 10:
                    reward = 5

                if reaction_count >= 25:
                    reward = 15

                if reaction_count >= 50:
                    reward = 30

                data["points"] += reward

                with open("users.json", "w") as f:
                    json.dump(users, f, indent=4)

                bot.reply_to(
                    message,
                    f"🔥 HOF Trader #{hof_number} "
                    f"{reaction_count} reaction aldı.\n"
                    f"+{reward} puan eklendi."
                )

                bot.send_message(
                    int(user_id),
                    f"🔥 Gönderiniz toplulukta "
                    f"{reaction_count} reaction aldı!\n\n"
                    f"+{reward} bonus puan kazandınız 🦁"
                )

                return

        bot.reply_to(message, "Trader bulunamadı.")

    except:

        bot.reply_to(
            message,
            "Kullanım: /react 184 10"
        )


# PUBLIC STATS

@bot.message_handler(commands=['stats'])
def show_stats(message):

    try:

        hof_number = int(message.text.split()[1])

        for user_id, data in users.items():

            if data["hof_id"] == hof_number:

                achievements = "\n".join(
                    [f"🏅 {a}" for a in data.get("achievements", [])]
                )

                if achievements == "":
                    achievements = "Henüz achievement yok."

                bot.reply_to(
                    message,
                    f"🏷️ HOF {data['rank']} #{data['hof_id']}\n\n"
                    f"📈 Toplam Puan: {data['points']}\n"
                    f"🔥 Approved Paylaşım: {data['approved_posts']}\n\n"
                    f"🎖️ Achievementler:\n{achievements}"
                )

                return

        bot.reply_to(message, "Trader bulunamadı.")

    except:

        bot.reply_to(
            message,
            "Kullanım: /stats 184"
        )


# PRIVATE STATS

@bot.message_handler(commands=['mystats'])
def my_stats(message):

    user_id = str(message.from_user.id)

    if user_id not in users:

        bot.reply_to(
            message,
            "Henüz sistemde kaydınız yok."
        )

        return

    data = users[user_id]

    achievements = "\n".join(
        [f"🏅 {a}" for a in data.get("achievements", [])]
    )

    if achievements == "":
        achievements = "Henüz achievement yok."

    bot.reply_to(
        message,
        f"🏷️ HOF {data['rank']} #{data['hof_id']}\n\n"
        f"📈 Toplam Puanınız: {data['points']}\n"
        f"🔥 Approved Paylaşımınız: {data['approved_posts']}\n\n"
        f"🎖️ Achievementleriniz:\n{achievements}"
    )


# LEADERBOARD

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


# POST HANDLER

@bot.message_handler(content_types=['text', 'photo'])
def handle_post(message):

    user_id = str(message.from_user.id)

    if user_id not in users:

        hof_number = len(users) + 101

        users[user_id] = {
            "hof_id": hof_number,
            "rank": "Trader",
            "points": 0,
            "approved_posts": 0,
            "achievements": []
        }

        with open("users.json", "w") as f:
            json.dump(users, f, indent=4)

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


# APPROVE / REJECT

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):

    data = call.data

    # APPROVE

    if data.startswith("approve_"):

        msg_id = int(data.split("_")[1])

        if msg_id in pending_posts:

            msg = pending_posts[msg_id]

            user_id = str(msg.from_user.id)

            hof_tag = (
                f"HOF {users[user_id]['rank']} "
                f"#{users[user_id]['hof_id']}"
            )

            users[user_id]["approved_posts"] += 1
            users[user_id]["points"] += 3

            # FIRST BLOOD

            if (
                users[user_id]["approved_posts"] >= 1 and
                "First Blood" not in users[user_id]["achievements"]
            ):

                users[user_id]["achievements"].append(
                    "First Blood"
                )

                bot.send_message(
                    msg.chat.id,
                    "🎖️ Achievement Unlocked: First Blood\n\n"
                    "İlk approved paylaşımınızı yaptınız 🦁"
                )

            # CONSISTENCY

            if (
                users[user_id]["approved_posts"] >= 10 and
                "Consistency" not in users[user_id]["achievements"]
            ):

                users[user_id]["achievements"].append(
                    "Consistency"
                )

                bot.send_message(
                    msg.chat.id,
                    "🎖️ Achievement Unlocked: Consistency\n\n"
                    "10 approved paylaşım seviyesine ulaştınız 🔥"
                )

            with open("users.json", "w") as f:
                json.dump(users, f, indent=4)

            # SEND CHANNEL POST

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

            # POSTS DATABASE

            posts[str(sent_message.message_id)] = {
                "owner_id": user_id,
                "hof_id": users[user_id]["hof_id"],
                "rank": users[user_id]["rank"],
                "reactions": 0,
                "rewarded_10": False
            }

            with open("posts.json", "w") as f:
                json.dump(posts, f, indent=4)

            # MODERATION LOG

            admin_id = call.from_user.id

            preview_text = ""

            if msg.content_type == "text":

                preview_text = msg.text[:200]

            elif msg.content_type == "photo":

                preview_text = (
                    msg.caption[:200]
                    if msg.caption else "Fotoğraf paylaşımı"
                )

            log_entry = {
                "action": "approve",
                "admin_id": admin_id,
                "hof_id": users[user_id]["hof_id"],
                "rank": users[user_id]["rank"],
                "post_preview": preview_text,
                "time": str(datetime.now())
            }

            moderation_logs.append(log_entry)

            with open("moderation_logs.json", "w") as f:
                json.dump(moderation_logs, f, indent=4)

            # ADMIN REPORT

            bot.send_message(
                519641863,
                f"📋 Eylem Raporu\n\n"
                f"✅ Approve\n"
                f"👮 Admin ID: {admin_id}\n"
                f"🏷️ HOF {users[user_id]['rank']} "
                f"#{users[user_id]['hof_id']}\n\n"
                f"📝 Gönderi:\n"
                f"{preview_text}\n\n"
                f"🕒 "
                f"{datetime.now().strftime('%d.%m.%Y %H:%M')}"
            )

            bot.answer_callback_query(
                call.id,
                "Onaylandı ✅"
            )

            # USER REPORT

            bot.send_message(
                msg.chat.id,
                f"Gönderiniz H.O.F 🦁 "
                f"Başarı Duvarı’nda paylaşıldı 🔥\n\n"
                f"Toplam approved paylaşımınız: "
                f"{users[user_id]['approved_posts']}\n"
                f"Toplam puanınız: "
                f"{users[user_id]['points']} 📈\n\n"
                f"Paylaşımlarınıza devam etmeyi "
                f"ve başarı duvarında "
                f"beğendiğiniz gönderilere "
                f"emoji bırakarak topluluk "
                f"kültürümüzü güçlendirmeyi "
                f"unutmayın 🦁"
            )

            bot.edit_message_reply_markup(
                call.message.chat.id,
                call.message.message_id,
                reply_markup=None
            )

    # REJECT

    elif data.startswith("reject_"):

        msg_id = int(data.split("_")[1])

        admin_id = call.from_user.id

        preview_text = ""

        if msg_id in pending_posts:

            rejected_msg = pending_posts[msg_id]

            if rejected_msg.content_type == "text":

                preview_text = rejected_msg.text[:200]

            elif rejected_msg.content_type == "photo":

                preview_text = (
                    rejected_msg.caption[:200]
                    if rejected_msg.caption
                    else "Fotoğraf paylaşımı"
                )

        log_entry = {
            "action": "reject",
            "admin_id": admin_id,
            "post_preview": preview_text,
            "time": str(datetime.now())
        }

        moderation_logs.append(log_entry)

        with open("moderation_logs.json", "w") as f:
            json.dump(moderation_logs, f, indent=4)

        bot.send_message(
            519641863,
            f"📋 Eylem Raporu\n\n"
            f"❌ Reject\n"
            f"👮 Admin ID: {admin_id}\n\n"
            f"📝 Gönderi:\n"
            f"{preview_text}\n\n"
            f"🕒 "
            f"{datetime.now().strftime('%d.%m.%Y %H:%M')}"
        )

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
