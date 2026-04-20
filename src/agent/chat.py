"""
Model selector chat agent.

Conversational agent that helps developers choose an AI model.
Asks clarifying questions when needed, recommends when it has enough info.

Run:
  python -m src.agent.chat
"""
from __future__ import annotations

import json
import os
from typing import Iterator

from openai import OpenAI

from src.db.tools import TOOL_DEFINITIONS, TOOL_DISPATCH

_SYSTEM = """\
You are an expert AI model advisor helping developers choose the right model for their project. Always respond in English.

## Your goal
Recommend the best model(s) from the database for the developer's needs.
Use query_db to search. Always query the views, not the raw tables:
- v_api_models: model_id, name, provider, model_category, is_open_source, is_deprecated, context_window, max_output, input_price, output_price, cached_price, per_image, per_minute, per_1m_characters, price_tier, parameter_count_b, description, ideal_for
- v_self_hosted_models: model_id, name, provider, model_category, is_open_source, context_window, parameter_count_b, min_vram_gb, gated, hf_model_id, license, description, ideal_for
- model_features: model_id, source ('api'|'self_hosted'), feature  ← JOIN this to filter by capability
- model_benchmarks: model_id, source, name, value

Valid model_category: 'llm', 'code', 'embedding', 'image_gen', 'tts', 'video_gen', 'realtime'
Valid price_tier: 'budget' (<$1/1M), 'mid' ($1–$10), 'premium' (>$10)
Valid features: 'streaming', 'function_calling', 'structured_output', 'fine_tuning', 'caching', 'batch', 'reasoning', 'vision', 'audio_input', 'audio_output'
Providers (api): Anthropic, OpenAI, Google, Mistral, DeepSeek, xAI, Meta
Providers (self_hosted): Meta, Mistral, Google, DeepSeek, xAI

## How to behave
- Call query_db immediately when you have enough context. Do not explain what you are about to do.
- If the request is missing use case OR budget/deployment, ask ONE focused question before searching.
- After getting results, call set_recommendations (best first, max 3) then write your response.
- If a query returns < 3 results, retry with relaxed filters.
- When the user says "no budget limit", prioritize the most capable models — don't default to cheap or open-source.
- Mention trade-offs honestly: cost, latency, privacy, VRAM, rate limits.
- For self-hosted models: function_calling and tool use depend on the serving framework (vLLM, Ollama, llama.cpp), not just the model. Most instruction-tuned self-hosted LLMs support it when served correctly. Do not treat the absence of a function_calling feature tag in the DB as meaning the model doesn't support it.
- Never recommend a model not returned by query_db.
- Always SELECT model_id, name, provider, context_window, input_price, output_price (and min_vram_gb for self-hosted) in every query.

## Critical info needed
- use_case: what the model will do
- budget / deployment: API (which price tier?) or self-hosted?

## Ask if relevant
- Vision or audio inputs? Context size? Reasoning-heavy tasks? Real-time or batch?
"""


_REDIRECT = "I can only help you choose the right AI model for your project. What are you building?"
_CUTOFF   = "I'm not able to help with that. Feel free to start a new conversation if you need model recommendations."


def _is_off_topic(message: str) -> bool:
    return False


_REASONING_MODELS = {"o1", "o1-mini", "o3", "o3-mini", "o4-mini"}


