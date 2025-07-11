"""Configuration management for Invopop Expert."""

import os
from pathlib import Path
from typing import Any

import yaml
from dotenv import load_dotenv
from langgraph.checkpoint.base import BaseCheckpointSaver
from langgraph.checkpoint.memory import InMemorySaver


class Config:
    """Configuration manager for Invopop Expert."""

    def __init__(self, config_path: str | None = None):
        """Initialize configuration."""
        # Load environment variables
        load_dotenv()

        # Load YAML config
        if config_path is None:
            config_path = Path(__file__).parent.parent.parent / "config.yaml"

        self.config_path = Path(config_path)
        self.config = self._load_config()

        # Validate required environment variables
        self._validate_env_vars()

    def _load_config(self) -> dict[str, Any]:
        """Load configuration from YAML file."""
        try:
            with open(self.config_path) as f:
                return yaml.safe_load(f)
        except FileNotFoundError as e:
            raise FileNotFoundError(f"Configuration file not found: {self.config_path}") from e
        except yaml.YAMLError as e:
            raise ValueError(f"Invalid YAML configuration: {e}") from e

    def _validate_env_vars(self):
        """Validate required environment variables."""
        if not os.getenv("OPENAI_API_KEY"):
            raise ValueError("OPENAI_API_KEY environment variable is required")

        # Opik configuration - check if either env vars are set or opik is configured
        opik_api_key = os.getenv("OPIK_API_KEY")

        if not opik_api_key:
            # Inform about Opik configuration options
            print("ℹ️  Opik tracing is not configured.")
            print("   This is optional but enables tracking of agent interactions.")
            print("   To enable Opik tracing, you can:")
            print("   1. Set OPIK_API_KEY environment variable")
            print("   2. Run 'opik configure' to set up Opik configuration")

    @property
    def opik_api_key(self) -> str | None:
        """Get Opik API key."""
        return os.getenv("OPIK_API_KEY")

    @property
    def opik_config(self) -> dict[str, Any]:
        """Get Opik configuration."""
        config = self.config.get("opik", {})

        opik_project_name = os.getenv("OPIK_PROJECT_NAME")
        if opik_project_name:
            config["project_name"] = opik_project_name

        return config

    @property
    def llm_config(self) -> dict[str, Any]:
        """Get LLM configuration."""
        return self.config.get("llm", {})

    @property
    def mcp_config(self) -> dict[str, Any]:
        """Get MCP server configuration."""
        config = self.config.get("mcp", {}).get("servers", {})

        # Override with environment variables if provided
        invopop_path = os.getenv("INVOPOP_MCP_PATH")
        if invopop_path:
            config["invopop"]["args"] = [invopop_path]

        gobl_path = os.getenv("GOBL_MCP_PATH")
        if gobl_path:
            config["gobl"]["args"] = [gobl_path]

        # Expand home directory paths
        for server_config in config.values():
            if "args" in server_config:
                server_config["args"] = [os.path.expanduser(arg) for arg in server_config["args"]]

        return config

    @property
    def chat_config(self) -> dict[str, Any]:
        """Get chat configuration."""
        return self.config.get("chat", {})

    @property
    def checkpointer(self) -> BaseCheckpointSaver | None:
        """Get checkpointer configuration."""
        checkpointer = self.config.get("checkpointer", None)
        match checkpointer:
            case "memory":
                return InMemorySaver()
            case None:
                return None
            case _:
                raise ValueError(f"Invalid checkpointer configuration: {checkpointer}")
