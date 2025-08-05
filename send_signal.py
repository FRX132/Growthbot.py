{
  "symbol": "XAUUSD",
  "direction": "BUY",
  "entry": 2335.25,
  "sl": 2330.00,
  "tp": 2345.00,
  "lotsize": 0.25,
  "category": "A+ Setup"
}

# ========================
# Mac-Skript: send_signal.py
# ========================
import requests
import json

BOT_TOKEN = "7630113729:AAHp9RzzOPsgX56UcSkuHqx_2LB_habpCHQ"
CHAT_ID = "5316804058"

def send_trade_signal(signal_data):
    message = json.dumps(signal_data, indent=2)
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": f"📡 Neues Trade-Signal:\n```json\n{message}\n```",
        "parse_mode": "Markdown"
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        print("✅ Signal erfolgreich gesendet")
    else:
        print(f"❌ Fehler beim Senden: {response.text}")

# Beispiel-Aufruf
if __name__ == "__main__":
    test_signal = {
        "symbol": "XAUUSD",
        "direction": "BUY",
        "entry": 2335.25,
        "sl": 2330.00,
        "tp": 2345.00,
        "lotsize": 0.25,
        "category": "A+ Setup"
    }
    send_trade_signal(test_signal)


# ==========================
# Windows-Skript: receiver_bot.py
# ==========================
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import json
from executor import execute_trade

BOT_TOKEN = "7630113729:AAHp9RzzOPsgX56UcSkuHqx_2LB_habpCHQ"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        message = update.message.text
        if not message.strip().startswith("{"):
            return  # kein JSON
        signal = json.loads(message)
        execute_trade(signal)
        await update.message.reply_text("🟢 Signal empfangen und ausgeführt.")
    except Exception as e:
        await update.message.reply_text(f"❌ Fehler: {str(e)}")

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("🚀 Bot läuft – wartet auf Signale...")
    app.run_polling()


# ==========================
# Windows: executor.py
# ==========================
import MetaTrader5 as mt5

def execute_trade(signal):
    if not mt5.initialize():
        raise Exception("MT5 konnte nicht initialisiert werden")

    action = mt5.ORDER_TYPE_BUY if signal["direction"].upper() == "BUY" else mt5.ORDER_TYPE_SELL
    price = mt5.symbol_info_tick(signal["symbol"]).ask if action == mt5.ORDER_TYPE_BUY else mt5.symbol_info_tick(signal["symbol"]).bid

    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": signal["symbol"],
        "volume": float(signal["lotsize"]),
        "type": action,
        "price": price,
        "sl": float(signal["sl"]),
        "tp": float(signal["tp"]),
        "deviation": 10,
        "magic": 234000,
        "comment": f"TelegramSignal {signal['category']}",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC
    }

    result = mt5.order_send(request)
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        raise Exception(f"Trade-Fehler: {result.comment}")
    print(f"✅ Trade ausgeführt: {signal['symbol']} {signal['direction']} @ {price}")
