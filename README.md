# 🚀 RAG Insight Pipeline

> A production-ready RAG pipeline featuring automated document ingestion, observability with Langfuse, RAGAS evaluation, and Dockerized CI/CD.

## 🏗 Architecture
This project moves beyond simple RAG demos by integrating:
- **Ingestion Pipeline**: Automated PDF/DOCX processing (Extraction -> Chunking -> Embedding -> Vector DB).
- **Vector Database**: Qdrant Cloud.
- **Observability**: Real-time tracing of queries, latency, and token usage via **Langfuse**.
- **Evaluation**: Automated metrics (faithfulness, answer relevance) using **RAGAS**.
- **Deployment**: Dockerized application on Hugging Face Spaces.

## 🛠 Tech Stack
- **Core**: Python, FastAPI, LangChain
- **Vector DB**: Qdrant
- **LLM**: Gemini Pro
- **Monitoring**: Langfuse
- **DevOps**: Docker, GitHub Actions