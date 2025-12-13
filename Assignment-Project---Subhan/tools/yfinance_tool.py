"""
YFinance Tools - Free stock data fetching
No API key required!
"""
from crewai.tools import BaseTool
from typing import Type, Optional
from pydantic import BaseModel, Field
import yfinance as yf
import pandas as pd
import json


class StockTickerInput(BaseModel):
    """Input schema for stock ticker tools."""
    ticker: str = Field(..., description="Stock ticker symbol (e.g., AAPL, MSFT, GOOGL)")
    period: str = Field(
        default="1y", 
        description="Time period for historical data: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max"
    )


class YFinanceStockTool(BaseTool):
    """
    Fetches stock price history and key metrics using yfinance.
    This is a FREE tool - no API key required.
    """
    name: str = "yfinance_stock_data"
    description: str = (
        "Fetches historical stock price data and key financial metrics for a given ticker. "
        "Returns price history (Open, High, Low, Close, Volume), and calculates key metrics "
        "like 52-week high/low, average volume, and price changes. Use this for financial analysis."
    )
    args_schema: Type[BaseModel] = StockTickerInput

    def _run(self, ticker: str, period: str = "1y") -> str:
        """Execute the tool to fetch stock data."""
        try:
            stock = yf.Ticker(ticker.upper())
            
            # Get historical data
            history = stock.history(period=period)
            
            if history.empty:
                return json.dumps({
                    "error": f"No data found for ticker: {ticker}",
                    "suggestion": "Please verify the ticker symbol is correct"
                })
            
            # Calculate key metrics
            current_price = history['Close'].iloc[-1]
            high_52w = history['High'].max()
            low_52w = history['Low'].min()
            avg_volume = history['Volume'].mean()
            
            # Price changes
            if len(history) > 1:
                price_change_1d = ((current_price - history['Close'].iloc[-2]) / history['Close'].iloc[-2]) * 100
            else:
                price_change_1d = 0
                
            if len(history) >= 5:
                price_change_5d = ((current_price - history['Close'].iloc[-5]) / history['Close'].iloc[-5]) * 100
            else:
                price_change_5d = 0
            
            if len(history) >= 22:  # ~1 month of trading days
                price_change_1m = ((current_price - history['Close'].iloc[-22]) / history['Close'].iloc[-22]) * 100
            else:
                price_change_1m = 0
            
            # Get recent data summary (last 30 days for readability)
            recent_data = history.tail(30)[['Open', 'High', 'Low', 'Close', 'Volume']]
            recent_summary = recent_data.describe().to_dict()
            
            result = {
                "ticker": ticker.upper(),
                "period": period,
                "current_price": round(current_price, 2),
                "52_week_high": round(high_52w, 2),
                "52_week_low": round(low_52w, 2),
                "average_volume": int(avg_volume),
                "price_changes": {
                    "1_day_pct": round(price_change_1d, 2),
                    "5_day_pct": round(price_change_5d, 2),
                    "1_month_pct": round(price_change_1m, 2)
                },
                "data_points": len(history),
                "date_range": {
                    "start": str(history.index[0].date()),
                    "end": str(history.index[-1].date())
                },
                "recent_30d_stats": {
                    "close_mean": round(recent_summary['Close']['mean'], 2),
                    "close_std": round(recent_summary['Close']['std'], 2),
                    "volume_mean": int(recent_summary['Volume']['mean'])
                }
            }
            
            return json.dumps(result, indent=2)
            
        except Exception as e:
            return json.dumps({
                "error": str(e),
                "ticker": ticker,
                "suggestion": "Check if the ticker symbol is valid"
            })


class CompanyInfoInput(BaseModel):
    """Input schema for company info tool."""
    ticker: str = Field(..., description="Stock ticker symbol (e.g., AAPL, MSFT, GOOGL)")


class YFinanceCompanyInfoTool(BaseTool):
    """
    Fetches comprehensive company information using yfinance.
    Includes business description, sector, financials, and key ratios.
    """
    name: str = "yfinance_company_info"
    description: str = (
        "Fetches comprehensive company information including business description, "
        "sector, industry, market cap, P/E ratio, dividend yield, and other fundamental data. "
        "Use this to understand what the company does and its financial health."
    )
    args_schema: Type[BaseModel] = CompanyInfoInput

    def _run(self, ticker: str) -> str:
        """Execute the tool to fetch company info."""
        try:
            stock = yf.Ticker(ticker.upper())
            info = stock.info
            
            if not info or info.get('regularMarketPrice') is None:
                # Try to get basic info anyway
                if not info:
                    return json.dumps({
                        "error": f"No company info found for ticker: {ticker}",
                        "suggestion": "Please verify the ticker symbol is correct"
                    })
            
            # Extract key information (handle missing fields gracefully)
            def safe_get(key, default="N/A"):
                return info.get(key, default)
            
            result = {
                "ticker": ticker.upper(),
                "company_name": safe_get("longName"),
                "business_summary": safe_get("longBusinessSummary", "No description available"),
                "sector": safe_get("sector"),
                "industry": safe_get("industry"),
                "country": safe_get("country"),
                "website": safe_get("website"),
                "employees": safe_get("fullTimeEmployees"),
                
                "market_data": {
                    "market_cap": safe_get("marketCap"),
                    "enterprise_value": safe_get("enterpriseValue"),
                    "current_price": safe_get("currentPrice"),
                    "target_high_price": safe_get("targetHighPrice"),
                    "target_low_price": safe_get("targetLowPrice"),
                    "target_mean_price": safe_get("targetMeanPrice"),
                },
                
                "valuation_ratios": {
                    "pe_ratio": safe_get("trailingPE"),
                    "forward_pe": safe_get("forwardPE"),
                    "peg_ratio": safe_get("pegRatio"),
                    "price_to_book": safe_get("priceToBook"),
                    "price_to_sales": safe_get("priceToSalesTrailing12Months"),
                },
                
                "profitability": {
                    "profit_margin": safe_get("profitMargins"),
                    "operating_margin": safe_get("operatingMargins"),
                    "return_on_equity": safe_get("returnOnEquity"),
                    "return_on_assets": safe_get("returnOnAssets"),
                },
                
                "growth": {
                    "revenue_growth": safe_get("revenueGrowth"),
                    "earnings_growth": safe_get("earningsGrowth"),
                },
                
                "dividends": {
                    "dividend_rate": safe_get("dividendRate"),
                    "dividend_yield": safe_get("dividendYield"),
                    "payout_ratio": safe_get("payoutRatio"),
                },
                
                "financials": {
                    "total_revenue": safe_get("totalRevenue"),
                    "gross_profit": safe_get("grossProfits"),
                    "ebitda": safe_get("ebitda"),
                    "net_income": safe_get("netIncomeToCommon"),
                    "total_cash": safe_get("totalCash"),
                    "total_debt": safe_get("totalDebt"),
                    "free_cash_flow": safe_get("freeCashflow"),
                },
                
                "analyst_recommendations": {
                    "recommendation": safe_get("recommendationKey"),
                    "number_of_analysts": safe_get("numberOfAnalystOpinions"),
                }
            }
            
            return json.dumps(result, indent=2)
            
        except Exception as e:
            return json.dumps({
                "error": str(e),
                "ticker": ticker,
                "suggestion": "Check if the ticker symbol is valid"
            })

