"""
Rich terminal output and display utilities for CLI.

Provides formatted console output using Rich library for better user experience.
"""

from pathlib import Path
from typing import List, Optional

from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.syntax import Syntax
from rich.table import Table
from rich.text import Text


# Create console instance
console = Console()


def display_error(message: str):
    """Display error message in red."""
    console.print(f"[bold red]✗[/bold red] {message}")


def display_success(message: str):
    """Display success message in green."""
    console.print(f"[bold green]✓[/bold green] {message}")


def display_info(message: str):
    """Display info message in cyan."""
    console.print(f"[cyan]ℹ[/cyan] {message}")


def display_warning(message: str):
    """Display warning message in yellow."""
    console.print(f"[yellow]⚠[/yellow] {message}")


def display_visual_result(file_paths: List[Path]):
    """
    Display generated visual file paths.
    
    Args:
        file_paths: List of generated file paths.
    """
    if not file_paths:
        return
    
    # Create table for files
    table = Table(
        title="Generated Files",
        show_header=True,
        header_style="bold cyan",
    )
    table.add_column("#", style="dim")
    table.add_column("Filename", style="green")
    table.add_column("Path", style="white")
    table.add_column("Size", style="yellow")
    
    for i, path in enumerate(file_paths, 1):
        # Get file size
        if path.exists():
            size = path.stat().st_size
            if size < 1024:
                size_str = f"{size} B"
            elif size < 1024 * 1024:
                size_str = f"{size / 1024:.1f} KB"
            else:
                size_str = f"{size / (1024 * 1024):.1f} MB"
        else:
            size_str = "N/A"
        
        table.add_row(
            str(i),
            path.name,
            str(path.parent),
            size_str,
        )
    
    console.print("\n")
    console.print(table)
    console.print()


def create_progress() -> Progress:
    """
    Create a progress spinner for long-running operations.
    
    Returns:
        Progress instance with spinner.
    """
    return Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
        transient=True,
    )


def display_api_response(data: dict, title: str = "API Response"):
    """
    Display API response data in formatted JSON.
    
    Args:
        data: Response data dictionary.
        title: Panel title.
    """
    import json
    
    # Format JSON with syntax highlighting
    json_str = json.dumps(data, indent=2, default=str)
    syntax = Syntax(json_str, "json", theme="monokai", line_numbers=False)
    
    # Display in panel
    panel = Panel(syntax, title=title, border_style="cyan")
    console.print(panel)


def display_style_preview(style_name: str, style_id: str, description: str):
    """
    Display a preview of a visual style.
    
    Args:
        style_name: Name of the style.
        style_id: Style ID.
        description: Style description.
    """
    content = f"""
[bold cyan]{style_name}[/bold cyan]
[dim]ID: {style_id}[/dim]

{description}
    """
    
    panel = Panel(
        content.strip(),
        title="Style Preview",
        border_style="green",
        padding=(1, 2),
    )
    console.print(panel)


def display_generation_summary(
    content: str,
    style: str,
    format: str,
    variations: int,
    **kwargs,
):
    """
    Display a summary of generation parameters.
    
    Args:
        content: Text content (truncated for display).
        style: Style name.
        format: Output format.
        variations: Number of variations.
        **kwargs: Additional parameters.
    """
    # Truncate content for display
    if len(content) > 100:
        display_content = content[:97] + "..."
    else:
        display_content = content
    
    # Create summary table
    table = Table(
        title="Generation Parameters",
        show_header=False,
        box=None,
    )
    table.add_column("Parameter", style="cyan")
    table.add_column("Value", style="white")
    
    # Add parameters
    table.add_row("Content", display_content)
    table.add_row("Style", style)
    table.add_row("Format", format.upper())
    table.add_row("Variations", str(variations))
    
    # Add optional parameters
    if kwargs.get("language"):
        table.add_row("Language", kwargs["language"])
    if kwargs.get("width"):
        table.add_row("Width", f"{kwargs['width']}px")
    if kwargs.get("height"):
        table.add_row("Height", f"{kwargs['height']}px")
    if kwargs.get("transparent"):
        table.add_row("Transparent", "Yes")
    if kwargs.get("inverted"):
        table.add_row("Inverted", "Yes")
    
    console.print(table)
    console.print()


def display_batch_progress(current: int, total: int, successful: int, failed: int):
    """
    Display batch generation progress.
    
    Args:
        current: Current item number.
        total: Total items.
        successful: Number of successful generations.
        failed: Number of failed generations.
    """
    # Create progress text
    progress = Text()
    progress.append(f"Progress: [{current}/{total}] ", style="cyan")
    progress.append(f"✓ {successful} ", style="green")
    if failed > 0:
        progress.append(f"✗ {failed}", style="red")
    
    console.print(progress)


def display_rate_limit_status(limit: int, remaining: int, reset_time: str):
    """
    Display current rate limit status.
    
    Args:
        limit: Total request limit.
        remaining: Remaining requests.
        reset_time: Time when limit resets.
    """
    # Calculate percentage
    percentage = (remaining / limit) * 100 if limit > 0 else 0
    
    # Choose color based on remaining
    if percentage > 50:
        color = "green"
    elif percentage > 20:
        color = "yellow"
    else:
        color = "red"
    
    # Create status text
    status = Text()
    status.append("Rate Limit: ", style="dim")
    status.append(f"{remaining}/{limit}", style=f"bold {color}")
    status.append(f" (resets at {reset_time})", style="dim")
    
    console.print(status)


def clear_screen():
    """Clear the terminal screen."""
    console.clear()


def print_divider(char: str = "─", style: str = "dim"):
    """
    Print a horizontal divider line.
    
    Args:
        char: Character to use for divider.
        style: Rich style for the divider.
    """
    width = console.width
    console.print(char * width, style=style)