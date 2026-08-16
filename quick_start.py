"""
Quick Start Guide for JARVIS
Run this to get started quickly!
"""

import os
import sys
from pathlib import Path


QUICK_START_GUIDE = """
╔════════════════════════════════════════════════════════════════════╗
║         🤖 JARVIS - Quick Start Guide                             ║
╚════════════════════════════════════════════════════════════════════╝

📋 STEP 1: Configuration
━━━━━━━━━━━━━━━━━━━━━━━━

Option A - Interactive Setup (Recommended):
  $ python3 cli.py setup

Option B - Manual Setup:
  1. Copy .env.example to .env
  2. Add your API key:
     OPENAI_API_KEY=your_key_here
     or
     ANTHROPIC_API_KEY=your_key_here

💬 STEP 2: Test with Chat
━━━━━━━━━━━━━━━━━━━━━━━━

Start interactive chat:
  $ python3 cli.py chat

Try these commands:
  > Create a Python file that prints Hello World
  > Generate a simple REST API with Flask
  > Build a CLI tool for managing TODOs

💼 STEP 3: Run Autonomous Tasks
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Execute complex tasks:
  $ python3 cli.py task "Create a complete Django project structure"

Examples:
  • "Build a Python package with setup.py and tests"
  • "Create a React component library with TypeScript"
  • "Generate a machine learning pipeline with PyTorch"

📚 STEP 4: Use Programmatically
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Create a Python script:

    # Run with: python3 your_script.py
    from jarvis import create_jarvis
    
    jarvis = create_jarvis()
    
    # Simple chat
    response = jarvis.chat("Generate a Python Fibonacci function")
    print(response)
    
    # Create files
    jarvis.execute_tool("create_file",
        path="hello.py",
        content="print('Hello from JARVIS!')"
    )
    
    # Execute tasks
    result = jarvis.autonomous_task(
        "Create a web scraper for news articles",
        max_iterations=5
    )

🛠️ COMMON TASKS
━━━━━━━━━━━━━

Generate Code:
  python cli.py chat
  > Create a Python class for managing a database

Build Projects:
  python cli.py task "Create complete FastAPI project with models and routes"

Review Code:
  python cli.py chat
  > Review this code for performance issues: [paste code]

Create Documentation:
  python cli.py chat
  > Generate API documentation for my Python module

Refactor Code:
  python cli.py chat
  > Refactor this code to be more Pythonic: [paste code]

⚙️ CONFIGURATION OPTIONS
━━━━━━━━━━━━━━━━━━━━━

Edit .env file:
  
  AI_PROVIDER=openai              # or anthropic
  OPENAI_API_KEY=sk-...          # Your OpenAI API key
  OPENAI_MODEL=gpt-4-turbo-preview
  
  ANTHROPIC_API_KEY=sk-ant-...    # Your Anthropic key
  ANTHROPIC_MODEL=claude-3-opus-20240229
  
  PROJECT_ROOT=./                 # Working directory
  MAX_TOKENS=4096                 # Response length
  TEMPERATURE=0.7                 # Creativity (0-1)
  DEBUG=false                      # Debug mode

📱 COMMAND REFERENCE
━━━━━━━━━━━━━━━━━

Chat Interface:
  python cli.py chat              # Interactive chat
  python cli.py chat --provider anthropic

Execute Tasks:
  python cli.py task "your task"  # Run autonomous task
  python cli.py task "..." --max-iterations 10

View Tools:
  python cli.py tools             # List all available tools

Setup:
  python cli.py setup             # Configuration wizard

🚀 ADVANCED USAGE
━━━━━━━━━━━━━━━━

# With custom tools
from jarvis import create_jarvis

jarvis = create_jarvis()

def my_tool(x):
    return x * 2

jarvis.tools.register_tool("double", my_tool)
result = jarvis.execute_tool("double", x=5)

# Conversation history
jarvis.chat("I'm building a web app")
jarvis.chat("Add authentication")  # Remembers context!
history = jarvis.get_history()

# Long-running tasks
result = jarvis.autonomous_task(
    "Build production-ready REST API with tests",
    max_iterations=10
)
print(result['final_status'])  # 'completed' or 'in_progress'

⭐ TIPS & TRICKS
━━━━━━━━━━━━━━

1. Be Specific
   ✓ "Create a Flask API with user authentication using JWT"
   ✗ "Create an API"

2. Use Conversation Context
   - Chat multiple times on related topics
   - JARVIS remembers previous messages

3. Large Projects
   - Break into smaller tasks
   - Use max_iterations=10+ for complex work

4. Cost Management
   - Monitor API usage
   - Use gpt-3.5-turbo for simpler tasks
   - Adjust MAX_TOKENS in .env

5. Debugging
   - Set DEBUG=true in .env for more output
   - Check jarvis.log for execution logs
   - Review conversation with jarvis.get_history()

📖 EXAMPLES
━━━━━━━━━━

See examples.py for:
  python -c "from examples import example_basic_chat; example_basic_chat()"
  python -c "from examples import example_create_project; example_create_project()"
  python -c "from examples import example_code_generation; example_code_generation()"

🆘 TROUBLESHOOTING
━━━━━━━━━━━━━━━━

"API key not found"
  → Add OPENAI_API_KEY or ANTHROPIC_API_KEY to .env

"ModuleNotFoundError"
  → Run: pip install -r requirements.txt

"Command timed out"
  → Some commands have a 30-second timeout
  → For longer tasks, use autonomous_task()

"Rate limit exceeded"
  → You've hit API rate limits
  → Wait a moment before making more requests

📚 RESOURCES
━━━━━━━━━━

Documentation: README.md
Examples: examples.py
Tests: test_jarvis.py
Advanced Features: advanced_features.py

API Keys:
  OpenAI: https://platform.openai.com/api-keys
  Anthropic: https://console.anthropic.com/

More Help:
  - Check README.md for detailed documentation
  - Review examples.py for code samples
  - Read inline code comments

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Ready to go? Start with: python cli.py setup
🚀 Let JARVIS build something amazing!
"""


