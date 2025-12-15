"""PDF Processing Module"""
import os
from typing import Dict, List
import PyPDF2
import pdfplumber


class PDFProcessor:
    """Extracts and processes content from PDF files"""
    
    def __init__(self):
        self.content = {}
    
    def extract_text(self, pdf_path: str) -> Dict[str, any]:
        """
        Extract text content from PDF file
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Dictionary containing extracted text and metadata
        """
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
        result = {
            'text': '',
            'pages': [],
            'metadata': {},
            'tables': []
        }
        
        # Extract text using pdfplumber for better accuracy
        with pdfplumber.open(pdf_path) as pdf:
            result['metadata'] = {
                'num_pages': len(pdf.pages),
                'file_name': os.path.basename(pdf_path)
            }
            
            for page_num, page in enumerate(pdf.pages, 1):
                page_text = page.extract_text()
                if page_text:
                    result['pages'].append({
                        'page_number': page_num,
                        'text': page_text
                    })
                    result['text'] += page_text + '\n\n'
                
                # Extract tables if present
                tables = page.extract_tables()
                if tables:
                    for table in tables:
                        result['tables'].append({
                            'page': page_num,
                            'data': table
                        })
        
        return result
    
    def extract_headings(self, text: str) -> List[str]:
        """
        Extract potential headings from text
        Simple heuristic: lines that are short and end without punctuation
        
        Args:
            text: Text content to analyze
            
        Returns:
            List of potential headings
        """
        lines = text.split('\n')
        headings = []
        
        for line in lines:
            line = line.strip()
            # Heuristic: lines less than 100 chars, no period at end, not empty
            if line and len(line) < 100 and not line.endswith('.'):
                # Check if it looks like a heading (has some capitals)
                if any(c.isupper() for c in line):
                    headings.append(line)
        
        return headings
    
    def chunk_content(self, text: str, chunk_size: int = 2000) -> List[str]:
        """
        Split content into manageable chunks for processing
        
        Args:
            text: Text to chunk
            chunk_size: Maximum size of each chunk
            
        Returns:
            List of text chunks
        """
        words = text.split()
        chunks = []
        current_chunk = []
        current_size = 0
        
        for word in words:
            word_size = len(word) + 1  # +1 for space
            if current_size + word_size > chunk_size and current_chunk:
                chunks.append(' '.join(current_chunk))
                current_chunk = [word]
                current_size = word_size
            else:
                current_chunk.append(word)
                current_size += word_size
        
        if current_chunk:
            chunks.append(' '.join(current_chunk))
        
        return chunks
