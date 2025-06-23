"""Configuration management for Invopop Expert."""

import os
from pathlib import Path
from typing import Any

import yaml
from dotenv import load_dotenv


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
            raise FileNotFoundError(
                f"Configuration file not found: {self.config_path}"
            ) from e
        except yaml.YAMLError as e:
            raise ValueError(f"Invalid YAML configuration: {e}") from e

    def _validate_env_vars(self):
        """Validate required environment variables."""
        if not os.getenv("OPENAI_API_KEY"):
            raise ValueError("OPENAI_API_KEY environment variable is required")

    @property
    def openai_api_key(self) -> str:
        """Get OpenAI API key."""
        return os.getenv("OPENAI_API_KEY")

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
                server_config["args"] = [
                    os.path.expanduser(arg) for arg in server_config["args"]
                ]

        return config

    @property
    def chat_config(self) -> dict[str, Any]:
        """Get chat configuration."""
        return self.config.get("chat", {})
