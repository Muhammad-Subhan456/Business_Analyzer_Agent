# Database Schema Documentation

## Overview

The Business Analyst Agent uses SQLite to store minimal but essential data:
- User queries
- Generated reports
- Agent action logs
- Analysis metadata

## Database File

- **Location**: `business_analyst.db` (in project root)
- **Type**: SQLite 3

## Tables

### 1. `user_queries`

Stores core query information.

| Column | Type | Description |
|-------|------|-------------|
| `id` | INTEGER | Primary key, auto-increment |
| `ticker` | TEXT | Stock ticker symbol (e.g., "AAPL") |
| `company_name` | TEXT | Company name (nullable) |
| `analysis_type` | TEXT | "Full Analysis" or "Quick Analysis" |
| `period` | TEXT | Historical period ("6mo", "1y", "2y", "5y") |
| `status` | TEXT | "pending", "processing", "completed", "failed" |
| `created_at` | TIMESTAMP | Query creation timestamp |
| `error_message` | TEXT | Error message if failed (nullable) |

**Indexes:**
- `idx_queries_ticker` on `ticker`
- `idx_queries_created` on `created_at`

---

### 2. `reports`

Stores generated analysis reports.

| Column | Type | Description |
|-------|------|-------------|
| `id` | INTEGER | Primary key, auto-increment |
| `query_id` | INTEGER | Foreign key to `user_queries.id` |
| `ticker` | TEXT | Stock ticker symbol |
| `report_content` | TEXT | Full report content (markdown) |
| `word_count` | INTEGER | Number of words in report |
| `generated_at` | TIMESTAMP | Report generation timestamp |

**Indexes:**
- `idx_reports_query` on `query_id`

---

### 3. `agent_logs`

Minimal logging of agent actions (not full JSON, just summaries).

| Column | Type | Description |
|-------|------|-------------|
| `id` | INTEGER | Primary key, auto-increment |
| `query_id` | INTEGER | Foreign key to `user_queries.id` |
| `agent_name` | TEXT | Name of the agent (e.g., "Stock Data Agent") |
| `action_summary` | TEXT | Brief description (max 500 chars) |
| `status` | TEXT | "success" or "error" |
| `timestamp` | TIMESTAMP | Action timestamp |

**Indexes:**
- `idx_logs_query` on `query_id`

---

### 4. `analysis_metadata`

Stores analysis summaries and key decisions.

| Column | Type | Description |
|-------|------|-------------|
| `id` | INTEGER | Primary key, auto-increment |
| `query_id` | INTEGER | Foreign key to `user_queries.id` |
| `key_decisions` | TEXT | Summarized agent decisions (max 1000 chars) |
| `data_completeness` | REAL | Completeness score (0.0-1.0) |
| `confidence_score` | REAL | Confidence score (0.0-1.0) |
| `summary` | TEXT | Brief analysis summary (max 500 chars) |
| `created_at` | TIMESTAMP | Metadata creation timestamp |

**Indexes:**
- `idx_metadata_query` on `query_id`

---

## Usage Examples

### Python API

```python
from database.db_manager import DatabaseManager

# Initialize
db = DatabaseManager()

# Create a query
query_id = db.create_query(
    ticker="AAPL",
    company_name="Apple Inc.",
    analysis_type="Full Analysis",
    period="1y"
)

# Log agent action
db.log_agent_action(
    query_id=query_id,
    agent_name="Stock Data Agent",
    action_summary="Fetched stock data successfully"
)

# Save report
report_id = db.save_report(
    query_id=query_id,
    ticker="AAPL",
    report_content="# Report content...",
    word_count=1200
)

# Save metadata
metadata_id = db.save_metadata(
    query_id=query_id,
    key_decisions="Key insights...",
    data_completeness=0.85,
    confidence_score=0.90,
    summary="Brief summary..."
)

# Get recent queries
recent = db.get_recent_queries(limit=10)

# Get database stats
stats = db.get_stats()
print(stats)
```

### SQL Queries

```sql
-- Get all reports for a ticker
SELECT * FROM reports WHERE ticker = 'AAPL' ORDER BY generated_at DESC;

-- Get query with all related data
SELECT 
    q.*,
    r.report_content,
    m.summary,
    m.confidence_score
FROM user_queries q
LEFT JOIN reports r ON q.id = r.query_id
LEFT JOIN analysis_metadata m ON q.id = m.query_id
WHERE q.ticker = 'AAPL'
ORDER BY q.created_at DESC;

-- Get agent logs for a query
SELECT * FROM agent_logs WHERE query_id = 1 ORDER BY timestamp ASC;

-- Get success rate
SELECT 
    COUNT(*) as total,
    SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) as completed,
    ROUND(100.0 * SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) / COUNT(*), 2) as success_rate
FROM user_queries;
```

## Data Retention

The database includes a cleanup function to remove old data:

```python
# Delete data older than 90 days
deleted_count = db.cleanup_old_data(days=90)
```

## Storage Optimization

- **Minimal logging**: Only key agent actions, not full tool outputs
- **Text limits**: Summaries and decisions are truncated to prevent bloat
- **Indexes**: Added on frequently queried columns
- **Foreign keys**: Proper relationships for data integrity

## Notes

- Database is created automatically on first use
- All timestamps are in UTC
- Text fields have reasonable length limits to prevent excessive storage
- Reports are stored as full text (they are the main output)

