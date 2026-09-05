import asyncio
import json
from pathlib import Path

from harness import AgentLoop, BasePlugin, Context, EventBus, MockLLM, PluginLoader, SessionLog, Tool, ToolRegistry


def test_waterfall_can_rewrite_and_short_circuit():
    async def check():
        bus = EventBus()
        bus.on("x", lambda p, nxt: nxt({**p, "seen": True}))
        assert await bus.dispatch("x", "waterfall", {}) == {"seen": True}
        bus.on("x", lambda p, nxt: {**p, "denied": True})
        bus.on("x", lambda p, nxt: {**p, "should_not_run": True})
        result = await bus.dispatch("x", "waterfall", {})
        assert result == {"seen": True, "denied": True}
    asyncio.run(check())


def test_session_is_append_only_and_projects_surface(tmp_path: Path):
    log = SessionLog(tmp_path / "s.jsonl")
    log.append("turn/start", {})
    log.append("user/message", {"content": "hello"})
    log.append("assistant/chunk", {"content": "ignored in history"})
    log.append("assistant/message", {"content": "hi"})
    assert log.derive_messages() == [{"role": "user", "content": "hello"}, {"role": "assistant", "content": "hi"}]
    assert len((tmp_path / "s.jsonl").read_text().splitlines()) == 4
    restored = SessionLog(tmp_path / "s.jsonl")
    assert restored.derive_messages() == log.derive_messages()


def test_tool_pipeline_denies_unknown_and_policy():
    async def check():
        ctx, registry = Context(), None
        registry = ToolRegistry(ctx)
        log = SessionLog()
        ctx.provide("sessions", log)
        registry.register(Tool("echo", "echo", {"type": "object"}, lambda args: args))
        assert (await registry.execute("missing", {}))["error"] == "UNKNOWN_TOOL"
        assert (await registry.execute("echo", {"x": 1}))["content"] == json.dumps({"x": 1})
        registry.tools["echo"].allowed = False
        assert (await registry.execute("echo", {}))["error"] == "DENIED_BY_POLICY"
        assert [event.type for event in log.events] == ["tool/result", "tool/result", "tool/result"]
    asyncio.run(check())


def test_context_listener_is_reversible_and_plugin_boot_is_fail_loud():
    async def check():
        ctx = Context()
        order = []
        ctx.on("x", lambda _: order.append("listener"))
        await ctx.events.dispatch("x", "emit", {})
        await asyncio.sleep(0)
        assert order == ["listener"]
        await ctx.close()
        await ctx.events.dispatch("x", "emit", {})
        await asyncio.sleep(0)
        assert order == ["listener"]

        ctx = Context()
        BasePlugin().apply(ctx)
        class Broken:
            id = "broken"
            def apply(self, current):
                raise ValueError("boot failure")
        try:
            await PluginLoader(ctx).mount([Broken()])
        except ValueError:
            pass
        else:
            raise AssertionError("broken plugin boot did not fail")
    asyncio.run(check())


def test_base_plugin_composes_services_through_loader():
    async def check():
        ctx = Context()
        sessions, tools = SessionLog(), ToolRegistry(ctx)
        loader = PluginLoader(ctx)
        await loader.mount([BasePlugin(sessions, tools)])
        assert loader.loaded == ["harness-base"]
        assert ctx.get("sessions") is sessions
        assert ctx.get("tools") is tools
        await ctx.close()
    asyncio.run(check())


def test_loop_records_reconstruction_epoch(tmp_path: Path):
    async def check():
        ctx = Context()
        log = SessionLog(tmp_path / "session.jsonl")
        tools = ToolRegistry(ctx)
        answer = await AgentLoop(ctx, MockLLM("ok"), log, tools).run("ping")
        assert answer == "ok"
        assert {event.type for event in log.events} >= {"request/header", "request/context"}
        assert log.derive_messages()[-1] == {"role": "assistant", "content": "ok"}
    asyncio.run(check())


def test_failed_turn_is_closed_and_recorded():
    class FailingLLM:
        async def stream(self, messages, tools):
            raise ConnectionError("offline")
            yield "never"

    async def check():
        ctx, log = Context(), SessionLog()
        tools = ToolRegistry(ctx)
        try:
            await AgentLoop(ctx, FailingLLM(), log, tools).run("ping")
        except ConnectionError:
            pass
        else:
            raise AssertionError("failing provider did not raise")
        assert log.events[-2].type == "step/end"
        assert log.events[-2].data["status"] == "failed"
        assert log.events[-1].type == "turn/end"
        assert log.events[-1].data["status"] == "failed"
    asyncio.run(check())
