import chromadb
import uuid
import json

# Load the configuration from the JSON file
with open('../Resources/config.json', 'r') as config_file:
    _config = json.load(config_file)

chroma_client = chromadb.PersistentClient(path=_config['chroma_path'])

collection = chroma_client.get_or_create_collection(name="my_collection")

collection.upsert(
    documents=[
        "This is a document about pineapple",
        "This is a document about oranges"
    ],
    ids=[str(uuid.uuid4()), str(uuid.uuid4())]
)

results = collection.query(
    query_texts=["This is a query document about florida"],
    n_results=2 
)

print(results)
