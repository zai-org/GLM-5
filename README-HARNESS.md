# GLM-5.3-Flash H1 harness

This is a small local harness derived from `H1.md`. Its kernel has three
primitives: `Context`, `EventBus`, and `PluginLoader`. The session log,
tool registry, loop, and GLM adapter are replaceable services.

## Run without model weights

```bash
python3 harness.py --mock 'hello from the mock adapter' 'say hello'
python3 -m pytest -q test_harness.py
```

## Run the local snapshot

Install the optional runtime dependencies explicitly (`torch` and
`transformers>=5.0.0`), then:

```bash
python3 harness.py --session .sessions/demo.jsonl 'Explain this repository'
```

The default model path is the repository containing `harness.py`; pass
`--model-path` to use another compatible GLM snapshot. `--reasoning-effort`
accepts `low`, `high`, or `max`. The adapter explicitly sets
`clear_thinking=True` for chat, as required by the model guide.

## Deliberate MVP boundaries

The first harness exposes the H1 seams needed for a local one-shot runner:
plugin lifecycle, event dispatch, session replay projection, tool policy,
and a provider-neutral loop. Sandbox/approval, multi-step tool-call parsing,
network protocol, and production-grade streaming backpressure remain
follow-up plugins rather than being hidden inside the kernel.

Tool outcomes are appended as `tool/result` facts, and failed or cancelled
provider calls close their turn with a durable status marker.
