from fastapi import Request, UploadFile, APIRouter
from pydantic import BaseModel

from ..llm_chatbot import LLMChatbot
from ..utils import save_uploaded_file
from ..database_manager import DatabaseManager
from ..db.models.uploaded_files import UploadedFiles

class Response(BaseModel):
    result: str | None

chatbot_router = APIRouter(prefix="/chatbot", tags=["chatbot"])

class InputQuestion(BaseModel):
    question: str


async def save_file_in_db(file_name, file_path):
    try:
        db = next(DatabaseManager().get_db())
        uploaded_file = UploadedFiles(file_name=file_name, file_path=file_path)
        db.add(uploaded_file)
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"An error occurred: {e}")
    finally:
        db.close()


class ChatbotApi:
    CHATBOT = None
    
    @chatbot_router.get("/initialize", response_model = Response)
    async def initialize(request: Request):
        if ChatbotApi.CHATBOT:
            return  {"result": "chatbot already initialized"}
        ChatbotApi.CHATBOT = LLMChatbot()
        return {"result": "ok"}

    @chatbot_router.post("/upload_file", response_model = Response)
    async def upload_file(request: Request, file: UploadFile):

        form = await request.form()
        file = form.get("file")
        file_path = await save_uploaded_file(file)
        await save_file_in_db(file_name=file.filename, file_path=file_path)
        ChatbotApi.CHATBOT.set_or_update_context(file_path)
        return {"result": "ok"}


    @chatbot_router.post("/clear-context", response_model=str)
    async def clear_context(request: Request):
        ChatbotApi.CHATBOT.clear_context()
        return {"result": "ok"}


    @chatbot_router.post("/predict", response_model = Response)
    async def predict(request: Request, question: InputQuestion):
        # form = await request.form()
        # question = form.get("question") 
        answer = ChatbotApi.CHATBOT.answer_question(question.question)
        return {"result": answer}

