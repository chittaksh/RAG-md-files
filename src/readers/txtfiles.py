from pathlib import Path

from langchain_community.document_loaders import TextLoader

def load_txt_docs(data_path: Path):
    """
    Load all the txt files from the incoming data_path.

    Parameters:
    data_path: Path
        Path of the  folder containing the TXT files
    
    Return:
    docs: list
        list of langchain document objects

    TXT -> TextLoader -> Langchain document objects
    """
    docs = []

    for file in data_path.glob("*.txt"):
        print(f"Loading..: {file.name}")

        loader = TextLoader(str(file))  ## TextLoader reads the TXT file and extracts text.

        docs.extend(loader.load())
    return docs