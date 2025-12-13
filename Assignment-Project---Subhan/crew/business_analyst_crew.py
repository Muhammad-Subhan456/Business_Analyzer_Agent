"""
Business Analyst Crew - Main Orchestration
Brings together all agents and tasks into a working crew.
"""
from crewai import Crew, Process
from typing import Optional
import os
import re

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
from database.db_manager import DatabaseManager
from models.validation_models import ReportValidationModel, AnalysisMetadataModel


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
    
    def __init__(self, verbose: bool = True, enable_db: bool = True):
        """
        Initialize the crew with all agents.
        
        Args:
            verbose: Enable verbose logging
            enable_db: Enable database logging and storage
        """
        self.verbose = verbose
        self.enable_db = enable_db
        
        # Initialize database if enabled
        if self.enable_db:
            self.db = DatabaseManager()
        else:
            self.db = None
        
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
        
        # Create database query record
        query_id = None
        if self.enable_db and self.db:
            try:
                query_id = self.db.create_query(
                    ticker=ticker,
                    company_name=company_name,
                    analysis_type="Full Analysis",
                    period=period
                )
                self.db.log_agent_action(
                    query_id=query_id,
                    agent_name="Crew",
                    action_summary=f"Started full analysis for {ticker}"
                )
            except Exception as e:
                if self.verbose:
                    print(f"⚠️ Database logging error: {e}")
        
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
        try:
            result = crew.kickoff()
            report_content = str(result)
            
            # Log agent actions (minimal logging)
            if self.enable_db and self.db and query_id:
                try:
                    # Log key agent actions
                    self.db.log_agent_action(
                        query_id=query_id,
                        agent_name="Stock Data Agent",
                        action_summary=f"Fetched stock data for {ticker}"
                    )
                    self.db.log_agent_action(
                        query_id=query_id,
                        agent_name="Web Search Agent",
                        action_summary="Searched for competitors and news"
                    )
                    self.db.log_agent_action(
                        query_id=query_id,
                        agent_name="Financial Analyst",
                        action_summary="Analyzed financial data"
                    )
                    self.db.log_agent_action(
                        query_id=query_id,
                        agent_name="Competitor Analyst",
                        action_summary="Analyzed competitive landscape"
                    )
                    self.db.log_agent_action(
                        query_id=query_id,
                        agent_name="Report Writer",
                        action_summary="Generated final report"
                    )
                except Exception as e:
                    if self.verbose:
                        print(f"⚠️ Database logging error: {e}")
            
            # Validate and store report
            validated_report = self._validate_and_store_report(
                query_id=query_id,
                ticker=ticker,
                company_name=company_name,
                report_content=report_content,
                report_type="Full Analysis"
            )
            
            # Update query status
            if self.enable_db and self.db and query_id:
                try:
                    self.db.update_query_status(query_id, "completed")
                except Exception as e:
                    if self.verbose:
                        print(f"⚠️ Database update error: {e}")
            
            return validated_report
            
        except Exception as e:
            # Log error
            if self.enable_db and self.db and query_id:
                try:
                    self.db.update_query_status(query_id, "failed", str(e))
                    self.db.log_agent_action(
                        query_id=query_id,
                        agent_name="Crew",
                        action_summary=f"Analysis failed: {str(e)[:200]}",
                        status="error"
                    )
                except:
                    pass
            
            raise
    
    def quick_analysis(self, ticker: str) -> str:
        """
        Run a quick analysis with financial data and competitor analysis.
        Includes competitor analysis for comprehensive reports.
        
        Args:
            ticker: Stock ticker symbol
            
        Returns:
            Quick financial analysis report with competitor analysis
        """
        # Use ticker as company name if not provided
        company_name = ticker
        
        # Create database query record
        query_id = None
        if self.enable_db and self.db:
            try:
                query_id = self.db.create_query(
                    ticker=ticker,
                    company_name=None,
                    analysis_type="Quick Analysis",
                    period="6mo"
                )
                self.db.log_agent_action(
                    query_id=query_id,
                    agent_name="Crew",
                    action_summary=f"Started quick analysis for {ticker}"
                )
            except Exception as e:
                if self.verbose:
                    print(f"⚠️ Database logging error: {e}")
        
        # Task 1: Fetch stock data
        fetch_stock_task = self.tasks.fetch_stock_data_task(
            agent=self.stock_data_agent,
            ticker=ticker,
            period="6mo"  # Shorter period for quick analysis
        )
        
        # Task 2: Search for competitors (added for competitor analysis)
        search_competitors_task = self.tasks.search_competitors_task(
            agent=self.web_search_agent,
            company_name=company_name
        )
        
        # Task 3: Financial Analysis
        analyze_financials_task = self.tasks.analyze_financials_task(
            agent=self.financial_analyst,
            context_tasks=[fetch_stock_task]
        )
        
        # Task 4: Competitor Analysis (added for comprehensive report)
        analyze_competitors_task = self.tasks.analyze_competitors_task(
            agent=self.competitor_analyst,
            company_name=company_name,
            context_tasks=[search_competitors_task]
        )
        
        # Task 5: Final Report (includes competitor analysis)
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
                analyze_financials_task,
                analyze_competitors_task,
                write_report_task
            ],
            process=Process.sequential,
            verbose=self.verbose
        )
        
        try:
            result = crew.kickoff()
            report_content = str(result)
            
            # Log agent actions
            if self.enable_db and self.db and query_id:
                try:
                    self.db.log_agent_action(
                        query_id=query_id,
                        agent_name="Stock Data Agent",
                        action_summary=f"Fetched stock data for {ticker}"
                    )
                    self.db.log_agent_action(
                        query_id=query_id,
                        agent_name="Web Search Agent",
                        action_summary="Searched for competitors"
                    )
                    self.db.log_agent_action(
                        query_id=query_id,
                        agent_name="Financial Analyst",
                        action_summary="Analyzed financial data"
                    )
                    self.db.log_agent_action(
                        query_id=query_id,
                        agent_name="Competitor Analyst",
                        action_summary="Analyzed competitive landscape"
                    )
                    self.db.log_agent_action(
                        query_id=query_id,
                        agent_name="Report Writer",
                        action_summary="Generated final report"
                    )
                except Exception as e:
                    if self.verbose:
                        print(f"⚠️ Database logging error: {e}")
            
            # Validate and store report
            validated_report = self._validate_and_store_report(
                query_id=query_id,
                ticker=ticker,
                company_name=None,
                report_content=report_content,
                report_type="Quick Analysis"
            )
            
            # Update query status
            if self.enable_db and self.db and query_id:
                try:
                    self.db.update_query_status(query_id, "completed")
                except Exception as e:
                    if self.verbose:
                        print(f"⚠️ Database update error: {e}")
            
            return validated_report
            
        except Exception as e:
            # Log error
            if self.enable_db and self.db and query_id:
                try:
                    self.db.update_query_status(query_id, "failed", str(e))
                    self.db.log_agent_action(
                        query_id=query_id,
                        agent_name="Crew",
                        action_summary=f"Analysis failed: {str(e)[:200]}",
                        status="error"
                    )
                except:
                    pass
            
            raise
    
    def _validate_and_store_report(
        self,
        query_id: Optional[int],
        ticker: str,
        company_name: Optional[str],
        report_content: str,
        report_type: str
    ) -> str:
        """
        Validate report using Pydantic and store in database.
        
        Returns:
            Validated report content (same as input if valid)
        """
        try:
            # Validate report with Pydantic
            report_model = ReportValidationModel(
                ticker=ticker,
                company_name=company_name,
                report_content=report_content,
                report_type=report_type
            )
            
            # Extract metadata for storage
            summary = self._extract_summary(report_content)
            key_decisions = self._extract_key_decisions(report_content)
            
            # Calculate data completeness (simplified)
            data_completeness = report_model.completeness_score
            confidence_score = (report_model.completeness_score + report_model.structure_score) / 2
            
            # Store in database
            if self.enable_db and self.db and query_id:
                try:
                    # Save report
                    self.db.save_report(
                        query_id=query_id,
                        ticker=ticker,
                        report_content=report_content,
                        word_count=report_model.word_count
                    )
                    
                    # Save metadata
                    self.db.save_metadata(
                        query_id=query_id,
                        key_decisions=key_decisions,
                        data_completeness=data_completeness,
                        confidence_score=confidence_score,
                        summary=summary
                    )
                except Exception as e:
                    if self.verbose:
                        print(f"⚠️ Database storage error: {e}")
            
            if self.verbose:
                print(f"✅ Report validated - Completeness: {data_completeness:.2f}, Structure: {report_model.structure_score:.2f}")
            
            return report_content
            
        except Exception as e:
            # If validation fails, log but don't block
            if self.verbose:
                print(f"⚠️ Report validation error: {e}")
            
            # Still store the report even if validation has issues
            if self.enable_db and self.db and query_id:
                try:
                    self.db.save_report(
                        query_id=query_id,
                        ticker=ticker,
                        report_content=report_content
                    )
                except:
                    pass
            
            return report_content
    
    def _extract_summary(self, report_content: str) -> str:
        """Extract summary from report (first 200 chars or executive summary)."""
        # Try to find executive summary section
        summary_match = re.search(
            r'(?:##\s+Executive\s+Summary|#\s+Executive\s+Summary)(.*?)(?=##|$)',
            report_content,
            re.IGNORECASE | re.DOTALL
        )
        
        if summary_match:
            summary = summary_match.group(1).strip()
            # Clean up markdown
            summary = re.sub(r'[#*\-]', '', summary)
            summary = summary[:500].strip()
            return summary if len(summary) >= 50 else report_content[:500]
        
        # Fallback: first 500 chars
        return report_content[:500].strip()
    
    def _extract_key_decisions(self, report_content: str) -> str:
        """Extract key decisions/insights from report."""
        # Try to find key takeaways section
        takeaways_match = re.search(
            r'(?:##\s+Key\s+Takeaways|#\s+Key\s+Takeaways)(.*?)(?=##|$)',
            report_content,
            re.IGNORECASE | re.DOTALL
        )
        
        if takeaways_match:
            takeaways = takeaways_match.group(1).strip()
            # Clean up markdown
            takeaways = re.sub(r'[#*\-]', '', takeaways)
            return takeaways[:1000].strip()
        
        # Fallback: extract bullet points
        bullets = re.findall(r'^[-*+]\s+(.+)$', report_content, re.MULTILINE)
        if bullets:
            return ' | '.join(bullets[:5])[:1000]
        
        # Final fallback
        return "Key insights extracted from analysis"[:1000]


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

