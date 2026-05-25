# Mokusei AI — Agent Development Guide

This file helps AI coding agents understand the codebase architecture and conventions for productive development.

## Project Overview

**Mokusei AI** is an AI service backend where each "moon" (named after Jupiter's moons) is a specialized agent serving a specific project. The system uses FastAPI for REST API, LangChain for LLM orchestration, and Azure OpenAI for model inference.

**Current agents:**
- **Ganymede** — Personal Assistant (portfolio chat)

## Architecture Patterns

### 1. Agent Registration & Discovery

All agents are registered in [`mokusei_ai/agents/registry.py`](mokusei_ai/agents/registry.py):

```python
AGENTS = {
    "ganymede": GanymedeAgent,
}
```

Agents are discovered by name and instantiated via `get_agent(name, api_key)`. This allows automatic API endpoint creation without modification to router code. Use `get_agent_class(name)` to get the class without instantiating.

### 2. Agent Structure

Each agent lives in its own folder and follows this pattern:

```
mokusei_ai/agents/{moon_name}/
├── __init__.py
├── agent.py           # Extends BaseAgent
└── prompts/
    ├── {moon_name}_instructions.xml   # System prompt
    └── persona.xml                     # Personality definition
```

**Agent class requirements:**
- Extend `BaseAgent` from [`mokusei_ai/core/base_agent.py`](mokusei_ai/core/base_agent.py)
- Call `super().__init__(api_key)` in `__init__`
- The base class handles: API key loading, LLM setup, prompt loading, logging, and context injection
- Prompts are auto-loaded from XML files — no need to hardcode `self.persona`

**Reference implementation:** [`mokusei_ai/agents/ganymede/agent.py`](mokusei_ai/agents/ganymede/agent.py)

### 3. BaseAgent Class

[`mokusei_ai/core/base_agent.py`](mokusei_ai/core/base_agent.py) provides:

- **`__init__(api_key)`** — Loads env vars, validates `api_key` against `{AGENT}_API_KEY` env var, initializes `ChatOpenAI`, auto-loads persona from XML prompts
- **`_load_persona()`** — Reads `{moon}_instructions.xml` + `persona.xml` from the agent's `prompts/` folder
- **`chat(message, context=None, portfolio=None)`** — Sends message with optional conversation history (`context`) and user portfolio data (`portfolio`), logs banner/timer/success

```python
class GanymedeAgent(BaseAgent):
    def __init__(self, api_key=None):
        super().__init__(api_key)
```

### 4. API Layer

[`mokusei_ai/api/router.py`](mokusei_ai/api/router.py) provides REST endpoints:

```
POST /api/agents/{agent_name}/chat
Content-Type: application/json
Body: {"message": "user query", "api_key": "optional", "context": "optional", "portfolio": "optional"}
```

**Key conventions:**
- Agent instances are cached via `@lru_cache` to avoid recreating on each request
- Requests use Pydantic `BaseModel` for validation
- Optional `context` field injects conversation history into the system prompt
- Optional `portfolio` field injects the user's portfolio data (content from `.mokusei/ganymede_context.md`)
- Errors raise `HTTPException` with appropriate status codes

### 5. Logging & Theming

All agents use [`mokusei_ai/core/logger.py`](mokusei_ai/core/logger.py) for consistent, beautifully formatted logs:

```python
logger = get_logger("AGENT_NAME")
logger.info("Standard message")
logger.error("Error occurred")
```

**Custom colors by moon:**
- Ganymede: orange3
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
   from mokusei_ai.core.base_agent import BaseAgent
   
   
   class NewMoonAgent(BaseAgent):
       def __init__(self, api_key: str = None):
           super().__init__(api_key)
   ```

3. **Create prompt files** in `prompts/`:
   - `{new_moon}_instructions.xml` — system prompt content
   - `persona.xml` — personality definition

4. **Register in `mokusei_ai/agents/registry.py`:**
   ```python
   from mokusei_ai.agents.{new_moon}.agent import NewMoonAgent
   
   AGENTS = {
       "ganymede": GanymedeAgent,
       "{new_moon}": NewMoonAgent,
   }
   ```

5. **Done** — Agent is automatically available via API without router changes.

## Development Commands

**Activate virtual environment:**
```bash
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\Activate.ps1  # Windows PowerShell
```

**Install dependencies:**
```bash
pip install -r requirements.txt
```

**Start the server:**
```bash
python -m mokusei_ai
```

## Key Dependencies

- **FastAPI** — Web framework for REST API
- **uvicorn** — ASGI server
- **LangChain** — LLM orchestration (`langchain-openai` for Azure OpenAI integration)
- **Pydantic** — Request/response validation
- **python-dotenv** — Environment variable loading
- **Rich** — Beautiful terminal output

See [`requirements.txt`](requirements.txt) for full list.

## Environment Setup

Create `.env` file in project root:
```
GITHUB_TOKEN=your_github_token
GANYMEDE_API_KEY=your_secret_key
```

Each agent has its own API key via `{AGENT_NAME}_API_KEY`. Clients must send this key as `api_key` in requests. If no `{AGENT_NAME}_API_KEY` is set, the agent accepts any key (dev mode).

## File Structure Reference

| File/Folder | Purpose |
|---|---|
| [`mokusei_ai/core/base_agent.py`](mokusei_ai/core/base_agent.py) | Base agent class with shared logic |
| [`mokusei_ai/agents/registry.py`](mokusei_ai/agents/registry.py) | Central agent registration |
| [`mokusei_ai/api/router.py`](mokusei_ai/api/router.py) | FastAPI routes for all agents |
| [`mokusei_ai/core/logger.py`](mokusei_ai/core/logger.py) | Logging utilities with Rich theme |
| [`mokusei_ai/main.py`](mokusei_ai/main.py) | FastAPI app initialization |
| [`requirements.txt`](requirements.txt) | Python dependencies |

## Frontend Integration

Add a Ganymede chat widget to your portfolio site in three steps.

### 1. Create `.mokusei/ganymede_context.md`

In your frontend project root, create a file with your portfolio info:

```markdown
# Ganymede Context

## Profile
- Name: Your Name
- Role: Your Role
- Location: Your Location
- About: Short bio

## Projects
### Project Name
- Description: What it does
- Tech Stack: Languages/frameworks used
- Link: URL (optional)

## Skills
- Frontend: HTML, CSS, React, etc.
- Backend: Node.js, Python, etc.
- Tools: Git, Docker, etc.

## Education
- School: University name
- Degree: Your degree
- Year: Graduation year

## Contact
- GitHub: your-username
- LinkedIn: your-profile
- Email: your@email.com
```

### 2. Set your API key

Add your Mokusei AI API key to your frontend environment:

```bash
# .env (Vite)
VITE_MOKUSEI_API_KEY=sk_xxx

# .env (Create React App)
REACT_APP_MOKUSEI_API_KEY=sk_xxx

# .env (Next.js)
NEXT_PUBLIC_MOKUSEI_API_KEY=sk_xxx
```

### 3. Wire up the chat widget

**Build-time import** — for Vite, Next.js, or any bundler that supports raw imports:

```js
// React example
import portfolio from '../.mokusei/ganymede_context.md?raw'

async function sendMessage(message) {
  const res = await fetch('https://your-api.com/api/agents/ganymede/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      api_key: import.meta.env.VITE_MOKUSEI_API_KEY,
      message,
      portfolio
    })
  })
  return res.json()
}
```

**Runtime fetch** — for vanilla JS or script-based widgets:

```js
async function sendMessage(message) {
  const portfolio = await fetch('/.mokusei/ganymede_context.md').then(r => r.text())

  const res = await fetch('https://your-api.com/api/agents/ganymede/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      api_key: window.ENV.MOKUSEI_API_KEY,
      message,
      portfolio
    })
  })
  return res.json()
}
```

## Common Development Tasks

**Testing an agent endpoint:**
```bash
curl -X POST http://localhost:8000/api/agents/ganymede/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello Ganymede"}'
```

**Passing project context:**
```bash
curl -X POST http://localhost:8000/api/agents/ganymede/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Tell me about yourself", "context": "The owner is a full-stack developer"}'
```

**Passing portfolio data:**
```bash
curl -X POST http://localhost:8000/api/agents/ganymede/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Tell me about yourself", "portfolio": "## Profile\nName: Alice\nRole: Designer\n..."}'
```

**Adding a new LLM model:**
Override `self.llm` in the agent's `__init__` after calling `super().__init__()`.

**Changing agent behavior:**
Edit the XML prompt files — no code changes needed since `BaseAgent._load_persona()` reads them at runtime.

## Design Principles

1. **Minimal registry** — Agents self-register; no central configuration needed beyond registry.py
2. **Async by default** — All agent chat methods are async for FastAPI compatibility
3. **Personality-driven** — Each agent has distinct persona and voice in prompts
4. **Environment-first** — API keys come from env/requests, not hardcoded
5. **Beautifully logged** — Rich formatting for CLI and server logs
6. **Extensible** — Add agents by folder without touching router or main app code
