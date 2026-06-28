import requests
import time

# ================= TELEGRAM =================
TOKEN = "8793772063:AAGGPCah10LLEK3AXkcrXKmWM4xKkbamHTE"
CHAT_ID = "7301534362"

# ================= CRYPTO =================
crypto_symbols = ["BTCUSDT", "ETHUSDT", "BNBUSDT"]

# ================= FOREX MAJOR PAIRS =================
forex_symbols = [
    "EURUSD",
    "GBPUSD",
    "USDJPY",
    "USDCHF",
    "AUDUSD",
    "USDCAD",
    "NZDUSD"
]

# ================= TELEGRAM SEND =================
def send(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try:
        requests.post(url, data={"chat_id": CHAT_ID, "text": msg})
    except:
        pass

# ================= CRYPTO DATA =================
def get_crypto(symbol):
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval=1m&limit=20"
    data = requests.get(url).json()
    return [float(i[4]) for i in data]

# ================= FOREX DATA (SIMPLIFIED) =================
def get_forex(symbol):
    try:
        url = "https://api.exchangerate.host/latest?base=USD"
        data = requests.get(url).json()
        rates = data["rates"]

        base = symbol[:3]
        value = rates.get(base, 1)

        return [value for _ in range(20)]
    except:
        return [1 for _ in range(20)]

# ================= SIGNAL ENGINE =================
def signal_engine(prices):
    avg = sum(prices[-10:]) / 10
    last = prices[-1]
    high = max(prices[-10:])
    low = min(prices[-10:])

    score = 0

    if last > avg:
        score += 1
    else:
        score -= 1

    if last > high * 0.999:
        score += 2
    elif last < low * 0.001:
        score -= 2

    if score >= 3:
        return "BUY"
    elif score <= -3:
        return "SELL"
    return None

# ================= BUILD SIGNAL =================
def build_signal(symbol, prices, market):
    sig = signal_engine(prices)

    if not sig:
        return None

    entry = prices[-1]

    if sig == "BUY":
        sl = min(prices[-10:])
        tp = entry + (entry - sl) * 2
    else:
        sl = max(prices[-10:])
        tp = entry - (sl - entry) * 2

    return f"""
🔥 ICT SMC {market} SIGNAL

PAIR: {symbol}
TYPE: {sig}

ENTRY: {entry}
SL: {sl}
TP: {tp}

⏱ 1M STRUCTURE + LIQUIDITY
"""

# ================= MAIN LOOP =================
last_sent = {}

while True:
    try:
        # CRYPTO SCAN
        for sym in crypto_symbols:
            prices = get_crypto(sym)
            msg = build_signal(sym, prices, "CRYPTO")

            if msg and last_sent.get(sym) != msg:
                send(msg)
                last_sent[sym] = msg

        # FOREX SCAN
        for sym in forex_symbols:
            prices = get_forex(sym)
            msg = build_signal(sym, prices, "FOREX")

            if msg and last_sent.get(sym) != msg:
                send(msg)
                last_sent[sym] = msg

        print("Bot scanning crypto + forex...")

    except Exception as e:
        print("Error:", e)

    time.sleep(60)
