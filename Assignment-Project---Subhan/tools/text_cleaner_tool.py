"""
Text Cleaner Tool - Cleans and processes raw text data
"""
from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import re


class TextCleanerInput(BaseModel):
    """Input schema for text cleaner tool."""
    text: str = Field(..., description="Raw text to clean and process")
    remove_urls: bool = Field(default=True, description="Remove URLs from text")
    remove_emails: bool = Field(default=True, description="Remove email addresses")
    remove_extra_whitespace: bool = Field(default=True, description="Normalize whitespace")
    remove_special_chars: bool = Field(default=False, description="Remove special characters (keeps letters, numbers, basic punctuation)")


class TextCleanerTool(BaseTool):
    """
    Cleans and normalizes text data from web scraping or PDF extraction.
    Removes noise, boilerplate, and formats text for analysis.
    """
    name: str = "text_cleaner"
    description: str = (
        "Cleans raw text by removing URLs, emails, extra whitespace, and other noise. "
        "Use this to process scraped web content or PDF text before analysis. "
        "Returns clean, readable text suitable for LLM processing."
    )
    args_schema: Type[BaseModel] = TextCleanerInput

    def _run(
        self, 
        text: str, 
        remove_urls: bool = True,
        remove_emails: bool = True,
        remove_extra_whitespace: bool = True,
        remove_special_chars: bool = False
    ) -> str:
        """Execute the text cleaning."""
        if not text:
            return ""
        
        cleaned = text
        
        # Remove URLs
        if remove_urls:
            cleaned = re.sub(
                r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
                '',
                cleaned
            )
        
        # Remove email addresses
        if remove_emails:
            cleaned = re.sub(
                r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
                '',
                cleaned
            )
        
        # Remove common boilerplate patterns
        boilerplate_patterns = [
            r'Cookie Policy.*?Accept',
            r'Privacy Policy.*?Terms',
            r'Subscribe to our newsletter.*?Email',
            r'Follow us on.*?Twitter',
            r'©\s*\d{4}.*?All rights reserved',
            r'Loading\.\.\.',
            r'\[.*?\]',  # Remove bracketed content like [Click here]
        ]
        
        for pattern in boilerplate_patterns:
            cleaned = re.sub(pattern, '', cleaned, flags=re.IGNORECASE | re.DOTALL)
        
        # Remove special characters if requested
        if remove_special_chars:
            # Keep letters, numbers, basic punctuation, and whitespace
            cleaned = re.sub(r'[^a-zA-Z0-9\s.,!?;:\'"()-]', '', cleaned)
        
        # Normalize whitespace
        if remove_extra_whitespace:
            # Replace multiple spaces with single space
            cleaned = re.sub(r'[ \t]+', ' ', cleaned)
            # Replace multiple newlines with double newline (paragraph break)
            cleaned = re.sub(r'\n\s*\n', '\n\n', cleaned)
            # Remove leading/trailing whitespace from each line
            cleaned = '\n'.join(line.strip() for line in cleaned.split('\n'))
            # Remove leading/trailing whitespace from entire text
            cleaned = cleaned.strip()
        
        # Remove very short lines (likely noise)
        lines = cleaned.split('\n')
        cleaned_lines = [line for line in lines if len(line.strip()) > 3 or line.strip() == '']
        cleaned = '\n'.join(cleaned_lines)
        
        return cleaned

