import logging, requests, sys, re
from bs4 import BeautifulSoup
from ollama import chat, ChatResponse
from config import AppConfig
from services.chroma_db_handler import ChromaDBHandler

class Application:
    def __init__(self, config: AppConfig, chroma_db_handler: ChromaDBHandler):
        self.config = config
        self.chroma_db_handler = chroma_db_handler

    def runSetup(self):
        wikipedia_urls = self.config.wikipedia_urls
        vectorEntries = []
        
        logging.info("Scraping Wikipedia entries...")
        try:
            for url in wikipedia_urls:
                response = requests.get(url)
                soup = BeautifulSoup(response.content, 'html.parser')
                paragraphs = soup.find_all('p')
                for para in paragraphs:
                    content = para.get_text()
                    vectorEntries.append(content)
        except:
            logging.error("An error occurred while scraping Wikipedia entries")
            sys.exit(0)
        
        logging.info("Adding scraped entries to ChromaDB...")
        collection = self.chroma_db_handler.get_or_create_collection(self.config.chroma_collection_name)
        self.chroma_db_handler.upsert_documents(collection, vectorEntries)
        
        logging.info("Setup completed successfully - ChromaDB is now populated with scraped Wikipedia entries") 

    def runQuestion(self, queryText: str):
        collection = self.chroma_db_handler.get_or_create_collection(self.config.chroma_collection_name)
        
        logging.info(f"Querying ChromaDB for the question '{queryText}'...")
        queryResult = self.chroma_db_handler.query_documents(collection, queryText, 5)
        
        context = '\n'.join([doc for doc in queryResult['documents'][0]])
        
        logging.info(f"Querying LLM for the answer to the question '{queryText}'...")
        answer = self.get_answer_from_llm(context, queryText)
        
        logging.info(f"Query completed successfully - The answer to the question '{queryText}' is '{answer}'")

    def get_answer_from_llm(self, context: str, question: str) -> str:
        llm_prompt = f"Setup: You are a programming specialist. " \
                     f"You are given a question and a context. " \
                     f"You need to provide an answer to the question based on the context. " \
                     f"Question: {question} " \
                     f"Context: {context}"
        
        response: ChatResponse = chat(model='deepseek-r1:7b', messages=[
        {
            'role': 'user',
            'content': llm_prompt
        },
        ])
        cleaned_respense = re.sub(r'<think>.*?</think>', '', response.message.content, flags=re.DOTALL)
        return cleaned_respense