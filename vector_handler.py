import time
import threading
from pinecone import Pinecone, ServerlessSpec
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.vectorstores.pinecone import Pinecone as LangchainPinecone
from config import PINECONE_API_KEY

# Initialize Pinecone client with API key
pc = Pinecone(api_key=PINECONE_API_KEY)  # Replace with your actual key or use os.getenv if needed

# Initialize embedding model
embedding_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

# Create vector store (index) using session_id
def create_vector_store(session_id, texts):
    index_name = session_id
    if not pc.list_indexes().names or index_name not in pc.list_indexes().names:
        pc.create_index(
            name=index_name,
            dimension=768,  # Match your embedding model dimension
            spec=ServerlessSpec(cloud="aws", region="us-east-1")
        )
        time.sleep(5)  # Wait for index to be ready
    vectorstore = LangchainPinecone.from_texts(texts, embedding_model, index_name=index_name)

# Query vector store
def query_vector_store(session_id, question):
    index_name = session_id
    vectorstore = LangchainPinecone.from_existing_index(index_name, embedding_model)
    chain = get_chain()  # Make sure `get_chain` is defined elsewhere
    docs = vectorstore.similarity_search(question)
    result = chain({"input_documents": docs, "question": question}, return_only_outputs=True)
    return result["output_text"]

# Delete vector store with optional delay
def delete_vector_store(index_name, delay=0):
    def delayed_delete():
        if delay:
            time.sleep(delay)
        try:
            pc.delete_index(index_name)
            print(f"Deleted index {index_name}")
        except Exception as e:
            print(f"Error deleting index {index_name}: {e}")
    threading.Thread(target=delayed_delete).start()
