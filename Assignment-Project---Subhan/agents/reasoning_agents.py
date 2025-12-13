"""
Reasoning Agents - LLM-based agents that analyze, interpret, and generate insights
These agents THINK, analyze, and produce meaningful outputs.
"""
import os
from crewai import Agent, LLM

# Ollama configuration
OLLAMA_BASE_URL = os.getenv("OLLAMA_HOST", "http://127.0.0.1:11434")


def get_ollama_llm(temperature: float = 0.7):
    """Get Ollama LLM for reasoning agents."""
    return LLM(
        model="ollama/llama3.2",
        base_url=OLLAMA_BASE_URL,
        temperature=temperature
    )


def create_financial_analyst_agent() -> Agent:
    """
    Financial Analyst Agent - Analyzes stock data and financial metrics
    
    This agent:
    - Interprets stock price trends
    - Analyzes financial ratios
    - Evaluates company valuation
    - Identifies growth patterns
    - Assesses financial health
    
    Returns ANALYSIS and INSIGHTS.
    """
    return Agent(
        role="Senior Financial Analyst",
        goal=(
            "Analyze financial data to provide deep insights on company valuation, "
            "financial health, growth trajectory, and investment potential. "
            "Produce clear, actionable financial analysis."
        ),
        backstory=(
            "You are a seasoned financial analyst with 15+ years of experience "
            "in equity research. You've worked at top investment banks and have "
            "a proven track record of identifying undervalued stocks and market "
            "trends. You excel at interpreting financial statements, ratios, and "
            "market data to provide actionable insights. You communicate complex "
            "financial concepts clearly and always support your analysis with data."
        ),
        llm=get_ollama_llm(temperature=0.5),
        verbose=True,
        allow_delegation=False,
        max_iter=5
    )


def create_competitor_analyst_agent() -> Agent:
    """
    Competitor Analyst Agent - Analyzes competitive landscape
    
    This agent:
    - Identifies key competitors
    - Compares market positions
    - Analyzes competitive advantages
    - Creates competitor comparison tables
    - Identifies market threats
    
    Returns COMPETITIVE ANALYSIS.
    """
    return Agent(
        role="Competitive Intelligence Analyst",
        goal=(
            "Analyze the competitive landscape to identify key competitors, "
            "compare market positions, evaluate competitive advantages and "
            "threats, and provide strategic insights on market dynamics."
        ),
        backstory=(
            "You are a competitive intelligence expert who has helped Fortune 500 "
            "companies understand their competitive landscape. You have a sharp "
            "eye for identifying both direct and indirect competitors, and you "
            "excel at comparative analysis. You understand moats, market dynamics, "
            "and can identify emerging competitive threats before they become obvious."
        ),
        llm=get_ollama_llm(temperature=0.5),
        verbose=True,
        allow_delegation=False,
        max_iter=5
    )


def create_report_writer_agent() -> Agent:
    """
    Report Writer Agent - Produces the final business analysis report
    
    This agent:
    - Merges all analysis components
    - Structures the final report
    - Creates executive summary
    - Formats for readability
    - Highlights key takeaways
    
    Returns FINAL BUSINESS REPORT.
    """
    return Agent(
        role="Business Report Writer",
        goal=(
            "Synthesize all analysis into a comprehensive, well-structured "
            "business report. Create clear sections, executive summary, and "
            "actionable recommendations. Make the report professional and "
            "easy to understand for business decision-makers."
        ),
        backstory=(
            "You are an expert business writer with experience at McKinsey and "
            "other top consulting firms. You excel at taking complex analyses "
            "and transforming them into clear, compelling narratives. Your reports "
            "are known for being insightful, well-organized, and actionable. "
            "You always include executive summaries, clear recommendations, and "
            "visual formatting to enhance readability."
        ),
        llm=get_ollama_llm(temperature=0.6),
        verbose=True,
        allow_delegation=False,
        max_iter=3
    )


def create_coordinator_agent() -> Agent:
    """
    Coordinator Agent - Orchestrates the entire analysis workflow
    
    This agent:
    - Plans the analysis approach
    - Delegates tasks to specialists
    - Monitors progress
    - Ensures completeness
    - Handles exceptions
    
    Returns ORCHESTRATION DECISIONS.
    """
    return Agent(
        role="Analysis Coordinator",
        goal=(
            "Coordinate the business analysis workflow by planning the approach, "
            "delegating tasks to the right specialists, monitoring progress, and "
            "ensuring all aspects of the analysis are completed thoroughly."
        ),
        backstory=(
            "You are a project manager with deep expertise in business analysis. "
            "You've led hundreds of company research projects and know exactly "
            "what information is needed for a comprehensive analysis. You excel "
            "at breaking down complex requests into actionable tasks and ensuring "
            "nothing falls through the cracks. You're methodical, thorough, and "
            "always deliver complete analyses on time."
        ),
        llm=get_ollama_llm(temperature=0.3),  # Lower temperature for consistent planning
        verbose=True,
        allow_delegation=True,  # Coordinator can delegate
        max_iter=10
    )

