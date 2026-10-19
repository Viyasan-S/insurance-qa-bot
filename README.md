# Secure Insurance Policy Q&A Bot

A Retrieval-Augmented Generation (RAG) application that answers questions about a fictional life insurance policy using Python, ChromaDB, Sentence Transformers, Ollama, FastAPI, and Docker.

The application retrieves relevant passages from a policy PDF and uses a local Large Language Model (LLM) to generate answers grounded in the retrieved evidence.

> **Disclaimer:** This project uses a fictional insurance policy for educational and demonstration purposes. It does not provide real insurance or financial advice.

## Overview

Insurance documents often contain detailed coverage conditions, exclusions, waiting periods, and claims procedures. Finding the correct information manually can be time-consuming.

This project demonstrates how RAG can help users retrieve relevant policy information and receive concise answers with source references.

### Example question

**Question:** What is the accidental death benefit?

**Example answer:** The fictional policy provides an additional ¥5,000,000 accidental death benefit for qualifying accidental deaths, subject to policy conditions, exclusions, and claim approval.

**Source:** `mock_life_insurance_policy.pdf`, page 2.

*Example answer based on the mock policy.*

## Architecture

```text
                 Insurance Policy PDF
                          |
                          v
                 PDF Text Extraction
                      PyMuPDF
                          |
                          v
                    Text Chunking
                          |
                          v
                 Sentence Embeddings
                 Sentence Transformers
                          |
                          v
                  ChromaDB Vector Store
                          |
                          v
User Question ---> Semantic Retrieval
                          |
                          v
                Retrieved Policy Evidence
                          |
                          v
                    Ollama LLM
                          |
                          v
                  Generated Answer
                   + Source Pages
                          |
                          v
                    FastAPI API
                          |
                          v
                    Docker Container
```

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application development |
| PyMuPDF | Extract text from PDF documents |
| Sentence Transformers | Generate text embeddings |
| ChromaDB | Store and retrieve vector embeddings |
| Ollama | Run the language model locally |
| FastAPI | Expose the question-answering API |
| Pydantic | Validate API requests and responses |
| Pytest | Automated testing |
| Docker | Containerize the application |
| Docker Compose | Configure and run the container |

## Features

- PDF text extraction with page-number metadata.
- Text chunking for retrieval.
- Semantic search using vector embeddings.
- Local LLM integration using Ollama.
- RAG-based answers grounded in retrieved policy passages.
- Source references in API responses.
- FastAPI endpoints for health checks and policy questions.
- API-key authentication for the question-answering endpoint.
- Input validation and basic request-length limits.
- Automated API and authentication tests.
- Docker-based application deployment.

## Project Structure

```text
insurance-qa-bot/
├── data/
│   ├── raw/
│   │   └── mock_life_insurance_policy.pdf
│   └── processed/
├── src/
│   ├── ingestion/
│   │   ├── pdf_loader.py
│   │   ├── chunker.py
│   │   └── embed_store.py
│   ├── retrieval/
│   │   └── retriever.py
│   ├── generation/
│   │   └── llm.py
│   ├── api/
│   │   ├── routes.py
│   │   └── schemas.py
│   ├── security/
│   │   └── auth.py
│   └── main.py
├── scripts/
│   └── create_mock_policy.py
├── tests/
│   └── test_api.py
├── chroma_db/
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .env.example
├── .gitignore
└── README.md
```

*The structure above represents the intended organization. Some generated files and local data directories may be excluded from Git.*

## Prerequisites

Install the following:

- Python 3.11 or compatible Python version.
- Git.
- Docker Desktop.
- Ollama.
- The `llama3.2:3b` model, or another compatible model configured in the application.

Internet access is required initially to download Python dependencies, the embedding model, and the LLM.

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/Viyasan-S/insurance-qa-bot.git
cd insurance-qa-bot
```

### 2. Create a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install Python dependencies

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 4. Start Ollama

Install Ollama from [ollama.com](https://ollama.com/).

Download the model:

```powershell
ollama pull llama3.2:3b
```

Verify the model:

```powershell
ollama list
```

Ensure Ollama is running and accessible at `http://127.0.0.1:11434` when running the Python application locally.

