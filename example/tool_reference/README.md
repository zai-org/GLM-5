# `tool_reference` Handling in Anthropic-Compatible Tool Use

Reproduction and workaround for [issue #76](https://github.com/zai-org/GLM-5/issues/76):
GLM-5.1 does not natively interpret the `tool_reference` content block that
Claude Code emits when deferred tool discovery (`ToolSearch`) loads a tool.

## The problem

When a `tool_result` contains:

```json
{
  "type": "tool_reference",
  "tool_name": "Workflow"
}
```

the Anthropic tool-use protocol means: *"this deferred tool is now registered
and available for direct invocation."* Claude, Xiaomi MiMo, and other models
handle this natively. GLM-5.1 instead treats it as an unrecognized/empty
response and reports that no tools were found, halting agentic workflows.

## Reproduce

```bash
export ANTHROPIC_BASE_URL="https://api.z.ai/api/anthropic"
export ANTHROPIC_AUTH_TOKEN="your-zai-api-key"
python repro_tool_reference.py
```

The script runs two cases against the same conversation:

| Case | System prompt | Expected result |
|---|---|---|
| 1 | none | Model says "no tools found" (bug) |
| 2 | includes `tool_reference` guidance | Model calls `Workflow` directly |

## Workaround

Add explicit guidance about the `tool_reference` response type to the system
prompt (see `TOOL_REFERENCE_GUIDANCE` in the script). With this context,
GLM-5.1 correctly interprets the block and invokes the referenced tool.

## Supplementary test results (2026-08-26)

`repro_zen_supplementary.py` runs the same deferred-tool scenario against a
GLM-5-generation checkpoint served through OpenCode Zen (OpenAI-format
function calling, `tool_reference` payload emulated in the tool message):

| Case | Result |
|---|---|
| No guidance | PASS — model called `Workflow` directly |
| With guidance | PASS |

The weights handled the payload natively, suggesting the reported failure is
specific to the `glm-5.1` checkpoint or to the Anthropic-compatible serving
template rather than to GLM-5-generation weights generally. Official
confirmation still requires running `repro_tool_reference.py` against
`glm-5.1` on the Anthropic endpoint.

## Long-term fix

Per the issue's suggested fix, include `tool_reference` examples from the
Anthropic/Claude Code tool protocol in future GLM tool-use post-training data
so the behavior is native rather than prompt-dependent.
