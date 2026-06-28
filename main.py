from flask import Flask
from threading import Thread
import os
import requests
import time

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = "8793772063:AAGXXP3sQ9oaFZXTTEjzpTrnwFZm8aeOnpw"

app = Flask(__name__)

@app.route("/")
def home():
    return "Trading Bot Running 🚀"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

# --- Simple Crypto Price Function ---
def get_price():
    url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
    data = requests.get(url).json()
    return float(data['price'])

# --- Telegram Commands ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Trading Bot Active!")

async def price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    price = get_price()
    await update.message.reply_text(f"BTC Price: ${price}")

def main():
    telegram_app = Application.builder().token(TOKEN).build()

    telegram_app.add_handler(CommandHandler("start", start))
    telegram_app.add_handler(CommandHandler("price", price))

    print("Bot Started...")

    Thread(target=run_web).start()
    telegram_app.run_polling()

if __name__ == "__main__":
    main()
