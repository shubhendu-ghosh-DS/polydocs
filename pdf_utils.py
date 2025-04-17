from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter

async def extract_text_from_pdfs(files):
    text = ""
    for file in files:
        pdf = PdfReader(file.file)
        for page in pdf.pages:
            text += page.extract_text()
    return text

def split_text(text):
    splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    return splitter.split_text(text)
