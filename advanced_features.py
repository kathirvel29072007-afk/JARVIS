"""
JARVIS Advanced Features and Utilities
"""

import json
from typing import List, Dict, Any, Callable
from dataclasses import dataclass, asdict
from enum import Enum


class TaskPriority(Enum):
    """Task priority levels"""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


@dataclass
class Task:
    """Represents a task to be executed"""
    id: str
    description: str
    priority: TaskPriority
    status: str = "pending"  # pending, in_progress, completed, failed
    result: str = ""
    error: str = ""


class TaskQueue:
    """Queue for managing multiple tasks"""
    
    def __init__(self):
        self.tasks: Dict[str, Task] = {}
        self.execution_order: List[str] = []
    
    def add_task(self, task: Task) -> str:
        """Add a task to the queue"""
        self.tasks[task.id] = task
        self._sort_by_priority()
        return task.id
    
    def _sort_by_priority(self):
        """Sort tasks by priority"""
        self.execution_order = sorted(
            self.tasks.keys(),
            key=lambda x: self.tasks[x].priority.value,
            reverse=True
        )
    
    def get_next_task(self) -> Task:
        """Get the next task to execute"""
        for task_id in self.execution_order:
            if self.tasks[task_id].status == "pending":
                return self.tasks[task_id]
        return None
    
    def mark_completed(self, task_id: str, result: str = ""):
        """Mark a task as completed"""
        if task_id in self.tasks:
            self.tasks[task_id].status = "completed"
            self.tasks[task_id].result = result
    
    def mark_failed(self, task_id: str, error: str = ""):
        """Mark a task as failed"""
        if task_id in self.tasks:
            self.tasks[task_id].status = "failed"
            self.tasks[task_id].error = error
    
    def get_status(self) -> Dict[str, Any]:
        """Get queue status"""
        completed = sum(1 for t in self.tasks.values() if t.status == "completed")
        failed = sum(1 for t in self.tasks.values() if t.status == "failed")
        pending = sum(1 for t in self.tasks.values() if t.status == "pending")
        
        return {
            "total": len(self.tasks),
            "completed": completed,
            "failed": failed,
            "pending": pending,
            "tasks": {
                id: asdict(task) for id, task in self.tasks.items()
            }
        }


class ProjectStructure:
    """Helper for creating project structures"""
    
    @staticmethod
    def create_python_project(jarvis, project_name: str, with_tests: bool = True):
        """Create a Python project structure"""
        
        structure = {
            f"{project_name}/": None,
            f"{project_name}/src/": None,
            f"{project_name}/src/__init__.py": "",
            f"{project_name}/src/main.py": """#!/usr/bin/env python3
\"""
Main entry point for {project_name}
\"""

def main():
    print("Welcome to {project_name}!")


if __name__ == "__main__":
    main()
""",
            f"{project_name}/requirements.txt": "# Project dependencies\n",
            f"{project_name}/README.md": f"""# {project_name}

A Python project created with JARVIS.

## Setup

```bash
pip install -r requirements.txt
```

## Usage

```bash
python -m src.main
```
""",
        }
        
        if with_tests:
            structure[f"{project_name}/tests/"] = None
            structure[f"{project_name}/tests/__init__.py"] = ""
            structure[f"{project_name}/tests/test_main.py"] = """import pytest
from src.main import main


def test_main():
    \"\"\"Test main function\"\"\"
    # Add your tests here
    pass
"""
        
        # Create all files and directories
        for path, content in structure.items():
            if path.endswith("/"):
                jarvis.execute_tool("create_directory", path=path)
            elif content is not None:
                jarvis.execute_tool("create_file", path=path, content=content)
        
        return f"Created {project_name} project structure"


