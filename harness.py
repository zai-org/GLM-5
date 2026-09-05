#!/usr/bin/env python3
"""Small, auditable agent harness for a local GLM-5.3-Flash snapshot.

The kernel deliberately knows only Context, EventBus, and PluginLoader.
Everything else is mounted as a plugin/service and can be replaced in tests.
"""
from __future__ import annotations

import argparse
import asyncio
import copy
import json
import os
import re
import sys
import time
import uuid
from dataclasses import dataclass
from pathlib import Path
from threading import Thread
from typing import Any, Awaitable, Callable, Protocol


def parse_tool_calls(text: str) -> list[dict[str, Any]]:
    """Parse model-generated <tool_call>name<arg_key>k</arg_key><arg_value>v</arg_value>...</tool_call> blocks.

    Values are JSON-decoded when possible (numbers, objects, lists, bools, strings).
    Returns list of {"name": str, "arguments": dict}.
    """
    calls: list[dict[str, Any]] = []
    # Capture the interior of each tool_call block
    for block in re.findall(r"<tool_call>(.*?)</tool_call>", text, re.DOTALL | re.IGNORECASE):
        block = block.strip()
        if not block:
            continue
        # Name is leading text up to first <arg_key> (or whole if no args)
        if "<arg_key>" in block:
            name, rest = block.split("<arg_key>", 1)
            name = name.strip()
            rest = "<arg_key>" + rest
        else:
            name = block.strip()
            rest = ""
        arguments: dict[str, Any] = {}
        for km, vm in re.findall(
            r"<arg_key>(.*?)</arg_key>\s*<arg_value>(.*?)</arg_value>",
            rest,
            re.DOTALL,
        ):
            key = km.strip()
            vraw = vm.strip()
            try:
                val = json.loads(vraw)
            except Exception:
                val = vraw
            arguments[key] = val
        if name:
            calls.append({"name": name, "arguments": arguments})
    return calls


class EventBus:
    MODES = {"emit", "waterfall", "parallel", "serial"}

    def __init__(self) -> None:
        self._listeners: dict[str, list[tuple[int, Callable[..., Any]]]] = {}

    def on(self, event: str, listener: Callable[..., Any], *, prepend=False) -> Callable[[], None]:
        listeners = self._listeners.setdefault(event, [])
        item = (0 if prepend else len(listeners) + 1, listener)
        if prepend:
            listeners.insert(0, item)
        else:
            listeners.append(item)
        return lambda: listeners.remove(item) if item in listeners else None

    async def dispatch(self, event: str, mode: str, payload: Any) -> Any:
        if mode not in self.MODES:
            raise ValueError(f"unknown dispatch mode: {mode}")
        listeners = list(self._listeners.get(event, []))
        if mode == "emit":
            for _, listener in listeners:
                result = listener(payload)
                if asyncio.iscoroutine(result):
                    asyncio.create_task(result)
            return None
        if mode == "parallel":
            await asyncio.gather(*(self._call(listener, payload) for _, listener in listeners))
            return None
        if mode == "serial":
            result = None
            for _, listener in listeners:
                result = await self._call(listener, payload)
            return result
        # Waterfall listeners receive an explicit next() and may short-circuit.
        async def run(index: int, value: Any) -> Any:
            if index == len(listeners):
                return value
            listener = listeners[index][1]
            called = False

            async def next_(updated=value):
                nonlocal called
                called = True
                return await run(index + 1, updated)

            result = listener(value, next_)
            result = await result if asyncio.iscoroutine(result) else result
            return result if not called else result
        return await run(0, payload)

    @staticmethod
    async def _call(listener, payload):
        result = listener(payload)
        return await result if asyncio.iscoroutine(result) else result


