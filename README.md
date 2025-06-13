# Invopop Expert 🤖

An AI agent that helps you with Invopop and GOBL (Go Business Language) documentation and implementation questions. It has access to invopop, gobl docs and the [gobl repo](https://github.com/invopop/gobl)

## 🚀 Quick Start

### Prerequisites

- Node.js (for MCP servers)
- OpenAI API key
- uv package manager (you can install it with pip or brew: [install uv](https://docs.astral.sh/uv/getting-started/installation/))

### Installation

1. **Clone the repository:**

```bash
git clone https://github.com/invopop/expert.git
cd expert
```

2. **Install MCP servers**:

```bash
chmod +x scripts/install_mcp_servers.sh
./scripts/install_mcp_servers.sh
```

3. **Install Python dependencies**:

```bash
uv sync
```

4. **Configure environment**:

```bash
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

5. **Run the agent**:
```bash
uv run python -m src.expert.main
```

If you have Python > 3.13, you can also run it in cli from root like this:

Install the package: 
```bash
uv pip install -e .
```

Run it from root:
```bash
uv run expert
```

## 🛠️ Configuration
### Environment Variables (.env)

- `OPENAI_API_KEY`: Your OpenAI API key (required)
- `INVOPOP_MCP_PATH`: Custom path to Invopop MCP server (optional)
- `GOBL_MCP_PATH`: Custom path to GOBL MCP server (optional)

### Configuration File (config.yaml)
Customize the agent behavior by editing `config.yaml`:

- LLM model and parameters
- MCP server paths
- Chat interface settings

## 💬 Usage
Start a conversation with the agent:

```bash
uv run expert
```

Ask questions like:

- "How do I create a GOBL invoice?"
- "What are the tax requirements for Spain in Invopop?"
- "How do I integrate with the Invopop API?"

Or more complex ones like:
- "Give me an example of a valid invoice in Verifactu?"
- "For my case X in greece, what would be the fields required in the invoice and where should they appear?"

In case the result of some prompt is not as expected, report it as an issue and we will look into it. 

Type `exit`, `quit`, or `bye` to end the session.

Type `clear` to start a new thread.

## 🧪 Development

### Setup Development Environment
```bash
uv sync --group dev
```

### Code Formatting
```bash
uv run black src/
uv run ruff check src/
```

## 📁 Project Structure

``` bash
invopop-expert/
├── src/invopop_expert/    # Main package
├── config.yaml            # Configuration
└── scripts/               # Installation scripts
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and formatting
5. Submit a pull request

## 📄 License
Apache License 2.0 - see LICENSE file for details.

## 🆘 Support

📚 [Invopop Documentation](https://docs.invopop.com/home)
📚 [GOBL Documentation](https://docs.gobl.org/introduction)
🐛 [Report Issues or unexpected answer](https://github.com/invopop/expert/issues)