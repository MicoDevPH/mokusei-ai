from mokusei_ai.agents.ganymede.agent import GanymedeAgent

AGENTS = {
    "ganymede": GanymedeAgent,
}

def get_agent_class(name: str):
    cls = AGENTS.get(name.lower())
    if not cls:
        raise ValueError(f"Unknown agent: {name}")
    return cls

def get_agent(name: str, api_key: str = None):
    cls = get_agent_class(name)
    return cls(api_key=api_key)