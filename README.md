# Invopop Expert

An AI-powered agent library for answering questions about Invopop and GOBL documentation using LangChain and MCP (Model Context Protocol) servers.

## Features

- 🤖 **Intelligent Q&A**: Answers questions about Invopop and GOBL using advanced RAG
- 🔍 **Multi-source Search**: Searches through documentation and code repositories  
- 💬 **Interactive CLI**: Command-line interface for direct interaction
- 🔧 **Extensible**: Easy to integrate into your own applications
- 📚 **Context Aware**: Maintains conversation history and context

## Quick Start

### Prerequisites

- Python 3.13+
- Node.js 20+ (for MCP servers)
- OpenAI API key

### Installation

> **Note**: This project uses `uv` for dependency management. If you don't have `uv` installed, you can install it with `pip install uv` or use `pipx` for isolated installation.

1. **Install MCP servers** (required for documentation search):
   ```bash
   npx mint-mcp add invopop
   npx mint-mcp add gobl
   ```

2. **Install the package**:
   ```bash
   # Option 1: Development installation (recommended)
   git clone https://github.com/invopop/expert.git
   cd expert
   uv pip install -e .
   
   # Option 2: Using pipx (installs in isolated environment)
   pipx install git+https://github.com/invopop/expert.git
   
   # Option 3: Direct installation with pip
   pip install git+https://github.com/invopop/expert.git
   ```

3. **Set up environment variables**:
   ```bash
   export OPENAI_API_KEY=your_openai_api_key
   ```

4. **Run the CLI**:
   ```bash
   # If using development installation (Option 1)
   uv run expert
   
   # If using pipx installation (Option 2)
   expert
   
   # If using pip installation (Option 3)
   expert
   
   # Alternative: Run directly without activation (works for all options)
   python -m expert.main
   ```

## CLI Usage

The CLI provides an interactive chat interface:

```bash
$ expert
Welcome to Invopop Expert! Ask questions about GOBL, Invopop and the invopop/gobl library
Enter your multi-line question. Press Enter on an empty line to send.
----------------------------------------------------------------------

👤 You: How do I create an invoice with GOBL?

🤖 Thinking...
🔍 Searching GOBL docs: {"query": "create invoice GOBL"}

🤖 Assistant: To create an invoice with GOBL, you need to...
```

### CLI Options

```bash
expert --help                    # Show help
expert --config config.yaml     # Use custom config file  
expert --verbose                 # Enable verbose output
```

## Library Usage

You can also use Invopop Expert as a library in your own applications:

```python
import asyncio
from expert import InvopopExpert, Config

async def main():
    # Initialize the expert
    config = Config()
    expert = InvopopExpert(config)
    await expert.setup()
    
    # Ask a question
    thread_config = {"configurable": {"thread_id": "my-conversation"}}
    response = await expert.get_response(
        "How do I handle tax calculations in GOBL?", 
        thread_config
    )
    print(response)

# Run the example
asyncio.run(main())
```

## Configuration

The agent uses a YAML configuration file (`config.yaml`):

```yaml
# LLM Configuration
llm:
  provider: "openai" 
  model: "gpt-4.1-2025-04-14"
  temperature: 0.1

# MCP Server Configuration  
mcp:
  servers:
    invopop:
      command: "node"
      args: ["~/.mcp/invopop/src/index.js"]
      transport: "stdio"
    gobl:
      command: "node"
      args: ["~/.mcp/gobl/src/index.js"] 
      transport: "stdio"

# Chat Interface Configuration
chat:
  welcome_message: "Welcome to Invopop Expert!"
  input_prompt: "Enter your question:"
  max_history: 50
```

### Environment Variables

- `OPENAI_API_KEY` (required): Your OpenAI API key
- `INVOPOP_MCP_PATH` (optional): Custom path to Invopop MCP server
- `GOBL_MCP_PATH` (optional): Custom path to GOBL MCP server

## Integration Examples

### Building a Web API

```python
from fastapi import FastAPI
from expert import InvopopExpert, Config

app = FastAPI()
expert = InvopopExpert(Config())

@app.on_event("startup")
async def startup():
    await expert.setup()

@app.post("/ask")
async def ask_question(question: str):
    thread_config = {"configurable": {"thread_id": "api-user"}}
    response = await expert.get_response(question, thread_config)
    return {"answer": response}
```

## Architecture

- **LangChain + LangGraph**: AI agent framework with memory and tools
- **MCP Protocol**: Connects to Mintlify documentation servers
- **Multi-source RAG**: Searches Invopop docs, GOBL docs, and code repositories
- **Conversation Memory**: Maintains context across interactions
- **Modular Design**: Easy to extend with new tools and integrations

## File Structure

```
src/expert/
├── agent.py          # Core InvopopExpert agent implementation
├── config.py         # Configuration management  
├── main.py           # CLI interface
├── __init__.py       # Package exports
└── prompts/          # System prompts and tool descriptions
    ├── system_prompt.md
    ├── invopop_docs_description.md
    ├── gobl_docs_description.md
    └── gobl_code_description.md
```

## Development

### Local Development Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/invopop/expert.git
   cd expert
   ```

2. **Install MCP servers**:
   ```bash
   npx mint-mcp add invopop
   npx mint-mcp add gobl
   ```

3. **Install dependencies**:
   ```bash
   # Install uv if not already installed
   pip install uv
   
   # Install the package in development mode
   uv pip install -e .
   ```

4. **Set environment variables**:
   ```bash
   export OPENAI_API_KEY=your_api_key
   ```

5. **Run the CLI**:
   ```bash
   # Activate the virtual environment created by uv
   source .venv/bin/activate
   
   # Run the CLI
   expert
   
   # Or run directly without activating the venv
   python -m expert.main
   ```

### Running Tests

```bash
# Run tests (when implemented)
pytest

# Run linting
ruff check src/
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass and linting is clean
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

## Troubleshooting

### Common Issues

**Command 'expert' not found:**
```bash
# If using development installation, activate the virtual environment
source .venv/bin/activate
expert

# Or run directly as a Python module
python -m expert.main

# If using pipx, ensure pipx bin directory is in your PATH
export PATH="$HOME/.local/bin:$PATH"
```

**MCP servers not found:**
```bash
npx mint-mcp add invopop
npx mint-mcp add gobl
```

**OpenAI API errors:**
- Verify your API key is correct and has sufficient credits
- Check that you're using a supported model

**Import errors:**
- Ensure you've installed the package: `uv pip install -e .` or `pip install -e .`
- Check that all dependencies are installed
- Try reinstalling: `uv pip install -e . --force-reinstall`

### Getting Help

- 📖 [Invopop Documentation](https://docs.invopop.com)
- 📚 [GOBL Documentation](https://docs.gobl.org/introduction)  
- 🐛 [Report Issues](https://github.com/invopop/expert/issues)

## License

See [LICENSE](LICENSE) file for details.