class PromptTemplate:
    """Template for common prompts"""
    
    @staticmethod
    def create_code_review(code: str, language: str = "python") -> str:
        """Generate a code review prompt"""
        return f"""
Please review the following {language} code:

```{language}
{code}
```

Provide feedback on:
1. Code quality
2. Best practices
3. Performance
4. Security concerns
5. Suggestions for improvement
"""
    
    @staticmethod
    def create_documentation(code: str, language: str = "python") -> str:
        """Generate a documentation prompt"""
        return f"""
Generate comprehensive documentation for the following {language} code:

```{language}
{code}
```

Include:
1. Overview/Purpose
2. Parameters and return values
3. Usage examples
4. Edge cases
5. Related functions/classes
"""
    
    @staticmethod
    def refactor_code(code: str, language: str = "python", improvement: str = "") -> str:
        """Generate a refactoring prompt"""
        return f"""
Refactor the following {language} code {f"to {improvement}" if improvement else "for better quality"}:

```{language}
{code}
```

Provide the refactored code with explanations of changes.
"""
    
    @staticmethod
    def generate_tests(code: str, language: str = "python") -> str:
        """Generate a test generation prompt"""
        return f"""
Generate comprehensive unit tests for the following {language} code:

```{language}
{code}
```

Use appropriate testing frameworks:
- Python: pytest
- JavaScript: Jest
- Other: Industry standard

Cover:
1. Normal cases
2. Edge cases
3. Error handling
4. Integration points
"""


class ContextManager:
    """Manage context for JARVIS"""
    
    def __init__(self):
        self.context: Dict[str, Any] = {}
        self.file_cache: Dict[str, str] = {}
    
    def set_context(self, key: str, value: Any):
        """Set context value"""
        self.context[key] = value
    
    def get_context(self, key: str) -> Any:
        """Get context value"""
        return self.context.get(key)
    
    def cache_file(self, filepath: str, content: str):
        """Cache file content"""
        self.file_cache[filepath] = content
    
    def get_cached_file(self, filepath: str) -> str:
        """Get cached file content"""
        return self.file_cache.get(filepath)
    
    def get_context_summary(self) -> str:
        """Get a summary of current context"""
        return json.dumps({
            "context": self.context,
            "cached_files": list(self.file_cache.keys())
        }, indent=2)


class Logger:
    """Advanced logging for JARVIS operations"""
    
    def __init__(self, log_file: str = "jarvis.log"):
        self.log_file = log_file
        self.logs: List[Dict[str, Any]] = []
    
    def log(self, level: str, message: str, data: Dict[str, Any] = None):
        """Log a message"""
        import datetime
        
        log_entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "level": level,
            "message": message,
            "data": data or {}
        }
        
        self.logs.append(log_entry)
        
        # Also write to file
        with open(self.log_file, 'a') as f:
            f.write(json.dumps(log_entry) + "\n")
    
    def info(self, message: str, data: Dict[str, Any] = None):
        """Log info level"""
        self.log("INFO", message, data)
    
    def error(self, message: str, data: Dict[str, Any] = None):
        """Log error level"""
        self.log("ERROR", message, data)
    
    def warning(self, message: str, data: Dict[str, Any] = None):
        """Log warning level"""
        self.log("WARNING", message, data)
    
    def get_logs(self) -> List[Dict[str, Any]]:
        """Get all logs"""
        return self.logs.copy()


def integration_example():
    """Example of using advanced features"""
    from jarvis import create_jarvis
    
    jarvis = create_jarvis()
    
    # Create a task queue
    task_queue = TaskQueue()
    task_queue.add_task(Task(
        id="1",
        description="Create project structure",
        priority=TaskPriority.HIGH
    ))
    task_queue.add_task(Task(
        id="2",
        description="Add documentation",
        priority=TaskPriority.MEDIUM
    ))
    
    # Get status
    print("Queue status:", task_queue.get_status())
    
    # Use prompt templates
    code = "def hello(): print('Hello')"
    review_prompt = PromptTemplate.create_code_review(code, "python")
    
    # Use context manager
    context = ContextManager()
    context.set_context("project_name", "MyProject")
    
    # Log operations
    logger = Logger()
    logger.info("Started JARVIS operations")


if __name__ == "__main__":
    integration_example()
