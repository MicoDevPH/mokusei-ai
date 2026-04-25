import asyncio
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from mokusei_ai.core.logger import get_logger

# Initialize environment and logger
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

    async def chat(self, message: str):
        logger.info(f"Ganymede receiving message: {message[:30]}...")
        messages = [SystemMessage(content=self.persona), HumanMessage(content=message)]
        
        # LangChain's invoke is synchronous; wrap it if you want true async 
        # or just keep it simple for now:
        response = self.llm.invoke(messages)
        
        logger.info("Ganymede successfully generated response.")
        return response.content

async def main():
    # Aesthetic Header with Logger
    logger.info("SYSTEM START: GANYMEDE PROTOCOL")
    agent = GanymedeAgent()
    
    user_input = "What is your mission objective?"
    response = await agent.chat(user_input)
    
    print(f"\n[USER]: {user_input}")
    print(f"[GANYMEDE]: {response}\n")
    logger.info("SYSTEM SHUTDOWN: GANYMEDE PROTOCOL")

if __name__ == "__main__":
    asyncio.run(main())
