from fastapi import FastAPI, UploadFile, File, Form, BackgroundTasks, HTTPException
from fastapi.responses import JSONResponse
from uuid import uuid4
from vector_handler import create_vector_store, delete_vector_store, query_vector_store
from pdf_utils import extract_text_from_pdfs, split_text
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from pinecone.openapi_support.exceptions import NotFoundException

load_dotenv()

app = FastAPI()


@app.post("/upload")
async def upload_pdfs(background_tasks: BackgroundTasks, files: list[UploadFile] = File(...)):
    session_id = str(uuid4())
    raw_text = await extract_text_from_pdfs(files)
    chunks = split_text(raw_text)

    create_vector_store(session_id, chunks)

    created_at = datetime.utcnow()
    will_be_removed_at = created_at + timedelta(minutes=15)

    # Schedule deletion after 15 minutes
    background_tasks.add_task(delete_vector_store, session_id, delay=900)

    return {
        "session_id": session_id,
        "message": "PDF uploaded and processed.",
        "created_at": created_at.isoformat() + "Z",
        "will_be_removed_at": will_be_removed_at.isoformat() + "Z"
    }


@app.post("/query")
async def query_pdf(session_id: str = Form(...), question: str = Form(...)):
    try:
        response = query_vector_store(session_id, question)
        return JSONResponse(content={"answer": response})
    except NotFoundException:
        raise HTTPException(status_code=404, detail=f"Session '{session_id}' does not exist or has expired.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/clear")
async def clear_session(session_id: str = Form(...)):
    try:
        delete_vector_store(session_id)
        return {"message": f"Session '{session_id}' has been cleared."}
    except NotFoundException:
        raise HTTPException(status_code=404, detail=f"Session '{session_id}' does not exist.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
