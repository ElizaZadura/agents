# Sidekick

Small LangGraph + Gradio personal co-worker app.

It runs a worker/evaluator loop with tools for:
- browser automation (Playwright)
- web search (Serper)
- Python REPL
- Wikipedia lookup
- basic file management in a local `sandbox` folder
- optional Pushover notifications

## Files

- `app.py` - Gradio UI entrypoint
- `sidekick.py` - LangGraph workflow (worker, tools, evaluator)
- `sidekick_tools.py` - tool setup and external integrations

## Prerequisites

- Python 3.10+
- OpenAI API key
- Playwright browser installed

## Environment Variables

Required:
- `OPENAI_API_KEY`
- `SERPER_API_KEY` (for the search tool)

Optional (only needed if you use push notifications):
- `PUSHOVER_TOKEN`
- `PUSHOVER_USER`

## Quick Start

1. Install dependencies (from your project environment).
2. Ensure a local `sandbox/` folder exists (used by file tools).
3. Run:
   - `python app.py`

The UI opens in your browser (`inbrowser=True`).
