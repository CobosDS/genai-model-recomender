"""
Tool definitions for the model selector agent.
Each function is callable by the LLM and returns a JSON-serializable dict.
"""
from __future__ import annotations

from src.db import queries


def search_models(
    category: str = "llm",
    capabilities: list[str] | None = None,
    min_context: int | None = None,
    max_input_price: float | None = None,
    is_open_source: bool | None = None,
    provider: str | None = None,
    limit: int = 20,
) -> dict:
    """
    Search models by structured criteria.

    Args:
        category: Model type — "llm", "embedding", "image_gen", "tts". Default "llm".
        capabilities: Required capabilities. Options: reasoning, function_calling, structured_output, code, moe, fine_tuning, vision, audio_input.
        min_context: Minimum context window in tokens, e.g. 128000.
        max_input_price: Max input price per 1M tokens in USD, e.g. 5.0. Use 0.0 for free/open-source models.
        is_open_source: True to restrict to open-source models only.
        provider: Filter by provider name, e.g. "Anthropic", "OpenAI".
        limit: Max results to return (default 20).
    """
    results = queries.search_models(
        category=category,
        capabilities=capabilities,
        min_context=min_context,
        max_input_price=max_input_price,
        is_open_source=is_open_source,
        provider=provider,
        limit=limit,
    )
    return {
        "count": len(results),
        "models": [_model_summary(m) for m in results],
    }


def get_model_details(model_id: str) -> dict:
    """
    Get full details for a specific model including benchmarks.

    Args:
        model_id: Exact model ID, e.g. "claude-sonnet-4-6".
    """
    m = queries.get_model(model_id)
    if not m:
        return {"error": f"Model '{model_id}' not found"}
    return _model_full(m)


def compare_models(model_ids: list[str]) -> dict:
    """
    Compare multiple models side by side.

    Args:
        model_ids: List of model IDs to compare, e.g. ["gpt-4o", "claude-sonnet-4-6"].
    """
    results = queries.compare_models(model_ids)
    not_found = [mid for mid in model_ids if not any(m.model_id == mid for m in results)]
    return {
        "models": [_model_full(m) for m in results],
        "not_found": not_found,
    }


def list_providers() -> dict:
    """List all available providers in the database."""
    return {"providers": queries.list_providers()}


def set_recommendations(model_ids: list[str]) -> dict:
    """
    Declare the final recommended models in ranked order (best first).
    Call this after searching to set which models appear as cards in the UI.

    Args:
        model_ids: Ordered list of model IDs to recommend, best first. Max 3.
    """
    return {"ok": True, "model_ids": model_ids}


# ── Serialization helpers ─────────────────────────────────────────────────────

def _model_summary(m: queries.ModelRow) -> dict:
    return {
        "model_id": m.model_id,
        "name": m.name,
        "provider": m.provider,
        "family": m.family,
        "context_window": m.context_window,
        "input_per_1m": m.input_per_1m,
        "output_per_1m": m.output_per_1m,
        "capabilities": m.capabilities,
        "is_open_source": m.is_open_source,
    }


def _model_full(m: queries.ModelRow) -> dict:
    return {
        **_model_summary(m),
        "description": m.description,
        "strengths": m.strengths,
        "use_cases": m.use_cases,
        "ideal_for": m.ideal_for,
        "input_modalities": m.input_modalities,
        "output_modalities": m.output_modalities,
        "parameter_count_b": m.parameter_count_b,
        "cached_input_per_1m": m.cached_input_per_1m,
        "benchmarks": m.benchmarks,
    }


# ── Tool definitions for the LLM (OpenAI function calling format) ─────────────

TOOL_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "search_models",
            "description": "Search and filter AI models by structured criteria like price, context window, capabilities, or provider.",
            "parameters": {
                "type": "object",
                "properties": {
                    "category": {
                        "type": "string",
                        "enum": ["llm", "embedding", "image_gen", "tts", "realtime"],
                        "description": "Model category. Default: llm.",
                    },
                    "capabilities": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Required capabilities. Options: reasoning, function_calling, structured_output, code, moe, fine_tuning, vision, audio_input.",
                    },
                    "min_context": {
                        "type": "integer",
                        "description": "Minimum context window in tokens.",
                    },
                    "max_input_price": {
                        "type": "number",
                        "description": "Max input price per 1M tokens in USD. Use 0.0 for free/open-source models (gratis, cero euros, sin coste). Use 1.0 for cheap. Use 5.0 for mid-range.",
                    },
                    "is_open_source": {
                        "type": "boolean",
                        "description": "Restrict to open-source models.",
                    },
                    "provider": {
                        "type": "string",
                        "description": "Filter by provider name.",
                    },
                },
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_model_details",
            "description": "Get full details for a specific model including benchmarks, strengths, and use cases.",
            "parameters": {
                "type": "object",
                "properties": {
                    "model_id": {
                        "type": "string",
                        "description": "Exact model ID, e.g. 'claude-sonnet-4-6'.",
                    }
                },
                "required": ["model_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "compare_models",
            "description": "Compare multiple models side by side.",
            "parameters": {
                "type": "object",
                "properties": {
                    "model_ids": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of model IDs to compare.",
                    }
                },
                "required": ["model_ids"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "list_providers",
            "description": "List all available providers in the database.",
            "parameters": {"type": "object", "properties": {}, "required": []},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "set_recommendations",
            "description": "Declare the final recommended models in ranked order. Call this after searching, before writing your response, to set which model cards appear in the UI. Best match first, max 3.",
            "parameters": {
                "type": "object",
                "properties": {
                    "model_ids": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Ordered list of model IDs to recommend, best first. Max 3.",
                    }
                },
                "required": ["model_ids"],
            },
        },
    },
]

TOOL_DISPATCH: dict[str, callable] = {
    "search_models": search_models,
    "get_model_details": get_model_details,
    "compare_models": compare_models,
    "list_providers": list_providers,
    "set_recommendations": set_recommendations,
}
