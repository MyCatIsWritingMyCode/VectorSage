# VectorSage

VectorSage is a Python application that scrapes information from popular Wikipedia pages, stores the data in ChromaDB, and uses a local Ollama DeepSeek model to answer questions based on the stored data.

## Features

**Web Scraping:** Scrapes content from a list of Wikipedia URLs.
**Data Storage:** Stores the scraped content in ChromaDB.
**Question Answering:** Uses a local Ollama DeepSeek model to answer questions based on the stored data.

## Setup

Create a new venv enviroment, activate it and install all dependencies from the requirements.txt

```shell
python -m venv envname
```

```shell
.\envname\Scripts\activate
```

```shell
pip install -r requirements.txt
```

## Usage

### 1. Setup:

```shell
python main.py setup
```

Running the program in setup mode will create and populate a local chroma db inside a folder named **chroma**.

### 2. Ask a Question:

```shell
python main.py question
```

Running the program in question mode will promt a user to ask a question.
For best result enter a question that can be answered with the data stored in the chroma database.