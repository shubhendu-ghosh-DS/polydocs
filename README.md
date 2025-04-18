# 📄 Polydocs

Polydocs is a lightweight FastAPI-based backend application that enables users to **upload PDF files and chat with their contents**. This backend is designed to be containerized with Docker and is currently hosted on **Hugging Face Spaces**.

> ⚠️ Note: This repository only includes the backend APIs. A separate frontend can be developed to interact with this API for a complete user-facing application.

---
🌐 **Live Demo**: [Try Polydocs APIs on Hugging Face Spaces](https://shubhendu-ghosh-polydocs.hf.space)

---

## 🚀 Features

- 📁 Upload one or more PDF files
- 💬 Ask questions related to the uploaded documents
- 🧠 Powered by **LangChain**, **Google Generative AI**, and **Pinecone** vector store
- ⏳ Temporary sessions (auto-expire after 15 minutes)
- 🐳 Dockerized for easy deployment

---

## 🧪 Available API Endpoints

### `POST /upload`
Uploads and processes one or more PDF files.

- **Request:** `multipart/form-data`
  - `files`: list of PDF files
- **Response:**
```json
{
  "session_id": "generated-uuid",
  "message": "PDF uploaded and processed.",
  "created_at": "2025-04-18T12:00:00Z",
  "will_be_removed_at": "2025-04-18T12:15:00Z"
}
```

### `POST /query`\n\nAsks a question related to a previously uploaded PDF session.

- **Request:** `application/x-www-form-urlencoded`
  - `session_id`: ID received from `/upload`
  - `question`: Natural language query
- **Response**

```json
{
  "answer": "Relevant answer from the uploaded document"
}
```

---

### `POST /clear`

Manually clears a session before the automatic timeout.

- **Request:** `application/x-www-form-urlencoded`
  - `session_id`: Session to delete
- **Response:**

```json
{
  "message": "Session '...' has been cleared."
}
```

## 📦 Tech Stack  
- [FastAPI](https://fastapi.tiangolo.com/) – Web framework  
- [Pinecone](https://www.pinecone.io/) – Vector database  
- [LangChain](https://www.langchain.com/) – LLM orchestration  
- [Google Generative AI](https://ai.google.dev/) – Language model backend  
- [PyPDF2](https://pypi.org/project/PyPDF2/) – PDF parsing  
- [Docker](https://www.docker.com/) – Containerization  

## ⚙️ Installation & Usage (Local Development)  
### 1. Clone the repository  

```bash
git clone https://github.com/your-username/Polydocs.git
cd Polydocs
```

### 2. Create a `.env` file  

```env
PINECONE_API_KEY=your-key
GOOGLE_API_KEY=your-key
# Add any additional keys as needed
```

### 3. Install dependencies  

```bash
pip install -r requirements.txt
```

### 4. Run the application  

```bash
uvicorn main:app --reload
```

## 🐳 Running with Docker  
Make sure you have Docker installed.

```bash
docker build -t polydocs-backend .
docker run -p 8000:8000 --env-file .env polydocs-backend
```

## 📁 Project Structure  

```bash
Polydocs/
│
├── main.py                # FastAPI app
├── requirements.txt       # Python dependencies
├── pdf_utils.py           # PDF reading and splitting logic
├── vector_handler.py      # Pinecone vector operations
├── .env                   # API keys and configs (not committed)
└── Dockerfile             # (if present) for containerization
```

## 🧠 Motivation  
In an era of AI-enhanced productivity, Polydocs allows users to interact with documents more intelligently. Whether it's for research, customer support, or quick document search, Polydocs streamlines PDF interaction using natural language.

## 📬 Contact  
Built by [Shubhendu Ghosh](https://www.linkedin.com/in/shubhendu-ghosh-ds/)

If you find this project interesting, feel free to ⭐ the repo or connect with me on [LinkedIn](https://www.linkedin.com/in/shubhendu-ghosh-ds/)!


## 📝 License  
MIT License – Feel free to use and modify.


