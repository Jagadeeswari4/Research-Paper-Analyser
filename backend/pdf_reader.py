from pypdf import PdfReader
import re
from builtins import Exception,print


def extract_text(pdf_path):
    """Extract text from PDF file"""
    text = ""
    try:
        reader = PdfReader(pdf_path)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        
        # Clean the extracted text
        text = clean_extracted_text(text)
        return text
    except Exception as e:
        print(f"Error extracting text: {e}")
        return ""

def clean_extracted_text(text):
    """Clean the extracted text while preserving line breaks for parsing."""
    if not text:
        return ""

    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r'(\w+)-\s*\n\s*(\w+)', r'\1\2', text)
    text = re.sub(r'[ \t]+', ' ', text)
    text = re.sub(r'(?m)^\s*\d+\s*$', '', text)
    text = re.sub(r'(?m)^\s*[-•*]+\s*$', '', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()