# Testing Guide: Database & Pydantic Models

## 🧪 Quick Testing

### 1. Test Everything (Recommended)

Run the comprehensive test script:

```bash
python test_implementation.py
```

This will test:
- ✅ Pydantic validation models
- ✅ Database operations
- ✅ Integration between both
- ✅ Error handling

**Expected Output:**
```
🚀 TESTING DATABASE & PYDANTIC MODELS
🧪 Testing Pydantic Models
✅ ReportValidationModel created successfully!
✅ AnalysisMetadataModel created successfully!
✅ All Pydantic model tests passed!

🗄️  Testing Database Operations
✅ Query created with ID: 1
✅ Logged 2 agent actions
✅ Report saved with ID: 1
✅ All database tests passed!

📊 TEST SUMMARY
Pydantic Models: ✅ PASSED
Database: ✅ PASSED
Integration: ✅ PASSED

🎉 All tests passed!
```

---

## 📊 Viewing Database Data

### Option 1: Simple Viewer (Recommended)

```bash
python view_database.py
```

**Features:**
- View all queries, reports, logs, and metadata
- See statistics
- View by ticker
- Interactive menu

**Example Output:**
```
📊 BUSINESS ANALYST DATABASE VIEWER

📈 Database Statistics:
   Total Queries: 5
   Total Reports: 5
   Success Rate: 100.0%

📋 Recent Queries (5 found)

[1] Query ID: 1
    Ticker: AAPL
    Company: Apple Inc.
    Type: Full Analysis
    Status: completed
    Created: 2025-01-15 10:30:00
    
    📄 Report:
       ID: 1
       Word Count: 1200
       Preview: # Apple Inc. (AAPL) - Business Analysis Report...
    
    📊 Metadata:
       Completeness: 85.0%
       Confidence: 90.0%
```

### Option 2: Interactive Menu

```bash
python view_database.py --interactive
```

This gives you a menu:
```
📊 DATABASE VIEWER MENU
Options:
  1. View all data
  2. View by ticker
  3. View statistics
  4. Exit
```

### Option 3: View Specific Ticker

```bash
python view_database.py --ticker AAPL
```

---

## 🔍 Manual Testing

### Test Pydantic Models Only

```python
from models.validation_models import ReportValidationModel, AnalysisMetadataModel

# Test report validation
report = ReportValidationModel(
    ticker="AAPL",
    report_content="# Test Report\n## Executive Summary\nContent...",
    report_type="Full Analysis"
)

print(f"Completeness: {report.completeness_score:.2%}")
print(f"Structure: {report.structure_score:.2%}")
```

### Test Database Only

```python
from database.db_manager import DatabaseManager

db = DatabaseManager()

# Create query
query_id = db.create_query("AAPL", "Apple Inc.", "Full Analysis", "1y")
print(f"Created query: {query_id}")

# Save report
report_id = db.save_report(
    query_id=query_id,
    ticker="AAPL",
    report_content="# Test Report...",
    word_count=100
)
print(f"Saved report: {report_id}")

# Get statistics
stats = db.get_stats()
print(stats)
```

---

## 🗄️ View Database with SQLite Browser

### Option 1: Command Line (sqlite3)

```bash
# Windows (if sqlite3 is installed)
sqlite3 business_analyst.db

# Then run SQL queries:
.tables
SELECT * FROM user_queries;
SELECT * FROM reports;
SELECT * FROM agent_logs;
SELECT * FROM analysis_metadata;
```

### Option 2: GUI Tools

**DB Browser for SQLite** (Free):
1. Download: https://sqlitebrowser.org/
2. Open `business_analyst.db`
3. Browse tables and data

**VS Code Extension**:
1. Install "SQLite Viewer" extension
2. Open `business_analyst.db`
3. View tables in sidebar

---

## 📝 Test Individual Components

### Test Report Validation

```python
from models.validation_models import ReportValidationModel

# Valid report
report = ReportValidationModel(
    ticker="AAPL",
    company_name="Apple Inc.",
    report_content="# Report\n## Executive Summary\nContent here...",
    report_type="Full Analysis"
)

# Check scores
print(f"Completeness: {report.completeness_score}")
print(f"Structure: {report.structure_score}")
print(f"Sections: {report.sections_found}")
```

### Test Metadata Validation

```python
from models.validation_models import AnalysisMetadataModel

metadata = AnalysisMetadataModel(
    ticker="AAPL",
    summary="Apple shows strong performance...",
    key_decisions="Financial Analyst: Strong profitability.",
    data_completeness=0.85,
    confidence_score=0.90
)

print(f"Quality: {metadata.calculate_overall_quality():.2%}")
```

### Test Database Operations

```python
from database.db_manager import DatabaseManager

db = DatabaseManager()

# Create
query_id = db.create_query("TSLA", "Tesla", "Full Analysis", "1y")

# Log
db.log_agent_action(query_id, "Stock Agent", "Fetched data")

# Save
db.save_report(query_id, "TSLA", "# Report...", 500)
db.save_metadata(query_id, "Decisions...", 0.8, 0.9, "Summary...")

# Retrieve
query = db.get_query(query_id)
reports = db.get_reports_by_ticker("TSLA")
stats = db.get_stats()
```

---

## 🧪 Integration Test (Real Workflow)

Test the full integration:

```python
from crew.business_analyst_crew import BusinessAnalystCrew

# This will automatically:
# 1. Create query in database
# 2. Log agent actions
# 3. Validate report
# 4. Store report and metadata

crew = BusinessAnalystCrew(verbose=True)
report = crew.analyze_company("AAPL", period="1y")

# Check database
from database.db_manager import DatabaseManager
db = DatabaseManager()
recent = db.get_recent_queries(limit=1)
print(f"Last query: {recent[0]}")
```

---

## 🔧 Troubleshooting

### Database Not Found

If you see "database not found", the database is created automatically on first use. Run:

```python
from database.db_manager import DatabaseManager
db = DatabaseManager()  # Creates business_analyst.db
```

### Import Errors

Make sure you're in the project root:

```bash
cd "Assignment-Project---Subhan"
python test_implementation.py
```

### Validation Errors

If validation fails, check:
- Report content is at least 100 characters
- Ticker is 1-10 characters
- Report type is "Full Analysis" or "Quick Analysis"

---

## 📊 Expected Database Structure

After running tests, you should see:

```
business_analyst.db
├── user_queries (queries table)
├── reports (reports table)
├── agent_logs (logs table)
└── analysis_metadata (metadata table)
```

Check with:
```python
from database.db_manager import DatabaseManager
db = DatabaseManager()
stats = db.get_stats()
print(stats)
```

---

## ✅ Quick Checklist

- [ ] Run `python test_implementation.py` - All tests pass
- [ ] Run `python view_database.py` - Can see data
- [ ] Run actual analysis - Data is stored
- [ ] Check `business_analyst.db` exists
- [ ] Verify reports are validated
- [ ] Check metadata scores are calculated

---

## 🎯 Next Steps

1. **Run tests**: `python test_implementation.py`
2. **View data**: `python view_database.py`
3. **Run real analysis**: Use Streamlit app or crew directly
4. **Check database**: View stored reports and metadata

Happy testing! 🚀

