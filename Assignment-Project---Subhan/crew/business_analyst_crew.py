"""
Business Analyst Crew - Main Orchestration
Brings together all agents and tasks into a working crew.
"""
from crewai import Crew, Process
from typing import Optional
import os

from agents.tool_agents import (
    create_stock_data_agent,
    create_web_search_agent,
    create_web_scraper_agent
)
from agents.reasoning_agents import (
    create_financial_analyst_agent,
    create_competitor_analyst_agent,
    create_report_writer_agent
)
from crew.tasks import BusinessAnalysisTasks


class BusinessAnalystCrew:
    """
    Business Analyst Crew - Orchestrates the full analysis workflow.
    
    Architecture:
    - Tool Agents: Fetch data (no reasoning)
    - Reasoning Agents: Analyze and synthesize
    
    Workflow:
    1. Stock Data Agent → Fetch financial data
    2. Web Search Agent → Find competitors & news
    3. Financial Analyst → Analyze financial data
    4. Competitor Analyst → Analyze competitive landscape
    5. Report Writer → Create final report
    """
    
    def __init__(self, verbose: bool = True):
        """Initialize the crew with all agents."""
        self.verbose = verbose
        
        # Initialize Tool Agents
        self.stock_data_agent = create_stock_data_agent()
        self.web_search_agent = create_web_search_agent()
        self.web_scraper_agent = create_web_scraper_agent()
        
        # Initialize Reasoning Agents
        self.financial_analyst = create_financial_analyst_agent()
        self.competitor_analyst = create_competitor_analyst_agent()
        self.report_writer = create_report_writer_agent()
        
        # Task factory
        self.tasks = BusinessAnalysisTasks()
    
    def analyze_company(
        self,
        ticker: str,
        company_name: Optional[str] = None,
        period: str = "1y"
    ) -> str:
        """
        Run full business analysis for a company.
        
        Args:
            ticker: Stock ticker symbol (e.g., "AAPL")
            company_name: Company name (optional, will be fetched if not provided)
            period: Historical data period (default: 1 year)
            
        Returns:
            Complete business analysis report as string
        """
        # Use ticker as company name if not provided
        if not company_name:
            company_name = ticker
        
        # ============================================
        # PHASE 1: DATA GATHERING (Tool Agents)
        # ============================================
        
        # Task 1: Fetch stock data
        fetch_stock_task = self.tasks.fetch_stock_data_task(
            agent=self.stock_data_agent,
            ticker=ticker,
            period=period
        )
        
        # Task 2: Search for competitors
        search_competitors_task = self.tasks.search_competitors_task(
            agent=self.web_search_agent,
            company_name=company_name
        )
        
        # Task 3: Search for news
        search_news_task = self.tasks.search_company_news_task(
            agent=self.web_search_agent,
            company_name=company_name,
            ticker=ticker
        )
        
        # ============================================
        # PHASE 2: ANALYSIS (Reasoning Agents)
        # ============================================
        
        # Task 4: Financial Analysis (depends on stock data)
        analyze_financials_task = self.tasks.analyze_financials_task(
            agent=self.financial_analyst,
            context_tasks=[fetch_stock_task]
        )
        
        # Task 5: Competitor Analysis (depends on search results)
        analyze_competitors_task = self.tasks.analyze_competitors_task(
            agent=self.competitor_analyst,
            company_name=company_name,
            context_tasks=[search_competitors_task, search_news_task]
        )
        
        # ============================================
        # PHASE 3: REPORT GENERATION
        # ============================================
        
        # Task 6: Final Report (depends on all analysis)
        write_report_task = self.tasks.write_final_report_task(
            agent=self.report_writer,
            company_name=company_name,
            ticker=ticker,
            context_tasks=[
                fetch_stock_task,
                analyze_financials_task,
                analyze_competitors_task
            ]
        )
        
        # ============================================
        # CREATE AND RUN CREW
        # ============================================
        
        crew = Crew(
            agents=[
                self.stock_data_agent,
                self.web_search_agent,
                self.financial_analyst,
                self.competitor_analyst,
                self.report_writer
            ],
            tasks=[
                fetch_stock_task,
                search_competitors_task,
                search_news_task,
                analyze_financials_task,
                analyze_competitors_task,
                write_report_task
            ],
            process=Process.sequential,  # Tasks run in order
            verbose=self.verbose
        )
        
        # Execute the crew
        result = crew.kickoff()
        
        return str(result)
    
    def quick_analysis(self, ticker: str) -> str:
        """
        Run a quick analysis with just financial data.
        Skips competitor analysis for faster results.
        
        Args:
            ticker: Stock ticker symbol
            
        Returns:
            Quick financial analysis report
        """
        # Task 1: Fetch stock data
        fetch_stock_task = self.tasks.fetch_stock_data_task(
            agent=self.stock_data_agent,
            ticker=ticker,
            period="6mo"  # Shorter period for quick analysis
        )
        
        # Task 2: Financial Analysis
        analyze_financials_task = self.tasks.analyze_financials_task(
            agent=self.financial_analyst,
            context_tasks=[fetch_stock_task]
        )
        
        crew = Crew(
            agents=[
                self.stock_data_agent,
                self.financial_analyst
            ],
            tasks=[
                fetch_stock_task,
                analyze_financials_task
            ],
            process=Process.sequential,
            verbose=self.verbose
        )
        
        result = crew.kickoff()
        return str(result)


# Quick test function
def test_crew():
    """Test the crew with a sample ticker."""
    # Using local Ollama - no API key needed for LLM
    crew = BusinessAnalystCrew(verbose=True)
    
    print("🚀 Starting Business Analysis for AAPL...")
    print("=" * 50)
    
    result = crew.quick_analysis("AAPL")
    
    print("\n" + "=" * 50)
    print("📊 ANALYSIS COMPLETE")
    print("=" * 50)
    print(result)


if __name__ == "__main__":
    test_crew()

