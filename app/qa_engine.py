# app/qa_engine.py

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
# from langchain.chains.question_answering import load_qa_chain
from langchain.chains import RetrievalQA
from langchain_community.llms import HuggingFacePipeline
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from sentence_transformers import SentenceTransformer
import config, html_parser

class QAEngine:
    def __init__(self):
        print("🔄 Загружаю документы...")
        documents = [html_parser.fetch_html_content(url) for url in config.HTML_URLS]

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=config.CHUNK_SIZE,
            chunk_overlap=config.CHUNK_OVERLAP
        )
        docs = text_splitter.create_documents(documents)

        print("📐 Создание эмбеддингов...")
        # Используем sentence-transformers модель
        embedding_model = HuggingFaceEmbeddings(
            model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
        )
        self.db = FAISS.from_documents(docs, embedding_model)

        print("🧠 Загрузка языковой модели...")
        tokenizer = AutoTokenizer.from_pretrained("sberbank-ai/rugpt3small_based_on_gpt2")
        model = AutoModelForCausalLM.from_pretrained("sberbank-ai/rugpt3small_based_on_gpt2")

        pipe = pipeline("text-generation", model=model, tokenizer=tokenizer, max_new_tokens=150)
        llm = HuggingFacePipeline(pipeline=pipe)

        retriever = self.db.as_retriever()
        self.qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever, chain_type="stuff")

    def answer(self, query: str) -> str:
        return self.qa_chain.run(query)
