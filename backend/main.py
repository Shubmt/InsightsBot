from dotenv import load_dotenv
from fastapi import FastAPI, Request, UploadFile, File
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Any
from .document_processor import DocumentProcessor
from .llm_chatbot import LLMChatbot
from .database_manager import DatabaseManager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()

class Response(BaseModel):
    result: str | None

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000"
]

app = FastAPI()
database_manager = DatabaseManager("postgresql://postgres:postgres@localhost/prostgres")

engine = create_engine('postgresql://postgres:postgres@localhost/prostgres')
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

chatbot = LLMChatbot()

async def save_uploaded_file(file: UploadFile = File(...), destination: str = "C:/Users/shbhm/Downloads/llm-assignment-master/llm-assignment-master/backend/assets"):
    file_path = f"{destination}/{file.filename}"
    with open(file_path, "wb") as new_file:
        new_file.write(await file.read())
    return file_path


@app.post("/upload_file", response_model = Response)
async def upload_file(request: Request) -> Any:

    form = await request.form()
    file = form.get("file")
    file_path = await save_uploaded_file(file)
    chatbot.generate_vectorDB(file_path)

@app.post("/clear-context", response_model=str)
async def clear_context(request: Request) -> Any:
    chatbot.clear_context()

@app.post("/intialize-llm", response_model=str)
async def initialize_LLM(request: Request) -> Any:
    chatbot.initialize_LLM()

@app.post("/predict", response_model = Response)
async def predict(request: Request) -> Any:

    form = await request.form()
    question = form.get("question") 
    answer = chatbot.answer_question(question)
    return {"result": answer}
