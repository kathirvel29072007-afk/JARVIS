"""
JARVIS API Reference Documentation
Complete guide to all JARVIS APIs and usage
"""

# ============================================================================
# 1. INITIALIZATION
# ============================================================================

from jarvis import create_jarvis, JARVIS, JARVISConfig, AIProvider


# Quick initialization (uses .env)
jarvis = create_jarvis()

# Custom initialization
jarvis = create_jarvis(
    provider_name="openai",
    api_key="sk-...",
    model="gpt-4-turbo-preview"
)

# Direct configuration
config = JARVISConfig(
    provider=AIProvider.OPENAI,
    api_key="sk-...",
    model="gpt-4-turbo-preview",
    max_tokens=4096,
    temperature=0.7,
    debug=False
)
jarvis = JARVIS(config)


# ============================================================================
# 2. BASIC CHAT
# ============================================================================

# Simple prompt
response = jarvis.chat("Write a Python function to calculate factorial")
print(response)

# Multi-turn conversation (maintains history)
jarvis.chat("I need a web application")
jarvis.chat("Add user authentication")  # Has context from previous message


# ============================================================================
# 3. FILE OPERATIONS
# ============================================================================

# Create a file
result = jarvis.execute_tool(
    "create_file",
    path="hello.py",
    content="print('Hello, World!')"
)
print(result['result'])  # "File created: hello.py"

# Read a file
result = jarvis.execute_tool("read_file", path="hello.py")
print(result['result'])  # File content

# Edit a file (overwrite)
jarvis.execute_tool(
    "edit_file",
    path="hello.py",
    content="print('Hello, Universe!')",
    mode="overwrite"
)

# Edit a file (append)
jarvis.execute_tool(
    "edit_file",
    path="hello.py",
    content="\nprint('Goodbye!')",
    mode="append"
)

# Delete a file
jarvis.execute_tool("delete_file", path="hello.py")


# ============================================================================
# 4. DIRECTORY OPERATIONS
# ============================================================================

# Create directory
jarvis.execute_tool("create_directory", path="my_project/src")

# List directory contents
result = jarvis.execute_tool("list_directory", path="my_project")
files = result['result']  # ['src', 'config.py', ...]

# Search for files
result = jarvis.execute_tool("search_files", directory=".", pattern="test")
test_files = result['result']  # List of matching file paths


# ============================================================================
# 5. COMMAND EXECUTION
# ============================================================================

# Execute shell command
result = jarvis.execute_tool(
    "execute_command",
    command="python --version"
)
print(result['result']['stdout'])    # "Python 3.x.x"
print(result['result']['returncode']) # 0 (success)

# Complex command with pipes
result = jarvis.execute_tool(
    "execute_command",
    command="find . -name '*.py' | wc -l"
)

# Command with error handling
result = jarvis.execute_tool(
    "execute_command",
    command="invalid_command"
)
if result['result']['returncode'] != 0:
    print(result['result']['stderr'])  # Error message


# ============================================================================
# 6. AUTONOMOUS TASKS
# ============================================================================

# Execute a task with iterations
result = jarvis.autonomous_task(
    task_description="Create a Python Flask web application",
    max_iterations=5
)

# Result structure
print(result['task'])              # Original task
print(result['final_status'])      # 'completed' or 'in_progress'
print(len(result['iterations']))   # Number of iterations
print(result['iterations'][0]['response'])  # First iteration response


# ============================================================================
# 7. CONVERSATION MANAGEMENT
# ============================================================================

# Get conversation history
history = jarvis.get_history()
for message in history:
    print(f"{message['role']}: {message['content']}")

# Clear history (start fresh conversation)
jarvis.clear_history()


# ============================================================================
# 8. TOOL MANAGEMENT
# ============================================================================

# Get information about available tools
tools_info = jarvis.tools.get_tools_info()
for tool_name, description in tools_info.items():
    print(f"{tool_name}: {description}")

# Register custom tool
def calculate_fibonacci(n):
    """Calculate Fibonacci number"""
    if n <= 1:
        return n
    return calculate_fibonacci(n-1) + calculate_fibonacci(n-2)

jarvis.tools.register_tool("fibonacci", calculate_fibonacci)

# Execute custom tool
result = jarvis.execute_tool("fibonacci", n=10)
print(result['result'])  # 55


# ============================================================================
# 9. ERROR HANDLING
# ============================================================================

# Tool error handling
result = jarvis.execute_tool("read_file", path="nonexistent.txt")
if not result['success']:
    print(f"Error: {result['error']}")

# Exception handling in chat
try:
    response = jarvis.chat("Generate code")
except Exception as e:
    print(f"Chat error: {e}")

# Command execution error
result = jarvis.execute_tool("execute_command", command="bad_command")
if result['result']['returncode'] != 0:
    print("Command failed:", result['result']['stderr'])


# ============================================================================
# 10. ADVANCED PATTERNS
# ============================================================================

