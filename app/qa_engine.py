from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_community.llms import HuggingFacePipeline
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

import config
import html_parser


class QAEngine:
    """Два отдельных QA-движка для программ AI и AI Product."""

    def __init__(self) -> None:
        print("🔄 Загружаю и обрабатываю учебные планы...")

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=config.CHUNK_SIZE,
            chunk_overlap=config.CHUNK_OVERLAP,
        )

        print("📐 Создание эмбеддингов...")
        embedding_model = HuggingFaceEmbeddings(
            model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
        )

        print("🧠 Загрузка языковой модели cointegrated/rut5-base...")
        tokenizer = AutoTokenizer.from_pretrained("cointegrated/rut5-small")
        model = AutoModelForSeq2SeqLM.from_pretrained("cointegrated/rut5-small")
        pipe = pipeline(
            "text2text-generation",
            model=model,
            tokenizer=tokenizer,
            max_length=512,
            do_sample=False,
        )
        self.llm = HuggingFacePipeline(pipeline=pipe)

        self.prompt = PromptTemplate(
            template=(
                "Контекст:\n{context}\n\n"
                "Вопрос:\n{question}\n\n"
                "Ответ:"
            ),
            input_variables=["context", "question"],
        )

        # Создаём отдельные QA-цепочки для каждой программы
        self.qa_chains = {}
        for program, url in config.PDF_URLS.items():
            text = html_parser.fetch_pdf_text(url)
            if not text:
                raise ValueError(f"❌ Не удалось загрузить учебный план: {url}")

            docs = text_splitter.create_documents([text])
            db = FAISS.from_documents(docs, embedding_model)
            retriever = db.as_retriever(search_kwargs={"k": 3})
            chain = RetrievalQA.from_chain_type(
                llm=self.llm,
                retriever=retriever,
                chain_type="refine",
                chain_type_kwargs={"prompt": self.prompt},
            )
            self.qa_chains[program] = chain

    def _run_chain(self, query: str, program: str) -> str:
        chain = self.qa_chains.get(program)
        if not chain:
            raise ValueError("Неизвестная программа")
        result = chain.invoke({"query": query})
        if isinstance(result, dict):
            return result.get("result", "")
        return result

    def answer(self, query: str, program: str) -> str:
        """Ответ для конкретной программы."""
        return self._run_chain(query, program)

    def compare(self, query: str) -> str:
        """Сравнение ответов по обеим программам."""
        ai_answer = self._run_chain(query, "ai")
        ai_prod_answer = self._run_chain(query, "ai_product")
        return (
            f"Программа AI:\n{ai_answer}\n\n"
            f"Программа AI Product:\n{ai_prod_answer}"
        )


    def answer(self, query: str) -> str:
        result = self.qa_chain.invoke({"query": query})
        return result["result"]

