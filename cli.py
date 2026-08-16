"""
JARVIS CLI - Command-line interface for the JARVIS AI agent
"""

import click
import json
from colorama import Fore, Style
from jarvis import create_jarvis, AIProvider


def print_header():
    """Print JARVIS header"""
    print(f"\n{Fore.CYAN}")
    print("╔════════════════════════════════════════════════════════════╗")
    print("║  🤖 JARVIS - Autonomous AI Assistant                     ║")
    print("║  Generative AI with Full System Control                  ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print(f"{Style.RESET_ALL}\n")


def print_success(text):
    print(f"{Fore.GREEN}✓ {text}{Style.RESET_ALL}")


def print_info(text):
    print(f"{Fore.BLUE}ℹ {text}{Style.RESET_ALL}")


def print_warning(text):
    print(f"{Fore.YELLOW}⚠ {text}{Style.RESET_ALL}")


def print_error(text):
    print(f"{Fore.RED}✗ {text}{Style.RESET_ALL}")


@click.group()
def cli():
    """JARVIS - Autonomous AI Assistant CLI"""
    pass


@cli.command()
@click.option('--provider', default='openai', help='AI provider (openai, anthropic)')
@click.option('--api-key', prompt=False, help='API key (if not in .env)')
@click.option('--model', help='Model name')
def chat(provider, api_key, model):
    """Start interactive chat with JARVIS"""
    print_header()
    
    try:
        print_info(f"Initializing JARVIS with {provider}...")
        jarvis = create_jarvis(provider_name=provider, api_key=api_key, model=model)
        print_success("JARVIS initialized!")
        
        print(f"{Fore.CYAN}Type 'exit' to quit, 'clear' to clear history, 'tools' to see available tools{Style.RESET_ALL}\n")
        
        while True:
            try:
                user_input = click.prompt(f"{Fore.YELLOW}You{Style.RESET_ALL}")
                
                if user_input.lower() == 'exit':
                    print_info("Goodbye!")
                    break
                
                if user_input.lower() == 'clear':
                    jarvis.clear_history()
                    print_success("History cleared")
                    continue
                
                if user_input.lower() == 'tools':
                    tools = jarvis.tools.get_tools_info()
                    print_info("Available tools:")
                    for tool_name, description in tools.items():
                        print(f"  • {Fore.CYAN}{tool_name}{Style.RESET_ALL}: {description}")
                    continue
                
                if not user_input.strip():
                    continue
                
                print(f"\n{Fore.MAGENTA}JARVIS{Style.RESET_ALL}")
                response = jarvis.chat(user_input)
                print(response)
                print()
            
            except KeyboardInterrupt:
                print_warning("\nInterrupted by user")
                break
    
    except Exception as e:
        print_error(f"Error: {e}")
        raise click.Abort()


@cli.command()
@click.argument('task')
@click.option('--provider', default='openai', help='AI provider')
@click.option('--api-key', help='API key')
@click.option('--max-iterations', default=5, help='Maximum iterations')
def task(task, provider, api_key, max_iterations):
    """Execute an autonomous task"""
    print_header()
    
    try:
        print_info(f"Task: {task}")
        print_info(f"Initializing JARVIS with {provider}...")
        jarvis = create_jarvis(provider_name=provider, api_key=api_key)
        print_success("JARVIS initialized!\n")
        
        print_info("Executing task autonomously...")
        result = jarvis.autonomous_task(task, max_iterations=max_iterations)
        
        print_success("Task execution complete!\n")
        print(f"{Fore.CYAN}Summary:{Style.RESET_ALL}")
        print(f"Status: {result['final_status']}")
        print(f"Iterations: {len(result['iterations'])}")
        
        for i, iteration in enumerate(result['iterations'], 1):
            print(f"\n{Fore.YELLOW}--- Iteration {i} ---{Style.RESET_ALL}")
            print(iteration['response'][:500] + "..." if len(iteration['response']) > 500 else iteration['response'])
    
    except Exception as e:
        print_error(f"Error: {e}")
        raise click.Abort()


@cli.command()
@click.option('--provider', default='openai', help='AI provider')
@click.option('--api-key', help='API key')
def tools(provider, api_key):
    """List available tools"""
    print_header()
    
    try:
        jarvis = create_jarvis(provider_name=provider, api_key=api_key)
        tools_info = jarvis.tools.get_tools_info()
        
        print(f"{Fore.CYAN}Available Tools:{Style.RESET_ALL}\n")
        
        for tool_name, description in tools_info.items():
            print(f"{Fore.GREEN}• {tool_name}{Style.RESET_ALL}")
            print(f"  {description}\n")
    
    except Exception as e:
        print_error(f"Error: {e}")
        raise click.Abort()


@cli.command()
def setup():
    """Setup JARVIS configuration"""
    print_header()
    
    print(f"{Fore.CYAN}JARVIS Setup Wizard{Style.RESET_ALL}\n")
    
    # Provider selection
    print("Choose AI Provider:")
    print("1. OpenAI (GPT-4)")
    print("2. Anthropic (Claude)")
    choice = click.prompt("Select (1 or 2)", type=int, default=1)
    
    if choice == 1:
        provider = "openai"
        default_model = "gpt-4-turbo-preview"
    else:
        provider = "anthropic"
        default_model = "claude-3-opus-20240229"
    
    api_key = click.prompt("Enter your API key", hide_input=True)
    model = click.prompt(f"Enter model name", default=default_model)
    
    # Write .env file
    env_content = f"""AI_PROVIDER={provider}

# {provider.upper()} Configuration
{"OPENAI_API_KEY=" + api_key if provider == "openai" else "ANTHROPIC_API_KEY=" + api_key}
{"OPENAI_MODEL=" + model if provider == "openai" else "ANTHROPIC_MODEL=" + model}

# Settings
PROJECT_ROOT=./
MAX_TOKENS=4096
TEMPERATURE=0.7
DEBUG=false
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print_success("Configuration saved to .env file!")
    print_info(f"Provider: {provider}")
    print_info(f"Model: {model}")


if __name__ == '__main__':
    cli()
