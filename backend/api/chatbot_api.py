from fastapi import Request, UploadFile, APIRouter
from pydantic import BaseModel
from ..llm_chatbot import LLMChatbot
from ..utils import save_uploaded_file

class Response(BaseModel):
    result: str | None


chatbot_router = APIRouter(prefix="/chatbot", tags=["chatbot"])

class ChatbotApi:

    def __init__(self) -> None:
        self.chatbot = None

    @chatbot_router.get("/initialize", response_model = Response)
    async def initialize(self, request: Request):
        if self.chatbot:
            return  {"result": "chatbot already initialized"}
        self.chatbot = LLMChatbot()
        return {"result": "ok"}
    

    @chatbot_router.post("/upload_file", response_model = Response)
    async def upload_file(self, request: Request, file: UploadFile):

        form = await request.form()
        file = form.get("file")
        file_path = await save_uploaded_file(file)
        self.chatbot.set_or_update_context(file_path)
        return {"result": "ok"}


    @chatbot_router.post("/clear-context", response_model=str)
    async def clear_context(self, request: Request):
        self.chatbot.clear_context()
        return {"result": "ok"}


    @chatbot_router.post("/predict", response_model = Response)
    async def predict(self, request: Request):

        form = await request.form()
        question = form.get("question") 
        answer = self.chatbot.answer_question(question)
        return {"result": answer}

