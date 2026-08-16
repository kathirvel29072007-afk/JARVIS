"""
Unit tests for JARVIS
Run with: pytest test_jarvis.py -v
"""

import os
import tempfile
import pytest
from pathlib import Path
from jarvis import (
    JARVIS, 
    JARVISConfig, 
    AIProvider, 
    ToolRegistry,
    OpenAIProvider,
    AnthropicProvider
)


class TestToolRegistry:
    """Test the tool registry"""
    
    def test_tool_registry_initialization(self):
        """Test that tool registry initializes with default tools"""
        registry = ToolRegistry()
        tools = registry.get_tools_info()
        
        assert len(tools) > 0
        assert "create_file" in tools
        assert "read_file" in tools
        assert "delete_file" in tools
    
    def test_create_file_tool(self):
        """Test file creation"""
        with tempfile.TemporaryDirectory() as tmpdir:
            registry = ToolRegistry()
            filepath = os.path.join(tmpdir, "test.txt")
            
            result = registry.execute_tool(
                "create_file",
                path=filepath,
                content="Test content"
            )
            
            assert result["success"]
            assert Path(filepath).exists()
    
    def test_read_file_tool(self):
        """Test file reading"""
        with tempfile.TemporaryDirectory() as tmpdir:
            registry = ToolRegistry()
            filepath = os.path.join(tmpdir, "test.txt")
            test_content = "Test content"
            
            # Create file
            registry.execute_tool("create_file", path=filepath, content=test_content)
            
            # Read file
            result = registry.execute_tool("read_file", path=filepath)
            
            assert result["success"]
            assert result["result"] == test_content
    
    def test_delete_file_tool(self):
        """Test file deletion"""
        with tempfile.TemporaryDirectory() as tmpdir:
            registry = ToolRegistry()
            filepath = os.path.join(tmpdir, "test.txt")
            
            # Create file
            registry.execute_tool("create_file", path=filepath, content="test")
            assert Path(filepath).exists()
            
            # Delete file
            result = registry.execute_tool("delete_file", path=filepath)
            
            assert result["success"]
            assert not Path(filepath).exists()
    
    def test_create_directory_tool(self):
        """Test directory creation"""
        with tempfile.TemporaryDirectory() as tmpdir:
            registry = ToolRegistry()
            dirpath = os.path.join(tmpdir, "newdir")
            
            result = registry.execute_tool("create_directory", path=dirpath)
            
            assert result["success"]
            assert Path(dirpath).exists()
    
    def test_list_directory_tool(self):
        """Test directory listing"""
        with tempfile.TemporaryDirectory() as tmpdir:
            registry = ToolRegistry()
            
            # Create some files
            Path(os.path.join(tmpdir, "file1.txt")).touch()
            Path(os.path.join(tmpdir, "file2.txt")).touch()
            
            result = registry.execute_tool("list_directory", path=tmpdir)
            
            assert result["success"]
            assert len(result["result"]) >= 2
    
    def test_execute_command_tool(self):
        """Test command execution"""
        registry = ToolRegistry()
        
        result = registry.execute_tool(
            "execute_command",
            command="echo 'test'"
        )
        
        assert result["success"]
        assert "test" in result["result"]["stdout"]
    
    def test_register_custom_tool(self):
        """Test registering custom tools"""
        registry = ToolRegistry()
        
        def custom_tool(value):
            return f"Custom: {value}"
        
        registry.register_tool("custom", custom_tool)
        result = registry.execute_tool("custom", value="test")
        
        assert result["success"]
        assert result["result"] == "Custom: test"
    
    def test_tool_not_found(self):
        """Test handling of non-existent tool"""
        registry = ToolRegistry()
        result = registry.execute_tool("nonexistent")
        
        assert not result["success"]
        assert "not found" in result["error"]


class TestJARVISConfig:
    """Test JARVIS configuration"""
    
    def test_config_creation(self):
        """Test creating a configuration"""
        config = JARVISConfig(
            provider=AIProvider.OPENAI,
            api_key="test-key",
            model="gpt-4"
        )
        
        assert config.provider == AIProvider.OPENAI
        assert config.api_key == "test-key"
        assert config.model == "gpt-4"
        assert config.max_tokens == 4096
        assert config.temperature == 0.7


class TestJARVIS:
    """Test main JARVIS class"""
    
    def test_jarvis_initialization(self):
        """Test JARVIS initialization"""
        # This test requires a valid API key - skip if not available
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            pytest.skip("OPENAI_API_KEY not set")
        
        config = JARVISConfig(
            provider=AIProvider.OPENAI,
            api_key=api_key,
            model="gpt-4-turbo-preview"
        )
        
        jarvis = JARVIS(config)
        assert jarvis is not None
        assert jarvis.config == config
    
    def test_tool_execution(self):
        """Test executing tools through JARVIS"""
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            pytest.skip("OPENAI_API_KEY not set")
        
        config = JARVISConfig(
            provider=AIProvider.OPENAI,
            api_key=api_key,
            model="gpt-4-turbo-preview"
        )
        
        jarvis = JARVIS(config)
        
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, "test.txt")
            
            # Create file through JARVIS
            result = jarvis.execute_tool(
                "create_file",
                path=filepath,
                content="JARVIS test"
            )
            
            assert result["success"]
            assert Path(filepath).exists()
    
    def test_conversation_history(self):
        """Test conversation history management"""
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            pytest.skip("OPENAI_API_KEY not set")
        
        config = JARVISConfig(
            provider=AIProvider.OPENAI,
            api_key=api_key,
            model="gpt-4-turbo-preview"
        )
        
        jarvis = JARVIS(config)
        
        # Start with empty history
        assert len(jarvis.get_history()) == 0
        
        # Clear should work on empty history
        jarvis.clear_history()
        assert len(jarvis.get_history()) == 0


class TestLLMProviders:
    """Test LLM provider implementations"""
    
    def test_openai_provider_init(self):
        """Test OpenAI provider initialization"""
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            pytest.skip("OPENAI_API_KEY not set")
        
        config = JARVISConfig(
            provider=AIProvider.OPENAI,
            api_key=api_key,
            model="gpt-4-turbo-preview"
        )
        
        provider = OpenAIProvider(config)
        assert provider is not None
    
    def test_anthropic_provider_init(self):
        """Test Anthropic provider initialization"""
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            pytest.skip("ANTHROPIC_API_KEY not set")
        
        config = JARVISConfig(
            provider=AIProvider.ANTHROPIC,
            api_key=api_key,
            model="claude-3-opus-20240229"
        )
        
        provider = AnthropicProvider(config)
        assert provider is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
