from typing import Optional
from io import BytesIO
from pypdf import PdfReader
# IMPORT LOGGER KITA
from app.monitoring.logger import logger 

def extract_text_from_pdf(file_content: bytes) -> Optional[str]:
    try:
        pdf_reader = PdfReader(BytesIO(file_content))
        text = ""
        
        if pdf_reader.is_encrypted:
            # GANTI print JADI logger.error
            logger.error("PDF is encrypted/password protected.")
            return None

        count = 0
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
                count += 1
        
        if not text.strip():
            # GANTI print JADI logger.warning
            logger.warning("PDF opened successfully but NO TEXT found. Likely a scanned image.")
            return None
            
        # GANTI print JADI logger.info
        logger.info(f"✅ Successfully extracted text from {count} pages.")
        return text.strip()
    
    except Exception as e:
        # GANTI print JADI logger.critical (Error Parah)
        logger.critical(f"🔥 CRITICAL ERROR in extraction: {e}")
        return None

def extract_text_from_file(file_content: bytes, filename: str) -> Optional[str]:
    logger.info(f"📂 Processing file: {filename}") # Log nama file
    
    if filename.lower().endswith(".pdf"):
        return extract_text_from_pdf(file_content)
    elif filename.lower().endswith(".txt"):
        return file_content.decode("utf-8")
    else:
        logger.error(f"❌ Unsupported format: {filename}")
        return None