"""
View Database Contents - Simple GUI
Shows all stored data in the database.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from database.db_manager import DatabaseManager
from datetime import datetime


def format_timestamp(ts):
    """Format timestamp for display."""
    if isinstance(ts, str):
        return ts
    return ts.strftime("%Y-%m-%d %H:%M:%S") if ts else "N/A"


def print_section(title, char="="):
    """Print section header."""
    print(f"\n{char * 70}")
    print(f"{title}")
    print(f"{char * 70}")


def view_all_data():
    """View all data in the database."""
    db = DatabaseManager()
    
    print_section("📊 BUSINESS ANALYST DATABASE VIEWER", "=")
    
    # Get statistics
    stats = db.get_stats()
    print("\n📈 Database Statistics:")
    print(f"   Total Queries: {stats.get('total_queries', 0)}")
    print(f"   Total Reports: {stats.get('total_reports', 0)}")
    print(f"   Total Logs: {stats.get('total_logs', 0)}")
    print(f"   Total Metadata: {stats.get('total_metadata', 0)}")
    print(f"   Success Rate: {stats.get('success_rate', 0):.1f}%")
    
    # Get recent queries
    queries = db.get_recent_queries(limit=20)
    
    if not queries:
        print_section("⚠️  No Data Found", "-")
        print("The database is empty. Run an analysis first!")
        return
    
    print_section(f"📋 Recent Queries ({len(queries)} found)", "-")
    
    for i, query in enumerate(queries, 1):
        print(f"\n[{i}] Query ID: {query['id']}")
        print(f"    Ticker: {query['ticker']}")
        print(f"    Company: {query.get('company_name', 'N/A')}")
        print(f"    Type: {query['analysis_type']}")
        print(f"    Period: {query['period']}")
        print(f"    Status: {query['status']}")
        print(f"    Created: {format_timestamp(query['created_at'])}")
        
        if query.get('error_message'):
            print(f"    ❌ Error: {query['error_message'][:100]}")
        
        query_id = query['id']
        
        # Get related report
        reports = db.get_reports_by_ticker(query['ticker'], limit=1)
        report = None
        for r in reports:
            if r.get('query_id') == query_id:
                report = r
                break
        
        if report:
            print(f"\n    📄 Report:")
            print(f"       ID: {report['id']}")
            print(f"       Word Count: {report.get('word_count', 'N/A')}")
            print(f"       Generated: {format_timestamp(report.get('generated_at'))}")
            content_preview = report.get('report_content', '')[:150].replace('\n', ' ')
            print(f"       Preview: {content_preview}...")
        
        # Get metadata
        metadata = db.get_metadata(query_id)
        if metadata:
            print(f"\n    📊 Metadata:")
            print(f"       Completeness: {metadata.get('data_completeness', 0):.1%}")
            print(f"       Confidence: {metadata.get('confidence_score', 0):.1%}")
            summary = metadata.get('summary', '')[:100]
            print(f"       Summary: {summary}...")
            decisions = metadata.get('key_decisions', '')[:100]
            print(f"       Decisions: {decisions}...")
        
        # Get agent logs
        logs = db.get_agent_logs(query_id)
        if logs:
            print(f"\n    📝 Agent Logs ({len(logs)} actions):")
            for log in logs[:3]:  # Show first 3
                status_icon = "✅" if log.get('status') == 'success' else "❌"
                print(f"       {status_icon} {log.get('agent_name', 'Unknown')}: {log.get('action_summary', '')[:60]}")
            if len(logs) > 3:
                print(f"       ... and {len(logs) - 3} more")
        
        print("-" * 70)


def view_by_ticker(ticker: str):
    """View data for a specific ticker."""
    db = DatabaseManager()
    
    print_section(f"📊 Data for {ticker.upper()}", "=")
    
    reports = db.get_reports_by_ticker(ticker.upper(), limit=10)
    
    if not reports:
        print(f"\n⚠️  No reports found for {ticker.upper()}")
        return
    
    print(f"\nFound {len(reports)} report(s):\n")
    
    for i, report in enumerate(reports, 1):
        print(f"[{i}] Report ID: {report['id']}")
        print(f"    Query ID: {report.get('query_id', 'N/A')}")
        print(f"    Word Count: {report.get('word_count', 'N/A')}")
        print(f"    Generated: {format_timestamp(report.get('generated_at'))}")
        print(f"\n    Content Preview:")
        content = report.get('report_content', '')
        preview = content[:300] if len(content) > 300 else content
        print(f"    {preview}...")
        
        # Get query info
        query_id = report.get('query_id')
        if query_id:
            query = db.get_query(query_id)
            if query:
                print(f"\n    Query Info:")
                print(f"       Type: {query.get('analysis_type', 'N/A')}")
                print(f"       Period: {query.get('period', 'N/A')}")
                print(f"       Status: {query.get('status', 'N/A')}")
        
        print("-" * 70)


def interactive_menu():
    """Interactive menu for viewing database."""
    while True:
        print_section("📊 DATABASE VIEWER MENU", "=")
        print("\nOptions:")
        print("  1. View all data")
        print("  2. View by ticker")
        print("  3. View statistics")
        print("  4. Exit")
        
        choice = input("\nEnter choice (1-4): ").strip()
        
        if choice == "1":
            view_all_data()
        elif choice == "2":
            ticker = input("Enter ticker symbol: ").strip().upper()
            if ticker:
                view_by_ticker(ticker)
        elif choice == "3":
            db = DatabaseManager()
            stats = db.get_stats()
            print_section("📈 Database Statistics", "-")
            for key, value in stats.items():
                print(f"  {key}: {value}")
        elif choice == "4":
            print("\n👋 Goodbye!")
            break
        else:
            print("\n❌ Invalid choice. Please try again.")


def main():
    """Main function."""
    import argparse
    
    parser = argparse.ArgumentParser(description="View Business Analyst Database")
    parser.add_argument("--ticker", "-t", help="View data for specific ticker")
    parser.add_argument("--interactive", "-i", action="store_true", help="Interactive menu")
    
    args = parser.parse_args()
    
    if args.interactive:
        interactive_menu()
    elif args.ticker:
        view_by_ticker(args.ticker)
    else:
        view_all_data()


if __name__ == "__main__":
    main()

