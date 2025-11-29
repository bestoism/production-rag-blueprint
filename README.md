# 🚀 RAG Insight Pipeline

> A production-ready RAG pipeline featuring automated document ingestion, observability with Langfuse, RAGAS evaluation, and Dockerized CI/CD.

## 🏗 Architecture
This project moves beyond simple RAG demos by integrating:
- **Ingestion Pipeline**: Automated PDF/DOCX processing (Extraction -> Chunking -> Embedding -> Vector DB).
- **Vector Database**: Qdrant / Pinecone integration.
- **Observability**: Real-time tracing of queries, latency, and token usage via **Langfuse**.
- **Evaluation**: Automated metrics (faithfulness, answer relevance) using **RAGAS**.
- **Deployment**: Dockerized application with CI/CD workflows.

## 🛠 Tech Stack
- **Core**: Python, FastAPI, LangChain/LlamaIndex
- **Vector DB**: Qdrant
- **LLM**: OpenAI / Gemini / Groq
- **Monitoring**: Langfuse
- **DevOps**: Docker, GitHub Actions