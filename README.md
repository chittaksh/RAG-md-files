App ingestion.py - MD, chunk, embedd, vectorDB(faiss) retriever.py - question, embedded, llm, retrieve the relavant chunks from the vectorDB rag_chain.py - retrived chunks , llm , answer agents.py - orchestration layer

Data

all the input MD's
Store

all the generated chunks and vector Embeddings are stored
main.py

CLI interfaces
Working:

* PDF/MD/txt/docx documents
* Document loader
* Langchain documents
* Chunking -> Text chunks
* Embedding model -> Vectors -> FAISS vectorDB
* User query -> Query embedding -> similarity search on VectorDB
* Retrieve top-K chunks
* LLM (Groq)
* Answer


## How to run:
* uv pip install -r requirements.txt

* uv run python src/ingest.py

* uv run python src/main.py # runs a console application

* uv run streamlit run src/app.py # run a streamlit web application


## Sample .env file

GROQ_API_KEY="Your_Key_Here"