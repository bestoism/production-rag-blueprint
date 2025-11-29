from fastapi import APIRouter, UploadFile, File, HTTPException
from app.ingestion.extractor import extract_text_from_file

router = APIRouter()

@router.post("/ingest", summary="Upload document for ingestion")
async def ingest_document(file: UploadFile = File(...)):
    """
    Upload a PDF, extract text, and (in future) chunk & embed it.
    """
    # 1. Validasi tipe file
    if not file.filename.lower().endswith(('.pdf', '.txt')):
        raise HTTPException(status_code=400, detail="Only PDF and TXT files are supported")
    
    try:
        # 2. Baca file content
        content = await file.read()
        
        # 3. Extract Text
        extracted_text = extract_text_from_file(content, file.filename)
        
        if not extracted_text:
            raise HTTPException(status_code=400, detail="Failed to extract text from document")
            
        # --- TODO: Next steps (Chunking -> Embedding -> Vector DB) ---
        
        return {
            "filename": file.filename,
            "status": "success",
            "message": "Text extracted successfully",
            "text_preview": extracted_text[:200] + "..." # Tampilkan 200 karakter awal
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))