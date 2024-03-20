from dotenv import load_dotenv
from fastapi import FastAPI, Request, UploadFile, File
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Any
from .document_processor import DocumentProcessor
from .llm_chatbot import LLMChatbot
from .database_manager import DatabaseManager

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
database_manager = DatabaseManager("postgresql://postgres:postgres@localhost/prostgres")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def save_uploaded_file(file: UploadFile = File(...), destination: str = "C:/Users/shbhm/Downloads/llm-assignment-master/llm-assignment-master/backend/assets"):
    file_path = f"{destination}/{file.filename}"
    with open(file_path, "wb") as new_file:
        new_file.write(await file.read())
    return file_path




@app.post("/predict", response_model = Response)
async def predict(request: Request) -> Any:

    form = await request.form()
    question = form.get("question")
    file = form.get("file")
    file_path = await save_uploaded_file(file)

    vectorDB = DocumentProcessor([file_path])
    db = vectorDB.process_documents()   
    
    model_path = 'C:/Users/shbhm/Downloads/llm-assignment-master/llm-assignment-master/backend/llama-2-7b-chat.ggmlv3.q3_K_M.bin'
    db_path = './faiss'
    document_qa = LLMChatbot(model_path, db)

    answer = document_qa.answer_question(question)
    print(answer)
  
    return {"result": answer}

# import uvicorn
# from dotenv import load_dotenv
# from fastapi import FastAPI, Request
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel
# from typing import Any
# from .document_processor import DocumentProcessor
# from .llm_chatbot import LLMChatbot
# from .database_manager import DatabaseManager

# load_dotenv()

# class Response(BaseModel):
#     result: str | None

# class FastAPIApp:
#     def __init__(self):
#         self.app = FastAPI()
#         self.setup_middleware()
#         self.setup_database_manager()
#         self.setup_routes()

#     def setup_middleware(self):
#         origins = [
#             "http://localhost",
#             "http://localhost:8080",
#             "http://localhost:3000"
#         ]
#         self.app.add_middleware(
#             CORSMiddleware,
#             allow_origins=origins,
#             allow_credentials=True,
#             allow_methods=["*"],
#             allow_headers=["*"],
#         )

#     def setup_database_manager(self):
#         self.database_manager = DatabaseManager("postgresql://postgres:postgres@localhost/prostgres")

#     def setup_routes(self):
#         @self.app.post("/predict", response_model=Response)
#         async def predict(request: Request) -> Any:
#             form = await request.form()
#             question = form.get("question")
#             answer = self.document_qa.answer_question(question)
#             print(answer)
#             return {"result": answer}

#     def run(self):
#         self.vectorDB = DocumentProcessor(['C:/Users/shbhm/Downloads/llm-assignment-master/llm-assignment-master/backend/assets/info.txt'])
#         self.db = self.vectorDB.process_documents()
#         model_path = 'C:/Users/shbhm/Downloads/llm-assignment-master/llm-assignment-master/backend/llama-2-7b-chat.ggmlv3.q3_K_M.bin'
#         self.db_path = './faiss'
#         self.document_qa = LLMChatbot(model_path, self.db)
#         self.app.run()

# app = FastAPIApp

# if __name__ == "__main__":
#     uvicorn.run("main:app", host="127.0.0.1", port=8000, log_level="info")
