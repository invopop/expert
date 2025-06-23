"""Main CLI entry point for Invopop Expert."""

import asyncio
import sys

import click

from .agent import InvopopExpert
from .config import Config


@click.command()
@click.option("--config", "-c", help="Path to configuration file")
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose output")
def cli(config: str, verbose: bool):
    """Invopop Expert - AI agent for Invopop and GOBL documentation."""
    try:
        # Initialize configuration
        config_obj = Config(config) if config else Config()

        if verbose:
            print(f"🔧 Configuration loaded from: {config_obj.config_path}")
            print(f"🤖 Using model: {config_obj.llm_config.get('model', 'gpt-4o')}")

        # Create and run the agent
        expert = InvopopExpert(config_obj)
        asyncio.run(expert.chat_loop())

    except Exception as e:
        click.echo(f"❌ Error: {str(e)}", err=True)
        sys.exit(1)


if __name__ == "__main__":
    cli()