class ModelSelectorChat:
    def __init__(self, model: str = "gpt-4.1-mini", api_key: str | None = None):
        self.client = OpenAI(api_key=api_key or os.environ.get("OPENAI_API_KEY", ""))
        self.model = model
        self.is_reasoning = model in _REASONING_MODELS
        self.history: list[dict] = []
        self._offtopic_count: int = 0

    def _run_tools(self, tool_calls) -> list[dict]:
        results = []
        for tc in tool_calls:
            name = tc.function.name
            args = json.loads(tc.function.arguments)
            fn = TOOL_DISPATCH.get(name)
            if fn:
                try:
                    result = fn(**args)
                except Exception as e:
                    result = {"error": str(e)}
            else:
                result = {"error": f"Unknown tool: {name}"}
            results.append({
                "tool_call_id": tc.id,
                "role": "tool",
                "name": name,
                "content": json.dumps(result),
            })
        return results

    def chat(self, user_message: str) -> str:
        if _is_off_topic(user_message):
            self._offtopic_count += 1
            reply = _CUTOFF if self._offtopic_count >= 2 else _REDIRECT
            self.history.append({"role": "user", "content": user_message})
            self.history.append({"role": "assistant", "content": reply})
            return reply
        self._offtopic_count = 0
        self.history.append({"role": "user", "content": user_message})

        while True:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "system", "content": _SYSTEM}] + self.history,
                tools=TOOL_DEFINITIONS,
                tool_choice="auto",
            )
            msg = response.choices[0].message

            if msg.tool_calls:
                self.history.append(msg)
                tool_results = self._run_tools(msg.tool_calls)
                self.history.extend(tool_results)
            else:
                reply = msg.content or ""
                self.history.append({"role": "assistant", "content": reply})
                if reply.strip() == _REDIRECT:
                    self._offtopic_count += 1
                else:
                    self._offtopic_count = 0
                return reply

    def stream(self, user_message: str) -> Iterator[tuple[str, str]]:
        """
        Yields (event, data) tuples:
          ("token",  str)        — text chunk to stream
          ("models", json_str)   — JSON list of model dicts from search_models/compare_models
        """
        if _is_off_topic(user_message):
            self._offtopic_count += 1
            reply = _CUTOFF if self._offtopic_count >= 2 else _REDIRECT
            self.history.append({"role": "user", "content": user_message})
            self.history.append({"role": "assistant", "content": reply})
            yield ("token", reply)
            return
        self._offtopic_count = 0
        self.history.append({"role": "user", "content": user_message})

        all_models: dict[str, dict] = {}
        recommended_ids: list[str] = []

        # Run tool calls synchronously, capture model results
        while True:
            yield ("status", "Searching...")
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "system", "content": _SYSTEM}] + self.history,
                tools=TOOL_DEFINITIONS,
                tool_choice="auto",
            )
            msg = response.choices[0].message
            if msg.tool_calls:
                self.history.append(msg)
                tool_results = self._run_tools(msg.tool_calls)
                self.history.extend(tool_results)
                for tc, tr in zip(msg.tool_calls, tool_results):
                    data = json.loads(tr["content"])
                    print(f"[TOOL] {tc.function.name}({tc.function.arguments})")
                    if tc.function.name == "query_db":
                        for m in data.get("rows", []):
                            if "model_id" in m:
                                all_models[m["model_id"]] = m
                    elif tc.function.name == "set_recommendations":
                        recommended_ids = data.get("model_ids", [])
            else:
                break

        if recommended_ids:
            # Fill any missing models via DB lookup
            missing = [mid for mid in recommended_ids if mid not in all_models or "name" not in all_models[mid]]
            if missing:
                from src.db.tools import query_db as _qdb
                placeholders = ",".join(f"'{m}'" for m in missing)
                for tbl, src in [("v_api_models", "api"), ("v_self_hosted_models", "self_hosted")]:
                    res = _qdb(f"SELECT * FROM {tbl} WHERE model_id IN ({placeholders})")
                    for row in res.get("rows", []):
                        all_models[row["model_id"]] = row
            found_models = [all_models[mid] for mid in recommended_ids if mid in all_models]
        else:
            found_models = list(all_models.values())[:3]

        if found_models:
            yield ("models", json.dumps(found_models))

        if self.is_reasoning:
            # Reasoning models: no streaming, tool_choice="auto" (they ignore "none")
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "system", "content": _SYSTEM}] + self.history,
                tools=TOOL_DEFINITIONS,
                tool_choice="auto",
            )
            full = response.choices[0].message.content or ""
            yield ("token", full)
        else:
            stream = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "system", "content": _SYSTEM}] + self.history,
                tools=TOOL_DEFINITIONS,
                tool_choice="none",
                stream=True,
            )
            full = ""
            for chunk in stream:
                delta = chunk.choices[0].delta.content or ""
                full += delta
                yield ("token", delta)

        self.history.append({"role": "assistant", "content": full})
        if full.strip() == _REDIRECT:
            self._offtopic_count += 1
        else:
            self._offtopic_count = 0

    def reset(self) -> None:
        self.history.clear()


# ── CLI ───────────────────────────────────────────────────────────────────────

def _cli() -> None:
    from rich.console import Console
    from rich.markdown import Markdown

    console = Console()
    agent = ModelSelectorChat()

    console.print("\n[bold cyan]AI Model Selector[/bold cyan] — escribe tu necesidad o 'exit' para salir\n")

    while True:
        try:
            user = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not user:
            continue
        if user.lower() in ("exit", "quit", "q"):
            break
        if user.lower() == "reset":
            agent.reset()
            console.print("[dim]Conversación reiniciada.[/dim]\n")
            continue

        console.print("\n[bold]Assistant:[/bold]")
        reply = agent.chat(user)
        console.print(Markdown(reply))
        console.print()


if __name__ == "__main__":
    _cli()