class Context:
    def __init__(self) -> None:
        self.events = EventBus()
        self.services: dict[str, Any] = {}
        self._disposers: list[Callable[[], Any]] = []

    def provide(self, key: str, service: Any) -> None:
        if key in self.services:
            raise RuntimeError(f"duplicate service provider: {key}")
        self.services[key] = service

    def get(self, key: str) -> Any:
        try:
            return self.services[key]
        except KeyError as exc:
            raise RuntimeError(f"missing service: ctx.{key}") from exc

    def effect(self, disposer: Callable[[], Any]) -> None:
        self._disposers.append(disposer)

    def on(self, event: str, listener: Callable[..., Any], *, prepend=False) -> Callable[[], None]:
        """Register an event listener whose teardown is owned by this context."""
        disposer = self.events.on(event, listener, prepend=prepend)
        self.effect(disposer)
        return disposer

    async def close(self) -> None:
        for disposer in reversed(self._disposers):
            result = disposer()
            if asyncio.iscoroutine(result):
                await result
        self._disposers.clear()


class Plugin(Protocol):
    id: str
    def apply(self, ctx: Context) -> Any: ...


class PluginLoader:
    def __init__(self, ctx: Context):
        self.ctx = ctx
        self.loaded: list[str] = []

    async def mount(self, plugins: list[Plugin]) -> None:
        try:
            for plugin in plugins:
                result = plugin.apply(self.ctx)
                if asyncio.iscoroutine(result):
                    await result
                self.loaded.append(plugin.id)
        except Exception:
            await self.ctx.close()
            raise


@dataclass(frozen=True)
class SessionEvent:
    type: str
    data: dict[str, Any]
    ts: float


class SessionLog:
    SURFACE = {"user/message", "assistant/message", "tool/result"}

    def __init__(self, path: Path | None = None):
        self.path = path
        self.events: list[SessionEvent] = []
        if path and path.exists():
            for line in path.read_text().splitlines():
                row = json.loads(line)
                self.events.append(SessionEvent(row["type"], row["data"], row["ts"]))

    def append(self, event_type: str, data: dict[str, Any]) -> SessionEvent:
        event = SessionEvent(event_type, copy.deepcopy(data), time.time())
        self.events.append(event)
        if self.path:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            with self.path.open("a") as stream:
                stream.write(json.dumps({"type": event.type, "data": event.data, "ts": event.ts}) + "\n")
                stream.flush()
                os.fsync(stream.fileno())
        return event

    def derive_messages(self) -> list[dict[str, str]]:
        messages = []
        for event in self.events:
            if event.type == "user/message":
                messages.append({"role": "user", "content": event.data["content"]})
            elif event.type == "assistant/message":
                messages.append({"role": "assistant", "content": event.data["content"]})
            elif event.type == "tool/result":
                messages.append({"role": "tool", "content": event.data["content"]})
        return messages


@dataclass
class Tool:
    name: str
    description: str
    schema: dict[str, Any]
    handler: Callable[[dict[str, Any]], Awaitable[Any] | Any]
    allowed: bool = True


class ToolRegistry:
    def __init__(self, ctx: Context):
        self.ctx, self.tools = ctx, {}

    def register(self, tool: Tool) -> Callable[[], None]:
        if tool.name in self.tools:
            raise RuntimeError(f"duplicate tool: {tool.name}")
        self.tools[tool.name] = tool
        return lambda: self.tools.pop(tool.name, None)

    def schemas(self) -> list[dict[str, Any]]:
        return [{"type": "function", "function": {"name": t.name, "description": t.description, "parameters": t.schema}}
                for t in self.tools.values()]

    def _finish(self, call: dict[str, Any], response: dict[str, Any]) -> dict[str, Any]:
        sessions = self.ctx.services.get("sessions")
        if sessions is not None:
            sessions.append("tool/result", {
                "call_id": call["id"], "name": call["name"],
                "ok": response.get("ok", False),
                "content": response.get("content", response.get("error", "")),
            })
        return response

    async def execute(self, name: str, arguments: dict[str, Any]) -> dict[str, Any]:
        call = {"name": name, "arguments": copy.deepcopy(arguments), "id": str(uuid.uuid4())}
        call = await self.ctx.events.dispatch("tools/pre-execute", "waterfall", call)
        if call.get("denied"):
            return self._finish(call, {"ok": False, "error": call.get("error", "DENIED_BY_POLICY")})
        tool = self.tools.get(call["name"])
        if not tool:
            return self._finish(call, {"ok": False, "error": "UNKNOWN_TOOL"})
        if not tool.allowed:
            return self._finish(call, {"ok": False, "error": "DENIED_BY_POLICY"})
        try:
            result = tool.handler(copy.deepcopy(call["arguments"]))
            result = await result if asyncio.iscoroutine(result) else result
            post = await self.ctx.events.dispatch("tools/post-execute", "waterfall", {"call": call, "result": result})
            return self._finish(call, {"ok": True, "content": json.dumps(post["result"], ensure_ascii=False)})
        except Exception as exc:
            return self._finish(call, {"ok": False, "error": type(exc).__name__, "content": str(exc)})


