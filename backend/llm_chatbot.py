from langchain.llms.ctransformers import CTransformers
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from langchain.vectorstores.faiss import FAISS
from langchain.prompts import PromptTemplate
from langchain.chains.retrieval_qa.base import RetrievalQA

class LLMChatbot:
    def __init__(self, model_path: str, db):
        self.model_path = model_path
        self.db = db

        self.llm = CTransformers(model=model_path,
                                 model_type='llama',
                                 config={'max_new_tokens': 256, 'temperature': 0.01})

        # self.embeddings = HuggingFaceEmbeddings(
        #     model_name="sentence-transformers/all-MiniLM-L6-v2",
        #     model_kwargs={'device': 'cpu'})
        # self.db = FAISS.load_local(db_path, self.embeddings)

        retriever = self.db.as_retriever(search_kwargs={'k': 2})
        self.prompt = PromptTemplate(
            template="""Please utilize the provided information to respond to the user's inquiry. If you're unsure of the answer, simply state that you don't know; please refrain from inventing an answer.
                        Context: {context}
                        Question: {question}
                        Kindly provide only the relevant answer below, excluding any additional information.
                        Helpful answer:
                        """,
            input_variables=['context', 'question'])
        self.qa_llm = RetrievalQA.from_chain_type(llm=self.llm,
                                                  chain_type='stuff',
                                                  retriever=retriever,
                                                  return_source_documents=True,
                                                  chain_type_kwargs={'prompt': self.prompt})

    def answer_question(self, question: str) -> str:
        output = self.qa_llm({'query': question})
        return output["result"]