def print_guide():
    """Print the quick start guide"""
    print(QUICK_START_GUIDE)


def check_setup():
    """Check if JARVIS is properly set up"""
    print("\n🔍 Checking JARVIS Setup...\n")
    
    checks = {
        "✓ Python environment": True,
        ".env file": Path('.env').exists(),
        "requirements.txt": Path('requirements.txt').exists(),
        "jarvis.py": Path('jarvis.py').exists(),
        "cli.py": Path('cli.py').exists(),
    }
    
    for check, passed in checks.items():
        status = "✓" if passed else "✗"
        print(f"  {status} {check}")
    
    if not Path('.env').exists():
        print("\n⚠️  .env file not found!")
        print("Run: python cli.py setup")
        return False
    
    # Check API key
    from dotenv import load_dotenv
    load_dotenv()
    
    provider = os.getenv('AI_PROVIDER', 'openai')
    if provider == 'openai':
        if not os.getenv('OPENAI_API_KEY'):
            print("\n⚠️  OPENAI_API_KEY not found in .env!")
            return False
    elif provider == 'anthropic':
        if not os.getenv('ANTHROPIC_API_KEY'):
            print("\n⚠️  ANTHROPIC_API_KEY not found in .env!")
            return False
    
    print("\n✓ Setup looks good!")
    return True


def main():
    """Main entry point"""
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "guide":
            print_guide()
        elif command == "check":
            check_setup()
        else:
            print_guide()
    else:
        # Check setup and show guide
        print_guide()
        print("\n" + "="*70)
        if not check_setup():
            print("\nRun setup first: python cli.py setup")
            sys.exit(1)


if __name__ == "__main__":
    main()
