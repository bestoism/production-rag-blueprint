# Contributing to Production RAG Blueprint

Thank you for your interest in contributing to **Production RAG Blueprint**! 🚀
This document provides guidelines for setting up the development environment and submitting contributions.

## 🛠 Development Setup

To ensure consistency, please follow these steps to set up your local environment.

### 1. Prerequisites
- Python 3.11+
- Docker & Docker Compose
- Git

### 2. Installation
```bash
# Clone the repository
git clone https://github.com/bestoism/production-rag-blueprint.git
cd production-rag-blueprint

# Create Virtual Environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install Dependencies
pip install -r requirements.txt
```

### 3. Environment Variables
Copy the example environment file and fill in the required keys.
```bash
cp .env.example .env
```
*Note: For local development, you can leave `QDRANT_URL` empty to use the local Qdrant instance.*

---

## 🧪 Running Tests

We use **Pytest** for unit testing and **GitHub Actions** for CI/CD. Before submitting a Pull Request (PR), please ensure all tests pass locally.

```bash
# Run all tests
pytest tests/

# Run tests with verbose output
pytest -v tests/
```

---

## 🐳 Docker Orchestration

If you are working on the database or API integration, we recommend using Docker Compose to spin up the full stack locally.

```bash
cd docker
docker-compose up --build
```
This will start:
- **FastAPI Backend** at `http://localhost:8000`
- **Qdrant DB** at `http://localhost:6333`

---

## 📝 Commit Guidelines

We follow the **Conventional Commits** specification. Please structure your commit messages as follows:

- `feat: description` (New features)
- `fix: description` (Bug fixes)
- `docs: description` (Documentation updates)
- `refactor: description` (Code restructuring without behavior changes)
- `chore: description` (Maintenance, dependencies, etc.)

**Example:**
```text
feat: add hybrid search capability to retriever
fix: resolve pypdf extraction error on encrypted files
```

---

## 📮 Pull Request Process

1.  Fork the repository.
2.  Create a new branch (`git checkout -b feature/amazing-feature`).
3.  Commit your changes.
4.  Push to the branch.
5.  Open a Pull Request targeting the `main` branch.

Happy Coding! 💻
