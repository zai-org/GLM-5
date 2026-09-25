"""Reproduction for zai-org/GLM-5#76.

Demonstrates that GLM-5.1 (Anthropic-compatible endpoint) does not natively
interpret a `tool_reference` content block inside a `tool_result`, and shows
that adding explicit guidance to the system prompt fixes the behavior.

Usage:
    export ANTHROPIC_BASE_URL="https://api.z.ai/api/anthropic"
    export ANTHROPIC_AUTH_TOKEN="your-zai-api-key"
    python repro_tool_reference.py
"""

import json
import os
import sys

import urllib.request

BASE_URL = os.environ.get("ANTHROPIC_BASE_URL", "https://api.z.ai/api/anthropic")
API_KEY = os.environ.get("ANTHROPIC_AUTH_TOKEN", "")
MODEL = os.environ.get("GLM_MODEL", "glm-5.1")

TOOL_REFERENCE_GUIDANCE = """
## Understanding tool_reference Response Type

When ToolSearch returns a response containing:
{"type": "tool_reference", "tool_name": "Workflow"}

This means the tool is now available. Call it directly:
Workflow({script: "...", title: "..."})
""".strip()


def send(messages: list, system: str | None = None) -> dict:
    body = {
        "model": MODEL,
        "max_tokens": 1024,
        "messages": messages,
        "tools": [
            {
                "name": "ToolSearch",
                "description": "Search for deferred tools by name and load them into the session.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string"},
                    },
                    "required": ["query"],
                },
            },
            {
                "name": "Workflow",
                "description": "Run a multi-step workflow script. Deferred tool, must be loaded via ToolSearch.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "script": {"type": "string"},
                        "title": {"type": "string"},
                    },
                    "required": ["script"],
                },
            },
        ],
    }
    if system:
        body["system"] = system

    req = urllib.request.Request(
        f"{BASE_URL}/v1/messages",
        data=json.dumps(body).encode(),
        headers={
            "Content-Type": "application/json",
            "x-api-key": API_KEY,
            "anthropic-version": "2023-06-01",
        },
        method="POST",
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())


def run_case(label: str, system: str | None) -> None:
    print(f"\n=== {label} ===")
    messages = [
        {"role": "user", "content": "ultracode: please run the Workflow tool"},
        {
            "role": "assistant",
            "content": [
                {"type": "tool_use", "id": "call_1", "name": "ToolSearch",
                 "input": {"query": "Workflow"}},
            ],
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "tool_result",
                    "tool_use_id": "call_1",
                    "content": [
                        {"type": "tool_reference", "tool_name": "Workflow"},
                    ],
                }
            ],
        },
    ]
    try:
        result = send(messages, system)
    except Exception as exc:  # noqa: BLE001
        print(f"Request failed: {exc}")
        sys.exit(1)

    blocks = result.get("content", [])
    tool_calls = [b["name"] for b in blocks if b.get("type") == "tool_use"]
    text = " ".join(b.get("text", "") for b in blocks if b.get("type") == "text")
    print(f"Tool calls made: {tool_calls or 'NONE'}")
    print(f"Text output: {text[:300]}")

    if "Workflow" in tool_calls:
        print("PASS: model recognized tool_reference and called the tool.")
    else:
        print("FAIL: model did not call Workflow (issue #76 behavior).")


if __name__ == "__main__":
    if not API_KEY:
        sys.exit("Set ANTHROPIC_AUTH_TOKEN first.")
    run_case("Case 1: no guidance (expected FAIL per issue #76)", None)
    run_case("Case 2: with tool_reference guidance (expected PASS)",
             TOOL_REFERENCE_GUIDANCE)