class LLM(Protocol):
    async def stream(self, messages: list[dict[str, str]], tools: list[dict[str, Any]]) -> Any: ...


class TransformersGLM:
    """Thin adapter; prompt assembly, logging, and retry remain harness-owned.

    Uses real streaming via TextIteratorStreamer + cross-thread queue to avoid
    blocking the event loop. Passes tools to the chat template. Performs
    incremental generation and attempts to release device memory after use.
    """
    def __init__(self, model_path: Path, reasoning_effort: str = "max", max_new_tokens: int = 8192):
        self.model_path = model_path
        self.reasoning_effort = reasoning_effort
        self.max_new_tokens = max_new_tokens
        self.model = self.tokenizer = None

    def _load(self):
        if self.model is not None:
            return
        try:
            from transformers import AutoModelForCausalLM, AutoTokenizer
        except ImportError as exc:
            raise RuntimeError("local mode requires transformers and torch") from exc
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_path, trust_remote_code=True)
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_path, device_map="auto", trust_remote_code=True, torch_dtype="auto"
        )

    def _maybe_clear_memory(self) -> None:
        try:
            import torch
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
            if hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
                torch.mps.empty_cache()
        except Exception:
            pass

    async def stream(self, messages, tools=None):
        self._load()
        # Pass tools so the jinja template can emit <tools> and tool reference blocks
        prompt = self.tokenizer.apply_chat_template(
            messages,
            tools=tools or None,
            tokenize=False,
            add_generation_prompt=True,
            clear_thinking=True,
            reasoning_effort=self.reasoning_effort,
        )
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)

        from transformers import TextIteratorStreamer

        streamer = TextIteratorStreamer(
            self.tokenizer, skip_prompt=True, skip_special_tokens=True
        )
        generation_kwargs = dict(
            **inputs,
            streamer=streamer,
            max_new_tokens=self.max_new_tokens,
        )

        def _generate():
            try:
                import torch
                with torch.inference_mode():
                    self.model.generate(**generation_kwargs)
            except Exception:
                # Streamer will end; error surfaced via queue if needed
                pass

        thread = Thread(target=_generate, daemon=True)
        thread.start()

        # Bridge the blocking TextIteratorStreamer into the async event loop
        # without blocking the loop thread for the entire generation.
        loop = asyncio.get_running_loop()
        q: asyncio.Queue[str | None] = asyncio.Queue()

        def _feed():
            try:
                for text in streamer:
                    asyncio.run_coroutine_threadsafe(q.put(text), loop)
                asyncio.run_coroutine_threadsafe(q.put(None), loop)
            except Exception as exc:
                asyncio.run_coroutine_threadsafe(
                    q.put(f"__STREAM_ERROR__{type(exc).__name__}: {exc}"), loop
                )
                asyncio.run_coroutine_threadsafe(q.put(None), loop)

        feeder = Thread(target=_feed, daemon=True)
        feeder.start()

        try:
            while True:
                item = await q.get()
                if item is None:
                    break
                if isinstance(item, str) and item.startswith("__STREAM_ERROR__"):
                    raise RuntimeError(item[len("__STREAM_ERROR__") :])
                yield item
        finally:
            thread.join(timeout=30)
            feeder.join(timeout=5)
            self._maybe_clear_memory()


class MockLLM:
    def __init__(self, response: str): self.response = response
    async def stream(self, messages, tools=None):
        yield self.response


