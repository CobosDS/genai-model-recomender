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

## How to behave
- If the developer's message is vague and missing critical info (use case OR budget), ask ONE focused question before searching.
- If you have enough context, call search_models or other tools immediately — don't ask unnecessary questions.
- After getting tool results, give a direct recommendation with clear reasoning.
- Mention trade-offs honestly (cost spikes, latency, privacy, rate limits).
- If the best option depends on a factor you don't know, say so and explain the two paths.
- Only add capabilities filter if the user explicitly mentions them (vision, audio, reasoning...). Do NOT infer capabilities from the use case.
- If search returns fewer than 3 results, call search_models again with fewer or no filters to get more options.

## Critical fields (need at least one before recommending)
- use_case: what the model will do (chat, code, document processing, embeddings...)
- budget: free/cheap/no limit, or a specific $/1M tokens

## Fields that change the recommendation significantly — mention assumptions if unknown
- vision: does the app process images?
- context size: how long are the inputs?
- open source: is self-hosting required?
- reasoning: does it need to solve complex multi-step problems?

## Context window reference
"documentos largos / long documents" → min_context=32000
"contexto muy largo / huge context" → min_context=128000

## Format
- Keep responses concise and practical.
- When recommending, always include: model name, provider, price, context window, and why it fits.
- Never recommend a model not returned by the tools.
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

        found_models: list[dict] = []

        # Run tool calls synchronously, capture model results
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
                for tc, tr in zip(msg.tool_calls, tool_results):
                    if tc.function.name in ("search_models", "compare_models"):
                        data = json.loads(tr["content"])
                        found_models.extend(data.get("models", []))
            else:
                break

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
