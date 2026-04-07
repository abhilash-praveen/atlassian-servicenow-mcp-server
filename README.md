# Jira & Confluence Assistant

A conversational AI assistant for Jira and Confluence, powered by an MCP (Model Context Protocol) server and a chat UI. Talk to your projects and knowledge base in plain English.

## Capabilities

### Jira
- **Search** issues using natural language (converted to JQL)
- **Get** issue details by ID
- **Create** new issues
- **Update** issue fields (summary, description, priority, labels)
- **Transition** issues through workflow states (e.g. "Move PROJ-123 to Done")
- **Comment** on issues
- **List** all accessible Jira projects

### Confluence
- **Search** pages using CQL (e.g. "Find pages about onboarding")
- **Get** a page by ID (returns title, content, space, and URL)
- **Create** a new page in a given space
- **List** all accessible Confluence spaces

## Stack

- **MCP server** — FastMCP + `atlassian-python-api`
- **Backend** — FastAPI, OpenAI-compatible client (OpenAI or Ollama)
- **Frontend** — Single-page chat UI (HTML + Tailwind)

## Installation

**Prerequisites:** Python 3.10+, [uv](https://github.com/astral-sh/uv)

```bash
git clone <repo-url>
cd jira-mcp
uv sync
```

Copy the sample env file and fill in your credentials:

```bash
cp .env.sample .env
```

Run the web server:

```bash
uv run uvicorn web:app --reload
```

Open [http://localhost:8000](http://localhost:8000).

## Using Ollama (local LLM)

Install Ollama from [ollama.com](https://ollama.com), then pull a model that supports tool calling:

```bash
ollama pull llama3.2
```

Set in `.env`:

```env
LLM_PROVIDER=ollama
LLM_MODEL=llama3.2
```

Recommended models: `llama3.2`, `llama3.1`, `qwen2.5`, `mistral-nemo`.

## Environment Variables

See `.env.sample` for all available options.