class AgentLoop:
    def __init__(self, ctx: Context, llm: LLM, sessions: SessionLog, tools: ToolRegistry):
        self.ctx, self.llm, self.sessions, self.tools = ctx, llm, sessions, tools

    async def run(self, prompt: str) -> str:
        self.sessions.append("turn/start", {})
        self.sessions.append("user/message", {"content": prompt})
        try:
            max_rounds = 12
            final_answer = ""
            for round_idx in range(max_rounds):
                messages = self.sessions.derive_messages()
                tools_schemas = self.tools.schemas()
                req = {"messages": messages, "tools": tools_schemas}
                req = await self.ctx.events.dispatch("agent/request", "waterfall", req)

                if round_idx == 0:
                    # Reconstruction epoch: record exactly what is sent to the provider on first turn.
                    request_id = str(uuid.uuid4())
                    self.sessions.append("request/header", {"id": request_id, "message_count": len(req["messages"])})
                    self.sessions.append("request/context", {"id": request_id, "request": copy.deepcopy(req)})

                chunks: list[str] = []
                async for chunk in self.llm.stream(req["messages"], req.get("tools")):
                    chunks.append(chunk)
                    self.sessions.append("assistant/chunk", {"content": chunk})
                    await self.ctx.events.dispatch("llm/stream", "emit", {"content": chunk})

                answer = "".join(chunks)
                self.sessions.append("assistant/message", {"content": answer})

                tool_calls = parse_tool_calls(answer)
                if not tool_calls:
                    final_answer = answer
                    self.sessions.append("step/end", {"status": "completed", "rounds": round_idx + 1})
                    break

                # Execute tools; ToolRegistry._finish will append "tool/result" events
                for tc in tool_calls:
                    await self.tools.execute(tc["name"], tc.get("arguments", {}))

                # Continue loop so model can consume tool results and produce final answer (or more calls)
            else:
                # Exhausted rounds
                final_answer = answer
                self.sessions.append("step/end", {"status": "max_rounds_reached", "rounds": max_rounds})

            self.sessions.append("turn/end", {"status": "completed"})
            await self.ctx.events.dispatch("session/flush", "serial", {"session": len(self.sessions.events)})
            return final_answer
        except asyncio.CancelledError:
            self.sessions.append("interrupted", {"reason": "cancelled"})
            self.sessions.append("turn/end", {"status": "cancelled"})
            raise
        except Exception as exc:
            self.sessions.append("step/end", {"status": "failed", "error": type(exc).__name__})
            self.sessions.append("turn/end", {"status": "failed"})
            raise


class BasePlugin:
    id = "harness-base"

    def __init__(self, sessions: SessionLog | None = None, tools: ToolRegistry | None = None):
        self.sessions = sessions
        self.tools = tools

    def apply(self, ctx):
        if "sessions" not in ctx.services:
            ctx.provide("sessions", self.sessions or SessionLog())
        if "tools" not in ctx.services:
            ctx.provide("tools", self.tools or ToolRegistry(ctx))


async def main() -> int:
    parser = argparse.ArgumentParser(description="Run GLM-5.3-Flash through the H1 plugin harness")
    parser.add_argument("prompt", nargs="?", help="one-shot user prompt")
    parser.add_argument("--model-path", type=Path, default=Path(__file__).parent)
    parser.add_argument("--session", type=Path, help="append-only JSONL session log")
    parser.add_argument("--mock", help="use a deterministic response instead of loading the model")
    parser.add_argument("--reasoning-effort", choices=("low", "high", "max"), default="max")
    parser.add_argument("--max-new-tokens", type=int, default=8192, help="Maximum new tokens to generate")
    args = parser.parse_args()
    prompt = args.prompt or input("you> ")
    ctx = Context()
    sessions = SessionLog(args.session)
    tools = ToolRegistry(ctx)
    llm = (
        MockLLM(args.mock)
        if args.mock is not None
        else TransformersGLM(args.model_path, args.reasoning_effort, args.max_new_tokens)
    )
    try:
        loader = PluginLoader(ctx)
        await loader.mount([BasePlugin(sessions, tools)])
        print(await AgentLoop(ctx, llm, ctx.get("sessions"), ctx.get("tools")).run(prompt))
    finally:
        await ctx.close()
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
