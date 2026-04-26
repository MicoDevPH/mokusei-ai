from mokusei_ai.agents.ganymede.agent import GanymedeAgent
from mokusei_ai.agents.europa.agent import EuropaAgent

AGENTS = {
    "ganymede": GanymedeAgent,
    "europa": EuropaAgent,
}

def get_agent(name: str, api_key: str = None):
    cls = AGENTS.get(name.lower())
    if not cls:
        raise ValueError(f"Unknown agent: {name}")
    return cls(api_key=api_key)  # ✅ pass api_key down