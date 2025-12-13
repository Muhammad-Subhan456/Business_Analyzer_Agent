# 📊 AI Business Analyst Agent

An intelligent multi-agent system for comprehensive business analysis powered by **CrewAI** and **Google Gemini**.

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![CrewAI](https://img.shields.io/badge/CrewAI-0.86.0-green)
![Gemini](https://img.shields.io/badge/Gemini-1.5_Flash-orange)

## 🎯 Features

- **Real-time Stock Data**: Fetch live stock prices and historical data using yfinance (FREE)
- **Automated Research**: AI-powered competitor and news research
- **Multi-Agent Architecture**: Specialized agents for different tasks
- **Professional Reports**: Generate comprehensive business analysis reports
- **Beautiful UI**: Modern Streamlit interface with dark theme

## 🏗️ Architecture

```
                         ┌──────────────────────────────┐
                         │     Streamlit Frontend       │
                         └───────────────┬──────────────┘
                                         │
                               User Request (Ticker)
                                         │
                                ▼ Coordinator Agent
                                         │
                    ┌───────────────────────────────────────────┐
                    │                 Subtasks                  │
                    └───────────────────────────────────────────┘
            ┌────────────────┬─────────────────────────┬───────────────┐
            ▼                ▼                         ▼
 Stock Data Agent   Web Search Agent          Web Scraper Agent
(yfinance tool)    (SerperTool)              (ScraperTool)
            │                │                         │
            │                │                         │
            └──────────┬────┴──────────────┬──────────┘
                       ▼                   ▼
              Financial Analyst     Competitor Analyst
                       │                   │
                       └───────────┬───────┘
                                   ▼
                           Report Writer Agent
                                   ▼
                        Final Report → Streamlit UI
```

### Agent Types

**Tool Agents** (Action-only, no reasoning):
| Agent | Purpose | Technology |
|-------|---------|------------|
| Stock Data Agent | Fetch stock & financial data | yfinance |
| Web Search Agent | General research | Serper API |
| Web Scraper Agent | Scrape specific URLs | CrewAI ScraperTool |
| PDF Loader Agent | Load filings | PyPDF |

**Reasoning Agents** (LLM-based):
| Agent | Purpose |
|-------|---------|
| Financial Analyst | Analyze financials, valuation |
| Competitor Analyst | Competitive landscape analysis |
| Report Writer | Final report generation |

## 🚀 Quick Start

### 1. Clone and Setup

```bash
# Navigate to project directory
cd "Assignment Project - Subhan"

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
.\venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure API Keys

Create a `.env` file in the project root:

```env
# Google Gemini API (FREE)
# Get yours at: https://aistudio.google.com/apikey
GOOGLE_API_KEY=your_google_api_key_here

# Serper API (FREE tier: 2500 searches)
# Get yours at: https://serper.dev/
SERPER_API_KEY=your_serper_api_key_here
```

### 3. Run the Application

```bash
streamlit run app.py
```

Open your browser at `http://localhost:8501`

## 📁 Project Structure

```
project/
├── agents/
│   ├── __init__.py
│   ├── tool_agents.py       # Stock, Search, Scraper agents
│   └── reasoning_agents.py  # Analyst & Report agents
├── tools/
│   ├── __init__.py
│   ├── yfinance_tool.py     # Stock data fetching
│   ├── text_cleaner_tool.py # Text processing
│   └── pdf_loader_tool.py   # PDF extraction
├── crew/
│   ├── __init__.py
│   ├── tasks.py             # Task definitions
│   └── business_analyst_crew.py  # Main crew orchestration
├── app.py                   # Streamlit frontend
├── config.py               # Configuration
├── requirements.txt
└── README.md
```

## 🔧 Configuration

### API Keys Required

| Service           | Purpose            | Free Tier              |
| ----------------- | ------------------ | ---------------------- |
| **Google Gemini** | LLM for all agents | ✅ Free (rate limited) |
| **Serper**        | Web search         | ✅ 2500 searches free  |
| **yfinance**      | Stock data         | ✅ Completely free     |

### Getting API Keys

1. **Google Gemini**:

   - Go to [Google AI Studio](https://aistudio.google.com/apikey)
   - Create a new API key
   - It's free with generous limits

2. **Serper** (for web search):
   - Go to [Serper.dev](https://serper.dev/)
   - Sign up for free account
   - Get 2500 free searches

## 📊 Usage Examples

### Full Analysis

```python
from crew.business_analyst_crew import BusinessAnalystCrew

crew = BusinessAnalystCrew()
report = crew.analyze_company(
    ticker="AAPL",
    company_name="Apple Inc.",
    period="1y"
)
print(report)
```

### Quick Analysis (Financials Only)

```python
from crew.business_analyst_crew import BusinessAnalystCrew

crew = BusinessAnalystCrew()
report = crew.quick_analysis("TSLA")
print(report)
```

## 🎨 UI Features

- **Dark Theme**: Modern dark interface with teal accents
- **Real-time Progress**: Visual feedback during analysis
- **Download Reports**: Export reports as Markdown
- **Popular Tickers**: Quick access to commonly analyzed stocks

## 🔒 Free Tier Limits

| Service          | Limit               |
| ---------------- | ------------------- |
| Gemini 1.5 Flash | 1500 requests/day   |
| Serper           | 2500 searches total |
| yfinance         | Unlimited           |

## 🐛 Troubleshooting

### "API Key not set"

Make sure your `.env` file is in the project root and contains valid keys.

### "No data found for ticker"

- Verify the ticker symbol is correct
- Some international tickers may not be available

### "Rate limit exceeded"

- Wait a few minutes for Gemini rate limits to reset
- Consider upgrading to paid tier for production use

## 📝 License

MIT License - feel free to use for personal or commercial projects.

## 🤝 Contributing

Contributions welcome! Please feel free to submit a Pull Request.

---

Built with ❤️ using CrewAI, Google Gemini, and Streamlit
