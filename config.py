import json
import logging
from dataclasses import dataclass

@dataclass
class AppConfig:
    chroma_path: str
    chroma_collection_name: str
    wikipedia_urls: list[str]

def load_config(path : str) -> AppConfig:
    
    try:
        with open(path, "r") as f:
            data = json.load(f)
    except:
        error = "Could not load config file, please check the path"
        logging.error(error)
        raise Exception(error)
    
    return AppConfig(**data)