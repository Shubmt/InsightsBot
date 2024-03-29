from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class UploadedFiles(Base):
    __tablename__ = 'uploaded_files'

    id = Column(Integer, primary_key=True)
    file_name = Column(String, nullable=False)
    file_path = Column(String, nullable=False)

    def __repr__(self):
        return f"<UploadedFile(id={self.id}, file_name={self.file_name}, file_path={self.file_path})>"
        
