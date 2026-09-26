## Responsible for runing the main project, which will take the user input
from logging import logging

from rag_chain import generate_answer

def main():
    logging.info("Hello from rag-project!")

    while True:
        query = input("\n Ask a question: ").strip()

        ## Handle empty input:

        if not query:
            logging.warning("Please enter a valid question")
            continue

        ## Exit condition
        if query.lower() in ["exit", "quit"]:
            logging.info("Exiting RAG application")
            break

        ## Execute RAG pipeline
        try:
            answer = generate_answer(query)
            logging.info("\n Answer: ")
            logging.info(answer)
        except Exception as e:
            logging.error(f"\nError : {e}")


if __name__ == "__main__":
    main()