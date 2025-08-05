# receiver_bot.py
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import json
from executor import execute_trade

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