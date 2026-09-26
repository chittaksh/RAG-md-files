# AI Tutor: Multi-Format Retrieval-Augmented Generation (RAG) System

A specialized, context-aware Retrieval-Augmented Generation (RAG) system engineered to serve as an intelligent **AI Tutor**. The system parses, indexes, and queries heterogeneous learning materials across multiple formats (`.pdf`, `.docx`, `.txt`, `.md`, `.epub`) to deliver accurate, source-attributed academic explanations, concept summaries, and study guides.

## 1. Project Overview

This project implements an AI Tutor powered by a multi-document RAG pipeline designed to eliminate hallucinations and provide students with grounded, accurate academic support. By indexing course syllabi, textbooks, lecture notes, lab manuals, and supplementary e-books into a vector space, the AI Tutor retrieves exact context passages to answer student questions and generate study aids with precise citations.

**Key Features:**

* **Multi-Format Course Material Support:** Ingests textbooks (`.epub`), lecture slides/notes (`.pdf`), assignment sheets (`.docx`), developer tutorials (`.md`), and raw transcripts (`.txt`) simultaneously.

* **Academic Domain Awareness:** Chunking and retrieval pipelines optimized for preserving educational hierarchy (chapters, sub-sections, problem sets).

* **Source-Backed Tutoring:** Generates answers with direct citations back to course materials, helping students verify facts and locate relevant readings.

* **Interactive Learning Interface:** Simple UI/CLI for students to ask questions, request concept summaries, or generate practice questions based strictly on uploaded course files.

## 2. Domain Chosen

**Primary Domain:** **AI Tutor / Intelligent Educational Assistant**

### Why This Domain?

* **Fragmented Course Ecosystems:** Students regularly navigate disparate learning materials—digital textbooks (`.epub`), syllabus PDFs (`.pdf`), assignment guidelines (`.docx`), coding guides (`.md`), and revision notes (`.txt`).

* **High Need for Accuracy:** Educational tools cannot afford hallucinated explanations. Answers must strictly reflect assigned textbooks, course standards, and official curricula.

* **Personalized & On-Demand Guidance:** An AI Tutor provides 24/7 interactive assistance, breaking down complex academic concepts and pointing students directly to relevant textbook chapters or lecture notes.

* **Traceability for Study Efficiency:** Citing specific page numbers, e-book chapters, and lecture sections allows students to quickly cross-reference source material.

## 3. Description of Dataset (Educational Materials Used)

The knowledge base comprises sample course materials spanning all supported document formats:

| File Name | Extension | Educational Content | Focus / Academic Subject |
| :--- | :--- | :--- | :--- |
| `Linear_Algebra_Lecture_04.pdf` | `.pdf` | Lecture Slides & Formulas | Matrix Transformations & Vector Spaces |
| `Syllabus_and_Grading_Policy.docx` | `.docx` | Course Logistics & Policies | Assignment rubrics, exam schedules, policy rules |
| `Lecture_Transcript_Unit3.txt` | `.txt` | Audio Transcript | Class discussion on optimization algorithms |
| `Python_DataStructures_Guide.md` | `.md` | Lab Instructions & Code Examples | Arrays, Linked Lists, and Tree Data Structures |
| `Intro_to_Machine_Learning_Vol1.epub` | `.epub` | Digital Textbook | Foundational ML concepts, gradient descent, neural networks |

### Dataset Characteristics & Processing Challenges:

* **Format-Specific Extraction:** Employs targeted document loaders (`PyPDFLoader`, `Docx2txtLoader`, `TextLoader`, `UnstructuredMarkdownLoader`, `UnstructuredEPubLoader`) to process course material regardless of file type.

* **Math & Technical Syntax:** Handles embedded mathematical formulas, code blocks, structured markdown headers, and multi-chapter e-book layouts.

* **Cross-Material Synthesis:** Solves complex queries by synthesizing facts across different course assets (e.g., linking a lecture slide PDF concept to an assignment guide DOCX).

## 4. Architecture Explanation

The AI Tutor architecture employs a two-stage pipeline: **Educational Knowledge Ingestion** and **Interactive Tutoring / Retrieval**.

```
                   [ KNOWLEDGE BASE INGESTION PIPELINE ]
  +-------------------------------------------------------------------+
  | Course Directory (PDF / DOCX / TXT / MD / EPUB Materials)         |
  +-------------------------------------------------------------------+
                                    |
                                    v
  +-------------------------------------------------------------------+
  | Multi-Format Document Loaders                                     |
  | (PyPDF / Docx2txt / Text / Markdown / EPub Loaders)              |
  +-------------------------------------------------------------------+
                                    |
                                    v
  +-------------------------------------------------------------------+
  | Recursive Text Splitter (Preserves Paragraphs & Sections)         |
  +-------------------------------------------------------------------+
                                    |
                                    v
  +-------------------------------------------------------------------+
  | Embedding Model -> Vector Database (Chroma / FAISS)               |
  +-------------------------------------------------------------------+

                    [ TUTOR CHAT & RETRIEVAL PIPELINE ]
  +-------------------+     +-------------------+     +-------------------+
  | Student Query /   | --> | Vector DB Search  | --> | Relevant Passage  |
  | Prompt Input      |     | (Cosine / L2)     |     | Chunks + Context  |
  +-------------------+     +-------------------+     +-------------------+
                                                                |
                                                                v
  +-------------------+                               +-------------------+
  | Cited Academic    | <---------------------------- | LLM Tutoring Engine|
  | Explanation       |                               | (System Prompted) |
  +-------------------+                               +-------------------+
```

