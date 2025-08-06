"""
CLI commands for Napkin AI API Playground.

Provides command-line interface for generating visuals using the Napkin API.
"""

import asyncio
import logging
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.logging import RichHandler

from ..core.generator import generate_visual
from ..utils.config import get_settings
from ..utils.constants import STYLES
from ..api.client import NapkinAPIError, AuthenticationError, RateLimitError
from .display import (
    display_error,
    display_success,
    display_info,
    display_visual_result,
    create_progress,
)


# Create Typer app
app = typer.Typer(
    name="napkin",
    help="Napkin AI API Playground - Generate beautiful visuals from text",
    no_args_is_help=True,
    add_completion=True,
)

# Console for rich output
console = Console()


def setup_logging(level: str = "INFO"):
    """Configure logging with Rich handler."""
    logging.basicConfig(
        level=level,
        format="%(message)s",
        handlers=[
            RichHandler(
                console=console,
                rich_tracebacks=True,
                tracebacks_show_locals=False,
            )
        ],
    )


@app.command()
def generate(
    content: str = typer.Argument(
        ...,
        help="Text content to generate visual from",
    ),
    style: Optional[str] = typer.Option(
        None,
        "--style",
        "-s",
        help="Visual style name or ID (e.g., 'vibrant-strokes')",
    ),
    format: Optional[str] = typer.Option(
        None,
        "--format",
        "-f",
        help="Output format: svg or png",
    ),
    output: Optional[Path] = typer.Option(
        None,
        "--output",
        "-o",
        help="Output directory for generated files",
    ),
    variations: Optional[int] = typer.Option(
        None,
        "--variations",
        "-n",
        help="Number of variations to generate (1-4)",
        min=1,
        max=4,
    ),
    language: Optional[str] = typer.Option(
        None,
        "--language",
        "-l",
        help="Language code (BCP 47 format, e.g., 'en-US')",
    ),
    context_before: Optional[str] = typer.Option(
        None,
        "--context-before",
        help="Context before the main content",
    ),
    context_after: Optional[str] = typer.Option(
        None,
        "--context-after",
        help="Context after the main content",
    ),
    width: Optional[int] = typer.Option(
        None,
        "--width",
        "-w",
        help="Width in pixels (PNG only)",
        min=100,
        max=4096,
    ),
    height: Optional[int] = typer.Option(
        None,
        "--height",
        "-h",
        help="Height in pixels (PNG only)",
        min=100,
        max=4096,
    ),
    transparent: bool = typer.Option(
        False,
        "--transparent",
        help="Enable transparent background",
    ),
    inverted: bool = typer.Option(
        False,
        "--inverted",
        help="Invert colors",
    ),
    debug: bool = typer.Option(
        False,
        "--debug",
        help="Enable debug logging",
    ),
):
    """
    Generate visual from text content.

    Examples:
        napkin generate "Machine Learning Pipeline"
        napkin generate "Data Flow" --style sketch-notes --format png
        napkin generate "Architecture" -s corporate-clean -n 3 -o ./output
    """
    # Setup logging
    setup_logging("DEBUG" if debug else "INFO")

    try:
        # Load settings
        settings = get_settings()

        # Validate format if specified
        if format and format.lower() not in ["svg", "png"]:
            display_error(f"Invalid format: {format}. Must be 'svg' or 'png'")
            raise typer.Exit(1)

        # Show generation info
        style_name = style or settings.default_style
        output_format = format or settings.default_format
        num_variations = variations or settings.default_variations

        display_info(
            f"Generating {num_variations} visual(s) in {output_format} format "
            f"with style '{style_name}'"
        )

        # Create progress spinner
        with create_progress() as progress:
            task = progress.add_task(
                "[cyan]Creating visual...",
                total=None,
            )

            # Run async generation
            status, file_paths = asyncio.run(
                generate_visual(
                    content=content,
                    style=style,
                    format=format,
                    output_dir=output,
                    language=language,
                    variations=variations,
                    context_before=context_before,
                    context_after=context_after,
                    transparent=transparent,
                    inverted=inverted,
                    width=width,
                    height=height,
                )
            )

            progress.update(task, completed=True)

        # Display results
        if file_paths:
            display_visual_result(file_paths)
            display_success(f"Successfully generated {len(file_paths)} visual(s)")
        else:
            display_error("No files were generated")
            raise typer.Exit(1)

    except AuthenticationError as e:
        display_error(f"Authentication failed: {e}")
        display_info("Please check your NAPKIN_API_TOKEN environment variable")
        raise typer.Exit(1)
    except RateLimitError as e:
        display_error(f"Rate limit exceeded: {e}")
        display_info(f"Please wait {e.retry_after} seconds before retrying")
        raise typer.Exit(1)
    except NapkinAPIError as e:
        display_error(f"API error: {e}")
        raise typer.Exit(1)
    except Exception as e:
        if debug:
            console.print_exception()
        else:
            display_error(f"Unexpected error: {e}")
            display_info("Use --debug for more details")
        raise typer.Exit(1)


