from flask import Flask
from threading import Thread
import os

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# तुझा Telegram Bot Token इथे टाक
TOKEN = "8793772063:AAGGPCah10LLEK3AXkcrXKmWM4xKkbamHTE"

# Flask App
web = Flask(__name__)

@web.route("/")
def home():
    return "Trading Bot is Running!"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    web.run(host="0.0.0.0", port=port)

# Telegram Commands
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Bot Working Successfully!")

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    print("Bot Started...")

    # Flask server background मध्ये चालू कर
    Thread(target=run_web).start()

    # Telegram Bot चालू कर
    app.run_polling()

if __name__ == "__main__":
    main()
