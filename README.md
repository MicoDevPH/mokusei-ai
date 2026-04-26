# Mokusei AI

**A multi-agent AI framework powered by Jupiter's moons** 🪐

## Overview

Mokusei AI is a specialized AI agent system where each "moon" represents a unique AI assistant with its own personality and expertise. Built with FastAPI and LangChain, it provides a clean, extensible architecture for deploying multiple specialized agents through a single unified API.

## The Moon System

Each moon in the Mokusei system is a distinct AI agent optimized for specific use cases:

- **🌙 Ganymede** — Personal Assistant Specialist  
  Lives on portfolio websites as a friendly AI assistant that answers visitor questions about the owner's work, skills, and projects. Talks like a supportive homie with authentic enthusiasm.

- **🌙 Europa** — Travel Agent *(coming soon)*  
  Designed for high-adventure trip planning. Lives on travel and booking platforms as a proactive concierge that scouts destinations, handles reservations, and tracks flight updates. Talks like a seasoned backpacker who knows all the best local spots and hidden gem

- **🌙 More moons in development...**

## Features

- 🚀 **FastAPI-powered** — Fast, modern REST API
- 🔌 **Plug-and-play agents** — Add new moon agents by dropping in a folder
- 🎭 **Distinct personalities** — Each agent has its own tone, style, and expertise
- 📦 **pip installable** — Use as a package in any Python project
- 🛠️ **LangChain integration** — Powered by GPT-4 via Azure OpenAI
- 🎨 **Beautiful CLI** — Jupiter-themed startup experience

## Installation

```bash
pip install mokusei-ai
```

## Quick Start

```python
from mokusei_ai.agents.ganymede import GanymedeAgent

# Initialize Ganymede
agent = GanymedeAgent(api_key="your-openai-key")

# Chat with the agent
response = await agent.chat("Tell me about the portfolio owner's React projects")
print(response)
```

## API Usage

```bash
# Start the server
uvicorn mokusei_ai.main:app --reload

# Chat with any moon agent
curl -X POST http://localhost:8000/api/agents/ganymede/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What skills does the owner have?"}'
```

## Architecture

```
mokusei-ai/
├── mokusei_ai/
│   ├── agents/
│   │   ├── ganymede/      # Personal Assistant Specialist
│   │   ├── europa/        # Travel Agent (coming soon)
│   │   └── registry.py    # Agent registration
│   ├── api/
│   │   └── router.py      # FastAPI routes
│   ├── core/
│   │   └── logger.py      # Logging utilities
│   └── main.py            # FastAPI app
```

## Adding a New Moon Agent

1. Create a new folder in `mokusei_ai/agents/`
2. Add your agent class in `agent.py`
3. Register it in `agents/registry.py`
4. Done — it's automatically available via the API

## Use Cases

- **Portfolio Websites** — Embed Ganymede as a chat assistant for visitors
- **Travel and Booking Platforms** — Use Europa for tutoring and learning support
- **Custom AI Workflows** — Build specialized agents for specific domains

## Tech Stack

- **FastAPI** — Web framework
- **LangChain** — LLM orchestration
- **Azure OpenAI** — GPT-4 models
- **Python 3.10+** — Runtime

## Roadmap

- [ ] Europa agent (Travel Agent)
- [ ] Io agent (Creative Writing Specialist)
- [ ] Callisto agent (Data Analysis Specialist)
- [ ] Streaming responses
- [ ] Conversation memory across sessions
- [ ] Function calling / tool use
- [ ] PyPI publishing

## Philosophy

Mokusei AI is built on the idea that different tasks need different AI personalities. Instead of one generic assistant trying to do everything, each moon specializes deeply in its domain — with its own voice, expertise, and approach.

## Contributing

This is an early-stage project. Contributions, ideas, and feedback are welcome!

## License

MIT

---

**Built by [MicoDevPH](https://github.com/MicoDevPH)** 🚀
