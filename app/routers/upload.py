from fastapi import APIRouter, UploadFile, File, HTTPException
from app.ingestion.extractor import extract_text_from_file
from app.ingestion.embedder import index_document
from app.core.database import get_qdrant_client
from app.core.config import settings

router = APIRouter()

@router.post("/ingest", summary="Upload document for ingestion")
async def ingest_document(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(('.pdf', '.txt')):
        raise HTTPException(status_code=400, detail="Only PDF and TXT files are supported")
    
    try:
        content = await file.read()
        extracted_text = extract_text_from_file(content, file.filename)
        
        if not extracted_text:
            raise HTTPException(status_code=400, detail="Failed to extract text")
            
        # --- PROSES BARU: Indexing ke Qdrant ---
        num_chunks = await index_document(extracted_text, file.filename)
        
        return {
            "filename": file.filename,
            "status": "success",
            "message": f"Successfully indexed {num_chunks} chunks to Vector DB",
        }

    except Exception as e:
        print(f"Error: {e}") # Debugging
        raise HTTPException(status_code=500, detail=str(e))
    
@router.delete("/reset", summary="Reset/Clear Vector Database")
async def reset_database():
    """
    Menghapus seluruh collection di Qdrant (Menghapus ingatan bot).
    """
    try:
        client = get_qdrant_client()
        # Hapus collection
        client.delete_collection(collection_name=settings.QDRANT_COLLECTION_NAME)
        
        return {"status": "success", "message": "Database has been reset. Knowledge base is empty."}
    except Exception as e:
        # Jika collection memang belum ada, tidak apa-apa
        return {"status": "warning", "message": f"Database reset failed or already empty: {str(e)}"}