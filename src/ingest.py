## Responsible for 1. Taking the documents. 2. Chunking 3. Embedding 4. FAISS vectorDB

import pickle

from pathlib import Path
import faiss

from readers.pdffiles import load_pdf_docs
from readers.mdfiles import load_md_docs
from readers.txtfiles import load_txt_docs
from readers.docxfiles import load_docx_docs

from langchain_text_splitters import RecursiveCharacterTextSplitter  ## Used for chunking
from sentence_transformers import SentenceTransformer  ## for converting chunks to embeddings

EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"  ## this is a huggingface model

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR/ "data"
STORE_DIR = BASE_DIR/ "store"
## location where vectors will be stored in FAISS db inside STORE
INDEX_PATH = STORE_DIR/ "faiss_index"
CHUNKS_PATH = STORE_DIR / "chunks"

### STEP 1: SPLIT DOCS into Chunks

def split_docs(docs):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size = 750, ##approx size of each chunk is 750 characters. This is a good size for embeddings and also for LLMs to process.
        chunk_overlap = 50
    )
    return splitter.split_documents(docs)

### STEP 2: Create embeddings

def create_embeddings(chunks):
    model = SentenceTransformer(EMBEDDING_MODEL_NAME)
    texts = [chunk.page_content for chunk in chunks]  ## extracting only the actual text content. becase a document contains other thinsg as well such as page_content, metadata, etc.
    embeddings = model.encode(
        texts,
        show_progress_bar= True,
        convert_to_numpy= True, ## return embeddings to Numpy arrays
        normalize_embeddings= True  ## this is imp: we normalize all the embeddings because we want all the chunks to be converted into similar looking embeddings
    )
    return embeddings

## STEP 3: STORE EMBEDDINGS in FAISS vectorDB

def store_faiss(embeddings, chunks):
    ## CREATE the STORE_DIR if it does not already exists. 
    STORE_DIR.mkdir(exist_ok= True)

    ## Determine the dims of our vectors, because they will the same size required for user_query embedding
    dim = embeddings.shape[1]

    ## Create FAISS index using IndexFlatIP - which will be later used for performing Similarity Search
    index = faiss.IndexFlatIP(dim)

    ## add all the document vectors to FAISS
    index.add(embeddings)

    ## save the faiss index to disk location
    faiss.write_index(index, str(INDEX_PATH))

    ## -------------------------------------------------
    ## Store the actual text chunks
    with open(CHUNKS_PATH, "wb") as f:
        pickle.dump(chunks, f)


## STEP 4: MAIN INGESTION PIPELINE

if __name__ == "__main__":

    docs = []

    ## 1.1 load the md doc
    docs.extend(load_md_docs(DATA_DIR))
    print(f"Loaded {len(docs)} md document pages.")

    ## 1.2 load the pdf doc
    docs.extend(load_pdf_docs(DATA_DIR))
    print(f"Loaded {len(docs)} pdf document pages.")

    ## 1.3 load the txt doc 
    docs.extend(load_txt_docs(DATA_DIR))
    print(f"Loaded {len(docs)} txt document pages.")

    ## 1.4 load the docx doc
    docs.extend(load_docx_docs(DATA_DIR))
    print(f"Loaded {len(docs)} docx document pages.")
          
    ## 2. Split docs into Chunks
    chunks = split_docs(docs)
    print(f"Split into {len(chunks)} chunks.")

    ## 3. Embeddings
    embeddings = create_embeddings(chunks)
    print(f"Created embeddings for {len(chunks)} chunks. Embedding shape: {embeddings.shape}")

    ## 4. Store vectors and chunk
    store_faiss(embeddings, chunks)

    print(
        f"Processed {len(docs)} document pages "
        f"into {len(chunks)} chunks "
        f"and stored into FAISS vector DB."
    )