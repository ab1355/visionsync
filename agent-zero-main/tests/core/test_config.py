#!/usr/bin/env python3
"""
Tests for the configuration system.
"""

import pytest
from typing import Dict, Any

from core.config import (
    ModelConfig,
    SystemConfig,
    PatternConfig,
    ResourceConfig,
    LearningConfig,
    CooperationConfig,
    EvolutionConfig,
    AnalyticsConfig,
    InterfaceConfig,
    AgentConfig
)

@pytest.fixture
def model_config_data() -> Dict[str, Any]:
    """Create test model configuration data."""
    return {
        "provider": "test-provider",
        "name": "test-model",
        "ctx_length": 4096,
        "limit_requests": 100,
        "limit_input": 2048,
        "limit_output": 2048,
        "kwargs": {"temperature": 0.7}
    }

@pytest.fixture
def system_config_data() -> Dict[str, Any]:
    """Create test system configuration data."""
    return {
        "enabled": True,
        "debug": True,
        "log_level": "DEBUG"
    }

def test_model_config_initialization(model_config_data):
    """Test ModelConfig initialization."""
    config = ModelConfig(**model_config_data)
    
    assert config.provider == model_config_data["provider"]
    assert config.name == model_config_data["name"]
    assert config.ctx_length == model_config_data["ctx_length"]
    assert config.limit_requests == model_config_data["limit_requests"]
    assert config.limit_input == model_config_data["limit_input"]
    assert config.limit_output == model_config_data["limit_output"]
    assert config.kwargs == model_config_data["kwargs"]

def test_system_config_initialization(system_config_data):
    """Test SystemConfig initialization."""
    config = SystemConfig(**system_config_data)
    
    assert config.enabled == system_config_data["enabled"]
    assert config.debug == system_config_data["debug"]
    assert config.log_level == system_config_data["log_level"]

def test_pattern_config_initialization():
    """Test PatternConfig initialization."""
    config = PatternConfig(
        similarity_threshold=0.8,
        min_examples=10,
        learning_rate=0.2
    )
    
    assert config.similarity_threshold == 0.8
    assert config.min_examples == 10
    assert config.learning_rate == 0.2
    assert config.enabled  # inherited from SystemConfig
    assert not config.debug  # inherited default

def test_resource_config_initialization():
    """Test ResourceConfig initialization."""
    config = ResourceConfig(
        optimization_threshold=0.9,
        allocation_strategy="static",
        max_memory_usage=0.7,
        max_cpu_usage=0.7
    )
    
    assert config.optimization_threshold == 0.9
    assert config.allocation_strategy == "static"
    assert config.max_memory_usage == 0.7
    assert config.max_cpu_usage == 0.7

def test_learning_config_initialization():
    """Test LearningConfig initialization."""
    config = LearningConfig(
        experience_threshold=0.6,
        learning_rate=0.15,
        max_memory_entries=500,
        retention_period=14
    )
    
    assert config.experience_threshold == 0.6
    assert config.learning_rate == 0.15
    assert config.max_memory_entries == 500
    assert config.retention_period == 14

def test_cooperation_config_initialization():
    """Test CooperationConfig initialization."""
    config = CooperationConfig(
        coordination_threshold=0.85,
        team_size=5,
        max_delegation_depth=4,
        timeout=600
    )
    
    assert config.coordination_threshold == 0.85
    assert config.team_size == 5
    assert config.max_delegation_depth == 4
    assert config.timeout == 600

def test_evolution_config_initialization():
    """Test EvolutionConfig initialization."""
    config = EvolutionConfig(
        evolution_rate=0.3,
        adaptation_threshold=0.8,
        mutation_rate=0.2,
        generation_limit=20
    )
    
    assert config.evolution_rate == 0.3
    assert config.adaptation_threshold == 0.8
    assert config.mutation_rate == 0.2
    assert config.generation_limit == 20

