# receiver_bot.py
from telegram import Update
from telegram import ApplicationBuilder, MessageHandler, filters, ContextTypes
import json
from executor import execute_trade

import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.error(f"Fehler: {str(e)}")

# Set your Telegram Bot Token here
BOT_TOKEN = "7630113729:AAHp9RzzOPsgX56UcSkuHqx_2LB_habpCHQ"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        message = update.message.text.strip()

        if not message.startswith("{"):
            await update.message.reply_text("⚠️ Kein gültiges JSON erkannt.")
            return

        signal = json.loads(message)
        execute_trade(signal)

        await update.message.reply_text(f"🟢 Trade empfangen und ausgeführt:\n{signal['symbol']} {signal['direction']}")
    except Exception as e:
        await update.message.reply_text(f"❌ Fehler bei Ausführung: {str(e)}")
        print(f"❌ Fehler: {str(e)}")

if __name__ == "__main__":
    print("🚀 Telegram-Bot läuft und wartet auf Signale...")
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
    
required_keys = ['symbol', 'direction', 'entry', 'sl', 'tp', 'lot']
missing = [key for key in required_keys if key not in signal]

if missing:
    await update.message.reply_text(f"❌ Signal unvollständig, fehlende Felder: {', '.join(missing)}")
    print(f"❌ Signal unvollständig, fehlende Felder: {', '.join(missing)}")
    # Optional: Sende eine Nachricht an den Chat, dass das Signal unvollständig ist
    return
    print("🚀 Bot läuft – wartet auf Signale...")
    