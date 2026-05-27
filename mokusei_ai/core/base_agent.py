import os
import re
import time
import inspect
from pathlib import Path
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, ToolMessage
from langchain_core.tools import tool
from mokusei_ai.core.logger import get_logger, log_agent_banner, log_success, log_execution_timer

load_dotenv()

OFF_TOPIC_PATTERNS = [
    r"write\s+(a\s+|some\s+|me\s+)?(a\s+|some\s+)?(code|function|program|script|app|website)",
    r"write\s+me\s+a\s+(code|function|program|script)",
    r"create\s+(a\s+|some\s+|me\s+)?(website|app|function|code|tool|program)",
    r"implement\s+(a\s+|me\s+)?\w*\s*(function|code|algorithm|feature)",
    r"^code\s+(this|me|a|the)",
    r"generate\s+(\w+\s+)*(code|function|program|script|website|app)",
    r"build\s+(a\s+|an\s+|me\s+)?(website|app|tool|program|function)",
    r"^debug\s+(this|my|the)\s+(code|script|app|function|program)",
    r"^fix\s+(this|my|the|a)\s+(code|bug|error)",
]


class BaseAgent:
    def __init__(self, api_key: str = None, agent_name: str = None):
        self.agent_name = agent_name or self.__class__.__name__.replace("Agent", "")
        self.logger = get_logger(self.agent_name.upper())

        expected = os.getenv(f"{self.agent_name.upper()}_API_KEY")
        if expected:
            if not api_key:
                raise PermissionError(f"API key required for '{self.agent_name}'.")
            if api_key != expected:
                raise PermissionError(f"Invalid API key for '{self.agent_name}'.")

        key = os.getenv("GITHUB_TOKEN")
        if not key:
            self.logger.error("Failed to initialize: GITHUB_TOKEN missing.")
            raise ValueError("Server misconfigured: GITHUB_TOKEN missing.")

        self.version = getattr(self.__class__, 'version', "1.0")
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

    def _is_off_topic(self, message: str) -> str | None:
        for pattern in OFF_TOPIC_PATTERNS:
            if re.search(pattern, message, re.IGNORECASE):
                return "I'm here to talk about the portfolio owner and their work! Got any questions about their projects, skills, or background?"
        return None

    def _contains_code(self, text: str) -> bool:
        return bool(re.search(r"```", text))

    def _search_portfolio(self, query: str, portfolio: str) -> str:
        sections = re.split(r"(?m)^##\s", portfolio)
        if sections and sections[0].strip() == "":
            sections = sections[1:]

        query_lower = query.lower()
        query_terms = query_lower.split()

        matched = []
        for section in sections:
            text = section.strip()
            if not text:
                continue
            lines = text.split("\n")
            header = lines[0]
            body = "\n".join(lines[1:]).strip()
            section_lower = text.lower()
            if any(term in section_lower for term in query_terms):
                label = f"## {header}" if header else ""
                matched.append(f"{label}\n{body}" if label and body else label or body)

        if not matched:
            return "No matching information found in the portfolio."

        result = "\n\n".join(matched)
        if len(result) > 3000:
            result = result[:3000] + "..."
        return result

    async def chat(self, message: str, context: str = None, portfolio: str = None, summary: str = None) -> str:
        start_time = time.perf_counter()

        log_agent_banner(self.logger, self.agent_name)
        self.logger.info(f"{self.agent_name} [bold white]{self.version}[/bold white]")
        self.logger.info(f"{self.agent_name} receiving message: {message[:50]}...")

        redirect = self._is_off_topic(message)
        if redirect:
            self.logger.info(f"{self.agent_name} redirected off-topic request")
            log_success(self.logger, "REDIRECTED OFF-TOPIC REQUEST")
            log_execution_timer(self.logger, start_time)
            return redirect

        system_content = self.persona
        if summary:
            system_content += f"\n\n## Portfolio Summary\n{summary}"
        elif portfolio:
            system_content += f"\n\n## Portfolio Context\n{portfolio}"
        if context:
            system_content += f"\n\n## Conversation History\n{context}"

        if portfolio:
            @tool
            def search_portfolio(query: str) -> str:
                """Search the portfolio for information matching the query. Use this to find specific details about projects, skills, experience, education, or anything else."""
                return self._search_portfolio(query, portfolio)

            llm = self.llm.bind_tools([search_portfolio])
        else:
            llm = self.llm

        messages = [
            SystemMessage(content=system_content),
            HumanMessage(content=message)
        ]

        response = await llm.ainvoke(messages)

        if hasattr(response, "tool_calls") and response.tool_calls:
            self.logger.info(f"{self.agent_name} searching portfolio for: {response.tool_calls[0].get('args', {}).get('query', '')}")
            for tc in response.tool_calls:
                result = search_portfolio.invoke(tc["args"])
                messages.append(ToolMessage(content=result, tool_call_id=tc["id"]))
            response = await llm.ainvoke(messages)

        if self._contains_code(response.content):
            response_text = "I'm a portfolio assistant — I don't generate code. Want to ask about the owner's projects or experience instead?"
        else:
            response_text = response.content

        log_success(self.logger, "RESPONDED SUCCESSFULLY")
        log_execution_timer(self.logger, start_time)

        return response_text
