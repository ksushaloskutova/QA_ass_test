from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import HuggingFacePipeline
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from app import config, html_parser

class QAEngine:
    def __init__(self):
        print("🔄 Загружаю документы...")
        documents = [html_parser.fetch_html_content(url) for url in config.HTML_URLS]

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=config.CHUNK_SIZE, chunk_overlap=config.CHUNK_OVERLAP
        )
        docs = text_splitter.create_documents(documents)

        print("📐 Создание эмбеддингов...")
        embedding_model = HuggingFaceEmbeddings(model_name="intfloat/multilingual-e5-small")
        self.db = FAISS.from_documents(docs, embedding_model)

        print("🧠 Загрузка модели...")
        tokenizer = AutoTokenizer.from_pretrained("sberbank-ai/rugpt3small_based_on_gpt2")
        model = AutoModelForCausalLM.from_pretrained("sberbank-ai/rugpt3small_based_on_gpt2")

        pipe = pipeline("text-generation", model=model, tokenizer=tokenizer, max_new_tokens=150)
        llm = HuggingFacePipeline(pipeline=pipe)

        self.qa_chain = load_qa_chain(llm, chain_type="stuff")

    def answer(self, query: str) -> str:
        docs = self.db.similarity_search(query)
        return self.qa_chain.run(input_documents=docs, question=query)
