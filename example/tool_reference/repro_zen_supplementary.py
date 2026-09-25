"""Supplementary test for zai-org/GLM-5#76 via OpenCode Zen free endpoint.

Tests whether GLM-5-generation weights natively understand a `tool_reference`
tool-result payload (deferred-tool-loaded signal from Claude Code's protocol).
Uses OpenAI-format function calling since Zen is OpenAI-compatible; semantics
of the tool_result payload mirror issue #76.
"""

import json
import urllib.request

URL = "https://opencode.ai/zen/v1/chat/completions"
MODEL = "x-preview-f-free"

TOOLS = [
    {"type": "function", "function": {
        "name": "ToolSearch",
        "description": "Search for deferred tools by name and load them into the session.",
        "parameters": {"type": "object", "properties": {
            "query": {"type": "string"}}, "required": ["query"]}}},
    {"type": "function", "function": {
        "name": "Workflow",
        "description": "Run a multi-step workflow script. Deferred tool, must be loaded via ToolSearch.",
        "parameters": {"type": "object", "properties": {
            "script": {"type": "string"}, "title": {"type": "string"}},
            "required": ["script"]}}},
]

GUIDANCE = (
    '## Understanding tool_reference Response Type\n'
    'When ToolSearch returns {"type": "tool_reference", "tool_name": "Workflow"}, '
    'it means the Workflow tool is now registered and available. Call it directly.'
)

TOOL_RESULT = json.dumps(
    {"content": [{"type": "tool_reference", "tool_name": "Workflow"}]})


def call(messages, tools=None):
    body = json.dumps({"model": MODEL, "max_tokens": 512,
                       "messages": messages,
                       "tools": tools if tools is not None else TOOLS}).encode()
    req = urllib.request.Request(URL, data=body, headers={
        "Content-Type": "application/json", "User-Agent": "curl/8.5.0"})
    with urllib.request.urlopen(req, timeout=120) as resp:
        return json.loads(resp.read())


def run(label, system=None):
    print(f"\n=== {label} ===")
    msgs = [{"role": "user",
             "content": "Please run the Workflow tool (use ToolSearch first if needed)."}]
    if system:
        msgs.insert(0, {"role": "system", "content": system})

    # Phase 1 mirrors deferred tool discovery: only ToolSearch is loaded.
    r1 = call(msgs, tools=[TOOLS[0]])
    m1 = r1["choices"][0]["message"]
    tcalls = m1.get("tool_calls") or []
    search_calls = [t for t in tcalls if t["function"]["name"] == "ToolSearch"]
    if not search_calls:
        names = [t["function"]["name"] for t in tcalls]
        text = (m1.get("content") or "")[:250]
        # Calling a not-yet-loaded Workflow would be invalid behavior here.
        verdict = "INVALID" if "Workflow" in names else "INCONCLUSIVE"
        print(f"ToolSearch not called; went to {names or 'text'}. Text: {text}")
        print(f"--> {verdict}")
        return
    msgs.append(m1)
    msgs.append({"role": "tool",
                 "tool_call_id": search_calls[0]["id"],
                 "content": TOOL_RESULT})

    # Phase 2: tool_reference payload signals that Workflow is now loaded.
    r2 = call(msgs, tools=TOOLS)
    m2 = r2["choices"][0]["message"]
    names = [t["function"]["name"] for t in (m2.get("tool_calls") or [])]
    text = (m2.get("content") or "")[:250]
    print(f"Follow-up tool calls: {names or 'NONE'}")
    print(f"Text: {text}")
    verdict = "PASS" if "Workflow" in names else "FAIL"
    print(f"--> {verdict}")


if __name__ == "__main__":
    run("Case 1: no guidance (issue #76 predicts FAIL)")
    run("Case 2: with tool_reference guidance (predicts PASS)", GUIDANCE)
