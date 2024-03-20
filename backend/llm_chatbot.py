from langchain.llms.ctransformers import CTransformers
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from langchain.vectorstores.faiss import FAISS
from langchain.prompts import PromptTemplate
from langchain.chains.retrieval_qa.base import RetrievalQA

from .document_processor import DocumentProcessor

class LLMChatbot:
    def __init__(self):
        self.model_path = 'C:/Users/shbhm/Downloads/llm-assignment-master/llm-assignment-master/backend/llama-2-7b-chat.ggmlv3.q3_K_M.bin'
        self.doc_processor = DocumentProcessor()
        self.llm = None
        self.prompt = None
        self.qa_llm = None
        self.initialize_LLM()

   
    def initialize_LLM(self):
        self.llm = CTransformers(
                        model=self.model_path,
                        model_type='llama',
                        config={'max_new_tokens': 256, 'temperature': 0.01}
                    )

        self.prompt = PromptTemplate(
            template="""Please utilize the provided information to respond to the user's inquiry. If you're unsure of the answer, simply state that you don't know; please refrain from inventing an answer.
                        Context: {context}
                        Question: {question}
                        Kindly provide only the relevant answer below, excluding any additional information.
                        Helpful answer:
                        """,
            input_variables=['context', 'question']
        )
      
        
    def set_or_update_context(self, file_path):
        self.doc_processor.process_document(file_path)
        self._build_llm()
        
    def _build_llm(self):
        retriever = self.doc_processor.vectorDB.as_retriever(search_kwargs={'k': 2})
        self.qa_llm = RetrievalQA.from_chain_type(llm=self.llm,
                                            chain_type='stuff',
                                            retriever=retriever,
                                            return_source_documents=True,
                                            chain_type_kwargs={'prompt': self.prompt})


    def clear_context(self):
        self.doc_processor.vectorDB = None

    def answer_question(self, question: str) -> str:
        if self.doc_processor.vectorDB is None:
            raise Exception("File context not set yet.")
        output = self.qa_llm({'query': question})
        return output["result"] 
