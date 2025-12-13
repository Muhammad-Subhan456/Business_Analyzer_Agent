"""
Business Analyst AI Agent - Streamlit Frontend
A beautiful, modern UI for AI-powered company analysis
"""
import os
from dotenv import load_dotenv

# Load environment variables FIRST (before any other imports)
load_dotenv()

# Windows compatibility fix for crewai (Unix signals don't exist on Windows)
import signal
import sys
if sys.platform == 'win32':
    # Add ALL missing Unix signals as dummy values for Windows compatibility
    UNIX_SIGNALS = {
        'SIGHUP': 1,
        'SIGQUIT': 3,
        'SIGTSTP': 20,
        'SIGCONT': 18,
        'SIGUSR1': 10,
        'SIGUSR2': 12,
        'SIGWINCH': 28,
        'SIGALRM': 14,
        'SIGCHLD': 17,
        'SIGPIPE': 13,
    }
    for sig_name, sig_value in UNIX_SIGNALS.items():
        if not hasattr(signal, sig_name):
            setattr(signal, sig_name, sig_value)

# Set Ollama host for local LLM
os.environ["OLLAMA_HOST"] = "http://127.0.0.1:11434"

import streamlit as st
from datetime import datetime
import time

# Page configuration - must be first Streamlit command
st.set_page_config(
    page_title="AI Business Analyst",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern, distinctive design
st.markdown("""
<style>
    /* Import unique fonts */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
    
    /* Root variables - Dark theme with teal accents */
    :root {
        --bg-primary: #0a0f1c;
        --bg-secondary: #111827;
        --bg-tertiary: #1e293b;
        --accent-primary: #14b8a6;
        --accent-secondary: #22d3ee;
        --accent-gradient: linear-gradient(135deg, #14b8a6 0%, #22d3ee 100%);
        --text-primary: #f1f5f9;
        --text-secondary: #94a3b8;
        --text-muted: #64748b;
        --border-color: #334155;
        --success: #10b981;
        --warning: #f59e0b;
        --danger: #ef4444;
    }
    
    /* Global styles */
    .stApp {
        background: var(--bg-primary);
        font-family: 'Outfit', sans-serif;
    }
    
    /* Main container */
    .main .block-container {
        padding: 2rem 3rem;
        max-width: 1400px;
    }
    
    /* Headers */
    h1, h2, h3, h4 {
        font-family: 'Outfit', sans-serif;
        font-weight: 600;
        color: var(--text-primary);
    }
    
    h1 {
        font-size: 2.5rem;
        background: var(--accent-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: var(--bg-secondary);
        border-right: 1px solid var(--border-color);
    }
    
    [data-testid="stSidebar"] .block-container {
        padding: 2rem 1.5rem;
    }
    
    /* Input fields */
    .stTextInput > div > div > input {
        background: var(--bg-tertiary);
        border: 1px solid var(--border-color);
        border-radius: 12px;
        color: var(--text-primary);
        font-family: 'JetBrains Mono', monospace;
        font-size: 1.1rem;
        padding: 0.75rem 1rem;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: var(--accent-primary);
        box-shadow: 0 0 0 3px rgba(20, 184, 166, 0.2);
    }
    
    /* Select boxes */
    .stSelectbox > div > div {
        background: var(--bg-tertiary);
        border: 1px solid var(--border-color);
        border-radius: 12px;
    }
    
    /* Buttons */
    .stButton > button {
        background: var(--accent-gradient);
        color: var(--bg-primary);
        font-family: 'Outfit', sans-serif;
        font-weight: 600;
        font-size: 1rem;
        padding: 0.75rem 2rem;
        border: none;
        border-radius: 12px;
        cursor: pointer;
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 30px rgba(20, 184, 166, 0.3);
    }
    
    /* Cards */
    .metric-card {
        background: var(--bg-secondary);
        border: 1px solid var(--border-color);
        border-radius: 16px;
        padding: 1.5rem;
        margin: 0.5rem 0;
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        border-color: var(--accent-primary);
        transform: translateY(-2px);
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        background: var(--accent-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .metric-label {
        color: var(--text-secondary);
        font-size: 0.875rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-top: 0.25rem;
    }
    
    /* Report container */
    .report-container {
        background: var(--bg-secondary);
        border: 1px solid var(--border-color);
        border-radius: 20px;
        padding: 2.5rem;
        margin-top: 2rem;
        line-height: 1.8;
    }
    
    .report-container h1 {
        font-size: 1.75rem;
        margin-bottom: 1rem;
    }
    
    .report-container h2 {
        font-size: 1.35rem;
        color: var(--accent-primary);
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid var(--border-color);
    }
    
    .report-container h3 {
        font-size: 1.1rem;
        color: var(--text-primary);
        margin: 1.5rem 0 0.75rem 0;
    }
    
    .report-container p {
        color: var(--text-secondary);
        margin-bottom: 1rem;
    }
    
    .report-container ul, .report-container ol {
        color: var(--text-secondary);
        margin-left: 1.5rem;
        margin-bottom: 1rem;
    }
    
    .report-container li {
        margin-bottom: 0.5rem;
    }
    
    .report-container strong {
        color: var(--text-primary);
    }
    
    /* Status indicator */
    .status-indicator {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.75rem 1rem;
        background: var(--bg-tertiary);
        border-radius: 12px;
        margin: 1rem 0;
    }
    
    .status-dot {
        width: 10px;
        height: 10px;
        border-radius: 50%;
        animation: pulse 2s infinite;
    }
    
    .status-dot.running {
        background: var(--accent-secondary);
    }
    
    .status-dot.complete {
        background: var(--success);
        animation: none;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    
    /* Logo/Brand area */
    .brand-container {
        text-align: center;
        padding: 1.5rem 0;
        border-bottom: 1px solid var(--border-color);
        margin-bottom: 2rem;
    }
    
    .brand-icon {
        font-size: 3rem;
        margin-bottom: 0.5rem;
    }
    
    .brand-title {
        font-size: 1.25rem;
        font-weight: 600;
        color: var(--text-primary);
    }
    
    .brand-subtitle {
        font-size: 0.875rem;
        color: var(--text-muted);
    }
    
    /* Info boxes */
    .info-box {
        background: linear-gradient(135deg, rgba(20, 184, 166, 0.1) 0%, rgba(34, 211, 238, 0.1) 100%);
        border: 1px solid rgba(20, 184, 166, 0.3);
        border-radius: 12px;
        padding: 1rem 1.25rem;
        margin: 1rem 0;
    }
    
    .info-box p {
        color: var(--accent-secondary);
        margin: 0;
        font-size: 0.9rem;
    }
    
    /* Feature list */
    .feature-item {
        display: flex;
        align-items: flex-start;
        gap: 0.75rem;
        padding: 0.75rem 0;
        border-bottom: 1px solid var(--border-color);
    }
    
    .feature-item:last-child {
        border-bottom: none;
    }
    
    .feature-icon {
        font-size: 1.25rem;
    }
    
    .feature-text {
        color: var(--text-secondary);
        font-size: 0.9rem;
    }
    
    /* Spinner override */
    .stSpinner > div {
        border-color: var(--accent-primary) !important;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: var(--bg-tertiary);
        border-radius: 12px;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--bg-primary);
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--border-color);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--accent-primary);
    }
</style>
""", unsafe_allow_html=True)


def check_api_keys():
    """Check if required API keys are configured."""
    # GOOGLE_API_KEY no longer needed - using local Ollama
    serper_key = os.getenv("SERPER_API_KEY")
    
    missing = []
    if not serper_key:
        missing.append("SERPER_API_KEY (for web search)")
    
    return len(missing) == 0, missing


def render_sidebar():
    """Render the sidebar with inputs and settings."""
    with st.sidebar:
        # Brand header
        st.markdown("""
        <div class="brand-container">
            <div class="brand-icon">📊</div>
            <div class="brand-title">AI Business Analyst</div>
            <div class="brand-subtitle">Powered by CrewAI & Ollama (Local LLM)</div>
        </div>
        """, unsafe_allow_html=True)
        
        # API Key Status
        keys_ok, missing_keys = check_api_keys()
        if keys_ok:
            st.success("✅ API Keys Configured")
        else:
            st.error(f"❌ Missing: {', '.join(missing_keys)}")
            st.markdown("""
            <div class="info-box">
                <p>Set your API keys as environment variables before running.</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Input section
        st.markdown("### 🎯 Analysis Target")
        
        ticker = st.text_input(
            "Stock Ticker",
            placeholder="e.g., AAPL, MSFT, GOOGL",
            help="Enter the stock ticker symbol for the company you want to analyze"
        ).upper()
        
        company_name = st.text_input(
            "Company Name (Optional)",
            placeholder="e.g., Apple Inc.",
            help="Optional: Provide company name for better search results"
        )
        
        st.markdown("### ⚙️ Settings")
        
        analysis_type = st.selectbox(
            "Analysis Type",
            options=["Full Analysis", "Quick Analysis"],
            help="Full: Complete report with competitor analysis\nQuick: Just financial metrics"
        )
        
        period = st.selectbox(
            "Historical Period",
            options=["6mo", "1y", "2y", "5y"],
            index=1,
            help="Time period for historical stock data"
        )
        
        st.markdown("---")
        
        # Database Viewer Section
        with st.expander("📊 View Stored Reports", expanded=False):
            try:
                from database.db_manager import DatabaseManager
                db = DatabaseManager()
                
                # Get statistics
                stats = db.get_stats()
                if stats.get('total_queries', 0) > 0:
                    st.markdown(f"**Total Reports:** {stats.get('total_reports', 0)}")
                    st.markdown(f"**Success Rate:** {stats.get('success_rate', 0):.1f}%")
                    
                    # Get recent queries
                    recent = db.get_recent_queries(limit=5)
                    if recent:
                        st.markdown("**Recent Analyses:**")
                        for query in recent:
                            status_icon = "✅" if query['status'] == 'completed' else "⏳" if query['status'] == 'pending' else "❌"
                            st.markdown(f"{status_icon} **{query['ticker']}** - {query['analysis_type']}")
                            st.caption(f"Created: {query['created_at']}")
                            
                            # Show report if available
                            reports = db.get_reports_by_ticker(query['ticker'], limit=1)
                            if reports and reports[0].get('query_id') == query['id']:
                                with st.expander(f"View Report for {query['ticker']}"):
                                    report = reports[0]
                                    st.markdown(f"**Word Count:** {report.get('word_count', 'N/A')}")
                                    st.markdown(f"**Generated:** {report.get('generated_at', 'N/A')}")
                                    
                                    # Show metadata if available
                                    metadata = db.get_metadata(query['id'])
                                    if metadata:
                                        col1, col2 = st.columns(2)
                                        with col1:
                                            st.metric("Completeness", f"{metadata.get('data_completeness', 0):.1%}")
                                        with col2:
                                            st.metric("Confidence", f"{metadata.get('confidence_score', 0):.1%}")
                                    
                                    # Show FULL report (not truncated)
                                    content = report.get('report_content', '')
                                    st.markdown("**Full Report:**")
                                    # Display complete report without truncation
                                    st.markdown(content)
                                    
                                    # Also provide download option
                                    try:
                                        pdf_data = markdown_to_pdf(content, query['ticker'], str(query['created_at']))
                                        st.download_button(
                                            label="📥 Download PDF",
                                            data=pdf_data,
                                            file_name=f"{query['ticker']}_report_{query['id']}.pdf",
                                            mime="application/pdf",
                                            key=f"download_{query['id']}"
                                        )
                                    except:
                                        st.download_button(
                                            label="📥 Download Markdown",
                                            data=content,
                                            file_name=f"{query['ticker']}_report_{query['id']}.md",
                                            mime="text/markdown",
                                            key=f"download_md_{query['id']}"
                                        )
                else:
                    st.info("No reports stored yet. Run an analysis to see data here!")
                    
            except Exception as e:
                st.warning(f"Database not available: {str(e)[:50]}")
        
        st.markdown("---")
        
        # Features list
        st.markdown("### 🚀 Features")
        st.markdown("""
        <div class="feature-item">
            <span class="feature-icon">📈</span>
            <span class="feature-text">Real-time stock data via yfinance</span>
        </div>
        <div class="feature-item">
            <span class="feature-icon">🔍</span>
            <span class="feature-text">Automated competitor research</span>
        </div>
        <div class="feature-item">
            <span class="feature-icon">📰</span>
            <span class="feature-text">Latest news aggregation</span>
        </div>
        <div class="feature-item">
            <span class="feature-icon">🤖</span>
            <span class="feature-text">AI-powered insights</span>
        </div>
        <div class="feature-item">
            <span class="feature-icon">📄</span>
            <span class="feature-text">Professional report generation</span>
        </div>
        <div class="feature-item">
            <span class="feature-icon">💾</span>
            <span class="feature-text">Automatic database storage</span>
        </div>
        """, unsafe_allow_html=True)
        
        return ticker, company_name, analysis_type, period


def render_main_content(ticker, company_name, analysis_type, period):
    """Render the main content area."""
    
    # Header
    st.markdown("""
    <h1>🔮 AI Business Analyst</h1>
    <p style="color: #94a3b8; font-size: 1.1rem; margin-bottom: 2rem;">
        Get comprehensive business analysis powered by AI agents. Enter a stock ticker to begin.
    </p>
    """, unsafe_allow_html=True)
    
    # Analysis button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        analyze_button = st.button(
            "🚀 Start Analysis" if ticker else "Enter a Ticker to Begin",
            disabled=not ticker,
            use_container_width=True
        )
    
    # Run analysis
    if analyze_button and ticker:
        run_analysis(ticker, company_name, analysis_type, period)
    
    # Show instructions if no analysis started
    elif not st.session_state.get('report'):
        render_instructions()


def render_instructions():
    """Render getting started instructions."""
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3 style="color: #14b8a6; margin-bottom: 1rem;">📝 Step 1</h3>
            <p style="color: #94a3b8;">Enter a stock ticker symbol in the sidebar (e.g., AAPL, TSLA, MSFT)</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3 style="color: #14b8a6; margin-bottom: 1rem;">⚙️ Step 2</h3>
            <p style="color: #94a3b8;">Choose analysis type and time period for historical data</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3 style="color: #14b8a6; margin-bottom: 1rem;">🚀 Step 3</h3>
            <p style="color: #94a3b8;">Click "Start Analysis" and let AI agents do the work</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Popular tickers
    st.markdown("### 💡 Popular Analysis Targets")
    
    popular_tickers = [
        ("AAPL", "Apple Inc.", "Technology"),
        ("MSFT", "Microsoft", "Technology"),
        ("GOOGL", "Alphabet", "Technology"),
        ("AMZN", "Amazon", "E-Commerce"),
        ("TSLA", "Tesla", "Automotive"),
        ("NVDA", "NVIDIA", "Semiconductors"),
    ]
    
    cols = st.columns(6)
    for i, (ticker, name, sector) in enumerate(popular_tickers):
        with cols[i]:
            st.markdown(f"""
            <div class="metric-card" style="text-align: center; padding: 1rem;">
                <div class="metric-value" style="font-size: 1.25rem;">{ticker}</div>
                <div class="metric-label" style="font-size: 0.7rem;">{sector}</div>
            </div>
            """, unsafe_allow_html=True)


def run_analysis(ticker, company_name, analysis_type, period):
    """Run the business analysis."""
    
    # Check API keys first
    keys_ok, missing_keys = check_api_keys()
    if not keys_ok:
        st.error(f"❌ Cannot run analysis. Missing API keys: {', '.join(missing_keys)}")
        st.info("Please set the required environment variables and restart the app.")
        return
    
    # Progress container
    progress_container = st.container()
    
    with progress_container:
        st.markdown(f"""
        <div class="status-indicator">
            <div class="status-dot running"></div>
            <span style="color: #94a3b8;">Analyzing <strong style="color: #22d3ee;">{ticker}</strong>...</span>
        </div>
        """, unsafe_allow_html=True)
        
        # Progress stages
        stages = [
            "🔍 Fetching stock data...",
            "🌐 Searching for competitors...",
            "📰 Gathering news...",
            "📊 Analyzing financials...",
            "🎯 Evaluating competition...",
            "📝 Generating report..."
        ]
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            # Import crew
            from crew.business_analyst_crew import BusinessAnalystCrew
            
            # Initialize crew
            crew = BusinessAnalystCrew(verbose=False)
            
            # Simulate progress while analysis runs
            for i, stage in enumerate(stages):
                status_text.markdown(f"**{stage}**")
                progress_bar.progress((i + 1) / len(stages))
                time.sleep(0.5)  # Brief pause for visual feedback
            
            # Run actual analysis
            if analysis_type == "Full Analysis":
                report = crew.analyze_company(
                    ticker=ticker,
                    company_name=company_name if company_name else None,
                    period=period
                )
            else:
                report = crew.quick_analysis(ticker=ticker)
            
            # Complete
            progress_bar.progress(1.0)
            status_text.markdown("**✅ Analysis Complete!**")
            
            # Show database save confirmation
            try:
                from database.db_manager import DatabaseManager
                db = DatabaseManager()
                stats = db.get_stats()
                st.success(f"💾 Report saved to database! (Total reports: {stats.get('total_reports', 0)})")
            except:
                pass  # Database might not be available
            
            # Store in session state
            st.session_state['report'] = report
            st.session_state['ticker'] = ticker
            st.session_state['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
        except Exception as e:
            st.error(f"❌ Analysis failed: {str(e)}")
            st.exception(e)
            return
    
    # Display report
    if st.session_state.get('report'):
        display_report(
            st.session_state['report'],
            st.session_state['ticker'],
            st.session_state['timestamp']
        )


def markdown_to_pdf(markdown_content: str, ticker: str, timestamp: str) -> bytes:
    """
    Convert markdown content to PDF bytes using ReportLab (production-safe).
    This generates a real, standards-compliant PDF that opens in all viewers.
    """
    from io import BytesIO
    import re
    from reportlab.lib.pagesizes import A4
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.lib.colors import HexColor
    
    try:
        buffer = BytesIO()
        
        # Create PDF document
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )
        
        # Get styles
        styles = getSampleStyleSheet()
        
        # Create custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Title'],
            fontSize=20,
            textColor=HexColor('#14b8a6'),
            spaceAfter=12,
            alignment=1  # Center
        )
        
        heading1_style = ParagraphStyle(
            'CustomHeading1',
            parent=styles['Heading1'],
            fontSize=16,
            textColor=HexColor('#14b8a6'),
            spaceAfter=12,
            spaceBefore=20
        )
        
        heading2_style = ParagraphStyle(
            'CustomHeading2',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=HexColor('#22d3ee'),
            spaceAfter=10,
            spaceBefore=16
        )
        
        heading3_style = ParagraphStyle(
            'CustomHeading3',
            parent=styles['Heading3'],
            fontSize=12,
            textColor=HexColor('#64748b'),
            spaceAfter=8,
            spaceBefore=12
        )
        
        normal_style = ParagraphStyle(
            'CustomNormal',
            parent=styles['Normal'],
            fontSize=10,
            leading=14,
            spaceAfter=6
        )
        
        # Build story (content)
        story = []
        
        # Title
        title = Paragraph(f"<b>Analysis Report: {ticker}</b>", title_style)
        story.append(title)
        story.append(Spacer(1, 6))
        
        # Timestamp
        timestamp_para = Paragraph(f"<i>Generated: {timestamp}</i>", normal_style)
        story.append(timestamp_para)
        story.append(Spacer(1, 12))
        
        # Helper function to escape HTML and convert markdown
        def markdown_to_paragraph(text, style):
            """Convert markdown text to ReportLab Paragraph."""
            if not text.strip():
                return None
            
            # Escape HTML special characters
            text = text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            
            # Convert markdown bold **text** to <b>text</b>
            text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
            
            # Convert markdown italic *text* to <i>text</i> (but not if already bold)
            text = re.sub(r'(?<!\*)\*([^*]+?)\*(?!\*)', r'<i>\1</i>', text)
            
            # Convert markdown code `text` to <font face="Courier">text</font>
            text = re.sub(r'`([^`]+?)`', r'<font face="Courier">\1</font>', text)
            
            return Paragraph(text, style)
        
        # Parse markdown content line by line
        lines = markdown_content.split('\n')
        in_list = False
        
        for i, line in enumerate(lines):
            line = line.rstrip()
            
            # Empty line
            if not line.strip():
                if in_list:
                    story.append(Spacer(1, 3))
                else:
                    story.append(Spacer(1, 6))
                in_list = False
                continue
            
            # Headers
            if line.startswith('# '):
                text = line[2:].strip()
                para = markdown_to_paragraph(text, heading1_style)
                if para:
                    story.append(para)
                in_list = False
                
            elif line.startswith('## '):
                text = line[3:].strip()
                para = markdown_to_paragraph(text, heading2_style)
                if para:
                    story.append(para)
                in_list = False
                
            elif line.startswith('### '):
                text = line[4:].strip()
                para = markdown_to_paragraph(text, heading3_style)
                if para:
                    story.append(para)
                in_list = False
                
            elif line.startswith('#### '):
                text = line[5:].strip()
                para = markdown_to_paragraph(f"<b>{text}</b>", normal_style)
                if para:
                    story.append(para)
                in_list = False
                
            # Horizontal rule
            elif line.strip() == '---' or line.strip() == '***':
                story.append(Spacer(1, 12))
                in_list = False
                
            # List items
            elif line.startswith('- ') or line.startswith('* ') or line.startswith('+ '):
                text = line[2:].strip()
                para = markdown_to_paragraph(f"• {text}", normal_style)
                if para:
                    story.append(para)
                in_list = True
                
            # Numbered list
            elif re.match(r'^\d+\.\s+', line):
                text = re.sub(r'^\d+\.\s+', '', line)
                para = markdown_to_paragraph(text, normal_style)
                if para:
                    story.append(para)
                in_list = True
                
            # Regular paragraph
            else:
                para = markdown_to_paragraph(line, normal_style)
                if para:
                    story.append(para)
                in_list = False
        
        # Build PDF
        doc.build(story)
        
        # Get PDF bytes
        buffer.seek(0)
        pdf_data = buffer.getvalue()
        buffer.close()
        
        # Verify it's a valid PDF (starts with %PDF)
        if pdf_data.startswith(b'%PDF'):
            return pdf_data
        else:
            raise Exception("Generated file is not a valid PDF")
            
    except ImportError as e:
        raise Exception(f"ReportLab is required for PDF generation. Install with: pip install reportlab. Error: {e}")
    except Exception as e:
        raise Exception(f"PDF generation failed: {str(e)}")


def display_report(report, ticker, timestamp):
    """Display the analysis report."""
    
    st.markdown("---")
    
    # Report header
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f"""
        <h2 style="color: #f1f5f9; margin-bottom: 0.5rem;">
            📊 Analysis Report: {ticker}
        </h2>
        <p style="color: #64748b; font-size: 0.875rem;">
            Generated: {timestamp}
        </p>
        """, unsafe_allow_html=True)
    
    with col2:
        # Generate PDF
        try:
            pdf_data = markdown_to_pdf(report, ticker, timestamp)
            file_name = f"{ticker}_analysis_{timestamp.replace(':', '-').replace(' ', '_')}.pdf"
            
            st.download_button(
                label="📥 Download PDF",
                data=pdf_data,
                file_name=file_name,
                mime="application/pdf"
            )
        except Exception as e:
            # Fallback to markdown if PDF generation fails
            st.download_button(
                label="📥 Download Report",
                data=report,
                file_name=f"{ticker}_analysis_{timestamp.replace(':', '-').replace(' ', '_')}.md",
                mime="text/markdown"
            )
            st.warning(f"PDF generation failed, downloading as markdown: {str(e)[:50]}")
    
    # Report content - Display FULL report (not truncated)
    st.markdown("---")
    st.markdown("### 📄 Full Report")
    
    # Display full report using markdown - this ensures no truncation
    # Use a container with proper styling
    with st.container():
        st.markdown(report)


def main():
    """Main application entry point."""
    
    # Initialize session state
    if 'report' not in st.session_state:
        st.session_state['report'] = None
    
    # Render sidebar and get inputs
    ticker, company_name, analysis_type, period = render_sidebar()
    
    # Render main content
    render_main_content(ticker, company_name, analysis_type, period)


if __name__ == "__main__":
    main()

