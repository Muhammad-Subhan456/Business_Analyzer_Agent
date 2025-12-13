"""
Task Definitions for Business Analyst Crew
Each task defines what an agent should do and what output is expected.
"""
from crewai import Task, Agent
from typing import List


class BusinessAnalysisTasks:
    """
    Factory class for creating analysis tasks.
    Tasks are the units of work that agents perform.
    """
    
    @staticmethod
    def fetch_stock_data_task(
        agent: Agent,
        ticker: str,
        period: str = "1y"
    ) -> Task:
        """
        Task: Fetch stock price data and history
        Agent: Stock Data Agent
        """
        return Task(
            description=f"""
            Fetch comprehensive stock market data for ticker: {ticker}
            
            Required Actions:
            1. Use yfinance_stock_data tool to get price history for period: {period}
            2. Use yfinance_company_info tool to get company fundamentals
            
            Data to Retrieve:
            - Historical price data (Open, High, Low, Close, Volume)
            - Current stock price
            - 52-week high/low
            - Key financial metrics (P/E, market cap, etc.)
            - Company description and sector
            
            Return all data in a structured format. Do NOT analyze - just retrieve.
            """,
            expected_output="""
            Structured JSON data containing:
            - Stock price history and metrics
            - Company fundamental information
            - All retrieved financial data
            """,
            agent=agent
        )
    
    @staticmethod
    def search_competitors_task(
        agent: Agent,
        company_name: str,
        industry: str = ""
    ) -> Task:
        """
        Task: Search for company competitors
        Agent: Web Search Agent
        """
        return Task(
            description=f"""
            Search the web to find competitors for: {company_name}
            Industry context: {industry if industry else 'Unknown - please identify'}
            
            Required Searches:
            1. "{company_name} competitors"
            2. "{company_name} vs" to find comparison articles
            3. "{industry} market leaders" (if industry known)
            4. "{company_name} market share"
            
            Return:
            - List of identified competitors (minimum 5)
            - Brief description of each competitor
            - Source URLs for the information
            - Any market share data found
            
            Return raw search results - do NOT analyze deeply.
            """,
            expected_output="""
            List of competitors with:
            - Company names
            - Brief descriptions
            - Source URLs
            - Any market share data found
            """,
            agent=agent
        )
    
    @staticmethod
    def search_company_news_task(
        agent: Agent,
        company_name: str,
        ticker: str
    ) -> Task:
        """
        Task: Search for recent company news
        Agent: Web Search Agent
        """
        return Task(
            description=f"""
            Search for recent news and developments for: {company_name} ({ticker})
            
            Required Searches:
            1. "{company_name} news" - recent developments
            2. "{ticker} stock news" - market news
            3. "{company_name} earnings" - financial news
            4. "{company_name} CEO" - leadership news
            
            Focus on:
            - Recent earnings reports
            - Major announcements
            - Product launches
            - Leadership changes
            - Market-moving events
            
            Return search results with URLs and snippets.
            """,
            expected_output="""
            Collection of recent news items:
            - Headlines and snippets
            - Source URLs
            - Approximate dates
            - Categories (earnings, product, leadership, etc.)
            """,
            agent=agent
        )
    
    @staticmethod
    def scrape_company_info_task(
        agent: Agent,
        urls: List[str]
    ) -> Task:
        """
        Task: Scrape detailed content from specific URLs
        Agent: Web Scraper Agent
        """
        urls_formatted = "\n".join([f"- {url}" for url in urls])
        return Task(
            description=f"""
            Scrape and extract text content from the following URLs:
            
            {urls_formatted}
            
            For each URL:
            1. Scrape the page content
            2. Clean the extracted text (remove ads, navigation, etc.)
            3. Return the relevant business information
            
            Focus on extracting:
            - Company descriptions
            - Business model information
            - Key statistics
            - Recent updates
            
            Return cleaned text content - do NOT analyze.
            """,
            expected_output="""
            Cleaned text content from each URL:
            - Source URL
            - Extracted relevant content
            - Any key data points found
            """,
            agent=agent
        )
    
    @staticmethod
    def analyze_financials_task(
        agent: Agent,
        context_tasks: List[Task]
    ) -> Task:
        """
        Task: Analyze financial data and provide insights
        Agent: Financial Analyst Agent
        """
        return Task(
            description="""
            Analyze the financial data provided from previous tasks and provide expert insights.
            
            Your Analysis Should Cover:
            
            1. STOCK PERFORMANCE ANALYSIS
               - Price trend analysis (bullish/bearish/neutral)
               - Volatility assessment
               - Support and resistance levels
               - Comparison to 52-week range
            
            2. VALUATION ANALYSIS
               - P/E ratio interpretation (vs industry average)
               - Price-to-Book assessment
               - PEG ratio analysis
               - Fair value estimation
            
            3. FINANCIAL HEALTH
               - Profitability metrics (margins, ROE, ROA)
               - Growth rates (revenue, earnings)
               - Dividend analysis (if applicable)
               - Debt levels and coverage
            
            4. KEY INSIGHTS
               - Top 3 financial strengths
               - Top 3 financial concerns
               - Investment thesis summary
            
            Be specific with numbers. Support all conclusions with data.
            """,
            expected_output="""
            Comprehensive financial analysis including:
            - Stock performance assessment with specific metrics
            - Valuation analysis with fair value estimate
            - Financial health scorecard
            - Key strengths and concerns
            - Investment thesis
            """,
            agent=agent,
            context=context_tasks  # Takes output from data gathering tasks
        )
    
    @staticmethod
    def analyze_competitors_task(
        agent: Agent,
        company_name: str,
        context_tasks: List[Task]
    ) -> Task:
        """
        Task: Analyze competitive landscape
        Agent: Competitor Analyst Agent
        """
        return Task(
            description=f"""
            Analyze the competitive landscape for: {company_name}
            
            Using the competitor data gathered, provide analysis on:
            
            1. COMPETITOR IDENTIFICATION
               - List top 5-7 direct competitors
               - Identify any indirect competitors
               - Note emerging competitive threats
            
            2. COMPETITIVE POSITIONING
               - Market position of {company_name}
               - Market share estimates (if available)
               - Competitive advantages (moat analysis)
               - Competitive disadvantages
            
            3. COMPARISON TABLE
               Create a comparison table with:
               - Company names
               - Market cap / size
               - Key products/services
               - Geographic presence
               - Competitive advantage
            
            4. STRATEGIC INSIGHTS
               - Main competitive threats
               - Opportunities vs competitors
               - Market dynamics assessment
            
            Be specific and data-driven where possible.
            """,
            expected_output="""
            Competitive analysis including:
            - Ranked list of competitors with descriptions
            - Competitive positioning analysis
            - Comparison table
            - Strategic insights and threats
            """,
            agent=agent,
            context=context_tasks
        )
    
    @staticmethod
    def write_final_report_task(
        agent: Agent,
        company_name: str,
        ticker: str,
        context_tasks: List[Task]
    ) -> Task:
        """
        Task: Write the final comprehensive business report
        Agent: Report Writer Agent
        """
        return Task(
            description=f"""
            Create a comprehensive Business Analysis Report for {company_name} ({ticker}).
            
            REPORT STRUCTURE:
            
            # {company_name} ({ticker}) - Business Analysis Report
            
            ## Executive Summary
            - One paragraph overview
            - Key investment highlights
            - Overall recommendation
            
            ## Company Overview
            - Business description
            - Products/services
            - Industry and sector
            - Key statistics
            
            ## Financial Analysis
            - Stock performance summary
            - Valuation assessment
            - Financial health metrics
            - Growth trajectory
            
            ## Competitive Landscape
            - Key competitors
            - Market position
            - Competitive advantages
            - Competitive threats
            
            ## SWOT Analysis
            - Strengths
            - Weaknesses
            - Opportunities
            - Threats
            
            ## Key Takeaways
            - Top 5 things investors should know
            
            ## Risk Factors
            - Key risks to consider
            
            FORMAT REQUIREMENTS:
            - Use clear headers and subheaders
            - Include specific numbers and data points
            - Use bullet points for readability
            - Keep language professional but accessible
            - Total length: 800-1200 words
            """,
            expected_output="""
            Complete business analysis report in markdown format with:
            - Executive summary
            - Company overview
            - Financial analysis
            - Competitive analysis
            - SWOT analysis
            - Key takeaways
            - Risk factors
            
            Professional formatting with headers, bullet points, and clear structure.
            """,
            agent=agent,
            context=context_tasks
        )

