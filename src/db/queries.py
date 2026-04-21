"""
DB connection for the llm-etl models database.
"""
from __future__ import annotations

import os
import sqlite3
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

_REPO_ROOT = Path(__file__).resolve().parents[2]
_DEFAULT_DB = _REPO_ROOT / "data" / "models.db"
DB_PATH = Path(os.getenv("DB_PATH", str(_DEFAULT_DB)))

_MAX_ROWS = 60


def connect() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def execute_query(sql: str) -> list[dict]:
    """Execute a SELECT and return up to _MAX_ROWS rows as dicts."""
    conn = connect()
    try:
        cur = conn.execute(sql)
        return [dict(r) for r in cur.fetchmany(_MAX_ROWS)]
    finally:
        conn.close()
