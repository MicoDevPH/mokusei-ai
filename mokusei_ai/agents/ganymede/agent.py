from mokusei_ai.core.base_agent import BaseAgent


class GanymedeAgent(BaseAgent):
    version = "1.2"

    def __init__(self, api_key: str = None):
        super().__init__(api_key)
