from mokusei_ai.agents.ganymede.agent import GanymedeAgent
# from mokusei_ai.agents.io.agent import IoAgent
# from mokusei_ai.agents.europa.agent import EuropaAgent

AGENTS = {
    "ganymede": GanymedeAgent,
    # "io": IoAgent,
    # "europa": EuropaAgent,
}

def get_agent(name: str):
    cls = AGENTS.get(name.lower())
    if not cls:
        raise ValueError(f"Unknown agent: {name}")
    return cls()