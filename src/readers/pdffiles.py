from pathlib import Path
from logger import logging

from langchain_community.document_loaders import PyPDFLoader   ## to process pdf doc

def load_pdf_docs(data_path: Path):
    """
    Load all the pdf files from the incoming data_path.

    Parameters:
    data_path: Path
        Path of the  folder containing the PDF files
    
    Return:
    docs: list
        list of langchain document objects

    PDF -> PyPDFLoader -> Langchain document objects
    """
    docs = []

    for file in data_path.glob("*.pdf"):
        logging.info(f"Loading..: {file.name}")

        loader = PyPDFLoader(str(file))  ## PyPDFLoader reads the PDF and extracts text.

        docs.extend(loader.load())
    return docs