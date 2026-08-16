"""
Example usage of JARVIS AI Agent
"""

from jarvis import create_jarvis


def example_basic_chat():
    """Example 1: Basic chat interface"""
    print("=" * 60)
    print("Example 1: Basic Chat")
    print("=" * 60)
    
    jarvis = create_jarvis()
    
    # Have a conversation
    response = jarvis.chat("Hello JARVIS! Create a Python script that prints 'Hello World'")
    print(f"\nJARVIS: {response}\n")


def example_create_project():
    """Example 2: Create a complete project structure"""
    print("=" * 60)
    print("Example 2: Create Project Structure")
    print("=" * 60)
    
    jarvis = create_jarvis()
    
    task = """
    Create a Python project structure for a simple TODO app with:
    1. Main app file (app.py)
    2. Requirements file (requirements.txt) with Flask dependency
    3. Configuration file (config.py)
    4. Templates directory with index.html
    5. Static directory for CSS
    
    Make it a functional Flask TODO application.
    """
    
    result = jarvis.autonomous_task(task, max_iterations=5)
    print(f"\nTask Status: {result['final_status']}")
    print(f"Completed in {len(result['iterations'])} iterations")


def example_code_generation():
    """Example 3: Generate and create code files"""
    print("=" * 60)
    print("Example 3: Code Generation")
    print("=" * 60)
    
    jarvis = create_jarvis()
    
    prompt = """
    I need a Python module for data processing. Create:
    1. A file called data_processor.py with functions:
       - load_data(filepath): Load CSV data
       - clean_data(data): Remove null values
       - calculate_statistics(data): Get min, max, mean
       - save_results(results, filepath): Save to JSON
    
    2. Make it production-ready with proper error handling and docstrings
    """
    
    response = jarvis.chat(prompt)
    print(f"\nJARVIS: {response}\n")


def example_file_operations():
    """Example 4: Direct file operations"""
    print("=" * 60)
    print("Example 4: File Operations")
    print("=" * 60)
    
    jarvis = create_jarvis()
    
    # Create a file
    result = jarvis.execute_tool("create_file", 
        path="test_project/example.txt",
        content="This is an example file created by JARVIS!"
    )
    print(f"Create: {result}")
    
    # Read it back
    result = jarvis.execute_tool("read_file", path="test_project/example.txt")
    print(f"Read: {result['result']}")
    
    # List directory
    result = jarvis.execute_tool("list_directory", path="test_project")
    print(f"Directory contents: {result['result']}")


def example_command_execution():
    """Example 5: Execute shell commands"""
    print("=" * 60)
    print("Example 5: Command Execution")
    print("=" * 60)
    
    jarvis = create_jarvis()
    
    # Execute a command
    result = jarvis.execute_tool("execute_command", command="python --version")
    output = result['result']
    print(f"Python version: {output['stdout']}")


def example_complex_task():
    """Example 6: Complex autonomous task"""
    print("=" * 60)
    print("Example 6: Complex Autonomous Task")
    print("=" * 60)
    
    jarvis = create_jarvis()
    
    task = """
    Build a complete web API project with:
    1. Create project directory structure (src/, tests/, docs/)
    2. Create main FastAPI application (src/main.py) with:
       - GET /health endpoint
       - POST /users endpoint to create users
       - GET /users/{id} endpoint to get user
    3. Create models.py with User model (id, name, email)
    4. Create requirements.txt with fastapi and uvicorn
    5. Create a README.md with setup instructions
    6. Create a basic test file (tests/test_api.py)
    
    Make it production-ready and well-documented.
    """
    
    result = jarvis.autonomous_task(task, max_iterations=8)
    print(f"\nTask Status: {result['final_status']}")
    print(f"Completed in {len(result['iterations'])} iterations")


if __name__ == "__main__":
    # Uncomment any example to run it
    
    # example_basic_chat()
    # example_create_project()
    # example_code_generation()
    # example_file_operations()
    # example_command_execution()
    # example_complex_task()
    
    print("Uncomment any example function in main to run it!")
    print("Or use the CLI: python cli.py chat")
