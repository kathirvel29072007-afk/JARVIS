# 🤖 JARVIS - Autonomous AI Assistant

A powerful, flexible generative AI framework with full system control. JARVIS can autonomously create files, manage projects, execute commands, and generate code across multiple platforms using your choice of AI provider.

## Features

✨ **Full System Control**
- Create, read, edit, and delete files
- Create and manage directories  
- Execute shell commands and scripts
- Search and analyze code

🧠 **Multiple AI Providers**
- OpenAI (GPT-4, GPT-3.5)
- Anthropic (Claude)
- Easily extensible for other providers

🚀 **Autonomous Task Execution**
- Break down complex tasks into steps
- Iterative execution with verification
- Self-correcting and adaptive

💬 **Interactive Interface**
- Chat interface for conversations
- CLI for quick tasks
- Programmatic API for integration

🛠️ **Rich Tool Registry**
- Extensible tool system
- Built-in file operations
- Command execution
- File search and analysis

## Installation

### Prerequisites
- Python 3.8+
- An API key from your chosen AI provider (OpenAI or Anthropic)

### Setup

1. **Clone or navigate to the JARVIS directory:**
```bash
cd JARVIS
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Configure JARVIS:**

Option A - Using setup wizard:
```bash
python3 cli.py setup
```

Option B - Manual configuration:
```bash
cp .env.example .env
```

Edit `.env` with your settings:
```env
AI_PROVIDER=openai
OPENAI_API_KEY=your_key_here
OPENAI_MODEL=gpt-4-turbo-preview
```

## Quick Start

### 1. Interactive Chat

Start an interactive conversation with JARVIS:
```bash
python3 cli.py chat
```

Commands:
- Type normally to chat
- `exit` - Quit
- `clear` - Clear conversation history
- `tools` - List available tools

### 2. Autonomous Tasks

Execute a complex task autonomously:
```bash
python3 cli.py task "Create a Flask web application with user authentication"
```

### 3. View Available Tools

```bash
python3 cli.py tools
```

## Programmatic Usage

### Basic Chat

```python
from jarvis import create_jarvis

jarvis = create_jarvis()
response = jarvis.chat("Create a Python script that generates Fibonacci numbers")
print(response)
```

### Create Files

```python
from jarvis import create_jarvis

jarvis = create_jarvis()

# Tell JARVIS to create files
jarvis.chat("Create a file called 'hello.py' that prints 'Hello, World!'")

# Or use tools directly
jarvis.execute_tool("create_file", 
    path="hello.py",
    content="print('Hello, World!')"
)
```

### Autonomous Task Execution

```python
from jarvis import create_jarvis

jarvis = create_jarvis()

task = """
Create a complete Python project structure:
1. Create src/ directory
2. Create src/main.py with a simple class
3. Create requirements.txt
4. Create README.md
"""

result = jarvis.autonomous_task(task, max_iterations=5)
print(f"Status: {result['final_status']}")
```

### Execute Commands

```python
from jarvis import create_jarvis

jarvis = create_jarvis()

# Execute shell commands
result = jarvis.execute_tool("execute_command", command="pip list")
print(result['result']['stdout'])
```

## Available Tools

JARVIS comes with these built-in tools:

| Tool | Description |
|------|-------------|
| `create_file` | Create a new file with content |
| `edit_file` | Edit existing file (overwrite or append) |
| `read_file` | Read file content |
| `delete_file` | Delete a file |
| `create_directory` | Create a directory |
| `list_directory` | List directory contents |
| `execute_command` | Execute shell commands |
| `search_files` | Search for files by pattern |

### Tool Usage Example

```python
jarvis = create_jarvis()

# Create a file
jarvis.execute_tool("create_file",
    path="data/users.json",
    content='{"users": []}'
)

# Read it
content = jarvis.execute_tool("read_file", path="data/users.json")
print(content['result'])

# List directory
files = jarvis.execute_tool("list_directory", path="data")
print(files['result'])
```

## Custom Tools

Add custom tools to extend JARVIS:

```python
from jarvis import create_jarvis

jarvis = create_jarvis()

def my_custom_tool(param1, param2):
    """My custom tool that does something specific"""
    return f"Result: {param1} + {param2}"

# Register the tool
jarvis.tools.register_tool("my_tool", my_custom_tool)

# Use it
result = jarvis.execute_tool("my_tool", param1="hello", param2="world")
print(result)
```

## Configuration

### Environment Variables (.env)

```env
# AI Provider
AI_PROVIDER=openai                          # openai or anthropic
OPENAI_API_KEY=sk-...                       # Your OpenAI API key
OPENAI_MODEL=gpt-4-turbo-preview            # Model to use

# For Anthropic
ANTHROPIC_API_KEY=sk-ant-...                # Your Anthropic API key
ANTHROPIC_MODEL=claude-3-opus-20240229      # Model to use

