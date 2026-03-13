from agents import SQLiteSession
from support_team_models import SupportContext
from typing import Dict, Optional
import sqlite3
import json
from datetime import datetime


class SupportSessionManager:
    """Manages persistent sessions for the support team."""

    def __init__(self, db_path: str = "support_sessions.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """Initialize the database with required tables."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Table for storing customer context
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS customer_contexts (
                customer_id TEXT PRIMARY KEY,
                context_json TEXT,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Table for storing conversation history
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS conversation_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id TEXT,
                session_id TEXT,
                message_type TEXT,
                content TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        conn.commit()
        conn.close()

    def get_session(self, customer_id: str) -> SQLiteSession:
        """Get or create a SQLite session for a customer."""
        session_id = f"support_{customer_id}"
        return SQLiteSession(session_id, self.db_path)

    def save_customer_context(self, customer_id: str, context: SupportContext):
        """Save the customer's context to persistent storage."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        context_dict = context.dict()
        context_json = json.dumps(context_dict)

        cursor.execute("""
            INSERT OR REPLACE INTO customer_contexts
            (customer_id, context_json, last_updated)
            VALUES (?, ?, ?)
        """, (customer_id, context_json, datetime.now()))

        conn.commit()
        conn.close()

    def load_customer_context(self, customer_id: str) -> Optional[SupportContext]:
        """Load the customer's context from persistent storage."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT context_json FROM customer_contexts
            WHERE customer_id = ?
        """, (customer_id,))

        row = cursor.fetchone()
        conn.close()

        if row:
            context_dict = json.loads(row[0])
            return SupportContext(**context_dict)
        return None

    def log_conversation_item(self, customer_id: str, session_id: str, message_type: str, content: str):
        """Log a conversation item to the history."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO conversation_history
            (customer_id, session_id, message_type, content, timestamp)
            VALUES (?, ?, ?, ?, ?)
        """, (customer_id, session_id, message_type, content, datetime.now()))

        conn.commit()
        conn.close()

    def get_recent_conversation_history(self, customer_id: str, limit: int = 10) -> list:
        """Get recent conversation history for a customer."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT message_type, content, timestamp
            FROM conversation_history
            WHERE customer_id = ?
            ORDER BY timestamp DESC
            LIMIT ?
        """, (customer_id, limit))

        rows = cursor.fetchall()
        conn.close()

        return [{"type": row[0], "content": row[1], "timestamp": row[2]} for row in rows]

    def clear_session(self, customer_id: str):
        """Clear a customer's session data."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Delete customer context
        cursor.execute("DELETE FROM customer_contexts WHERE customer_id = ?", (customer_id,))

        # Delete conversation history
        cursor.execute("DELETE FROM conversation_history WHERE customer_id = ?", (customer_id,))

        conn.commit()
        conn.close()


# Global session manager instance
session_manager = SupportSessionManager()