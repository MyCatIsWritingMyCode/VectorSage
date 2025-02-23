import logging, sys
from app import Application
from services.chroma_db_handler import ChromaDBHandler
from config import load_config

def main():
    
    if len(sys.argv) < 2:
        logging.error("Usage: python main.py <mode> \n mode: setup - fill chroma db with scraped information from wikipedia, \n query - query the chroma db for information")
        sys.exit(1)
    
    # Set up logging
    logging.basicConfig(filename='log.txt', format='%(asctime)s %(levelname)-8s %(message)s', encoding='utf-8', level=logging.INFO)
    
    # Load config
    config_data = load_config("./resources/config.json")
    
    # Create ChromaDBHandler
    chroma_db_handler = ChromaDBHandler(config_data)
    
    # Create Application
    app = Application(config_data, chroma_db_handler)
    
    match(sys.argv[1]):
        case "setup":
            app.runSetup()
            
        case "question":
            print("Please enter your question: ")
            try:
                question = input()
                app.runQuestion(question)
            except:
                logging.error("An error occurred while processing the query")
                sys.exit(1)
                
        case _:
            logging.warning("Invalid mode, please choose either setup or query")
            sys.exit(1)

    logging.info("Program completed successfully. closing...")
    sys.exit(0)

if __name__ == "__main__":
    main()