# Settings
PROJECT_ROOT=./                             # Working directory
MAX_TOKENS=4096                             # Maximum response tokens
TEMPERATURE=0.7                             # Creativity level (0-1)
DEBUG=false                                 # Enable debug logging
```

### Provider Configuration

#### OpenAI
1. Get API key from https://platform.openai.com/api-keys
2. Set `OPENAI_API_KEY` in `.env`
3. Choose model: `gpt-4-turbo-preview`, `gpt-4`, `gpt-3.5-turbo`, etc.

#### Anthropic (Claude)
1. Get API key from https://console.anthropic.com/
2. Set `ANTHROPIC_API_KEY` in `.env`
3. Choose model: `claude-3-opus-20240229`, `claude-3-sonnet-20240229`, etc.

## Examples

See `examples.py` for complete working examples:

```python
python -c "from examples import example_basic_chat; example_basic_chat()"
```

## Use Cases

### Code Generation
```bash
python cli.py chat
> Generate a Python class for managing a blog with CRUD operations
```

### Project Scaffolding
```bash
python cli.py task "Create a complete Django project structure with models, views, and URLs"
```

### Automation
```bash
python cli.py task "Create 10 test Python files with basic unit tests"
```

### Documentation
```bash
python cli.py chat
> Create comprehensive API documentation for a REST API
```

## Advanced Features

### Conversation History

JARVIS maintains conversation history for context-aware responses:

```python
jarvis = create_jarvis()

jarvis.chat("I'm building a web app")
jarvis.chat("Add authentication to it")  # Context aware!

# View history
history = jarvis.get_history()
print(history)

# Clear history
jarvis.clear_history()
```

### Autonomous Iteration

Tasks can iterate multiple times to refine results:

```python
result = jarvis.autonomous_task(
    "Create a production-ready API with tests",
    max_iterations=10
)
```

## Troubleshooting

### API Key Issues
- Make sure `.env` file exists and has correct API key
- Check that API key is valid and has sufficient credits
- For OpenAI: https://platform.openai.com/account/api-keys
- For Anthropic: https://console.anthropic.com/

### Import Errors
```bash
pip install -r requirements.txt
```

### Tool Execution Errors
- Check file paths are correct
- Ensure proper permissions for file operations
- Commands timeout after 30 seconds

### Model Not Found
- Verify model name matches your provider
- Check your account has access to the model

## Performance Tips

1. **Use appropriate models** - Larger models are slower but smarter
2. **Set realistic max_tokens** - Balance quality vs speed
3. **Batch operations** - Group related tasks together
4. **Clear history regularly** - Keeps context window manageable

## Security Considerations

⚠️ **IMPORTANT:**
- Never commit `.env` file with real API keys
- Use environment variables or secret managers in production
- JARVIS has full system access - be careful with untrusted prompts
- Monitor API usage and costs
- Implement rate limiting for production use

## Architecture

```
JARVIS/
├── jarvis.py           # Core AI agent
├── cli.py              # Command-line interface
├── examples.py         # Usage examples
├── requirements.txt    # Python dependencies
├── .env.example        # Configuration template
└── README.md           # This file
```

### Component Architecture

```
┌─────────────────────────────────────────┐
│         User Interface (CLI/API)         │
└────────────────┬────────────────────────┘
                 │
┌────────────────▼────────────────────────┐
│      JARVIS Core Agent                  │
│  - Conversation Management              │
│  - Task Orchestration                   │
│  - Tool Coordination                    │
└────────────────┬────────────────────────┘
         ┌───────┴───────────────┬─────────┐
    ┌────▼────┐  ┌──────────┐  ┌─▼──────┐
    │ LLM     │  │   Tool   │  │ File   │
    │Provider │  │ Registry │  │ System │
    └────┬────┘  └──────────┘  └────────┘
         │
    ┌────▼────────────────────────────────┐
    │   OpenAI / Anthropic / Other APIs   │
    └─────────────────────────────────────┘
```

## Extending JARVIS

### Adding New LLM Providers

1. Create a new provider class inheriting from `LLMProvider`
2. Implement the `send_message` method
3. Update `_initialize_llm()` in JARVIS class
4. Add configuration variables to `.env.example`

### Adding New Tools

```python
from jarvis import create_jarvis

jarvis = create_jarvis()

def analyze_code(code):
    """Analyze code quality"""
    # Your logic here
    return analysis_result

jarvis.tools.register_tool("analyze_code", analyze_code)
```

## Contributing

Feel free to extend JARVIS with:
- New tool plugins
- Additional LLM providers
- Performance optimizations
- Bug fixes

## License

MIT License - Use freely for personal and commercial projects

## Support

For issues, questions, or suggestions:
1. Check the examples in `examples.py`
2. Review the configuration in `.env`
3. Check that all dependencies are installed
4. Verify your API key and credentials

## Changelog

### Version 1.0.0
- Initial release
- OpenAI and Anthropic support
- Core tool registry
- CLI interface
- Autonomous task execution
- Conversation history

---

**JARVIS is designed for your personal projects. Use it responsibly! 🚀**
