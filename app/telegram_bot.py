import os
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from qa_engine import QAEngine

qa_engine = QAEngine()

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    try:
        response = qa_engine.answer(user_input)

        if not isinstance(response, str):
            response = str(response)

        if len(response) > 4000:
            response = response[:4000] + "...\n\n🔹 Ответ был обрезан из-за длины."

        await update.message.reply_text(response)

    except Exception as e:
        await update.message.reply_text("⚠️ Произошла ошибка. Попробуйте позже.")
        print(f"❌ Ошибка при обработке сообщения: {e}")

def run_telegram_bot():
    app = ApplicationBuilder().token(os.getenv("TELEGRAM_TOKEN")).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("🤖 Агент-бот запущен и ждёт сообщений!")
    app.run_polling()
