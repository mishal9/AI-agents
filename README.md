# AI-agents

Experiments with [Deep Agents](https://docs.langchain.com/oss/python/deepagents/quickstart) (LangChain) running on Google Gemini.

## Files

| File | Description |
| --- | --- |
| `search_agent.py` | Research agent that answers a question using Google Search grounding and prints a report. |
| `agent_customized.py` | Work in progress: agent with custom tools, `AGENTS.md` memory, and skills. `search` and `fetch_url` are not defined yet. |

## Setup

```bash
python -m venv venv
source venv/bin/activate
pip install deepagents langchain-google-genai
export GOOGLE_API_KEY=your-key
```

## Run

```bash
python search_agent.py
```

## Notes

The Deep Agents quickstart passes Gemini's built-in search tool (`{"google_search": {}}`) directly to `create_deep_agent`. With current packages (`langchain-google-genai` 4.4.0, `deepagents` 0.7.19) this fails with:

```
400 INVALID_ARGUMENT: Please enable tool_config.include_server_side_tool_invocations
to use Built-in tools with Function calling.
```

Deep Agents always adds its own function tools (`write_todos`, file tools, `task`), and Gemini rejects built-in tools mixed with function tools unless that flag is set, which LangChain doesn't do. `search_agent.py` works around this by wrapping Google Search in a regular function tool, `internet_search`, that makes a separate grounded Gemini call and returns the answer with source URLs.
