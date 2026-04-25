import logging
from rich.logging import RichHandler
from rich.console import Console


console = Console()


def get_logger(name: str = "mokusei_ai") -> logging.Logger:
    """
    Create and return a configured Rich logger.
    Safe for CLI, agents, and FastAPI usage.
    """

    logger = logging.getLogger(name)

    # Prevent duplicate handlers (important in CLI apps)
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    handler = RichHandler(
        console=console,
        show_time=True,
        show_level=True,
        show_path=False,
        markup=True,
    )

    formatter = logging.Formatter(
        fmt="%(message)s"
    )

    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger