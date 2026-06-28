import requests
from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# ================= CONFIG =================
TOKEN = "8793772063:AAFSr_LQC0RPa2C6B_AV0KxcpCWL7MTivAo"

app = Flask(__name__)

@app.route("/")
def home():
    return "🤖 ICT + SMC Trading Bot Live"

# ================= MARKET DATA =================
def get_market_data():
    return {
        "price": 43250,
        "high": 44000,
        "low": 42000,
        "trend": "BULLISH"
    }

# ================= ICT + SMC =================
def ict_smc_signal():
    data = get_market_data()

    range_size = data["high"] - data["low"]
    current = data["price"]

    if current > data["low"] + range_size * 0.65:
        signal = "🔥 STRONG BUY"
        confidence = 80
    elif current < data["low"] + range_size * 0.35:
        signal = "🔻 STRONG SELL"
        confidence = 78
    else:
        signal = "⚖️ WAIT"
        confidence = 50

    return {
        "pair": "BTC/USDT",
        "trend": data["trend"],
        "signal": signal,
        "confidence": confidence
    }

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 ICT + SMC Bot Active!\n\n/signal - Market Signal"
    )

async def signal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    s = ict_smc_signal()

    msg = f"""
📊 ICT + SMC SIGNAL

💱 Pair : {s['pair']}
📈 Trend : {s['trend']}

🔥 Signal : {s['signal']}
🎯 Confidence : {s['confidence']}%
"""

    await update.message.reply_text(msg)

def main():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("signal", signal))

    application.run_polling()

if __name__ == "__main__":
    Thread(target=lambda: app.run(host="0.0.0.0", port=10000)).start()
    main()
