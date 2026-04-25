from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
import os

class EuropaAgent:
    """
    Mokusei AI: Europa Protocol
    The 'Creative & Human Specialist' moon.
    Designed for brainstorming, empathy, and creative writing.
    """
    def __init__(self, api_key: str = None):
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            openai_api_key=api_key or os.getenv("GITHUB_TOKEN"),
            base_url="https://azure.com"
        )
        self.persona = (
            "You are EUROPA, the Creative Specialist of the Mokusei AI system. "
            "Named after the icy moon with a hidden ocean, you are intuitive, "
            "friendly, and imaginative. Your goal is to help users find creative "
            "solutions and write with a warm, human tone."
        )

    def chat(self, message: str):
        return self.llm.invoke([SystemMessage(content=self.persona), HumanMessage(content=message)])
