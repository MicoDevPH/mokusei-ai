import typer
import asyncio
from rich.console import Console

from mokusei_ai.agents.ganymede.agent import GanymedeAgent
from mokusei_ai.agents.europa.agent import EuropaAgent
from mokusei_ai.core.logger import get_logger

app = typer.Typer()
console = Console()

logger = get_logger("CLI")


@app.command()
def run(agent: str):
    """
    Run a specific Mokusei AI agent.
    Example:
        mokusei-ai run ganymede
    """

    logger.info(f"Starting agent: {agent}")

    if agent == "ganymede":
        console.print("[bold green]Launching Ganymede Agent...[/bold green]")

        ganymede = GanymedeAgent()
        response = asyncio.run(
            ganymede.chat("What is your mission objective?")
        )

        console.print(f"\n[GANYMEDE]: {response}\n")

    elif agent == "europa":
        console.print("[bold pink]Launching Europa Agent...[/bold pink]")

        europa = EuropaAgent()
        response = asyncio.run(
            europa.chat("Where do you want to go?")
        )
    else:
        console.print(f"[red]Unknown agent:[/red] {agent}")


@app.command()
def agents():
    """
    List available agents
    """
    console.print("""
Available Mokusei AI Agents:
- Ganymede (Personal Assistant)
- Europa (Travel Agent)
""")


@app.command()
def start():
    """
    Default entry point (optional)
    """
    console.print("[bold cyan]Mokusei AI is running...[/bold cyan]")


if __name__ == "__main__":
    app()