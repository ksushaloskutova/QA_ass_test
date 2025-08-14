from telegram import Update
import os
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from langchain.agents import initialize_agent, AgentType
from agent_tools import tools
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from langchain.llms import HuggingFacePipeline

from qa_engine import QAEngine

# Загружаем LLM
tokenizer = AutoTokenizer.from_pretrained("sberbank-ai/rugpt3small_based_on_gpt2")
model = AutoModelForCausalLM.from_pretrained("sberbank-ai/rugpt3small_based_on_gpt2")
pipe = pipeline("text-generation", model=model, tokenizer=tokenizer, max_new_tokens=150)
llm = HuggingFacePipeline(pipeline=pipe)

# Инициализируем агента
# agent = initialize_agent(
#     tools,
#     llm=llm,
#     agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
#     verbose=True
# )
qa_engine = QAEngine()

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    response = qa_engine.answer(user_input)
    await update.message.reply_text(response)

def run_telegram_bot():
    app = ApplicationBuilder().token(os.getenv("TELEGRAM_TOKEN")).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("🤖 Агент-бот запущен!")
    app.run_polling()
