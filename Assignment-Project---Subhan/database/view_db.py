"""
Simple script to view database contents.
Usage: python database/view_db.py
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from database.db_manager import DatabaseManager
import json


def print_table(data, title):
    """Print table data in a readable format."""
    if not data:
        print(f"\n{title}: No data")
        return
    
    print(f"\n{'='*60}")
    print(f"{title} ({len(data)} records)")
    print('='*60)
    
    for i, row in enumerate(data, 1):
        print(f"\n[{i}]")
        for key, value in row.items():
            if isinstance(value, str) and len(value) > 100:
                value = value[:100] + "..."
            print(f"  {key}: {value}")


def main():
    """Main function."""
    db = DatabaseManager()
    
    print("📊 Business Analyst Database Viewer")
    print("="*60)
    
    # Get stats
    stats = db.get_stats()
    print("\n📈 Database Statistics:")
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    # Get recent queries
    queries = db.get_recent_queries(limit=10)
    print_table(queries, "Recent Queries")
    
    # Show reports for each query
    if queries:
        print("\n" + "="*60)
        print("Reports")
        print("="*60)
        
        for query in queries[:3]:  # Show first 3
            query_id = query['id']
            ticker = query['ticker']
            
            # Get reports for this ticker
            reports = db.get_reports_by_ticker(ticker, limit=1)
            report = reports[0] if reports else None
            if report:
                print(f"\n📄 Report for {ticker} (Query #{query_id}):")
                print(f"  Word Count: {report.get('word_count', 'N/A')}")
                print(f"  Generated: {report.get('generated_at', 'N/A')}")
                content_preview = report.get('report_content', '')[:200]
                print(f"  Preview: {content_preview}...")
            
            metadata = db.get_metadata(query_id)
            if metadata:
                print(f"\n📊 Metadata for {ticker}:")
                print(f"  Completeness: {metadata.get('data_completeness', 0):.2%}")
                print(f"  Confidence: {metadata.get('confidence_score', 0):.2%}")
                summary = metadata.get('summary', '')[:150]
                print(f"  Summary: {summary}...")
            
            logs = db.get_agent_logs(query_id)
            if logs:
                print(f"\n📝 Agent Logs ({len(logs)} actions):")
                for log in logs[:5]:  # Show first 5
                    print(f"  - {log.get('agent_name', 'Unknown')}: {log.get('action_summary', '')[:60]}")


if __name__ == "__main__":
    main()

