"""
Tool Agents - Action-only agents that execute specific tasks
These agents don't write summaries - they only perform actions and return raw data.
"""
import os
from crewai import Agent, LLM
from crewai_tools import SerperDevTool, ScrapeWebsiteTool
from tools.yfinance_tool import YFinanceStockTool, YFinanceCompanyInfoTool
from tools.text_cleaner_tool import TextCleanerTool
from tools.pdf_loader_tool import PDFLoaderTool

# Ollama configuration
OLLAMA_BASE_URL = os.getenv("OLLAMA_HOST", "http://127.0.0.1:11434")


def get_ollama_llm():
    """Get Ollama LLM for agents."""
    return LLM(
        model="ollama/llama3.2",
        base_url=OLLAMA_BASE_URL
    )


def create_stock_data_agent() -> Agent:
    """
    Stock Data Agent - Fetches financial data using yfinance
    
    This agent:
    - Retrieves historical stock prices
    - Gets company financial information
    - Extracts key metrics and ratios
    
    Returns RAW DATA - no analysis or summary.
    """
    return Agent(
        role="Stock Data Retrieval Specialist",
        goal=(
            "Accurately fetch and return stock market data, price history, "
            "and company financial information. Return raw data without interpretation."
        ),
        backstory=(
            "You are a data retrieval specialist focused on fetching accurate "
            "financial data from stock markets. You don't analyze or interpret - "
            "you simply retrieve the requested data efficiently and return it in "
            "a structured format for other specialists to analyze."
        ),
        tools=[
            YFinanceStockTool(),
            YFinanceCompanyInfoTool()
        ],
        llm=get_ollama_llm(),
        verbose=True,
        allow_delegation=False,
        max_iter=3
    )


def create_web_search_agent() -> Agent:
    """
    Web Search Agent - Searches the internet for relevant information
    
    Uses Serper (Google Search API) or Tavily for web searches.
    
    This agent:
    - Finds competitors
    - Searches for news articles
    - Discovers market trends
    - Finds qualitative information
    
    Returns SEARCH RESULTS - URLs and snippets, no analysis.
    """
    return Agent(
        role="Web Research Specialist",
        goal=(
            "Search the web to find relevant information about companies, "
            "competitors, market trends, and news. Return search results with "
            "URLs and relevant snippets."
        ),
        backstory=(
            "You are a web research expert who knows how to craft effective "
            "search queries to find relevant business information. You search "
            "for competitors, news, market analysis, and company information. "
            "You return raw search results for other specialists to analyze."
        ),
        tools=[
            SerperDevTool()  # Uses SERPER_API_KEY from env
        ],
        llm=get_ollama_llm(),
        verbose=True,
        allow_delegation=False,
        max_iter=5
    )


def create_web_scraper_agent() -> Agent:
    """
    Web Scraper Agent - Scrapes content from specific URLs
    
    Uses CrewAI's built-in ScrapeWebsiteTool.
    
    This agent:
    - Scrapes investor relations pages
    - Extracts content from Yahoo Finance
    - Gets Wikipedia company information
    - Scrapes news articles
    
    Returns SCRAPED TEXT - no analysis.
    """
    scraper_tool = ScrapeWebsiteTool()
    text_cleaner = TextCleanerTool()
    
    return Agent(
        role="Web Content Extraction Specialist",
        goal=(
            "Extract text content from specified web pages accurately. "
            "Clean the extracted text and return it in a readable format. "
            "Do not analyze - just extract and clean."
        ),
        backstory=(
            "You are an expert at extracting content from websites. You can "
            "navigate complex web pages and extract the relevant text content "
            "while filtering out ads, navigation, and other noise. You clean "
            "the text and return it for analysis by other specialists."
        ),
        tools=[
            scraper_tool,
            text_cleaner
        ],
        llm=get_ollama_llm(),
        verbose=True,
        allow_delegation=False,
        max_iter=5
    )


def create_pdf_loader_agent() -> Agent:
    """
    PDF Loader Agent - Downloads and extracts text from PDFs
    
    This agent:
    - Downloads PDF files from URLs
    - Extracts text content
    - Handles SEC filings, annual reports, etc.
    
    Returns EXTRACTED TEXT - no analysis.
    """
    return Agent(
        role="Document Extraction Specialist",
        goal=(
            "Download and extract text content from PDF documents. "
            "Handle SEC filings, annual reports, and other business documents. "
            "Return the extracted text without analysis."
        ),
        backstory=(
            "You are a document processing expert who can extract text from "
            "PDF files efficiently. You handle various document types including "
            "SEC filings, annual reports, and investor presentations. You return "
            "clean extracted text for other specialists to analyze."
        ),
        tools=[
            PDFLoaderTool(),
            TextCleanerTool()
        ],
        llm=get_ollama_llm(),
        verbose=True,
        allow_delegation=False,
        max_iter=3
    )

