from langchain.prompts import PromptTemplate
import google.generativeai as genai
from langchain.chains.question_answering import load_qa_chain
from langchain_google_genai import ChatGoogleGenerativeAI
from config import GOOGLE_API_KEY

genai.configure(api_key=GOOGLE_API_KEY)

def get_chain():
    template = """
    Respond in as much detail as possible within the provided context. Provide full details. If the answer does not exist within the context, simply state, "answer not available in context".
Context:
{context}
Question:
{question}
Answer:
    """
    prompt = PromptTemplate(template=template, input_variables=["context", "question"])
    model = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.3)
    return load_qa_chain(model, chain_type="stuff", prompt=prompt)
