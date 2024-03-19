from typing import Type, Union
from langchain.document_loaders.directory import DirectoryLoader
from langchain.document_loaders.unstructured import UnstructuredAPIFileLoader
from langchain.document_loaders.text import TextLoader
from langchain.document_loaders.pdf import PyPDFLoader
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from langchain.vectorstores.faiss import FAISS

class DocumentProcessor():
    def __init__(self, files):
        self.files = files
        self.db = None

    def process_documents(self):
        if self.db:
            return self.db
        loader = UnstructuredAPIFileLoader(file_path=self.files, api_key='BNVlgWXMVO0whIKPc1xVWK0atGxNR2')
        documents = loader.load()
        print(documents)
        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        texts = splitter.split_documents(documents)
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2", model_kwargs={'device': 'cpu'})
        self.db = FAISS.from_documents(texts, embeddings)
        self.db.save_local("faiss")
        return self.db


        