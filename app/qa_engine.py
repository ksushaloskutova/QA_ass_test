from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_community.llms import HuggingFacePipeline
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
import config, html_parser


class QAEngine:
    def __init__(self):
        print("🔄 Загружаю и обрабатываю учебные планы...")

        documents = []
        self.course_data = []
        for url in config.PDF_URLS:
            text = html_parser.fetch_pdf_text(url)
            if text:
                documents.append(text)
                parsed = html_parser.parse_course_data(text)
                if parsed:
                    self.course_data.extend(parsed)

        if not documents:
            raise ValueError("❌ Не удалось загрузить ни одного учебного плана.")

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=config.CHUNK_SIZE,
            chunk_overlap=config.CHUNK_OVERLAP
        )
        docs = text_splitter.create_documents(documents)

        print("📐 Создание эмбеддингов...")
        embedding_model = HuggingFaceEmbeddings(
            model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
        )
        self.db = FAISS.from_documents(docs, embedding_model)

        print("🧠 Загрузка языковой модели cointegrated/rut5-base...")
        tokenizer = AutoTokenizer.from_pretrained("cointegrated/rut5-small")
        model = AutoModelForSeq2SeqLM.from_pretrained("cointegrated/rut5-small")

        pipe = pipeline(
            "text2text-generation",
            model=model,
            tokenizer=tokenizer,
            max_length=512,
            do_sample=False
        )
        self.llm = HuggingFacePipeline(pipeline=pipe)

        self.retriever = self.db.as_retriever(search_kwargs={"k": 3})

        self.prompt = PromptTemplate(
            template=(
                "Контекст:\n{context}\n\n"
                "Вопрос:\n{question}\n\n"
                "Ответ:"
            ),
            input_variables=["context", "question"]
        )

        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            retriever=self.retriever,
            chain_type="refine",
            chain_type_kwargs={"prompt": self.prompt}
        )

    def answer(self, query: str) -> str:
        result = self.qa_chain.invoke({"query": query})
        return result["result"]
