"""
JARVIS - Generative AI Assistant with Full System Control
A flexible autonomous AI agent framework supporting multiple LLM providers
"""

import os
import json
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from enum import Enum
import subprocess
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AIProvider(Enum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GOOGLE = "google"


@dataclass
class JARVISConfig:
    """Configuration for JARVIS"""
    provider: AIProvider
    api_key: str
    model: str
    max_tokens: int = 4096
    temperature: float = 0.7
    debug: bool = False
    project_root: str = "./"


class ToolRegistry:
    """Registry for AI tools/actions"""
    
    def __init__(self):
        self.tools = {}
        self._register_default_tools()
    
    def _register_default_tools(self):
        """Register default system tools"""
        self.register_tool("create_file", self.create_file)
        self.register_tool("edit_file", self.edit_file)
        self.register_tool("read_file", self.read_file)
        self.register_tool("delete_file", self.delete_file)
        self.register_tool("list_directory", self.list_directory)
        self.register_tool("create_directory", self.create_directory)
        self.register_tool("execute_command", self.execute_command)
        self.register_tool("search_files", self.search_files)
    
    def register_tool(self, name: str, func):
        """Register a custom tool"""
        self.tools[name] = func
        logger.info(f"Registered tool: {name}")
    
    def execute_tool(self, tool_name: str, **kwargs) -> Dict[str, Any]:
        """Execute a registered tool"""
        if tool_name not in self.tools:
            return {"error": f"Tool '{tool_name}' not found"}
        
        try:
            result = self.tools[tool_name](**kwargs)
            return {"success": True, "result": result}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    # ===================== File Operations =====================
    def create_file(self, path: str, content: str) -> str:
        """Create a new file with content"""
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as f:
            f.write(content)
        logger.info(f"Created file: {path}")
        return f"File created: {path}"
    
    def edit_file(self, path: str, content: str, mode: str = "overwrite") -> str:
        """Edit an existing file"""
        if not os.path.exists(path):
            raise FileNotFoundError(f"File not found: {path}")
        
        if mode == "overwrite":
            with open(path, 'w') as f:
                f.write(content)
        elif mode == "append":
            with open(path, 'a') as f:
                f.write(content)
        else:
            raise ValueError(f"Unknown mode: {mode}")
        
        logger.info(f"Edited file: {path}")
        return f"File edited: {path}"
    
    def read_file(self, path: str) -> str:
        """Read file content"""
        if not os.path.exists(path):
            raise FileNotFoundError(f"File not found: {path}")
        
        with open(path, 'r') as f:
            content = f.read()
        return content
    
    def delete_file(self, path: str) -> str:
        """Delete a file"""
        if not os.path.exists(path):
            raise FileNotFoundError(f"File not found: {path}")
        
        os.remove(path)
        logger.info(f"Deleted file: {path}")
        return f"File deleted: {path}"
    
    def list_directory(self, path: str = ".") -> List[str]:
        """List directory contents"""
        try:
            items = os.listdir(path)
            return items
        except Exception as e:
            raise Exception(f"Error listing directory: {e}")
    
    def create_directory(self, path: str) -> str:
        """Create a directory"""
        os.makedirs(path, exist_ok=True)
        logger.info(f"Created directory: {path}")
        return f"Directory created: {path}"
    
    def execute_command(self, command: str, shell: bool = True) -> Dict[str, Any]:
        """Execute a shell command"""
        try:
            result = subprocess.run(
                command,
                shell=shell,
                capture_output=True,
                text=True,
                timeout=30
            )
            return {
                "returncode": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr
            }
        except subprocess.TimeoutExpired:
            return {"error": "Command timed out"}
        except Exception as e:
            return {"error": str(e)}
    
    def search_files(self, directory: str, pattern: str) -> List[str]:
        """Search for files matching a pattern"""
        matches = []
        for root, dirs, files in os.walk(directory):
            for file in files:
                if pattern.lower() in file.lower():
                    matches.append(os.path.join(root, file))
        return matches
    
    def get_tools_info(self) -> Dict[str, str]:
        """Get information about available tools"""
        return {
            name: func.__doc__ or "No description"
            for name, func in self.tools.items()
        }


class LLMProvider:
    """Base class for LLM providers"""
    
    def __init__(self, config: JARVISConfig):
        self.config = config
    
    def send_message(self, messages: List[Dict[str, str]]) -> str:
        """Send message to LLM - to be implemented by subclasses"""
        raise NotImplementedError


class OpenAIProvider(LLMProvider):
    """OpenAI API provider"""
    
    def __init__(self, config: JARVISConfig):
        super().__init__(config)
        try:
            import openai
            openai.api_key = config.api_key
            self.client = openai.OpenAI(api_key=config.api_key)
        except ImportError:
            raise ImportError("openai package not installed. Run: pip install openai")
    
    def send_message(self, messages: List[Dict[str, str]]) -> str:
        """Send message to OpenAI API"""
        response = self.client.chat.completions.create(
            model=self.config.model,
            messages=messages,
            max_tokens=self.config.max_tokens,
            temperature=self.config.temperature
        )
        return response.choices[0].message.content


class AnthropicProvider(LLMProvider):
    """Anthropic Claude provider"""
    
    def __init__(self, config: JARVISConfig):
        super().__init__(config)
        try:
            import anthropic
            self.client = anthropic.Anthropic(api_key=config.api_key)
        except ImportError:
            raise ImportError("anthropic package not installed. Run: pip install anthropic")
    
    def send_message(self, messages: List[Dict[str, str]]) -> str:
        """Send message to Anthropic API"""
        response = self.client.messages.create(
            model=self.config.model,
            max_tokens=self.config.max_tokens,
            system="You are JARVIS, an autonomous AI assistant with full system control. You can create files, execute commands, and manage projects.",
            messages=messages
        )
        return response.content[0].text


class JARVIS:
    """Main JARVIS AI Agent"""
    
    def __init__(self, config: JARVISConfig):
        self.config = config
        self.tools = ToolRegistry()
        self.llm = self._initialize_llm()
        self.conversation_history: List[Dict[str, str]] = []
        
        logger.info(f"JARVIS initialized with {config.provider.value} provider")
    
    def _initialize_llm(self) -> LLMProvider:
        """Initialize the appropriate LLM provider"""
        if self.config.provider == AIProvider.OPENAI:
            return OpenAIProvider(self.config)
        elif self.config.provider == AIProvider.ANTHROPIC:
            return AnthropicProvider(self.config)
        else:
            raise ValueError(f"Unsupported provider: {self.config.provider}")
    
    def think(self, prompt: str) -> str:
        """Process a prompt with the AI and return response"""
        self.conversation_history.append({
            "role": "user",
            "content": prompt
        })
        
        # Add system context
        messages = [
            {
                "role": "system",
                "content": self._get_system_prompt()
            },
            *self.conversation_history
        ]
        
        response = self.llm.send_message(messages)
        
        self.conversation_history.append({
            "role": "assistant",
            "content": response
        })
        
        return response
    
    def _get_system_prompt(self) -> str:
        """Get the system prompt for JARVIS"""
        available_tools = json.dumps(self.tools.get_tools_info(), indent=2)
        
        return f"""You are JARVIS, an autonomous AI assistant with full system control.

Your capabilities:
- Create, read, edit, and delete files
- Create and manage directories
- Execute system commands and shell scripts
- Search and analyze code
- Generate code and documentation
- Manage entire projects autonomously

Available tools:
{available_tools}

When the user asks you to:
1. Create/modify files - use the appropriate file tools
2. Run commands - use execute_command
3. Manage files/folders - use file/directory tools
4. Search for patterns - use search_files

IMPORTANT:
- Always confirm what you're about to do before major operations
- Provide clear feedback on actions taken
- Explain your reasoning when making decisions
- Be proactive in suggesting improvements

You work in project root: {self.config.project_root}
Debug mode: {self.config.debug}
"""
    
    def execute_tool(self, tool_name: str, **kwargs) -> Dict[str, Any]:
        """Execute a tool directly"""
        return self.tools.execute_tool(tool_name, **kwargs)
    
    def chat(self, prompt: str) -> str:
        """Interactive chat interface"""
        response = self.think(prompt)
        return response
    
    def autonomous_task(self, task_description: str, max_iterations: int = 5) -> Dict[str, Any]:
        """Execute a task autonomously with multiple iterations"""
        logger.info(f"Starting autonomous task: {task_description}")
        
        task_prompt = f"""
You are given this task to complete autonomously:
{task_description}

Work through this systematically:
1. Break down the task into steps
2. Execute each step using available tools
3. Verify results at each step
4. Adapt if needed
5. Provide final summary

Begin:
"""
        
        results = {
            "task": task_description,
            "iterations": [],
            "final_status": "pending"
        }
        
        for i in range(max_iterations):
            logger.info(f"Iteration {i+1}/{max_iterations}")
            response = self.think(task_prompt)
            results["iterations"].append({
                "iteration": i + 1,
                "response": response
            })
            
            # Check if task is complete
            if "task complete" in response.lower() or "completed" in response.lower():
                results["final_status"] = "completed"
                break
        
        return results
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
    
    def get_history(self) -> List[Dict[str, str]]:
        """Get conversation history"""
        return self.conversation_history.copy()


def create_jarvis(provider_name: str = None, api_key: str = None, model: str = None) -> JARVIS:
    """Factory function to create JARVIS instance with environment variables or parameters"""
    from dotenv import load_dotenv
    
    load_dotenv()
    
    provider_name = provider_name or os.getenv("AI_PROVIDER", "openai")
    
    if provider_name.lower() == "openai":
        provider = AIProvider.OPENAI
        api_key = api_key or os.getenv("OPENAI_API_KEY")
        model = model or os.getenv("OPENAI_MODEL", "gpt-4-turbo-preview")
    elif provider_name.lower() == "anthropic":
        provider = AIProvider.ANTHROPIC
        api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        model = model or os.getenv("ANTHROPIC_MODEL", "claude-3-opus-20240229")
    else:
        raise ValueError(f"Unsupported provider: {provider_name}")
    
    if not api_key:
        raise ValueError(f"API key not provided for {provider_name}")
    
    config = JARVISConfig(
        provider=provider,
        api_key=api_key,
        model=model,
        debug=os.getenv("DEBUG", "false").lower() == "true"
    )
    
    return JARVIS(config)
