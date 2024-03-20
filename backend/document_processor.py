from typing import List, Type, Union
from langchain.document_loaders.directory import DirectoryLoader
from langchain.document_loaders.unstructured import UnstructuredAPIFileLoader
from langchain.document_loaders.text import TextLoader
from langchain.document_loaders.pdf import PyPDFLoader
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from langchain.vectorstores.faiss import FAISS

class DocumentProcessor():
    def __init__(self):
        self.vecorDB = None
        self.embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2", model_kwargs={'device': 'cpu'})

    def process_documents(self, file_path: str, new_context=False):
        if new_context:
            self.vecorDB = None

        loader = UnstructuredAPIFileLoader(file_path=file_path, api_key='BNVlgWXMVO0whIKPc1xVWK0atGxNR2')
        documents = loader.load()
        print(documents)
        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        texts = splitter.split_documents(documents)

        if self.vecorDB:
            self.vecorDB.add_documents(texts)
        else:
            self.vecorDB = FAISS.from_documents(texts, self.embeddings)
        self.vecorDB.save_local("faiss")
        return self.vecorDB


        