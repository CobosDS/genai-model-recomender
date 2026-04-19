"""
Typed query functions over data/models.db.
These are the building blocks for agent tools.
"""
from __future__ import annotations

import json
import os
import sqlite3
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv

load_dotenv()

_REPO_ROOT = Path(__file__).resolve().parents[2]
DB_PATH = Path(os.getenv("DB_PATH", str(_REPO_ROOT / "data" / "models.db")))


def connect() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


@dataclass
class ModelRow:
    model_id: str
    name: str | None
    provider: str | None
    family: str | None
    is_open_source: bool
    model_category: str | None
    context_window: int | None
    parameter_count_b: float | None
    active_parameters_b: float | None
    input_modalities: list[str]
    output_modalities: list[str]
    capabilities: list[str]
    languages: list[str]
    license: str | None
    commercial_use: str | None
    description: str | None
    strengths: list[str]
    use_cases: list[str]
    ideal_for: str | None
    # pricing (joined)
    input_per_1m: float | None = None
    output_per_1m: float | None = None
    cached_input_per_1m: float | None = None
    batch_input_per_1m: float | None = None
    # benchmarks (joined as list)
    benchmarks: list[dict] = field(default_factory=list)


def _row_to_model(row: sqlite3.Row, benchmarks: list[dict] | None = None) -> ModelRow:
    return ModelRow(
        model_id=row["model_id"],
        name=row["name"],
        provider=row["provider"],
        family=row["family"],
        is_open_source=bool(row["is_open_source"]),
        model_category=row["model_category"],
        context_window=row["context_window"],
        parameter_count_b=row["parameter_count_b"],
        active_parameters_b=row["active_parameters_b"],
        input_modalities=json.loads(row["input_modalities"] or "[]"),
        output_modalities=json.loads(row["output_modalities"] or "[]"),
        capabilities=json.loads(row["capabilities"] or "[]"),
        languages=json.loads(row["languages"] or "[]"),
        license=row["license"],
        commercial_use=row["commercial_use"],
        description=row["description"],
        strengths=json.loads(row["strengths"] or "[]"),
        use_cases=json.loads(row["use_cases"] or "[]"),
        ideal_for=row["ideal_for"],
        input_per_1m=row["input_per_1m"],
        output_per_1m=row["output_per_1m"],
        cached_input_per_1m=row["cached_input_per_1m"],
        batch_input_per_1m=row["batch_input_per_1m"],
        benchmarks=benchmarks or [],
    )


def _get_benchmarks(conn: sqlite3.Connection, model_ids: list[str]) -> dict[str, list[dict]]:
    if not model_ids:
        return {}
    placeholders = ",".join("?" * len(model_ids))
    rows = conn.execute(
        f"SELECT model_id, name, value, metric FROM benchmark_scores WHERE model_id IN ({placeholders})",
        model_ids,
    ).fetchall()
    result: dict[str, list[dict]] = {mid: [] for mid in model_ids}
    for r in rows:
        result[r["model_id"]].append({"name": r["name"], "value": r["value"], "metric": r["metric"]})
    return result


def search_models(
    *,
    category: str = "llm",
    capabilities: list[str] | None = None,
    min_context: int | None = None,
    max_input_price: float | None = None,
    max_output_price: float | None = None,
    is_open_source: bool | None = None,
    provider: str | None = None,
    limit: int = 20,
    conn: sqlite3.Connection | None = None,
) -> list[ModelRow]:
    """
    Filter models by structured criteria.
    capabilities is AND-based: all listed caps must be present.
    """
    _conn = conn or connect()
    try:
        conditions = ["m.model_category = ?"]
        params: list = [category]

        if min_context is not None:
            conditions.append("m.context_window >= ?")
            params.append(min_context)

        if max_input_price is not None:
            conditions.append("(p.input_per_1m IS NOT NULL AND p.input_per_1m <= ?)")
            params.append(max_input_price)

        if max_output_price is not None:
            conditions.append("(p.output_per_1m IS NOT NULL AND p.output_per_1m <= ?)")
            params.append(max_output_price)

        if is_open_source is not None:
            conditions.append("m.is_open_source = ?")
            params.append(int(is_open_source))

        if provider is not None:
            conditions.append("LOWER(m.provider) = LOWER(?)")
            params.append(provider)

        for cap in capabilities or []:
            conditions.append("m.capabilities LIKE ?")
            params.append(f'%"{cap}"%')

        where = " AND ".join(conditions)
        rows = _conn.execute(
            f"""
            SELECT m.*, p.input_per_1m, p.output_per_1m, p.cached_input_per_1m, p.batch_input_per_1m
            FROM models m
            LEFT JOIN pricing p ON m.model_id = p.model_id
            WHERE {where}
            ORDER BY m.context_window DESC NULLS LAST
            LIMIT ?
            """,
            params + [limit],
        ).fetchall()

        model_ids = [r["model_id"] for r in rows]
        bench_map = _get_benchmarks(_conn, model_ids)
        return [_row_to_model(r, bench_map[r["model_id"]]) for r in rows]
    finally:
        if conn is None:
            _conn.close()


def get_model(model_id: str, *, conn: sqlite3.Connection | None = None) -> ModelRow | None:
    """Fetch a single model with pricing and benchmarks."""
    _conn = conn or connect()
    try:
        row = _conn.execute(
            """
            SELECT m.*, p.input_per_1m, p.output_per_1m, p.cached_input_per_1m, p.batch_input_per_1m
            FROM models m
            LEFT JOIN pricing p ON m.model_id = p.model_id
            WHERE m.model_id = ?
            """,
            (model_id,),
        ).fetchone()
        if not row:
            return None
        bench = _get_benchmarks(_conn, [model_id]).get(model_id, [])
        return _row_to_model(row, bench)
    finally:
        if conn is None:
            _conn.close()


def compare_models(model_ids: list[str], *, conn: sqlite3.Connection | None = None) -> list[ModelRow]:
    """Fetch multiple models by ID, preserving order."""
    _conn = conn or connect()
    try:
        placeholders = ",".join("?" * len(model_ids))
        rows = _conn.execute(
            f"""
            SELECT m.*, p.input_per_1m, p.output_per_1m, p.cached_input_per_1m, p.batch_input_per_1m
            FROM models m
            LEFT JOIN pricing p ON m.model_id = p.model_id
            WHERE m.model_id IN ({placeholders})
            """,
            model_ids,
        ).fetchall()
        row_map = {r["model_id"]: r for r in rows}
        bench_map = _get_benchmarks(_conn, model_ids)
        return [
            _row_to_model(row_map[mid], bench_map.get(mid, []))
            for mid in model_ids
            if mid in row_map
        ]
    finally:
        if conn is None:
            _conn.close()


def list_providers(*, conn: sqlite3.Connection | None = None) -> list[str]:
    _conn = conn or connect()
    try:
        rows = _conn.execute(
            "SELECT DISTINCT provider FROM models WHERE provider IS NOT NULL ORDER BY provider"
        ).fetchall()
        return [r["provider"] for r in rows]
    finally:
        if conn is None:
            _conn.close()
