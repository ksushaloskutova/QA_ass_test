import os

from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

from qa_engine import QAEngine

qa_engine = QAEngine()


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text.strip()

    # Запрашиваем выбор программы при первом обращении
    if "program" not in context.user_data and not context.user_data.get("awaiting_program"):
        context.user_data["awaiting_program"] = True
        await update.message.reply_text("Какую программу вы рассматриваете: AI или AI Product?")
        return

    # Обрабатываем выбор программы
    if context.user_data.get("awaiting_program"):
        choice = user_input.lower()
        if "product" in choice:
            context.user_data["program"] = "ai_product"
            context.user_data["awaiting_program"] = False
            await update.message.reply_text(
                "Отлично! Вы выбрали программу AI Product. Теперь задайте свой вопрос."
            )
        elif "ai" in choice:
            context.user_data["program"] = "ai"
            context.user_data["awaiting_program"] = False
            await update.message.reply_text(
                "Отлично! Вы выбрали программу AI. Теперь задайте свой вопрос."
            )
        else:
            await update.message.reply_text("Пожалуйста, выберите 'AI' или 'AI Product'.")
        return

    program = context.user_data.get("program")

    try:
        if "сравн" in user_input.lower():
            response = qa_engine.compare(user_input)
        else:
            response = qa_engine.answer(user_input, program)

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
