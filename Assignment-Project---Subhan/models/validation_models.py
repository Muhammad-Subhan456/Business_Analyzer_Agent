"""
Pydantic Validation Models for Business Analysis
All major outputs must pass through these validators.
"""
from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import datetime
import re


class ReportValidationModel(BaseModel):
    """
    Validates the final business analysis report structure.
    
    Ensures:
    - Required sections are present
    - Type enforcement
    - Completeness scoring
    """
    
    # Required fields
    ticker: str = Field(..., description="Stock ticker symbol")
    company_name: Optional[str] = Field(None, description="Company name")
    report_content: str = Field(..., min_length=100, description="Full report content in markdown")
    report_type: str = Field(..., description="Type: 'Full Analysis' or 'Quick Analysis'")
    generated_at: datetime = Field(default_factory=datetime.now, description="Report generation timestamp")
    
    # Optional but tracked fields
    word_count: Optional[int] = Field(None, description="Number of words in report")
    sections_found: Optional[List[str]] = Field(default_factory=list, description="Sections identified in report")
    
    # Validation scores
    completeness_score: float = Field(default=0.0, ge=0.0, le=1.0, description="Report completeness score (0-1)")
    structure_score: float = Field(default=0.0, ge=0.0, le=1.0, description="Report structure quality score (0-1)")
    
    @field_validator('ticker')
    @classmethod
    def validate_ticker(cls, v: str) -> str:
        """Validate ticker format."""
        if not v or len(v) < 1 or len(v) > 10:
            raise ValueError("Ticker must be 1-10 characters")
        return v.upper().strip()
    
    @field_validator('report_type')
    @classmethod
    def validate_report_type(cls, v: str) -> str:
        """Validate report type."""
        allowed = ["Full Analysis", "Quick Analysis"]
        if v not in allowed:
            raise ValueError(f"Report type must be one of: {allowed}")
        return v
    
    @field_validator('report_content')
    @classmethod
    def validate_report_content(cls, v: str) -> str:
        """Validate report content has minimum length."""
        if len(v.strip()) < 100:
            raise ValueError("Report content must be at least 100 characters")
        return v.strip()
    
    def calculate_completeness(self) -> float:
        """
        Calculate completeness score based on required sections.
        Returns score between 0.0 and 1.0
        """
        required_sections = [
            "executive summary",
            "company overview",
            "financial analysis",
            "key takeaways"
        ]
        
        content_lower = self.report_content.lower()
        found_sections = []
        
        for section in required_sections:
            # Check for section headers (markdown format)
            patterns = [
                f"## {section}",
                f"# {section}",
                f"**{section}**",
                section.replace(" ", ""),
            ]
            
            for pattern in patterns:
                if pattern in content_lower:
                    found_sections.append(section)
                    break
        
        # Base score: 0.5 for having content
        score = 0.5
        
        # Add 0.125 for each required section found (max 0.5)
        score += len(found_sections) * 0.125
        
        # Bonus for word count (if 800-1200 words, add 0.1)
        if self.word_count:
            if 800 <= self.word_count <= 1200:
                score += 0.1
            elif self.word_count >= 500:
                score += 0.05
        
        return min(score, 1.0)
    
    def calculate_structure_score(self) -> float:
        """
        Calculate structure quality score.
        Returns score between 0.0 and 1.0
        """
        score = 0.0
        
        # Check for markdown headers (## or #)
        header_count = len(re.findall(r'^#{1,3}\s+', self.report_content, re.MULTILINE))
        if header_count >= 3:
            score += 0.4
        elif header_count >= 1:
            score += 0.2
        
        # Check for bullet points or lists
        list_items = len(re.findall(r'^[-*+]\s+', self.report_content, re.MULTILINE))
        if list_items >= 5:
            score += 0.3
        elif list_items >= 2:
            score += 0.15
        
        # Check for numbers/data points (indicates data-driven analysis)
        numbers = len(re.findall(r'\d+[.,]\d+|\d+%|\$\d+', self.report_content))
        if numbers >= 10:
            score += 0.3
        elif numbers >= 5:
            score += 0.15
        
        return min(score, 1.0)
    
    def extract_sections(self) -> List[str]:
        """Extract section names from report content."""
        sections = []
        # Find all markdown headers
        headers = re.findall(r'^#{1,3}\s+(.+)$', self.report_content, re.MULTILINE)
        sections = [h.strip().lower() for h in headers]
        return sections
    
    def model_post_init(self, __context) -> None:
        """Calculate scores and extract sections after validation."""
        # Calculate word count if not provided
        if not self.word_count:
            words = self.report_content.split()
            self.word_count = len(words)
        
        # Extract sections
        self.sections_found = self.extract_sections()
        
        # Calculate scores
        self.completeness_score = self.calculate_completeness()
        self.structure_score = self.calculate_structure_score()
    
    class Config:
        """Pydantic config."""
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class AnalysisMetadataModel(BaseModel):
    """
    Validates analysis metadata and summaries.
    
    Stores:
    - Key decisions from agents
    - Data completeness
    - Confidence scores
    - Brief summaries
    """
    
    # Required fields
    ticker: str = Field(..., description="Stock ticker symbol")
    query_id: Optional[int] = Field(None, description="Associated query ID from database")
    
    # Summary fields
    summary: str = Field(..., min_length=50, description="Brief analysis summary (50+ chars)")
    key_decisions: str = Field(..., min_length=20, description="Summarized agent decisions (20+ chars)")
    
    # Scoring fields
    data_completeness: float = Field(..., ge=0.0, le=1.0, description="Data completeness score (0-1)")
    confidence_score: float = Field(..., ge=0.0, le=1.0, description="Overall confidence score (0-1)")
    
    # Optional metadata
    competitors_found: Optional[int] = Field(0, ge=0, description="Number of competitors identified")
    news_items_found: Optional[int] = Field(0, ge=0, description="Number of news items found")
    created_at: datetime = Field(default_factory=datetime.now, description="Metadata creation timestamp")
    
    @field_validator('ticker')
    @classmethod
    def validate_ticker(cls, v: str) -> str:
        """Validate ticker format."""
        if not v or len(v) < 1 or len(v) > 10:
            raise ValueError("Ticker must be 1-10 characters")
        return v.upper().strip()
    
    @field_validator('summary')
    @classmethod
    def validate_summary(cls, v: str) -> str:
        """Validate summary has minimum length."""
        if len(v.strip()) < 50:
            raise ValueError("Summary must be at least 50 characters")
        return v.strip()
    
    @field_validator('key_decisions')
    @classmethod
    def validate_key_decisions(cls, v: str) -> str:
        """Validate key decisions has minimum length."""
        if len(v.strip()) < 20:
            raise ValueError("Key decisions must be at least 20 characters")
        return v.strip()
    
    @field_validator('data_completeness', 'confidence_score')
    @classmethod
    def validate_scores(cls, v: float) -> float:
        """Ensure scores are in valid range."""
        if not 0.0 <= v <= 1.0:
            raise ValueError("Scores must be between 0.0 and 1.0")
        return round(v, 3)  # Round to 3 decimal places
    
    def calculate_overall_quality(self) -> float:
        """
        Calculate overall quality score from completeness and confidence.
        Returns weighted average.
        """
        # Weight: 60% completeness, 40% confidence
        return (self.data_completeness * 0.6) + (self.confidence_score * 0.4)
    
    class Config:
        """Pydantic config."""
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

