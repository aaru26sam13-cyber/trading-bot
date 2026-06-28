from flask import Flask
from threading import Thread
import os
import requests

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = "8793772063:AAGXXP3sQ9oaFZXTTEjzpTrnwFZm8aeOnpw"

app = Flask(__name__)

@app.route("/")
def home():
    return "Universal Crypto + Forex + Gold Bot Running 🚀"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

# ---------------- ASSETS ----------------
CRYPTO_PAIRS = [
    "BTCUSDT", "ETHUSDT", "SOLUSDT", "XRPUSDT", "ADAUSDT", "DOGEUSDT"
]

FOREX_PAIRS = [
    "EURUSD", "GBPUSD", "USDJPY", "AUDUSD", "USDCHF"
]

# 🟡 GOLD (XAUUSD)
GOLD_PAIRS = [
    "XAUUSD"
]

# ---------------- PRICE ----------------
def get_price(symbol):
    try:
        if symbol.endswith("USDT"):
            url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
            return float(requests.get(url).json()["price"])

        elif symbol == "XAUUSD":
            # Gold free API (demo source)
            url = "https://api.metals.live/v1/spot/gold"
            data = requests.get(url).json()
            return float(data[0]["price"])

        else:
            url = f"https://api.twelvedata.com/price?symbol={symbol}&apikey=demo"
            return float(requests.get(url).json()["price"])
    except:
        return 0

# ---------------- RSI ----------------
def get_rsi(symbol):
    try:
        if symbol.endswith("USDT"):
            url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval=5m&limit=100"
            data = requests.get(url).json()
            closes = [float(c[4]) for c in data]
        else:
            return 50

        gains, losses = [], []

        for i in range(1, len(closes)):
            diff = closes[i] - closes[i - 1]
            gains.append(max(diff, 0))
            losses.append(abs(min(diff, 0)))

        avg_gain = sum(gains[-14:]) / 14
        avg_loss = sum(losses[-14:]) / 14 or 1

        rs = avg_gain / avg_loss
        return 100 - (100 / (1 + rs))
    except:
        return 50

# ---------------- SIGNAL ----------------
def analyze(symbol):
    price = get_price(symbol)
    rsi = get_rsi(symbol)

    if rsi <= 30:
        signal = "🟢 STRONG BUY"
        score = 90
    elif rsi <= 45:
        signal = "BUY"
        score = 70
    elif rsi <= 55:
        signal = "NEUTRAL"
        score = 50
    elif rsi <= 70:
        signal = "SELL"
        score = 70
    else:
        signal = "🔴 STRONG SELL"
        score = 90

    return price, rsi, signal, score

# ---------------- TOP TRADES ----------------
def get_top_trades():
    results = []

    all_pairs = CRYPTO_PAIRS + FOREX_PAIRS + GOLD_PAIRS

    for sym in all_pairs:
        price, rsi, signal, score = analyze(sym)
        results.append((sym, price, rsi, signal, score))

    results.sort(key=lambda x: x[4], reverse=True)

    return results[:4]

# ---------------- TELEGRAM ----------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Universal Crypto + Forex + Gold Bot Active!")

async def signal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    top = get_top_trades()

    msg = "🔥 TOP 4 TRADING SETUPS (CRYPTO + FOREX + GOLD)\n\n"

    for sym, price, rsi, sig, score in top:
        msg += f"""
📊 {sym}
💰 Price: {price}
📈 RSI: {round(rsi,2)}
⚡ Signal: {sig}
💯 Strength: {score}%

-------------------
"""

    msg += "\n⚠️ Risk Management Important"

    await update.message.reply_text(msg)

# ---------------- MAIN ----------------
def main():
    bot = Application.builder().token(TOKEN).build()

    bot.add_handler(CommandHandler("start", start))
    bot.add_handler(CommandHandler("signal", signal))

    print("Bot Started...")

    Thread(target=run_web).start()
    bot.run_polling()

if __name__ == "__main__":
    main()
