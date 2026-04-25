
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from mokusei_ai.agents.registry import get_agent

router = APIRouter()

class ChatRequest(BaseModel):
    message: str

@router.post("/agents/{agent_name}/chat")
async def chat(agent_name: str, req: ChatRequest):
    try:
        agent = get_agent(agent_name)
        response = await agent.chat(req.message)

        return {
            "agent": agent_name,
            "response": response
        }

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))