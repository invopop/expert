"""Main agent implementation for Invopop Expert."""

from pathlib import Path
from typing import Dict, Any

from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_core.tools import StructuredTool
from langgraph.checkpoint.memory import InMemorySaver

from .config import Config


class InvopopExpert:
    """Main agent class for Invopop Expert."""

    def __init__(self, config: Config):
        """Initialize the agent."""
        self.config = config
        self.agent = None
        self.checkpointer = InMemorySaver()
        self._load_prompts()

    def _load_prompts(self):
        """Load prompt templates from files."""
        prompts_dir = Path(__file__).parent / "prompts"

        with open(prompts_dir / "system_prompt.txt", "r") as f:
            self.system_prompt = f.read().strip()

        with open(prompts_dir / "invopop_docs_description.txt", "r") as f:
            self.invopop_docs_description = f.read().strip()

        with open(prompts_dir / "gobl_docs_description.txt", "r") as f:
            self.gobl_docs_description = f.read().strip()

    async def setup(self):
        """Initialize the MCP client and create the agent."""
        # Initialize the MultiServerMCPClient
        client = MultiServerMCPClient(self.config.mcp_config)

        # Get and rename tools
        tools = await client.get_tools()
        renamed_tools = []

        for tool in tools:
            if "invopop" in tool.description.lower():
                new_name = "invopop_search"
                new_description = self.invopop_docs_description
            elif "gobl" in tool.description.lower():
                new_name = "gobl_search"
                new_description = self.gobl_docs_description
            else:
                new_name = tool.name
                new_description = tool.description

            # Create a new StructuredTool with the new name
            renamed_tool = StructuredTool.from_function(
                coroutine=tool.coroutine,
                name=new_name,
                description=new_description,
                response_format=tool.response_format,
                args_schema=tool.args_schema,
            )
            renamed_tools.append(renamed_tool)

        # Create the agent
        llm_config = self.config.llm_config
        model_name = f"{llm_config.get('provider', 'openai')}:{llm_config.get('model', 'gpt-4.1')}"

        self.agent = create_react_agent(
            model_name,
            renamed_tools,
            checkpointer=self.checkpointer,
            prompt=self.system_prompt,
        )

    async def get_response(self, user_input: str, config: Dict[str, Any]) -> str:
        """Get response from the agent for a given input."""
        if not self.agent:
            raise RuntimeError("Agent not initialized. Call setup() first.")

        async for chunk in self.agent.astream(
            {"messages": [{"role": "user", "content": user_input}]}, config
        ):
            if "agent" in chunk:
                for message in chunk["agent"]["messages"]:
                    if "tool_calls" in message.additional_kwargs:
                        for tool_call in message.additional_kwargs["tool_calls"]:
                            func_name = tool_call["function"]["name"]
                            if func_name == "invopop_search":
                                print(
                                    "🔍 Searching Invopop docs:",
                                    tool_call["function"]["arguments"],
                                )
                            elif func_name == "gobl_search":
                                print(
                                    "🔍 Searching GOBL docs:",
                                   tool_call["function"]["arguments"],
                               )
                    # Update the final message content
                    final_message_content = message.content

        return final_message_content

    async def chat_loop(self):
        """Run an interactive chat loop."""
        if not self.agent:
            await self.setup()

        chat_config = self.config.chat_config
        print(chat_config.get("welcome_message", "Welcome to Invopop Expert!"))
        print(chat_config.get("input_prompt", "Enter your question:"))
        print("-" * 70)

        thread_config = {"configurable": {"thread_id": "1"}}

        while True:
            try:
                # Get user input
                print("\n👤 You: ", end="")
                user_input_lines = []
                while True:
                    line = input()
                    if not line:
                        break
                    user_input_lines.append(line)

                user_input = "\n".join(user_input_lines).strip()

                if not user_input:
                    continue

                if user_input.lower() in ["exit", "quit", "bye"]:
                    print("\n🤖 Goodbye!")
                    break

                # Get and print agent response
                print("\n🤖 Thinking...", flush=True)
                response = await self.get_response(user_input, thread_config)
                print(f"\n🤖 Assistant: {response}")

            except KeyboardInterrupt:
                print("\n\n🤖 Exiting...")
                break
            except Exception as e:
                print(f"\n❌ Error: {str(e)}")
                continue
