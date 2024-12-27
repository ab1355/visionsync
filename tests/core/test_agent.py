#!/usr/bin/env python3
"""
Tests for the core Agent implementation.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from core.agent import Agent
from core.config import AgentConfig
from core.context import AgentContext

@pytest.fixture
def config():
    """Create a test configuration."""
    return AgentConfig()

@pytest.fixture
def context(config):
    """Create a test context."""
    return AgentContext(config=config)

@pytest.fixture
def agent(config, context):
    """Create a test agent."""
    return Agent(0, config, context)

@pytest.mark.asyncio
async def test_agent_initialization(agent):
    """Test agent initialization."""
    assert agent.number == 0
    assert agent.agent_name == "Agent 0"
    assert isinstance(agent.pattern_engine, object)
    assert isinstance(agent.resource_manager, object)
    assert isinstance(agent.learning_engine, object)
    assert isinstance(agent.cooperation_engine, object)
    assert isinstance(agent.evolution_engine, object)
    assert isinstance(agent.analytics_engine, object)
    assert isinstance(agent.interface_engine, object)

@pytest.mark.asyncio
async def test_initialize_loop(agent):
    """Test loop initialization."""
    loop_data = await agent.initialize_loop()
    
    assert isinstance(loop_data, dict)
    assert 'start_time' in loop_data
    assert 'context' in loop_data
    assert 'history' in loop_data
    assert isinstance(loop_data['history'], list)

@pytest.mark.asyncio
async def test_process_through_systems(agent):
    """Test processing through enhancement systems."""
    # Mock all system calls
    agent.pattern_engine.process_patterns = AsyncMock(return_value={})
    agent.resource_manager.optimize_resources = AsyncMock(return_value={})
    agent.learning_engine.process_learning = AsyncMock(return_value={})
    agent.cooperation_engine.coordinate_agents = AsyncMock(return_value={})
    agent.evolution_engine.evolve_system = AsyncMock(return_value={})
    agent.analytics_engine.analyze_system = AsyncMock(return_value={})
    agent.interface_engine.process_interaction = AsyncMock(return_value={})
    
    await agent.process_through_systems()
    
    # Verify all systems were called
    agent.pattern_engine.process_patterns.assert_called_once()
    agent.resource_manager.optimize_resources.assert_called_once()
    agent.learning_engine.process_learning.assert_called_once()
    agent.cooperation_engine.coordinate_agents.assert_called_once()
    agent.evolution_engine.evolve_system.assert_called_once()
    agent.analytics_engine.analyze_system.assert_called_once()
    agent.interface_engine.process_interaction.assert_called_once()

@pytest.mark.asyncio
async def test_prepare_prompt(agent):
    """Test prompt preparation."""
    # Mock system prompt and enhancements
    with patch.object(agent, 'get_system_prompt', new_callable=AsyncMock) as mock_system_prompt:
        with patch.object(agent, 'get_system_enhancements', new_callable=AsyncMock) as mock_enhancements:
            mock_system_prompt.return_value = ["System prompt"]
            mock_enhancements.return_value = ["Enhancement data"]
            
            prompt = await agent.prepare_prompt()
            
            assert "System prompt" in prompt
            assert "Enhancement data" in prompt
            mock_system_prompt.assert_called_once()
            mock_enhancements.assert_called_once()

@pytest.mark.asyncio
async def test_generate_response(agent):
    """Test response generation."""
    # Mock interface engine and model call
    agent.interface_engine.format_prompt = AsyncMock(return_value="Formatted prompt")
    agent.call_model = AsyncMock(return_value="Model response")
    agent.analytics_engine.analyze_response = AsyncMock()
    
    response = await agent.generate_response("Test prompt")
    
    assert response == "Model response"
    agent.interface_engine.format_prompt.assert_called_once_with("Test prompt")
    agent.call_model.assert_called_once_with("Formatted prompt")
    agent.analytics_engine.analyze_response.assert_called_once_with("Model response")

@pytest.mark.asyncio
async def test_process_response(agent):
    """Test response processing."""
    # Mock interface engine and tool processing
    agent.interface_engine.format_response = AsyncMock(return_value="Formatted response")
    agent.process_tools = AsyncMock(return_value="Tool result")
    agent.learning_engine.learn_from_execution = AsyncMock()
    
    result = await agent.process_response("Test response")
    
    assert result == "Tool result"
    agent.interface_engine.format_response.assert_called_once_with("Test response")
    agent.process_tools.assert_called_once_with("Formatted response")
    agent.learning_engine.learn_from_execution.assert_called_once_with("Tool result")

@pytest.mark.asyncio
async def test_handle_exception(agent):
    """Test exception handling."""
    error = Exception("Test error")
    
    # Mock analytics engine
    agent.analytics_engine.log_error = AsyncMock()
    
    await agent.handle_exception(error)
    
    agent.analytics_engine.log_error.assert_called_once_with(error)
    assert "Error: Test error" in [entry.message for entry in agent.context.log.entries]

@pytest.mark.asyncio
async def test_handle_critical_exception(agent):
    """Test critical exception handling."""
    error = Exception("Critical test error")
    
    # Mock analytics engine
    agent.analytics_engine.log_critical_error = AsyncMock()
    
    with pytest.raises(Exception) as exc_info:
        await agent.handle_critical_exception(error)
    
    assert str(exc_info.value) == "Critical test error"
    agent.analytics_engine.log_critical_error.assert_called_once_with(error)
    assert "Critical Error: Critical test error" in [entry.message for entry in agent.context.log.entries]

@pytest.mark.asyncio
async def test_monologue_success(agent):
    """Test successful monologue execution."""
    # Mock all required methods
    agent.initialize_loop = AsyncMock(return_value={})
    agent.process_through_systems = AsyncMock()
    agent.prepare_prompt = AsyncMock(return_value="Test prompt")
    agent.generate_response = AsyncMock(return_value="Test response")
    agent.process_response = AsyncMock(return_value="Final result")
    
    result = await agent.monologue()
    
    assert result == "Final result"
    agent.initialize_loop.assert_called_once()
    agent.process_through_systems.assert_called_once()
    agent.prepare_prompt.assert_called_once()
    agent.generate_response.assert_called_once_with("Test prompt")
    agent.process_response.assert_called_once_with("Test response")

@pytest.mark.asyncio
async def test_monologue_error_handling(agent):
    """Test monologue error handling."""
    # Mock methods to simulate an error
    agent.initialize_loop = AsyncMock(side_effect=Exception("Test error"))
    agent.handle_critical_exception = AsyncMock()
    
    await agent.monologue()
    
    agent.initialize_loop.assert_called_once()
    agent.handle_critical_exception.assert_called_once()
