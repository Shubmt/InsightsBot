from fastapi import FastAPI
from databases import Database
from typing import Optional, Dict, Any

class DatabaseManager:
    def __init__(self, database_url: str):
        self.database_url = database_url
        self.database = Database(database_url)
        
    def connect(self):
        self.database.connect()
        
    def disconnect(self):
        self.database.disconnect()
        
    def fetch_one(self, query: str, values: Optional[Dict[str, Any]] = None):
        return self.database.fetch_one(query=query, values=values)

