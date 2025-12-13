"""
SQLite Database Manager
Minimal storage for logs, reports, queries, and metadata.
"""
import sqlite3
import json
from typing import Optional, List, Dict, Any
from datetime import datetime
from pathlib import Path
import os


class DatabaseManager:
    """
    Manages SQLite database operations for the Business Analyst Agent.
    
    Tables:
    1. user_queries - Core query tracking
    2. reports - Generated reports/outputs
    3. agent_logs - Minimal agent action logging
    4. analysis_metadata - Summaries and decisions
    """
    
    def __init__(self, db_path: str = "business_analyst.db"):
        """
        Initialize database manager.
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        self._init_database()
    
    def _get_connection(self) -> sqlite3.Connection:
        """Get database connection."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Return rows as dict-like objects
        return conn
    
    def _init_database(self) -> None:
        """Initialize database schema."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # Table 1: user_queries
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_queries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ticker TEXT NOT NULL,
                company_name TEXT,
                analysis_type TEXT NOT NULL,
                period TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                error_message TEXT
            )
        """)
        
        # Table 2: reports
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                query_id INTEGER NOT NULL,
                ticker TEXT NOT NULL,
                report_content TEXT NOT NULL,
                word_count INTEGER,
                generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (query_id) REFERENCES user_queries(id)
            )
        """)
        
        # Table 3: agent_logs
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS agent_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                query_id INTEGER NOT NULL,
                agent_name TEXT NOT NULL,
                action_summary TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'success',
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (query_id) REFERENCES user_queries(id)
            )
        """)
        
        # Table 4: analysis_metadata
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS analysis_metadata (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                query_id INTEGER NOT NULL,
                key_decisions TEXT NOT NULL,
                data_completeness REAL NOT NULL,
                confidence_score REAL NOT NULL,
                summary TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (query_id) REFERENCES user_queries(id)
            )
        """)
        
        # Create indexes for better query performance
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_queries_ticker ON user_queries(ticker)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_queries_created ON user_queries(created_at)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_reports_query ON reports(query_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_logs_query ON agent_logs(query_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_metadata_query ON analysis_metadata(query_id)")
        
        conn.commit()
        conn.close()
    
    # ============================================
    # USER QUERIES METHODS
    # ============================================
    
    def create_query(
        self,
        ticker: str,
        company_name: Optional[str],
        analysis_type: str,
        period: str
    ) -> int:
        """
        Create a new user query record.
        
        Returns:
            Query ID (int)
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO user_queries (ticker, company_name, analysis_type, period, status)
            VALUES (?, ?, ?, ?, 'pending')
        """, (ticker.upper(), company_name, analysis_type, period))
        
        query_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return query_id
    
    def update_query_status(
        self,
        query_id: int,
        status: str,
        error_message: Optional[str] = None
    ) -> None:
        """Update query status."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE user_queries
            SET status = ?, error_message = ?
            WHERE id = ?
        """, (status, error_message, query_id))
        
        conn.commit()
        conn.close()
    
    def get_query(self, query_id: int) -> Optional[Dict[str, Any]]:
        """Get query by ID."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM user_queries WHERE id = ?", (query_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return dict(row)
        return None
    
    # ============================================
    # REPORTS METHODS
    # ============================================
    
    def save_report(
        self,
        query_id: int,
        ticker: str,
        report_content: str,
        word_count: Optional[int] = None
    ) -> int:
        """
        Save a generated report.
        
        Returns:
            Report ID (int)
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        if word_count is None:
            word_count = len(report_content.split())
        
        cursor.execute("""
            INSERT INTO reports (query_id, ticker, report_content, word_count)
            VALUES (?, ?, ?, ?)
        """, (query_id, ticker.upper(), report_content, word_count))
        
        report_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return report_id
    
    def get_report(self, report_id: int) -> Optional[Dict[str, Any]]:
        """Get report by ID."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM reports WHERE id = ?", (report_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return dict(row)
        return None
    
    def get_reports_by_ticker(self, ticker: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent reports for a ticker."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM reports
            WHERE ticker = ?
            ORDER BY generated_at DESC
            LIMIT ?
        """, (ticker.upper(), limit))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    # ============================================
    # AGENT LOGS METHODS
    # ============================================
    
    def log_agent_action(
        self,
        query_id: int,
        agent_name: str,
        action_summary: str,
        status: str = "success"
    ) -> int:
        """
        Log an agent action (minimal logging).
        
        Args:
            query_id: Associated query ID
            agent_name: Name of the agent
            action_summary: Brief description (not full JSON)
            status: "success" or "error"
        
        Returns:
            Log ID (int)
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO agent_logs (query_id, agent_name, action_summary, status)
            VALUES (?, ?, ?, ?)
        """, (query_id, agent_name, action_summary[:500], status))  # Limit summary length
        
        log_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return log_id
    
    def get_agent_logs(self, query_id: int) -> List[Dict[str, Any]]:
        """Get all logs for a query."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM agent_logs
            WHERE query_id = ?
            ORDER BY timestamp ASC
        """, (query_id,))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    # ============================================
    # METADATA METHODS
    # ============================================
    
    def save_metadata(
        self,
        query_id: int,
        key_decisions: str,
        data_completeness: float,
        confidence_score: float,
        summary: str
    ) -> int:
        """
        Save analysis metadata.
        
        Returns:
            Metadata ID (int)
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO analysis_metadata 
            (query_id, key_decisions, data_completeness, confidence_score, summary)
            VALUES (?, ?, ?, ?, ?)
        """, (query_id, key_decisions[:1000], data_completeness, confidence_score, summary[:500]))
        
        metadata_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return metadata_id
    
    def get_metadata(self, query_id: int) -> Optional[Dict[str, Any]]:
        """Get metadata for a query."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM analysis_metadata
            WHERE query_id = ?
        """, (query_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return dict(row)
        return None
    
    # ============================================
    # UTILITY METHODS
    # ============================================
    
    def get_recent_queries(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Get recent queries."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM user_queries
            ORDER BY created_at DESC
            LIMIT ?
        """, (limit,))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    def cleanup_old_data(self, days: int = 90) -> int:
        """
        Delete data older than specified days.
        Returns number of records deleted.
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cutoff_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        from datetime import timedelta
        cutoff_date = cutoff_date - timedelta(days=days)
        
        # Delete in order (respecting foreign keys)
        deleted = 0
        
        # Delete metadata
        cursor.execute("""
            DELETE FROM analysis_metadata
            WHERE created_at < ?
        """, (cutoff_date,))
        deleted += cursor.rowcount
        
        # Delete logs
        cursor.execute("""
            DELETE FROM agent_logs
            WHERE timestamp < ?
        """, (cutoff_date,))
        deleted += cursor.rowcount
        
        # Delete reports
        cursor.execute("""
            DELETE FROM reports
            WHERE generated_at < ?
        """, (cutoff_date,))
        deleted += cursor.rowcount
        
        # Delete queries
        cursor.execute("""
            DELETE FROM user_queries
            WHERE created_at < ?
        """, (cutoff_date,))
        deleted += cursor.rowcount
        
        conn.commit()
        conn.close()
        
        return deleted
    
    def get_stats(self) -> Dict[str, Any]:
        """Get database statistics."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        stats = {}
        
        # Count records
        cursor.execute("SELECT COUNT(*) FROM user_queries")
        stats['total_queries'] = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM reports")
        stats['total_reports'] = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM agent_logs")
        stats['total_logs'] = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM analysis_metadata")
        stats['total_metadata'] = cursor.fetchone()[0]
        
        # Success rate
        cursor.execute("SELECT COUNT(*) FROM user_queries WHERE status = 'completed'")
        completed = cursor.fetchone()[0]
        stats['success_rate'] = (completed / stats['total_queries'] * 100) if stats['total_queries'] > 0 else 0
        
        conn.close()
        
        return stats

