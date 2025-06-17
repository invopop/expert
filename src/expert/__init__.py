"""
Invopop Expert - AI agent library for Invopop and GOBL documentation.

This package provides an AI-powered agent that can answer questions about
Invopop and GOBL using advanced retrieval-augmented generation (RAG) with
MCP (Model Context Protocol) servers.

Example usage:
    import asyncio
    from expert import InvopopExpert, Config
    
    async def main():
        config = Config()
        expert = InvopopExpert(config)
        await expert.setup()
        
        thread_config = {"configurable": {"thread_id": "my-conversation"}}
        response = await expert.get_response("How do I create an invoice?", thread_config)
        print(response)
    
    asyncio.run(main())
"""

from .agent import InvopopExpert
from .config import Config

__version__ = "0.1.0"
__all__ = ["InvopopExpert", "Config"]


