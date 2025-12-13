"""
PDF Loader Tool - Extracts text from PDF files
"""
from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import requests
import tempfile
import os


class PDFLoaderInput(BaseModel):
    """Input schema for PDF loader tool."""
    source: str = Field(
        ..., 
        description="Either a URL to a PDF file or a local file path"
    )
    max_pages: int = Field(
        default=50, 
        description="Maximum number of pages to extract (to prevent memory issues)"
    )


class PDFLoaderTool(BaseTool):
    """
    Loads and extracts text from PDF files.
    Supports both URLs and local file paths.
    """
    name: str = "pdf_loader"
    description: str = (
        "Extracts text content from PDF files. Can load from URLs (like SEC filings, "
        "annual reports) or local file paths. Returns the extracted text content. "
        "Use this for analyzing company reports, 10-K filings, and other PDF documents."
    )
    args_schema: Type[BaseModel] = PDFLoaderInput

    def _run(self, source: str, max_pages: int = 50) -> str:
        """Execute PDF text extraction."""
        try:
            from pypdf import PdfReader
        except ImportError:
            return "Error: pypdf not installed. Please install with: pip install pypdf"
        
        temp_file = None
        
        try:
            # Check if source is URL or file path
            if source.startswith(('http://', 'https://')):
                # Download PDF from URL
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
                response = requests.get(source, headers=headers, timeout=30)
                response.raise_for_status()
                
                # Save to temp file
                temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
                temp_file.write(response.content)
                temp_file.close()
                pdf_path = temp_file.name
            else:
                # Local file path
                if not os.path.exists(source):
                    return f"Error: File not found at path: {source}"
                pdf_path = source
            
            # Extract text from PDF
            reader = PdfReader(pdf_path)
            total_pages = len(reader.pages)
            pages_to_extract = min(total_pages, max_pages)
            
            text_content = []
            text_content.append(f"=== PDF Document ===")
            text_content.append(f"Source: {source}")
            text_content.append(f"Total Pages: {total_pages}")
            text_content.append(f"Pages Extracted: {pages_to_extract}")
            text_content.append("=" * 50)
            text_content.append("")
            
            for i, page in enumerate(reader.pages[:pages_to_extract]):
                page_text = page.extract_text()
                if page_text:
                    text_content.append(f"\n--- Page {i + 1} ---\n")
                    text_content.append(page_text)
            
            result = '\n'.join(text_content)
            
            # Truncate if too long (to prevent token overflow)
            max_chars = 50000
            if len(result) > max_chars:
                result = result[:max_chars] + f"\n\n[... Content truncated at {max_chars} characters ...]"
            
            return result
            
        except requests.exceptions.RequestException as e:
            return f"Error downloading PDF: {str(e)}"
        except Exception as e:
            return f"Error processing PDF: {str(e)}"
        finally:
            # Cleanup temp file
            if temp_file and os.path.exists(temp_file.name):
                try:
                    os.unlink(temp_file.name)
                except:
                    pass