@app.command()
def styles(
    list_all: bool = typer.Option(
        False,
        "--list",
        "-l",
        help="List all available styles",
    ),
    category: Optional[str] = typer.Option(
        None,
        "--category",
        "-c",
        help="Filter by category (colorful, casual, hand_drawn, formal, monochrome)",
    ),
):
    """
    List and explore available visual styles.

    Examples:
        napkin styles --list
        napkin styles --category colorful
    """
    from ..utils.constants import StyleCategory, get_styles_by_category
    from rich.table import Table

    # Create table for displaying styles
    table = Table(
        title="Available Visual Styles",
        show_header=True,
        header_style="bold cyan",
    )
    table.add_column("Style Name", style="green")
    table.add_column("Category", style="yellow")
    table.add_column("Description", style="white")

    # Filter styles if category specified
    if category:
        try:
            cat_enum = StyleCategory(category.lower())
            styles_to_show = get_styles_by_category(cat_enum)
        except ValueError:
            display_error(f"Invalid category: {category}")
            display_info(
                "Valid categories: colorful, casual, hand_drawn, formal, monochrome"
            )
            raise typer.Exit(1)
    else:
        styles_to_show = list(STYLES.values())

    # Add styles to table
    for style in styles_to_show:
        table.add_row(
            style.name,
            style.category.value,
            style.description,
        )

    # Display table
    console.print(table)
    console.print(f"\n[dim]Total styles: {len(styles_to_show)}[/dim]")


@app.command()
def config(
    show: bool = typer.Option(
        False,
        "--show",
        "-s",
        help="Show current configuration",
    ),
    check: bool = typer.Option(
        False,
        "--check",
        "-c",
        help="Check configuration validity",
    ),
):
    """
    Manage configuration settings.

    Examples:
        napkin config --show
        napkin config --check
    """
    from rich.table import Table

    try:
        settings = get_settings()

        if check:
            # Check configuration
            display_success("Configuration is valid")

            # Check API token
            if not settings.api_token:
                display_error("NAPKIN_API_TOKEN is not set")
                raise typer.Exit(1)
            else:
                display_info("API token is configured")

        if show or not check:
            # Show configuration
            table = Table(
                title="Current Configuration",
                show_header=True,
                header_style="bold cyan",
            )
            table.add_column("Setting", style="yellow")
            table.add_column("Value", style="white")

            # Add non-sensitive settings
            config_items = [
                ("API Base URL", settings.api_base_url),
                ("Default Style", settings.default_style),
                ("Default Format", settings.default_format),
                ("Default Language", settings.default_language),
                ("Default Variations", str(settings.default_variations)),
                ("Storage Path", str(settings.storage_path)),
                ("Log Level", settings.log_level),
                ("API Token", "****" if settings.api_token else "[red]NOT SET[/red]"),
            ]

            for key, value in config_items:
                table.add_row(key, value)

            console.print(table)

    except Exception as e:
        display_error(f"Configuration error: {e}")
        display_info("Please check your .env file or environment variables")
        raise typer.Exit(1)


@app.command()
def version():
    """Show version information."""
    from rich.panel import Panel

    version_info = """
[bold cyan]Napkin AI API Playground[/bold cyan]
Version: 0.1.3
Python Client for Napkin AI Visual Generation API
    
[dim]API Version: v1
Documentation: https://github.com/yourusername/napkin-api-playground[/dim]
    """

    console.print(Panel(version_info.strip(), title="About", border_style="cyan"))


def main():
    """Main CLI entry point."""
    app()


if __name__ == "__main__":
    main()
