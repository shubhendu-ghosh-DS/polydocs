import time
import threading
from pinecone import Pinecone, ServerlessSpec
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_core.documents import Document
from config import PINECONE_API_KEY
from chat_utils import get_chain
from fastapi import HTTPException
from pinecone.openapi_support.exceptions import NotFoundException

# Initialize Pinecone client
pc = Pinecone(api_key=PINECONE_API_KEY)

# Initialize embedding model
embedding_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

# Create vector store using session_id
def create_vector_store(session_id, texts):
    index_name = session_id

    # Create index if not exists
    existing_indexes = [index["name"] for index in pc.list_indexes()]
    if index_name not in existing_indexes:
        pc.create_index(
            name=index_name,
            dimension=768,  # Adjust this if your model outputs a different dimension
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1")
        )
        while not pc.describe_index(index_name).status["ready"]:
            time.sleep(2)

    # Get index
    index = pc.Index(index_name)

    # Convert texts into Document format
    documents = [Document(page_content=text) for text in texts]

    # Create vector store and add documents
    vectorstore = PineconeVectorStore(index=index, embedding=embedding_model)
    vectorstore.add_documents(documents=documents)

# Query vector store
def query_vector_store(session_id, question):
    index_name = session_id
    try:
        index = pc.Index(index_name)

        vectorstore = PineconeVectorStore(index=index, embedding=embedding_model)
        retriever = vectorstore.as_retriever(
            search_type="similarity_score_threshold",
            search_kwargs={"k": 3, "score_threshold": 0.5},
        )

        docs = retriever.invoke(question)
        chain = get_chain()
        result = chain({"input_documents": docs, "question": question}, return_only_outputs=True)
        return result["output_text"]

    except NotFoundException as e:
        raise HTTPException(
            status_code=404,
            detail=f"Session '{session_id}' has expired or does not exist."
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred: {str(e)}"
        )

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
