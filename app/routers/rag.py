from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.rag.pipeline import query_rag

router = APIRouter()

# Schema Request (Format JSON yang dikirim user)
class QueryRequest(BaseModel):
    question: str

@router.post("/query", summary="Ask a question to your documents")
async def ask_rag(request: QueryRequest):
    try:
        result = await query_rag(request.question)
        return {
            "status": "success",
            "question": request.question,
            "answer": result["answer"],
            "sources": result["sources"]
        }
    except Exception as e:
        # Print error di terminal untuk debugging
        print(f"Error during RAG query: {e}")
        raise HTTPException(status_code=500, detail=str(e))