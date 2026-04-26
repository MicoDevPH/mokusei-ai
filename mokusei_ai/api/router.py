from fastapi import APIRouter, HTTPException
from functools import lru_cache
from pydantic import BaseModel
from mokusei_ai.agents.registry import get_agent

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    api_key: str | None = None  # optional, falls back to .env

# ✅ Cache agent instances — one per agent name, not recreated every request
@lru_cache(maxsize=None)
def get_cached_agent(agent_name: str, api_key: str | None = None):
    return get_agent(agent_name, api_key=api_key)

@router.post("/agents/{agent_name}/chat")
async def chat(agent_name: str, req: ChatRequest):
    try:
        agent = get_cached_agent(agent_name, req.api_key)
        response = await agent.chat(req.message)

        return {
            "agent": agent_name,
            "response": response
        }

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))