### 5. Configure environment variables

Copy `.env.example` to `.env` and configure a private API key.

Example `.env`:

```dotenv
API_KEY=replace-with-a-generated-secret
```

Generate a secret with:

```powershell
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Never commit `.env` or share its contents.

### 6. Generate the mock policy PDF

```powershell
python scripts/create_mock_policy.py
```

The PDF should be generated under `data/raw/`.

### 7. Ingest the policy into ChromaDB

```powershell
python -m src.ingestion.embed_store
```

This extracts policy text, creates chunks, generates embeddings, and stores the results in the local ChromaDB database.

### 8. Start the API locally

```powershell
python -m uvicorn src.main:app --reload
```

The API will be available at:

- Health endpoint: http://127.0.0.1:8000/health
- Interactive API documentation: http://127.0.0.1:8000/docs

## API Usage

### Health check

```http
GET /health
```

### Ask a policy question

```http
POST /ask
Content-Type: application/json
X-API-Key: YOUR_API_KEY
```

Request:

```json
{
  "question": "What is the accidental death benefit?"
}
```

Example response:

```json
{
  "question": "What is the accidental death benefit?",
  "answer": "The accidental death benefit is 5,000,000 yen, subject to policy conditions, exclusions, and claim approval.",
  "sources": [
    {
      "source": "mock_life_insurance_policy.pdf",
      "page": 2
    }
  ],
  "notice": "Illustrative answer based on a fictional insurance policy. Actual benefits depend on the applicable contract."
}
```

The precise answer and retrieved source pages depend on the indexed document and model output.

## Running with Docker

Ensure Docker Desktop is running, the policy has been ingested, and Ollama is running on the host.

Build and start the application:

```powershell
docker compose up --build
```

Open the API documentation at http://localhost:8000/docs.

The Docker configuration should connect to the host's Ollama service through `host.docker.internal` and mount the ChromaDB directory so the container can access the indexed policy.

Stop the application:

```powershell
docker compose down
```

**Note:** This setup runs the API in Docker while Ollama runs separately on the host machine. The LLM is not packaged inside the API image.

## Testing

Run the automated API tests:

```powershell
python -m pytest tests/test_api.py -v
```

The initial API test suite contains four checks:

- Health endpoint response.
- Rejection of requests without an API key.
- Rejection of invalid API keys.
- Rejection of questions that are too short.

The initial suite passed all four tests in the development environment. Further integration and RAG evaluation tests are planned.

## Security Considerations

This project demonstrates basic application security practices:

- API-key authentication for the question-answering endpoint.
- Request validation and maximum question length.
- Environment-based secret configuration.
- Exclusion of secrets and generated local files from Git.
- Local LLM inference through Ollama.
- Source references for retrieved policy evidence.

These controls are not a complete production security solution. Production deployments would require stronger identity and access management, rate limiting, audit logging, retrieval relevance thresholds, prompt-injection defenses, data protection controls, monitoring, and security testing.

## Limitations and Future Improvements

- Add retrieval relevance thresholds and reliable abstention for unsupported questions.
- Evaluate retrieval quality and answer faithfulness using a curated question set.
- Add tests for prompt injection and malicious document content.
- Add end-to-end tests covering PDF ingestion, retrieval, and answer generation.
- Improve citation accuracy and ensure citations support the generated claims.
- Add structured logging, request tracing, and latency measurement.
- Introduce production-grade authentication, rate limiting, and monitoring.
- Explore hybrid retrieval and reranking.
- Support multiple insurance policies with document-level access controls.

## Learning Outcomes

This project provides practical experience with:

- Retrieval-Augmented Generation (RAG).
- Text embeddings and vector search.
- Local LLM integration.
- PDF ingestion and document processing.
- Python API development.
- API authentication and input validation.
- Automated testing.
- Docker containerization.

## Author

**Viyasan Sivaraj**

GitHub: [@Viyasan-S](https://github.com/Viyasan-S)

Portfolio: [viyasans.lovable.app](https://viyasans.lovable.app/)

---

*Built as an educational AI engineering project to explore secure, document-grounded question answering for insurance use cases.*
