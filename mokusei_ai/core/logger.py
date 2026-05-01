import logging
import time
from rich.logging import RichHandler
from rich.console import Console
from rich.theme import Theme

# Custom theme for Mokusei AI - these are the colors for different log types
mokusei_theme = Theme({
    "info": "cyan",           # Normal messages - calm blue
    "warning": "yellow",      # Warnings - attention-grabbing yellow
    "error": "bold red",      # Errors - very noticeable red
    "success": "bold green",  # Success messages - happy green
    "agent": "magenta",       # Agent-specific logs - stands out
})

# Map your agents to specific colors for their moons
MOON_COLORS = {
    "Ganymede": "orange3",
    "Callisto": "brown",
    "Europa": "magenta",
    "Io": "orange3",
    "Default": "white"
}

# Create console with our custom theme
console = Console(theme=mokusei_theme)


def get_logger(name: str = "mokusei_ai") -> logging.Logger:
    """
    Create and return a configured Rich logger with Mokusei AI branding.
    
    What this does:
    - Adds pretty colors to different log levels
    - Shows timestamps so you know when things happened
    - Includes emojis for visual quick-scanning
    - Safe for CLI, agents, and FastAPI usage
    
    Args:
        name: The logger name (usually your module name)
        
    Returns:
        A configured logger instance
    """

    logger = logging.getLogger(name)

    # Prevent duplicate handlers
    # (Without this check, running the app multiple times adds more handlers,
    #  and you'd see the same log message repeated 2x, 3x, 4x... etc!)
    if logger.handlers:
        return logger

    # Set minimum log level - INFO means we ignore DEBUG messages
    logger.setLevel(logging.INFO)

    # RichHandler is what makes logs pretty with colors and formatting
    handler = RichHandler(
        console=console,
        show_time=True,        # Shows [04/26/26 09:38:56]
        show_level=True,       # Shows INFO, ERROR, etc.
        show_path=False,       # Hides file paths (keeps it clean)
        markup=True,           # Allows using [bold], [red], etc. in messages
        rich_tracebacks=True,  # Makes error tracebacks beautiful and readable
    )

    # Custom formatter with emojis for quick visual scanning
    # The %(message)s part is where your actual log message goes
    formatter = logging.Formatter(
        fmt="%(message)s",
        datefmt="[%m/%d/%y %H:%M:%S]"  # Formats the timestamp
    )

    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # Don't pass logs up to parent loggers (prevents duplicate logs)
    logger.propagate = False

    return logger

def log_agent_banner(logger: logging.Logger, agent_name: str):
    """Only prints the big top banner."""

    color = MOON_COLORS.get(agent_name, "magenta")

    spaced_name = " ".join(list(agent_name.upper()))
    console.print(f"\n[{color}]>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>[/{color}]")
    console.print(f"    [bold {color}]{spaced_name}   A G E N T   C A L L[/bold {color}]")
    console.print(f"[{color}]>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>[/{color}]\n")


# Example helper for success messages
def log_success(logger: logging.Logger, message: str):
    """Log a success message with a checkmark emoji."""
    logger.info(f"[success]✅ {message}[/success]")


# Example helper for warnings
def log_warning(logger: logging.Logger, message: str):
    """Log a warning message with a warning emoji."""
    logger.warning(f"[warning]⚠️  {message}[/warning]")


# Example helper for errors
def log_error(logger: logging.Logger, message: str):
    """Log an error message with an X emoji."""
    logger.error(f"[error]❌ {message}[/error]")


def log_agent_action(logger: logging.Logger, agent_name: str, message: str):
    """Log an agent action message with the agent moon color."""
    color = MOON_COLORS.get(agent_name, "magenta")
    logger.info(f"[agent][bold {color}]{agent_name}[/bold {color}] {message}[/agent]")


def log_execution_timer(logger: logging.Logger, start_time: float, message: str = "RESPONDED SUCCESSFULLY"):
    """Calculates elapsed time and logs the success message with a timer."""
    duration = time.perf_counter() - start_time
    # Logs the green square, message, and the duration in seconds
    logger.info(f"({duration:.2f}s)")



# Example usage (you can delete this part - it's just for demonstration)
if __name__ == "__main__":
    # Create a test logger
    test_logger = get_logger("test")
    
    # Show the startup banner
    log_agent_banner(test_logger, "Ganymede")
    
    # Test different log types
    log_success(test_logger, "Application started successfully")
    log_agent_action(test_logger, "Ganymede", "is ready to chat")
    log_warning(test_logger, "API key not found in environment")
    log_error(test_logger, "Failed to connect to database")
    test_logger.info("Regular info message without special formatting")