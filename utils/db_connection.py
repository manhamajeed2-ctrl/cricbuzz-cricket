"""
Database connection utilities for Cricbuzz LiveStats.
Supports SQLite (default), with easy extension to PostgreSQL/MySQL.
"""

import sqlite3
from pathlib import Path
from contextlib import contextmanager
from typing import Optional, List, Dict, Any, Tuple
import os

# Default path relative to project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DB_PATH = PROJECT_ROOT / "data" / "cricket.db"


def get_db_path() -> Path:
    """Return the database file path."""
    env_path = os.getenv("DATABASE_URL", "")
    if env_path.startswith("sqlite:///"):
        path = env_path.replace("sqlite:///", "")
        return Path(path) if Path(path).is_absolute() else PROJECT_ROOT / path
    return DEFAULT_DB_PATH


@contextmanager
def get_connection():
    """Context manager yielding a SQLite connection with row factory."""
    db_path = get_db_path()
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def execute_query(query: str, params: Optional[Tuple] = None) -> List[Dict[str, Any]]:
    """Execute a SELECT query and return list of dicts."""
    with get_connection() as conn:
        cursor = conn.execute(query, params or ())
        rows = cursor.fetchall()
        return [dict(row) for row in rows]


def execute_write(query: str, params: Optional[Tuple] = None) -> int:
    """Execute INSERT/UPDATE/DELETE and return lastrowid or affected rows."""
    with get_connection() as conn:
        cursor = conn.execute(query, params or ())
        return cursor.lastrowid or cursor.rowcount


def execute_many(query: str, params_list: List[Tuple]) -> int:
    """Execute many statements."""
    with get_connection() as conn:
        cursor = conn.executemany(query, params_list)
        return cursor.rowcount


def table_exists(table_name: str) -> bool:
    """Check if a table exists."""
    result = execute_query(
        "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
        (table_name,),
    )
    return len(result) > 0


def get_table_names() -> List[str]:
    """Return all user table names."""
    rows = execute_query(
        "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
    )
    return [r["name"] for r in rows]
