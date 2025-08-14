from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from app.qa_engine import QAEngine
from app.config import TELEGRAM_TOKEN

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    response = context.bot_data['qa_engine'].answer(user_input)
    await update.message.reply_text(response)

def run_telegram_bot():
    qa_engine = QAEngine()
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.bot_data['qa_engine'] = qa_engine
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("🤖 Бот запущен!")
    app.run_polling()
