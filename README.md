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
```

Create `.env` in project root:

```
GITHUB_TOKEN=your_github_token
GANYMEDE_API_KEY=your_secret_key
```

Start the server:

```bash
python -m mokusei_ai
```

Test it:

```bash
curl -X POST http://localhost:8000/api/agents/ganymede/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What skills do you have?", "api_key": "your_secret_key"}'
```

## How It Works

- **Each agent has its own API key** — set `{AGENT}_API_KEY` in `.env`. Clients send this as `api_key` in requests.
- **Portfolio data is per-request** — users pass their own info as the `portfolio` field. No hardcoded data, no env vars needed.
- **The server calls the LLM** — uses `GITHUB_TOKEN` internally. Clients never need direct LLM access.

## Frontend Integration

Add Ganymede to your portfolio site in three steps.

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

## Adding a New Agent

1. Create folder: `mokusei_ai/agents/{moon}/`
2. Create `agent.py` extending `BaseAgent`
3. Create `prompts/{moon}_instructions.xml` and `prompts/persona.xml`
4. Register in `mokusei_ai/agents/registry.py`
5. Set `{MOON}_API_KEY` in `.env`

The agent is automatically available via API — no router changes needed.

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
│   ├── base_agent.py       # Shared agent logic + API key validation
│   └── logger.py           # Rich logging
├── main.py                 # FastAPI app
└── __main__.py             # Entry point: python -m mokusei_ai
```

## Environment Variables

| Variable | Required | Purpose |
|---|---|---|
| `GITHUB_TOKEN` | ✅ Yes | GitHub PAT used for LLM inference (GitHub Models) |
| `GANYMEDE_API_KEY` | Optional | Per-agent API key. If unset, agent accepts any key (dev mode). |

Each agent uses its own `{AGENT_NAME}_API_KEY` env var for authentication.

## Tech Stack

- **FastAPI** — Web framework
- **LangChain** — LLM orchestration
- **GitHub Models (Azure OpenAI)** — GPT-4o-mini inference
- **Python 3.10+** — Runtime
- **Rich** — Beautiful terminal logging

## License

MIT

---

**Built by MicoDevPH**
