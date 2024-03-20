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
        self.vectorDB = None
        self.embeddings = self._set_embeddngs()

    def process_document(self, file_path: str):
        documents = self._preprocess_document(file_path=file_path)
        self._create_or_update_db(documents)    
        
        return self.vectorDB
    
    def _set_embeddngs(self):
        return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2", model_kwargs={'device': 'cpu'})

    def _preprocess_document(self, file_path: str):
        loader = UnstructuredAPIFileLoader(file_path=file_path, api_key='BNVlgWXMVO0whIKPc1xVWK0atGxNR2')
        doc = loader.load()
        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        documents = splitter.split_documents(doc)
        return documents
    
    def _create_or_update_db(self, documents):
        if self.vectorDB:
            self.vectorDB.add_documents(documents)
        else:
            self.vectorDB = FAISS.from_documents(documents, self.embeddings)
        self.vectorDB.save_local("faiss")




        