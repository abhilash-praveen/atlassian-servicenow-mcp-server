# Jira, Confluence & ServiceNow Assistant

A conversational AI assistant for Jira, Confluence and ServiceNow, powered by an MCP (Model Context Protocol) server and a chat UI. Talk to your projects, knowledge base and incidents in plain English.

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

### ServiceNow
- **Create** a new incident with urgency, impact and description
- **Get** an incident by number (e.g. INC0010001)
- **Search** incidents by state and/or urgency

## Stack

- **MCP server** — FastMCP + `atlassian-python-api` + `pysnow`
- **Backend** — FastAPI, OpenAI-compatible client (OpenAI or Ollama)
- **Frontend** — Single-page chat UI (HTML + Tailwind)

## Installation

**Prerequisites:** Python 3.10+, [uv](https://github.com/astral-sh/uv)

```bash
git clone <repo-url>
cd atlassian-servicenow-mcp-server
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

| Variable | Description |
|---|---|
| `JIRA_BASE_URL` | Your Atlassian base URL (e.g. `https://your-org.atlassian.net`) |
| `JIRA_EMAIL` | Atlassian account email |
| `JIRA_API_TOKEN` | Atlassian API token |
| `SERVICENOW_INSTANCE_URL` | ServiceNow instance URL (e.g. `https://dev12345.service-now.com`) |
| `SERVICENOW_USERNAME` | ServiceNow username |
| `SERVICENOW_PASSWORD` | ServiceNow password |
| `OPENAI_API_KEY` | OpenAI API key (if using OpenAI) |
| `LLM_PROVIDER` | `openai` (default) or `ollama` |
| `LLM_MODEL` | Model name (default: `gpt-4o` / `llama3.2`) |