# Pattern 1: Create multiple files in a loop
files_to_create = {
    "file1.py": "print('File 1')",
    "file2.py": "print('File 2')",
    "file3.py": "print('File 3')",
}

for filename, content in files_to_create.items():
    jarvis.execute_tool("create_file", path=filename, content=content)

# Pattern 2: Sequential task execution
tasks = [
    "Create project structure",
    "Add configuration files",
    "Create main application file"
]

for task in tasks:
    print(f"Executing: {task}")
    response = jarvis.chat(task)
    print(f"Result: {response}\n")

# Pattern 3: Context-aware conversation
jarvis.chat("I'm building a REST API with FastAPI")
jarvis.chat("Add database models")
jarvis.chat("Create API endpoints")
jarvis.chat("Add authentication")  # Will maintain full context

# Pattern 4: Large project creation
large_task = """
Create a production-ready Django project with:
1. Settings configuration
2. Database models (User, Post, Comment)
3. API views using DRF
4. Serializers for all models
5. URL routing
6. Admin configuration
7. Tests for all views
8. Docker configuration
"""

result = jarvis.autonomous_task(large_task, max_iterations=10)
if result['final_status'] == 'completed':
    print("Project created successfully!")


# ============================================================================
# 11. LLM PROVIDER SWITCHING
# ============================================================================

# Switch between providers
jarvis_openai = create_jarvis(provider_name="openai")
jarvis_claude = create_jarvis(provider_name="anthropic")

# Use different models
response1 = jarvis_openai.chat("Hello")
response2 = jarvis_claude.chat("Hello")


# ============================================================================
# 12. CONFIGURATION OPTIONS
# ============================================================================

from jarvis import JARVISConfig, AIProvider

# Full configuration example
config = JARVISConfig(
    provider=AIProvider.OPENAI,
    api_key="sk-...",
    model="gpt-4-turbo-preview",
    max_tokens=8192,      # Longer responses
    temperature=0.3,      # More focused/deterministic
    debug=True,           # Enable debug logging
    project_root="/path/to/project"
)

jarvis = JARVIS(config)


# ============================================================================
# 13. RESULT STRUCTURES
# ============================================================================

# Chat response
response = jarvis.chat("Write code")
# Returns: string (the response text)

# Tool execution result
result = jarvis.execute_tool("create_file", path="test.txt", content="hi")
# Returns: {
#   'success': bool,
#   'result': Any,
#   'error': str (if failed)
# }

# Autonomous task result
result = jarvis.autonomous_task("Create app")
# Returns: {
#   'task': str,
#   'iterations': [{
#       'iteration': int,
#       'response': str
#   }],
#   'final_status': str  # 'completed' or 'in_progress'
# }

# History
history = jarvis.get_history()
# Returns: [
#   {'role': 'user|assistant', 'content': str},
#   ...
# ]


# ============================================================================
# 14. BEST PRACTICES
# ============================================================================

# ✓ DO: Clear history for unrelated tasks
jarvis.clear_history()
jarvis.chat("New task")

# ✓ DO: Use specific, detailed prompts
jarvis.chat(
    "Create a Python class for managing users with "
    "add_user, delete_user, and get_user methods"
)

# ✓ DO: Handle errors gracefully
result = jarvis.execute_tool("create_file", path="test.txt", content="x")
if result['success']:
    print("Created successfully")
else:
    print(f"Failed: {result['error']}")

# ✓ DO: Use autonomous tasks for complex work
result = jarvis.autonomous_task(
    "Complex project creation",
    max_iterations=10
)

# ✗ DON'T: Rely on single iteration for complex tasks
# Instead, use autonomous_task with multiple iterations

# ✗ DON'T: Assume file operations succeeded without checking
result = jarvis.execute_tool("read_file", path="file.txt")
if result['success']:
    content = result['result']

# ✗ DON'T: Mix unrelated tasks in single conversation
# Start fresh with clear_history() for new topics


# ============================================================================
# 15. COMPLETE EXAMPLE: Build a Full Project
# ============================================================================

def build_complete_project():
    """Complete example of building a project"""
    jarvis = create_jarvis()
    
    # Step 1: Create structure
    jarvis.execute_tool("create_directory", path="myapp/src")
    jarvis.execute_tool("create_directory", path="myapp/tests")
    
    # Step 2: Generate main app with context
    jarvis.chat("We're building a Python CLI tool for managing TODOs")
    jarvis.chat("Create the main application file with add, list, delete commands")
    
    # Step 3: Get all responses (build files)
    jarvis.chat("Create a requirements.txt file with necessary dependencies")
    jarvis.chat("Create unit tests for the application")
    
    # Step 4: Run autonomous task for missing pieces
    result = jarvis.autonomous_task(
        "Add README.md with setup and usage instructions",
        max_iterations=3
    )
    
    print(f"Project status: {result['final_status']}")
    return jarvis


if __name__ == "__main__":
    # Run example
    # jarvis = build_complete_project()
    pass
