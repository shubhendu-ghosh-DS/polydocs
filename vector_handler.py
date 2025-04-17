import pinecone
import os
import time
import threading
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.vectorstores.pinecone import Pinecone as LangchainPinecone

pinecone.init(api_key=os.getenv("PINECONE_API_KEY"), environment=os.getenv("PINECONE_ENV"))

embedding_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

def create_vector_store(session_id, texts):
    index_name = session_id
    if index_name not in pinecone.list_indexes():
        pinecone.create_index(index_name, dimension=768)
    index = pinecone.Index(index_name)
    vectorstore = LangchainPinecone.from_texts(texts, embedding_model, index_name=index_name)


def query_vector_store(session_id, question):
    index_name = session_id
    vectorstore = LangchainPinecone.from_existing_index(index_name, embedding_model)
    chain = get_chain()
    docs = vectorstore.similarity_search(question)
    result = chain({"input_documents": docs, "question": question}, return_only_outputs=True)
    return result["output_text"]


def delete_vector_store(index_name, delay=0):
    def delayed_delete():
        if delay:
            time.sleep(delay)
        try:
            pinecone.delete_index(index_name)
            print(f"Deleted index {index_name}")
        except Exception as e:
            print(f"Error deleting index {index_name}: {e}")
    threading.Thread(target=delayed_delete).start()
