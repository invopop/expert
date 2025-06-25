"""Main agent implementation for Invopop Expert."""

from datetime import datetime
from pathlib import Path

from langchain_core.tools import StructuredTool
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.prebuilt import create_react_agent
from opik.integrations.langchain import OpikTracer

from .config import Config


class InvopopExpert:
    """Main agent class for Invopop Expert."""

    def __init__(self, config: Config):
        """Initialize the agent."""
        self.config = config
        self.agent = None
        self.checkpointer = InMemorySaver()
        self._load_prompts()
        self.opik_config = None

    def _load_prompts(self):
        """Load prompt templates from files."""
        prompts_dir = Path(__file__).parent / "prompts"

        with open(prompts_dir / "system_prompt.md") as f:
            self.system_prompt = f.read().strip()

        with open(prompts_dir / "invopop_docs_description.md") as f:
            self.invopop_docs_description = f.read().strip()

        with open(prompts_dir / "gobl_docs_description.md") as f:
            self.gobl_docs_description = f.read().strip()

        with open(prompts_dir / "gobl_code_description.md") as f:
            self.gobl_code_description = f.read().strip()

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
                new_schema = tool.args_schema
            elif "gobl" in tool.description.lower():
                new_name = "gobl_search"
                new_description = self.gobl_docs_description
                new_schema = tool.args_schema
            elif tool.name == "ask_question":
                new_name = "gobl_code_ask_question"
                new_description = self.gobl_code_description
                new_schema = tool.args_schema.copy()
                new_schema["properties"]["repoName"]["description"] = (
                    "This value will always be 'invopop/gobl'"
                )
                new_schema["properties"]["question"]["description"] = (
                    "The question to ask about the invopop/gobl repo"
                )
            else:
                continue
            # Create a new StructuredTool with the new name
            renamed_tool = StructuredTool.from_function(
                coroutine=tool.coroutine,
                name=new_name,
                description=new_description,
                response_format=tool.response_format,
                args_schema=new_schema,
            )
            renamed_tools.append(renamed_tool)

        # Create the agent
        llm_config = self.config.llm_config
        provider = llm_config.get("provider", "openai")
        model = llm_config.get("model", "gpt-4.1")
        model_name = f"{provider}:{model}"

        self.agent = create_react_agent(
            model_name,
            renamed_tools,
            checkpointer=self.checkpointer,
            prompt=self.system_prompt,
        )

        # Store Opik configuration if configured
        if self.config.opik_api_key:
            self.opik_config = self.config.opik_config
            project_name = self.opik_config.get("project_name", "invopop-expert")
            print(f"✅ Opik tracing enabled for project: {project_name}")
        else:
            self.opik_config = None
            print("⚠️  Opik tracing disabled - missing API key")

    def _create_opik_tracer(self, user_thread_id: str) -> OpikTracer | None:
        """Create a new OpikTracer instance for the given thread_id."""
        if not self.opik_config:
            return None

        project_name = self.opik_config.get("project_name", "invopop-expert")

        # Create tracer with user thread_id in metadata for proper thread tracking
        tracer = OpikTracer(
            graph=self.agent.get_graph(xray=True), project_name=project_name, tags=[user_thread_id]
        )
        return tracer

    async def get_response(self, user_input: str, thread_id: str) -> str:
        """Get response from the agent for a given input."""
        if not self.agent:
            raise RuntimeError("Agent not initialized. Call setup() first.")

        thread_config = {
            "configurable": {"thread_id": thread_id},
        }

        # Create a new tracer instance for this conversation
        # The tracer uses the original thread_id in metadata for proper Opik thread tracking
        tracer = self._create_opik_tracer(thread_id)
        if tracer:
            thread_config["callbacks"] = [tracer]

        async for chunk in self.agent.astream(
            {"messages": [{"role": "user", "content": user_input}]}, thread_config
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
                            elif func_name == "gobl_code_ask_question":
                                print(
                                    "🔍 Searching invopop/gobl repo:",
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

        # Create a thread id based on the current date and time
        thread_id = datetime.now().strftime("%Y%m%d%H%M%S")

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
                elif user_input.lower() in ["clear"]:
                    thread_id = datetime.now().strftime("%Y%m%d%H%M%S")
                    print("\n🤖 Cleared thread")
                    continue

                # Get and print agent response
                print("\n🤖 Thinking...", flush=True)
                response = await self.get_response(user_input, thread_id)
                print(f"\n🤖 Assistant: {response}")

            except KeyboardInterrupt:
                print("\n\n🤖 Exiting...")
                break
            except Exception as e:
                print(f"\n❌ Error: {str(e)}")
                continue
