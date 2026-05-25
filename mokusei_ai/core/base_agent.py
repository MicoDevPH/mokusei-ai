import os
import time
import inspect
from pathlib import Path
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from mokusei_ai.core.logger import get_logger, log_agent_banner, log_success, log_execution_timer

load_dotenv()


class BaseAgent:
    def __init__(self, api_key: str = None, agent_name: str = None):
        self.agent_name = agent_name or self.__class__.__name__.replace("Agent", "")
        self.logger = get_logger(self.agent_name.upper())

        # Validate per-agent API key
        expected = os.getenv(f"{self.agent_name.upper()}_API_KEY")
        if expected:
            if not api_key:
                raise PermissionError(f"API key required for '{self.agent_name}'.")
            if api_key != expected:
                raise PermissionError(f"Invalid API key for '{self.agent_name}'.")

        # Use server's own key for LLM calls
        key = os.getenv("GITHUB_TOKEN")
        if not key:
            self.logger.error("Failed to initialize: GITHUB_TOKEN missing.")
            raise ValueError("Server misconfigured: GITHUB_TOKEN missing.")

        self.version = "1.0"
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            openai_api_key=key,
            base_url="https://models.inference.ai.azure.com"
        )
        self.persona = self._load_persona()

    def _load_persona(self) -> str:
        module_path = inspect.getfile(self.__class__)
        prompts_dir = Path(module_path).parent / "prompts"
        moon = self.agent_name.lower()
        parts = []

        for filename in [f"{moon}_instructions.xml", "persona.xml"]:
            path = prompts_dir / filename
            if path.exists():
                content = path.read_text(encoding="utf-8")
                lines = [l for l in content.split("\n") if not l.strip().startswith("<?xml")]
                parts.append("\n".join(lines))

        return "\n\n".join(parts) if parts else f"You are {self.agent_name}, an AI assistant."

    async def chat(self, message: str, context: str = None, portfolio: str = None) -> str:
        start_time = time.perf_counter()

        log_agent_banner(self.logger, self.agent_name)
        self.logger.info(f"{self.agent_name} [bold white]{self.version}[/bold white]")
        self.logger.info(f"{self.agent_name} receiving message: {message[:50]}...")

        system_content = self.persona
        if portfolio:
            system_content += f"\n\n## Portfolio Context\n{portfolio}"
        if context:
            system_content += f"\n\n## Conversation History\n{context}"

        messages = [
            SystemMessage(content=system_content),
            HumanMessage(content=message)
        ]
        response = await self.llm.ainvoke(messages)

        log_success(self.logger, "RESPONDED SUCCESSFULLY")
        log_execution_timer(self.logger, start_time)

        return response.content
