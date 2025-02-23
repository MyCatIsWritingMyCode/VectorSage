import chromadb
import uuid
import json
import os
from config import AppConfig

class ChromaDBHandler:
    def __init__(self, config_data : AppConfig):
        self.config = config_data
        self.client = chromadb.PersistentClient(path=self.get_path(self.config.chroma_path))

    def get_or_create_collection(self, collection_name: str) -> chromadb.Collection:
        collection = self.client.get_or_create_collection(name=collection_name)
        return collection
    
    def get_path(self, relative_path: str) -> str:
        base_path = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(base_path, relative_path)

    def load_config(self, config_path: str) -> dict:
        with open(config_path, 'r') as config_file:
            return json.load(config_file)

    def upsert_documents(self, collection: chromadb.Collection, documents: list):
        ids = [str(uuid.uuid4()) for _ in documents]
        collection.upsert(documents=documents, ids=ids)

    def query_documents(self, collection: chromadb.Collection, query_texts: list, n_results: int) -> chromadb.QueryResult:
        return collection.query(query_texts=query_texts, n_results=n_results)

    def peek_collection(self, collection: chromadb.Collection) -> chromadb.GetResult:
        return collection.peek()
