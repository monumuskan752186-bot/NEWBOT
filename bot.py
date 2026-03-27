from telegram import ReplyKeyboardMarkup, KeyboardButton, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import os

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = 6834599479
REGISTER_LINK = "https://bdg-ipl.shop//#/register?invitationCode=6437315916837"

user_data_store = {}

keyboard = [
    [KeyboardButton("📝 Register")],
    [KeyboardButton("📥 Send UID")],
    [KeyboardButton("💰 Deposit Screenshot")],
    [KeyboardButton("📊 Get Prediction")]
]
reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


def start(update: Update, context: CallbackContext):
    text = (
        "👋 Welcome Trader!\n\n"
        "🔷 Steps:\n"
        "1️⃣ Register\n"
        "2️⃣ Send UID\n"
        "3️⃣ Deposit Screenshot\n"
        "4️⃣ Admin Approval\n"
        "5️⃣ Get Prediction\n\n"
        "👇 Choose option:"
    )
    update.message.reply_text(text, reply_markup=reply_markup)


def handle_buttons(update: Update, context: CallbackContext):
    msg = update.message.text
    user = update.message.from_user

    if msg == "📝 Register":
        update.message.reply_text(f"🔗 Register here:\n{REGISTER_LINK}")

    elif msg == "📥 Send UID":
        update.message.reply_text("📥 Please send your UID now:")
        context.user_data["waiting_uid"] = True

    elif context.user_data.get("waiting_uid"):
        uid = msg
        context.user_data["waiting_uid"] = False
        user_data_store[user.id] = uid

        context.bot.send_message(
            chat_id=ADMIN_ID,
            text=(
                f"📩 New UID Received\n\n"
                f"User: {user.first_name}\n"
                f"User ID: {user.id}\n"
                f"UID: {uid}"
            )
        )

        update.message.reply_text("⛔ Admin approval pending!")

    elif msg == "💰 Deposit Screenshot":
        update.message.reply_text("📸 Please send your deposit screenshot.")
        context.user_data["waiting_screenshot"] = True

    elif msg == "📊 Get Prediction":
        update.message.reply_text("⛔ You need admin approval first.")


def handle_photo(update: Update, context: CallbackContext):
    if context.user_data.get("waiting_screenshot"):
        user = update.message.from_user
        photo = update.message.photo[-1].file_id

        context.bot.send_photo(
            chat_id=ADMIN_ID,
            photo=photo,
            caption=(
                f"💰 Deposit Screenshot Received\n\n"
                f"User: {user.first_name}\n"
                f"User ID: {user.id}"
            )
        )

        context.user_data["waiting_screenshot"] = False
        update.message.reply_text("✅ Screenshot sent to admin. Please wait for approval.")


updater = Updater(TOKEN, use_context=True)
dp = updater.dispatcher

dp.add_handler(CommandHandler("start", start))
dp.add_handler(MessageHandler(Filters.photo, handle_photo))
dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_buttons))

updater.start_polling()
updater.idle()