def test_analytics_config_initialization():
    """Test AnalyticsConfig initialization."""
    config = AnalyticsConfig(
        analysis_window=2000,
        confidence_threshold=0.9,
        metrics_retention=60,
        sampling_rate=0.5
    )
    
    assert config.analysis_window == 2000
    assert config.confidence_threshold == 0.9
    assert config.metrics_retention == 60
    assert config.sampling_rate == 0.5

def test_interface_config_initialization():
    """Test InterfaceConfig initialization."""
    config = InterfaceConfig(
        response_format="html",
        style_preferences={"theme": "dark"},
        max_response_length=4000,
        stream_output=False
    )
    
    assert config.response_format == "html"
    assert config.style_preferences == {"theme": "dark"}
    assert config.max_response_length == 4000
    assert not config.stream_output

def test_agent_config_initialization():
    """Test AgentConfig initialization with defaults."""
    config = AgentConfig()
    
    assert isinstance(config.chat_model, ModelConfig)
    assert isinstance(config.utility_model, ModelConfig)
    assert isinstance(config.embeddings_model, ModelConfig)
    assert isinstance(config.pattern_recognition, PatternConfig)
    assert isinstance(config.resource_optimization, ResourceConfig)
    assert isinstance(config.learning_integration, LearningConfig)
    assert isinstance(config.multi_agent_cooperation, CooperationConfig)
    assert isinstance(config.system_evolution, EvolutionConfig)
    assert isinstance(config.analytics_system, AnalyticsConfig)
    assert isinstance(config.interface_system, InterfaceConfig)
    assert config.prompts_subdir == "default"
    assert config.memory_subdir == ""
    assert not config.debug
    assert config.log_level == "INFO"

def test_agent_config_to_dict():
    """Test AgentConfig serialization to dictionary."""
    config = AgentConfig()
    data = config.to_dict()
    
    assert isinstance(data, dict)
    assert "chat_model" in data
    assert "utility_model" in data
    assert "embeddings_model" in data
    assert "pattern_recognition" in data
    assert "resource_optimization" in data
    assert "learning_integration" in data
    assert "multi_agent_cooperation" in data
    assert "system_evolution" in data
    assert "analytics_system" in data
    assert "interface_system" in data
    assert "prompts_subdir" in data
    assert "memory_subdir" in data
    assert "debug" in data
    assert "log_level" in data

def test_agent_config_from_dict():
    """Test AgentConfig deserialization from dictionary."""
    original = AgentConfig()
    data = original.to_dict()
    
    # Modify some values
    data["prompts_subdir"] = "custom"
    data["debug"] = True
    data["log_level"] = "DEBUG"
    
    # Create new config from data
    config = AgentConfig.from_dict(data)
    
    assert config.prompts_subdir == "custom"
    assert config.debug is True
    assert config.log_level == "DEBUG"
    assert isinstance(config.chat_model, ModelConfig)
    assert isinstance(config.pattern_recognition, PatternConfig)

def test_agent_config_custom_initialization():
    """Test AgentConfig initialization with custom values."""
    custom_model = ModelConfig(
        provider="custom",
        name="custom-model",
        ctx_length=2048,
        limit_requests=50,
        limit_input=1024,
        limit_output=1024,
        kwargs={"temperature": 0.5}
    )
    
    custom_pattern = PatternConfig(
        similarity_threshold=0.9,
        min_examples=3,
        learning_rate=0.3
    )
    
    config = AgentConfig(
        chat_model=custom_model,
        pattern_recognition=custom_pattern,
        debug=True,
        log_level="DEBUG"
    )
    
    assert config.chat_model.provider == "custom"
    assert config.chat_model.name == "custom-model"
    assert config.pattern_recognition.similarity_threshold == 0.9
    assert config.debug is True
    assert config.log_level == "DEBUG"

def test_config_immutability():
    """Test that config objects maintain immutability of critical fields."""
    config = AgentConfig()
    original_chat_model = config.chat_model
    
    # Attempt to modify chat_model
    with pytest.raises(AttributeError):
        config.chat_model = ModelConfig(
            provider="new",
            name="new-model",
            ctx_length=1024,
            limit_requests=10,
            limit_input=512,
            limit_output=512
        )
    
    assert config.chat_model == original_chat_model