### Pipeline Breakdown:

1. **Course Material Parsing:** Automatically detects file types (`.pdf`, `.docx`, `.txt`, `.md`, `.epub`) and applies format-specific parsers.

2. **Pedagogical Chunking:** Breaks long textbooks and lecture files into semantically meaningful chunks (e.g., `chunk_size=1000`, `chunk_overlap=200`) while preserving logical section boundaries.

3. **Academic Context Metadata:** Attaches course metadata (course unit, file extension, source title, chapter/page number) to each chunk.

4. **Vector Indexing:** Converts text chunks into dense embeddings stored in a local vector index (e.g., ChromaDB or FAISS).

5. **Contextual Retrieval:** Performs top-$k$ similarity search on student queries to find relevant course passages.

6. **Tutor Answer Generation:** Prompts the LLM with retrieved course passages to generate clear, pedagogical responses complete with textbook/lecture citations.

## 5. Setup Instructions

### Prerequisites

* Python 3.9 or higher
* Git

### 1. Clone the Repository

```bash
git clone https://github.com/chittaksh/RAG-multi-files.git
cd RAG-multi-files
```

### 2. Create and Activate Virtual Environment

```bash
# macOS/Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the root directory and set your API credentials:

```env
OPENAI_API_KEY=your_openai_api_key_here
# Optional: HuggingFace Token for local open-source embedding models
HUGGINGFACE_HUB_TOKEN=your_huggingface_token_here
```

## 6. How to Run Ingestion

Place your course documents (`.pdf`, `.docx`, `.txt`, `.md`, `.epub`) inside the `./data/` folder.

Run the ingestion script to process course files and build the vector database:

```bash
python ingest.py
```

**Expected Output:**

```text
[INFO] Scanning course directory: ./data/
[INFO] Detected files: 1 PDF, 1 DOCX, 1 TXT, 1 MD, 1 EPUB.
[INFO] Loading course files using specialized parsers...
[INFO] Splitting text into pedagogical chunks (chunk_size=1000, overlap=200)...
[INFO] Generated 385 chunks across 5 learning assets.
[INFO] Generating vector embeddings and updating index...
[SUCCESS] Course knowledge base successfully indexed at ./vectorstore/
```

## 7. How to Run Chatbot

Once the ingestion pipeline has indexed your course materials, launch the AI Tutor:

### Command Line Interface (CLI) Mode:

```bash
python main.py
```

### Web Interface Mode (Streamlit / Gradio):

```bash
streamlit run app.py
```

*Open `http://localhost:8501` in your browser to interact with the AI Tutor.*

## 8. Sample Queries & Outputs

### Example 1: Concept Explanation from EPUB Textbook (`.epub`)

* **Student Query:** *"Can you explain gradient descent using the course textbook?"*

* **AI Tutor Response:**

  > **Gradient Descent** is an iterative optimization algorithm used to minimize a loss function by moving in the direction of steepest descent, defined by the negative of the gradient. 
  > 
  > In the context of machine learning, the parameters (weights) are updated using the formula:
  > $$\theta = \theta - \alpha \nabla_{\theta} J(\theta)$$
  > where $\alpha$ is the learning rate and $\nabla_{\theta} J(\theta)$ is the gradient of the loss function $J(\theta)$.
  >
  > **Recommended Study Citation:**
  > * `Intro_to_Machine_Learning_Vol1.epub` — *Chapter 3: Optimization Fundamentals, Section 3.2*

### Example 2: Synthesizing Syllabus Rules (`.docx`) and Lecture Transcripts (`.txt`)

* **Student Query:** *"What is the policy for late assignment submission and when is the mid-term?"*

* **AI Tutor Response:**

  > According to the course syllabus, late submissions incur a **10% penalty per day** up to a maximum of 3 days, after which submissions receive a zero (`Syllabus_and_Grading_Policy.docx`). 
  >
  > As mentioned in Unit 3's lecture discussion, the mid-term exam is scheduled for **Week 7** during regular class hours (`Lecture_Transcript_Unit3.txt`).
  >
  > **Recommended Study Citations:**
  > * `Syllabus_and_Grading_Policy.docx` — *Section: Grading & Late Policies*
  > * `Lecture_Transcript_Unit3.txt` — *Timestamp 00:14:20*

## 9. Limitations & Assumptions

### Assumptions

1. **Digital Document Quality:** PDFs, Word documents, and EPUB files must contain selectable text rather than flattened image scans (scanned files require OCR integration).
2. **Text Encoding:** `.txt` transcripts and `.md` code guides are assumed to be UTF-8 encoded.
3. **Domain Alignment:** Queries are assumed to pertain to the uploaded course materials. Out-of-scope questions will prompt the AI Tutor to inform the student that relevant context was not found in the uploaded documents.

### Limitations

1. **Complex Mathematical Notation & Diagrams:** Mathematical equations inside `.pdf` files or diagrams in `.epub` books may lose structural formatting during raw text extraction.
2. **Context Window Limits:** If a student asks a broad question requiring context from dozens of chapters across multiple textbooks, retrieval top-$k$ filters may omit secondary details.
3. **Static Course Snapshot:** The AI Tutor only knows about materials currently present in the vector store. Re-running `python ingest.py` is required whenever new lectures, readings, or assignments are added.


## How to run:
* uv pip install -r requirements.txt

* uv run python src/ingest.py

* uv run python src/main.py # runs a console application

* uv run streamlit run src/app.py # run a streamlit web application