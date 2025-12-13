"""
Business Analyst Agents - CrewAI Micro-Agents Architecture

Tool Agents: Action-only, no reasoning
Reasoning Agents: LLM-based analysis and report generation
"""
from agents.tool_agents import (
    create_stock_data_agent,
    create_web_search_agent,
    create_web_scraper_agent,
    create_pdf_loader_agent
)
from agents.reasoning_agents import (
    create_financial_analyst_agent,
    create_competitor_analyst_agent,
    create_report_writer_agent,
    create_coordinator_agent
)

__all__ = [
    # Tool Agents
    "create_stock_data_agent",
    "create_web_search_agent",
    "create_web_scraper_agent",
    "create_pdf_loader_agent",
    # Reasoning Agents
    "create_financial_analyst_agent",
    "create_competitor_analyst_agent",
    "create_report_writer_agent",
    "create_coordinator_agent"
]

