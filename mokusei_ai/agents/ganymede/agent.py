import os
import time
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from mokusei_ai.core.logger import get_logger
from mokusei_ai.core.logger import log_agent_banner, log_success, log_error, log_execution_timer
load_dotenv()
logger = get_logger("GANYMEDE")

class GanymedeAgent:
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
        self.persona = "You are GANYMEDE, the Personal Assistant Specialist..."
        self.version = "1.0"

    async def chat(self, message: str) -> str:
        start_time = time.perf_counter()

        # 1. Print the banner ONCE at the start
        log_agent_banner(logger, "Ganymede")
        
         # 2. Log Version
        logger.info(f"Ganymede [bold white]{self.version}[/bold white]")

        # 3. Print the receiving message (standard log)
        logger.info(f"Ganymede receiving message: {message[:30]}...")

        messages = [SystemMessage(content=self.persona), HumanMessage(content=message)]
        response = await self.llm.ainvoke(messages)

        # 4. Print the success line (green)
        log_success(logger, "RESPONDED SUCCESSFULLY")

        
        log_execution_timer(logger, start_time)
        
        return response.content
