from pathlib import Path
from logger import logging

from langchain_community.document_loaders import UnstructuredMarkdownLoader

def load_md_docs(data_path: Path):
    """
    Load all the md files from the incoming data_path.

    Parameters:
    data_path: Path
        Path of the  folder containing the md files
    
    Return:
    docs: list
        list of langchain document objects
    """
    docs = []

    for file in data_path.glob("*.md"):
        logging.info(f"Loading..: {file.name}")

        loader = UnstructuredMarkdownLoader(str(file))

        docs.extend(loader.load())
    return docs