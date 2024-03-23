from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.chatbot_api import chatbot_router

load_dotenv()

origins = [
    "http://localhost:8080",
    "http://localhost:3000",
    "http://localhost:8000",
    "http://tringle.zapto.org:52003/",
    "*"
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chatbot_router)