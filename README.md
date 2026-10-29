# PolicyGuard AI — Intelligent Policy Document Assistant

PolicyGuard AI is an AI-powered document assistant that helps users upload policy documents, search for relevant information, and ask questions in natural language. It combines semantic search with a locally running language model to generate answers grounded in retrieved policy text.

## Features

- **Document Upload:** Supports PDF, DOCX, and TXT policy documents.
- **Text Extraction:** Extracts readable text from supported document formats.
- **Semantic Search:** Finds relevant policy passages using Sentence Transformers and ChromaDB.
- **AI-Powered Q&A:** Answers policy questions using a locally running Ollama model.
- **Source Context:** Returns relevant policy passages alongside generated answers.
- **REST API:** Provides endpoints through FastAPI.
- **Input Validation:** Validates supported file formats, upload size, and question input.
- **Automated Testing:** Includes pytest tests for core API behavior.

## Tech Stack

- **Language:** Python
- **Backend:** FastAPI
- **AI / NLP:** Sentence Transformers, Ollama (`llama3.2:3b`)
- **Vector Database:** ChromaDB
- **Document Processing:** PyMuPDF, python-docx
- **Testing:** pytest, FastAPI TestClient

## How It Works

1. Upload a policy document.
2. Extract readable text from the document.
3. Split the text into overlapping chunks.
4. Generate embeddings and store them in ChromaDB.
5. Ask a question in natural language.
6. Retrieve relevant policy passages using semantic similarity.
7. Send the retrieved context to the local language model.
8. Return an answer with supporting source passages.

## Project Structure

```text
PolicyGuardAI/
├── app/
│   ├── routes/
│   │   ├── health.py
│   │   ├── policies.py
│   │   └── document_analysis.py
│   ├── services/
│   │   ├── document_processor.py
│   │   ├── nlp_processor.py
│   │   ├── retrieval.py
│   │   ├── llm_service.py
│   │   └── policy_qa.py
│   └── schemas/
├── data/
├── tests/
│   ├── test_health.py
│   └── test_policy_api.py
├── main.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Getting Started

### Prerequisites

- Python 3.13
- Git
- Ollama installed
- The `llama3.2:3b` model downloaded through Ollama

### 1. Clone the Repository

```bash
git clone https://github.com/poojaparab210/PolicyGuardAI.git
cd PolicyGuardAI
```

### 2. Create and Activate a Virtual Environment

On Windows PowerShell:

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```powershell
python -m pip install -r requirements.txt
```

### 4. Set Up Ollama

Download the model:

```powershell
ollama pull llama3.2:3b
```

Make sure Ollama is running before asking policy questions.

### 5. Start the API

```powershell
python -m uvicorn main:app --reload
```

### 6. Open the API Documentation

Visit **http://127.0.0.1:8000/docs** to upload policy documents and ask questions through the interactive Swagger interface.

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | API welcome/status |
| GET | `/health` | Health check |
| POST | `/policies/upload` | Upload and index a policy |
| GET | `/policies/{policy_id}/text` | Retrieve extracted policy text |
| POST | `/policies/{policy_id}/ask` | Ask a question about a policy |

## Running Tests

From the project root, run:

```powershell
python -m pytest -v
```

The current test suite contains four passing tests covering the root endpoint, health endpoint, missing policy handling, and empty-question validation.

## Limitations

- Answer quality depends on document extraction, retrieval relevance, and the language model.
- Scanned PDFs may require OCR, which is not currently included.
- AI-generated answers may be incomplete or incorrect and should be verified against the original policy.
- The project is a prototype and does not replace HR, legal, or compliance review.
- Ollama and the configured model must be available for AI-generated answers.

## Future Improvements

- Develop a Streamlit interface for easier document upload and question answering.
- Improve source citations and answer-grounding evaluation.
- Add automated tests for uploads, retrieval, and AI-generated answers.
- Add OCR support for scanned PDFs.
- Improve document management, security, and error handling.

## Disclaimer

PolicyGuard AI is an educational portfolio project. Always verify important policy interpretations against the original document and consult the appropriate policy owner when necessary.
