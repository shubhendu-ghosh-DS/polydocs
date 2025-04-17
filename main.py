from fastapi import FastAPI, UploadFile, File, Form, BackgroundTasks
from fastapi.responses import JSONResponse
from uuid import uuid4
from vector_handler import create_vector_store, delete_vector_store, query_vector_store
from pdf_utils import extract_text_from_pdfs, split_text
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()


@app.post("/upload/")
async def upload_pdfs(background_tasks: BackgroundTasks, files: list[UploadFile] = File(...)):
    session_id = str(uuid4())
    raw_text = await extract_text_from_pdfs(files)
    chunks = split_text(raw_text)

    create_vector_store(session_id, chunks)

    # Schedule deletion after 15 minutes
    background_tasks.add_task(delete_vector_store, session_id, delay=900)

    return {"session_id": session_id, "message": "PDF uploaded and processed."}


@app.post("/query/")
async def query_pdf(session_id: str = Form(...), question: str = Form(...)):
    response = query_vector_store(session_id, question)
    return JSONResponse(content={"answer": response})
