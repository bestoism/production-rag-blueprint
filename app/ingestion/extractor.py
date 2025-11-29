from typing import Optional
from io import BytesIO
from pypdf import PdfReader

def extract_text_from_pdf(file_content: bytes) -> Optional[str]:
    """
    Extracts text from a PDF file (in bytes).
    """
    try:
        # Create a PDF reader object from bytes
        pdf_reader = PdfReader(BytesIO(file_content))
        text = ""
        
        # Iterate over each page and extract text
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
                
        return text.strip()
    
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return None

def extract_text_from_file(file_content: bytes, filename: str) -> Optional[str]:
    """
    Router function to choose extractor based on file extension.
    """
    if filename.lower().endswith(".pdf"):
        return extract_text_from_pdf(file_content)
    # Nanti bisa tambah support .docx atau .txt di sini
    elif filename.lower().endswith(".txt"):
        return file_content.decode("utf-8")
    else:
        raise ValueError(f"Unsupported file format: {filename}")