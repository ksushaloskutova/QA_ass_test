import os
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from qa_engine import QAEngine
import recommendations

qa_engine = QAEngine()


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    user_data = context.user_data

    # Stage: ask for previous education or skills
    if not user_data.get("skills") and not user_data.get("awaiting_skills"):
        await update.message.reply_text(
            "Расскажите о вашем предыдущем образовании или навыках."  # noqa: E501
        )
        user_data["awaiting_skills"] = True
        return

    # Stage: receive skills and give elective recommendations
    if user_data.get("awaiting_skills"):
        user_data["skills"] = user_input
        user_data["awaiting_skills"] = False
        electives = recommendations.recommend_electives(user_input)
        if electives:
            rec_text = "\n- ".join(electives)
            await update.message.reply_text(
                "На основе ваших навыков рекомендуем следующие элективы:\n- "
                + rec_text
            )
        else:
            await update.message.reply_text(
                "Пока не могу подобрать элективы по указанным навыкам."
            )
        await update.message.reply_text(
            "Теперь вы можете задать вопрос о программе или учебных планах."
        )
        return

    # Regular QA handling once skills are known
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
