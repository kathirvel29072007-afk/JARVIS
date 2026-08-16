"""
JARVIS main entry point
Provides a simple interface to start using JARVIS
"""

import sys
import os
from pathlib import Path


def main():
    """Main entry point"""
    
    print("\n" + "="*60)
    print("  🤖 JARVIS - Autonomous AI Assistant")
    print("="*60 + "\n")
    
    # Check if .env exists
    if not Path('.env').exists():
        print("⚠️  No .env file found!")
        print("\nPlease run: python cli.py setup")
        print("Or copy .env.example to .env and add your API key\n")
        return 1
    
    print("Usage:\n")
    print("  Interactive Chat:")
    print("    python cli.py chat\n")
    
    print("  Execute Task:")
    print("    python cli.py task \"Your task description\"\n")
    
    print("  View Available Tools:")
    print("    python cli.py tools\n")
    
    print("  Setup Configuration:")
    print("    python cli.py setup\n")
    
    print("For examples, see examples.py")
    print("For documentation, see README.md\n")
    
    return 0


if __name__ == "__main__":
    # Note: Run with python3 on macOS/Linux
    sys.exit(main())
