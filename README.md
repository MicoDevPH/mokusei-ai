# Mokusei AI

**AI service backend for personal projects — powered by Jupiter's moons**

## Overview

Mokusei AI is a personal AI service where each "moon" is a specialized agent serving a different project. Built with FastAPI and LangChain, it provides a clean API for deploying AI assistants across your sites and apps.

## The Moons

| Moon | Agent | Used In |
|---|---|---|
| **Ganymede** | Personal Assistant | Portfolio website chat |

## Quick Start

```bash
pip install -r requirements.txt
python -m mokusei_ai
```

```bash
curl -X POST http://localhost:8000/api/agents/ganymede/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What skills does the owner have?"}'
```

## Customizing Ganymede for Your Portfolio

Edit the prompt files in `mokusei_ai/agents/ganymede/prompts/`:

- `ganymede_instructions.xml` — How the agent behaves
- `persona.xml` — The agent's personality and tone

Add your own data (projects, skills, background) directly into these files. No code changes needed — the agent reads them automatically.

You can also pass custom context per request:

```bash
curl -X POST http://localhost:8000/api/agents/ganymede/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Tell me about your React projects", "context": "The owner specializes in React and Node.js"}'
```

## Adding a New Agent

1. Create folder: `mokusei_ai/agents/{moon}/`
2. Create `agent.py` extending `BaseAgent`
3. Create `prompts/{moon}_instructions.xml` and `prompts/persona.xml`
4. Register in `mokusei_ai/agents/registry.py`

## Architecture

```
mokusei_ai/
├── agents/
│   ├── registry.py         # Agent registration
│   └── ganymede/           # Personal Assistant
│       ├── agent.py        # Extends BaseAgent
│       └── prompts/        # System prompt + persona
├── api/
│   └── router.py           # FastAPI routes
├── core/
│   ├── base_agent.py       # Shared agent logic
│   └── logger.py           # Rich logging
├── main.py                 # FastAPI app
└── __main__.py             # Entry point: python -m mokusei_ai
```

## Tech Stack

- **FastAPI** — Web framework
- **LangChain** — LLM orchestration
- **Azure OpenAI** — GPT-4 models
- **Python 3.10+** — Runtime

## License

MIT

---

**Built by MicoDevPH**
