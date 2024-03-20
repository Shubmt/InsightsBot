from langchain.llms.ctransformers import CTransformers
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from langchain.vectorstores.faiss import FAISS
from langchain.prompts import PromptTemplate
from langchain.chains.retrieval_qa.base import RetrievalQA

from .document_processor import DocumentProcessor

class LLMChatbot:
    def __init__(self):
        self.vectorDB = None
        self.model_path = 'C:/Users/shbhm/Downloads/llm-assignment-master/llm-assignment-master/backend/llama-2-7b-chat.ggmlv3.q3_K_M.bin'
        self.qa_llm = None

    def generate_vectorDB(self, file_path):
        doc_processor = DocumentProcessor()
        self.vectorDB = doc_processor.process_documents(file_path)

    def initialize_LLM(self):
        llm = CTransformers(model=self.model_path,
                            model_type='llama',
                            config={'max_new_tokens': 256, 'temperature': 0.01})

        retriever = self.vectorDB.as_retriever(search_kwargs={'k': 2})
        prompt = PromptTemplate(
            template="""Please utilize the provided information to respond to the user's inquiry. If you're unsure of the answer, simply state that you don't know; please refrain from inventing an answer.
                        Context: {context}
                        Question: {question}
                        Kindly provide only the relevant answer below, excluding any additional information.
                        Helpful answer:
                        """,
            input_variables=['context', 'question'])
        self.qa_llm = RetrievalQA.from_chain_type(llm=llm,
                                            chain_type='stuff',
                                            retriever=retriever,
                                            return_source_documents=True,
                                            chain_type_kwargs={'prompt': prompt})    



    def clear_context(self):
        self.vectorDB = None

    def answer_question(self, question: str) -> str:
        if self.vectorDB is None:
            raise Exception("File context not set yet.")
        output = self.qa_llm({'query': question})
        return output["result"]
