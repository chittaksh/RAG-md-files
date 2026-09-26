from pathlib import Path
from logger import logging

from langchain_community.document_loaders import Docx2txtLoader

def load_docx_docs(data_path: Path):
    """
    Load all the docx files from the incoming data_path.

    Parameters:
    data_path: Path
        Path of the  folder containing the DOCX files

    Return:
    docs: list
        list of langchain document objects

    DOCX -> Docx2txtLoader -> Langchain document objects
    """
    docs = []

    for file in data_path.glob("*.docx"):
        logging.info(f"Loading..: {file.name}")

        loader = Docx2txtLoader(str(file))  ## Docx2txtLoader reads the DOCX file and extracts text.

        docs.extend(loader.load())
    return docs