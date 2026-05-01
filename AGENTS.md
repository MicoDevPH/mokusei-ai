# Mokusei AI — Agent Development Guide

This file helps AI coding agents understand the codebase architecture and conventions for productive development.

## Project Overview

**Mokusei AI** is a multi-agent framework where each "moon" (named after Jupiter's moons) is a specialized AI assistant with distinct personality and expertise. The system uses FastAPI for REST API, LangChain for LLM orchestration, and Azure OpenAI for model inference.

**Current agents:**
- **Ganymede** — Personal Assistant Specialist (portfolio chat assistant)
- **Europa** — Travel Agent (coming soon)

## Architecture Patterns

### 1. Agent Registration & Discovery

All agents are registered in [`mokusei_ai/agents/registry.py`](mokusei_ai/agents/registry.py):
```python
AGENTS = {
    "ganymede": GanymedeAgent,
    "europa": EuropaAgent,
}
```

Agents are discovered by name and instantiated via `get_agent(name, api_key)`. This allows automatic API endpoint creation without modification to router code.

### 2. Agent Structure

Each agent lives in its own folder and follows this pattern:

```
mokusei_ai/agents/{moon_name}/
├── __init__.py
├── agent.py           # Core agent class
└── prompts/
    ├── {moon_name}_instructions.xml   # System prompt/persona
    └── persona.xml                     # Personality definition
```

**Agent class requirements:**
- Inherit or implement a base interface with `__init__(api_key)` and `async def chat(message: str) -> str`
- Store persona/system prompt as instance variable (e.g., `self.persona`)
- Use LangChain's `ChatOpenAI` for model interactions
- Log via [`mokusei_ai/core/logger.py`](mokusei_ai/core/logger.py) using `get_logger(agent_name)`
- Return response string from `chat()` method

**Reference implementation:** [`mokusei_ai/agents/ganymede/agent.py`](mokusei_ai/agents/ganymede/agent.py)

### 3. API Layer

[`mokusei_ai/api/router.py`](mokusei_ai/api/router.py) provides REST endpoints for all agents:

```
POST /api/agents/{agent_name}/chat
Content-Type: application/json
Body: {"message": "user query", "api_key": "optional"}
```

**Key conventions:**
- Agent instances are cached via `@lru_cache` to avoid recreating on each request
- Requests use Pydantic `BaseModel` for validation
- Errors raise `HTTPException` with appropriate status codes
- Optional `api_key` in request body falls back to env variable

### 4. Logging & Theming

All agents use [`mokusei_ai/core/logger.py`](mokusei_ai/core/logger.py) for consistent, beautifully formatted logs:

```python
logger = get_logger("AGENT_NAME")
logger.info("Standard message")
logger.error("Error occurred")
```

**Custom colors by moon:**
- Ganymede: orange3
- Europa: magenta
- Callisto: brown
- Io: orange3

## How to Add a New Agent

1. **Create agent folder:**
   ```bash
   mkdir -p mokusei_ai/agents/{new_moon}/prompts
   touch mokusei_ai/agents/{new_moon}/__init__.py
   ```

2. **Implement agent class** in `mokusei_ai/agents/{new_moon}/agent.py`:
   ```python
   import os
   from langchain_openai import ChatOpenAI
   from langchain_core.messages import SystemMessage, HumanMessage
   from mokusei_ai.core.logger import get_logger
   
   logger = get_logger("AGENT_NAME_UPPER")
   
   class NewMoonAgent:
       def __init__(self, api_key: str = None):
           key = api_key or os.getenv("GITHUB_TOKEN")
           if not key:
               raise ValueError("No API key found.")
           
           self.llm = ChatOpenAI(
               model="gpt-4o-mini",
               openai_api_key=key,
               base_url="https://models.inference.ai.azure.com"
           )
           self.persona = "You are..."
           self.version = "1.0"
       
       async def chat(self, message: str) -> str:
           messages = [
               SystemMessage(content=self.persona),
               HumanMessage(content=message)
           ]
           response = await self.llm.ainvoke(messages)
           return response.content
   ```

3. **Create prompt files** in `prompts/`:
   - `{new_moon}_instructions.xml` — system prompt content
   - `persona.xml` — personality definition

4. **Register in `mokusei_ai/agents/registry.py`:**
   ```python
   from mokusei_ai.agents.{new_moon}.agent import NewMoonAgent
   
   AGENTS = {
       "ganymede": GanymedeAgent,
       "europa": EuropaAgent,
       "{new_moon}": NewMoonAgent,  # Add here
   }
   ```

5. **Done** — Agent is automatically available via API and CLI without router changes.

## Development Commands

**Activate virtual environment:**
```bash
source .venv/bin/activate  # macOS/Linux
# or
.venv\Scripts\Activate.ps1  # Windows PowerShell
```

**Install in development mode:**
```bash
pip install -e .
```

**Install testing dependencies (if needed):**
```bash
python -m pip install pytest
```

**Run tests:**
```bash
python -m pytest
```

> Note: this repository does not use `uv run pytest`. Use `uvicorn` to run the server and `pytest` directly for tests.

**Start FastAPI server:**
```bash
uvicorn mokusei_ai.main:app --reload
```

**Run agent via CLI:**
```bash
mokusei-ai run ganymede
mokusei-ai run europa
```

**List available agents:**
```bash
mokusei-ai agents
```

## Key Dependencies

- **FastAPI** — Web framework for REST API
- **uvicorn** — ASGI server
- **LangChain** — LLM orchestration (`langchain-openai` for Azure OpenAI integration)
- **Pydantic** — Request/response validation
- **python-dotenv** — Environment variable loading
- **Typer** — CLI framework
- **Rich** — Beautiful terminal output

See [`pyproject.toml`](pyproject.toml) for full list and versions.

## Environment Setup

Create `.env` file in project root:
```
GITHUB_TOKEN=your_azure_openai_api_key
```

The system falls back to this when no API key is provided in requests.

## File Structure Reference

| File/Folder | Purpose |
|-----------|---------|
| [`mokusei_ai/agents/registry.py`](mokusei_ai/agents/registry.py) | Central agent registration |
| [`mokusei_ai/api/router.py`](mokusei_ai/api/router.py) | FastAPI routes for all agents |
| [`mokusei_ai/core/logger.py`](mokusei_ai/core/logger.py) | Logging utilities with Rich theme |
| [`mokusei_ai/main.py`](mokusei_ai/main.py) | FastAPI app initialization |
| [`mokusei_ai/cli.py`](mokusei_ai/cli.py) | CLI commands (Typer) |
| [`pyproject.toml`](pyproject.toml) | Project metadata & dependencies |

## Common Development Tasks

**Testing an agent endpoint:**
```bash
curl -X POST http://localhost:8000/api/agents/ganymede/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello Ganymede"}'
```

**Adding a new LLM model:**
Modify `self.llm` instantiation in agent class — currently uses `gpt-4o-mini` via Azure OpenAI.

**Changing agent behavior:**
Update `self.persona` string in agent class to modify system prompt without code logic changes.

## Design Principles

1. **Minimal registry** — Agents self-register; no central configuration needed beyond registry.py
2. **Async by default** — All agent chat methods are async for FastAPI compatibility
3. **Personality-driven** — Each agent has distinct persona and voice in prompts
4. **Environment-first** — API keys come from env/requests, not hardcoded
5. **Beautifully logged** — Rich formatting for CLI and server logs
6. **Extensible** — Add agents by folder without touching router or main app code
