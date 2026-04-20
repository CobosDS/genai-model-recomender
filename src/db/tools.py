"""
Tool definitions for the model selector agent.
"""
from __future__ import annotations

import json

from src.db.queries import execute_query


def query_db(sql: str) -> dict:
    """
    Execute a SELECT query against the models database.

    Args:
        sql: A valid SQLite SELECT statement.
    """
    sql = sql.strip()
    if not sql.upper().startswith("SELECT"):
        return {"error": "Only SELECT queries are allowed."}
    try:
        rows = execute_query(sql)
        return {"count": len(rows), "rows": rows}
    except Exception as e:
        return {"error": str(e)}


def set_recommendations(model_ids: list[str]) -> dict:
    """
    Declare the final recommended models in ranked order (best first, max 3).
    Call this after querying, before writing your response.

    Args:
        model_ids: Ordered list of model IDs to recommend, best first. Max 3.
    """
    return {"ok": True, "model_ids": model_ids}


# ── Tool definitions (OpenAI function calling format) ─────────────────────────

TOOL_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "query_db",
            "description": (
                "Execute a SELECT query against the models SQLite database. "
                "Returns up to 60 rows. Use this to search, filter, and compare models."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "sql": {
                        "type": "string",
                        "description": "A valid SQLite SELECT statement.",
                    }
                },
                "required": ["sql"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "set_recommendations",
            "description": (
                "Declare the final recommended models in ranked order. "
                "Call this after querying to set which model cards appear in the UI. "
                "Best match first, max 3."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "model_ids": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Ordered list of model IDs, best first. Max 3.",
                    }
                },
                "required": ["model_ids"],
            },
        },
    },
]

TOOL_DISPATCH: dict[str, callable] = {
    "query_db": query_db,
    "set_recommendations": set_recommendations,
}
