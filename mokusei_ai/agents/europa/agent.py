import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from mokusei_ai.core.logger import get_logger
from mokusei_ai.core.logger import log_agent_banner, log_success
load_dotenv()
logger = get_logger("EUROPA")

class EuropaAgent:
    def __init__(self, api_key: str = None):
        key = api_key or os.getenv("GITHUB_TOKEN")
        if not key:
            logger.error("Failed to initialize: GITHUB_TOKEN missing.")
            raise ValueError("No API key found.")

        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            openai_api_key=key,
            base_url="https://models.inference.ai.azure.com"
        )
        self.persona = "You are EUROPA, the Travel Agent ..."
        self.version = "1.0"

    
    async def chat(self, message: str) -> str:
        # 1. Print the banner ONCE at the start
        log_agent_banner(logger, "Europa")
        
        # 2. Log Version
        logger.info(f"Europa [bold white]{self.version}[/bold white]")

        # 3. Print the receiving message (standard log)
        logger.info(f"Europa receiving message: {message[:30]}...")

        messages = [SystemMessage(content=self.persona), HumanMessage(content=message)]
        response = await self.llm.ainvoke(messages)

        # 4. Print the success line (green)
        log_success(logger, "RESPONDED SUCCESSFULLY")
        
        return response.content