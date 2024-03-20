from dotenv import load_dotenv
from fastapi import FastAPI, Request, UploadFile, File, APIRouter
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
from typing import Any
from .document_processor import DocumentProcessor
from .database_manager import DatabaseManager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .api.chatbot_api import chatbot_router

load_dotenv()


origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000"
]

app = FastAPI()

engine = create_engine('postgresql://postgres:postgres@localhost/prostgres')
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
)



app.include_router(chatbot_router)