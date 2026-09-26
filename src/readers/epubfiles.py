from pathlib import Path
from logger import logging

from langchain_community.document_loaders import UnstructuredEPubLoader

def load_epub_docs(data_path: Path):
    """
    Load all the epub files from the incoming data_path.

    Parameters:
    data_path: Path
        Path of the  folder containing the epub files
    
    Return:
    docs: list
        list of langchain document objects
    """
    docs = []

    for file in data_path.glob("*.epub"):
        logging.info(f"Loading..: {file.name}")

        loader = UnstructuredEPubLoader(str(file))

        docs.extend(loader.load())
    return docs