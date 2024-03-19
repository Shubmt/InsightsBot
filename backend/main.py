from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Any
from .document_processor import DocumentProcessor
from .llm_chatbot import LLMChatbot

# Load environment variables from .env file (if any)
load_dotenv()

class Response(BaseModel):
    result: str | None

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000"
]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/predict", response_model = Response)
def predict() -> Any:
  
    vectorDB = DocumentProcessor(['C:/Users/shbhm/Downloads/llm-assignment-master/llm-assignment-master/backend/assets/info.txt'])
    db = vectorDB.process_documents()
    model_path = 'C:/Users/shbhm/Downloads/llm-assignment-master/llm-assignment-master/backend/llama-2-7b-chat.ggmlv3.q3_K_M.bin'
    db_path = './faiss'
    document_qa = LLMChatbot(model_path, db)
    question = "Who is the author of FftSharp? What is their favorite color?"
    answer = document_qa.answer_question(question)
    print(answer)
  
    return {"result": answer}