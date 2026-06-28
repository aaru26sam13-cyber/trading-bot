import os
import requests
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# ================= CONFIG =================
TOKEN = os.getenv("8793772063:AAHYAvsoh1gfUttx7fKDGh7VQm1WvX8OLYM")
app = Flask(__name__)

# ================= FLASK =================
@app.route("/")
def home():
    return "🤖 ICT + SMC Trading Bot Live"

# ================= MARKET DATA (simple mock logic) =================
def get_market_data():
    # इथे तू API (Binance/Forex) connect करू शकतोस पुढे
    return {
        "price": 43250,
        "high": 44000,
        "low": 42000,
        "trend": "BULLISH"
    }

# ================= ICT + SMC LOGIC =================
def ict_smc_signal():
    data = get_market_data()

    range_size = data["high"] - data["low"]
    current = data["price"]

    # Liquidity zones (simple ICT idea)
    upper_liquidity = data["high"]
    lower_liquidity = data["low"]

    # Smart structure logic
    if current > (data["low"] + range_size * 0.65):
        signal = "🔥 STRONG BUY"
        confidence = 80
    elif current < (data["low"] + range_size * 0.35):
        signal = "🔻 STRONG SELL"
        confidence = 78
    else:
        signal = "⚖️ WAIT / NEUTRAL"
        confidence = 50

    return {
        "pair": "BTC/USDT",
        "timeframes": ["3m", "5m", "15m", "1h"],
        "trend": data["trend"],
        "signal": signal,
        "confidence": f"{confidence}%",
        "liquidity_high": upper_liquidity,
        "liquidity_low": lower_liquidity
    }

# ================= TELEGRAM COMMANDS =================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 ICT + SMC Bot Active!\n\nUse:\n/signal - Get Market Analysis"
    )

async def signal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    s = ict_smc_signal()

    msg = f"""
📊 ICT + SMC ANALYSIS

💱 Pair: {s['pair']}
📈 Trend: {s['trend']}

⏱ Timeframes:
{', '.join(s['timeframes'])}

🔥 Signal: {s['signal']}
📊 Confidence: {s['confidence']}

💧 Liquidity High: {s['liquidity_high']}
💧 Liquidity Low: {s['liquidity_low']}
"""

    await update.message.reply_text(msg)

# ================= MAIN =================
def main():
    telegram_app = Application.builder().token(TOKEN).build()

    telegram_app.add_handler(CommandHandler("start", start))
    telegram_app.add_handler(CommandHandler("signal", signal))

    print("🤖 ICT SMC Bot Running...")

    telegram_app.run_polling()

# ================= RUN =================
if __name__ == "__main__":
    from threading import Thread
    Thread(target=lambda: app.run(host="0.0.0.0", port=10000)).start()

    main()
