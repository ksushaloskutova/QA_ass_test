from langchain.agents import Tool
from qa_engine import QAEngine

# Инициализируем QA
qa = QAEngine()

# Простой калькулятор
def calculator_tool(input_text: str) -> str:
    try:
        result = eval(input_text)
        return f"Результат: {result}"
    except Exception:
        return "Ошибка в вычислении"

tools = [
    Tool(
        name="QA",
        func=qa.answer,
        description="Отвечает на вопросы по HTML-документам"
    ),
    Tool(
        name="Calculator",
        func=calculator_tool,
        description="Выполняет простые вычисления, например '15 * 42'"
    ),
]
