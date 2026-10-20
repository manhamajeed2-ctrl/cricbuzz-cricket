"""
Database connection utilities for Cricbuzz LiveStats.
Works locally and on Streamlit Cloud (uses a writable copy under /tmp when needed).
"""

import sqlite3
import shutil
import os
from pathlib import Path
from contextlib import contextmanager
from typing import Optional, List, Dict, Any, Tuple

# Project root = parent of utils/
PROJECT_ROOT = Path(__file__).resolve().parent.parent
BUNDLED_DB = PROJECT_ROOT / "data" / "cricket.db"
SCHEMA_PATH = PROJECT_ROOT / "sql" / "schema.sql"

# On Streamlit Cloud the repo filesystem is often read-only / ephemeral.
# Prefer a writable location under /tmp when we cannot write next to the code.
TMP_DB = Path("/tmp") / "cricbuzz_livestats_cricket.db"


def _can_write(path: Path) -> bool:
    """Return True if we can create/write a file in path's parent."""
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        test = path.parent / ".write_test"
        test.write_text("ok")
        test.unlink(missing_ok=True)
        return True
    except Exception:
        return False


def get_db_path() -> Path:
    """
    Resolve the SQLite file to use.
    Priority:
      1. DATABASE_URL env (sqlite:///...)
      2. Writable project data/cricket.db
      3. /tmp copy (Streamlit Cloud safe)
    """
    env_path = os.getenv("DATABASE_URL", "").strip()
    if env_path.startswith("sqlite:///"):
        raw = env_path.replace("sqlite:///", "", 1)
        p = Path(raw)
        return p if p.is_absolute() else PROJECT_ROOT / p

    # Prefer bundled location if writable
    if _can_write(BUNDLED_DB):
        return BUNDLED_DB

    return TMP_DB


def _ensure_database():
    """
    Make sure a usable cricket.db exists.
    - If target missing and bundled exists → copy
    - If still missing / empty → create minimal schema (user should run init_db.py for full data)
    """
    db_path = get_db_path()

    # Copy from repo if we have a good source and target is missing or empty
    if BUNDLED_DB.exists() and BUNDLED_DB.stat().st_size > 10_000:
        if not db_path.exists() or db_path.stat().st_size < 10_000:
            try:
                db_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(BUNDLED_DB, db_path)
            except Exception:
                pass

    if not db_path.exists() or db_path.stat().st_size < 1000:
        # Last resort: create empty schema so the app doesn't crash
        db_path.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(str(db_path))
        try:
            if SCHEMA_PATH.exists():
                conn.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))
            conn.commit()
        finally:
            conn.close()


@contextmanager
def get_connection():
    """Context manager yielding a SQLite connection with row factory."""
    _ensure_database()
    db_path = get_db_path()
    # uri=True + mode=rwc helps on some restricted FS; timeout avoids lock errors
    conn = sqlite3.connect(str(db_path), timeout=30)
    conn.row_factory = sqlite3.Row
    try:
        conn.execute("PRAGMA foreign_keys = ON")
        conn.execute("PRAGMA journal_mode = DELETE")  # more portable than WAL on read-only hosts
    except Exception:
        pass
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


def ensure_seeded() -> bool:
    """
    Return True if core tables have data.
    Useful for showing a friendly message on Streamlit Cloud.
    """
    try:
        n = execute_query("SELECT COUNT(*) AS c FROM players")
        return bool(n and n[0]["c"] > 0)
    except Exception:
        return False
