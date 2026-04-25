from rich.console import Console

# Jupiter Colorway
RUST = "#a52a2a"    # Great Red Spot
BELT = "#a0522d"    # Deep Brownish Belt
GOLD = "#fdf5e6"    # Creamy Ammonia Zone
AMBER = "#ffbf00"   # New: Orangy Yellow (Vibrant Jupiter Amber)


console = Console()

class MokuseiLogger:
    @staticmethod
    def log_request(message: str):
        width = console.width
        # 1. Double dashes make the border look "Thick" and "Big"
        dash_line = ">" * width
        
        console.print("\n")
        # 2. Print the line twice for a heavy-weight border
        console.print(f"[bold {BELT}]{dash_line}[/bold {BELT}]")
        
        # 3. Spaced out and Uppercase letters make the title feel massive
        title = "   MOKUSEI UPLINK AGENT CALL"
        console.print(f"[bold {AMBER}]{title}[/bold {AMBER}]")
        
        # 4. Repeat bottom lines
        console.print(f"[bold {BELT}]{dash_line}[/bold {BELT}]")
        
        console.print(
            f"\n [dim #aaaaaa]SOURCE:[/] [bold {GOLD}]MicoDevPH[/] "
            f"[dim #aaaaaa]>>[/] "
            f"[bold {AMBER}]SIGNAL_INPUT:[/] [bold {GOLD}]\"{message}\"[/]\n"
        )
    # Missing functions to prevent the long red error from before
    @staticmethod
    def log_info(text: str):
        # Uses a gear emoji and the Belt color for consistent branding
        console.log(f"⚙️  [bold {BELT}]SYSTEM:[/][#d2b48c] {text}[/]")

    @staticmethod
    def log_success(text: str):
        # Professional Success checkmark with bold green
        console.log(f"✅ [bold green]SUCCESS:[/][white] {text.upper()}[/]")

    @staticmethod
    def log_error(text: str):
        # High-visibility error tag
        console.log(f"🚨 [bold red]CRITICAL:[/][white] {text}[/]")
