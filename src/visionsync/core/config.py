#!/usr/bin/env python3
"""
Configuration management for Agent Zero.

This module handles all configuration settings for agents and their enhancement systems.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, Optional

@dataclass
class ModelConfig:
    """Configuration for a specific model."""
    provider: str
    name: str
    ctx_length: int
    limit_requests: int
    limit_input: int
    limit_output: int
    kwargs: Dict[str, Any] = field(default_factory=dict)

@dataclass
class SystemConfig:
    """Base configuration for enhancement systems."""
    enabled: bool = True
    debug: bool = False
    log_level: str = "INFO"

@dataclass
class PatternConfig(SystemConfig):
    """Configuration for pattern recognition system."""
    similarity_threshold: float = 0.75
    min_examples: int = 5
    learning_rate: float = 0.1

@dataclass
class ResourceConfig(SystemConfig):
    """Configuration for resource optimization system."""
    optimization_threshold: float = 0.8
    allocation_strategy: str = "dynamic"
    max_memory_usage: float = 0.8
    max_cpu_usage: float = 0.8

@dataclass
class LearningConfig(SystemConfig):
    """Configuration for learning integration system."""
    experience_threshold: float = 0.7
    learning_rate: float = 0.1
    max_memory_entries: int = 1000
    retention_period: int = 7  # days

@dataclass
class CooperationConfig(SystemConfig):
    """Configuration for multi-agent cooperation system."""
    coordination_threshold: float = 0.8
    team_size: int = 3
    max_delegation_depth: int = 3
    timeout: int = 300  # seconds

@dataclass
class EvolutionConfig(SystemConfig):
    """Configuration for system evolution."""
    evolution_rate: float = 0.2
    adaptation_threshold: float = 0.7
    mutation_rate: float = 0.1
    generation_limit: int = 10

@dataclass
class AnalyticsConfig(SystemConfig):
    """Configuration for analytics system."""
    analysis_window: int = 1000
    confidence_threshold: float = 0.8
    metrics_retention: int = 30  # days
    sampling_rate: float = 1.0

@dataclass
class InterfaceConfig(SystemConfig):
    """Configuration for interface system."""
    response_format: str = "markdown"
    style_preferences: Dict[str, Any] = field(default_factory=dict)
    max_response_length: int = 2000
    stream_output: bool = True

@dataclass
class AgentConfig:
    """
    Main configuration for an agent instance.
    
    This class centralizes all configuration settings including:
    - Model configurations
    - Enhancement system configurations
    - General agent settings
    """
    
    # Model configurations
    chat_model: ModelConfig = field(default_factory=lambda: ModelConfig(
        provider="openai",
        name="gpt-4",
        ctx_length=8192,
        limit_requests=100,
        limit_input=4000,
        limit_output=4000,
        kwargs={"temperature": 0.7}
    ))
    
    utility_model: ModelConfig = field(default_factory=lambda: ModelConfig(
        provider="openai",
        name="gpt-3.5-turbo",
        ctx_length=4096,
        limit_requests=100,
        limit_input=2000,
        limit_output=2000,
        kwargs={"temperature": 0.3}
    ))
    
    embeddings_model: ModelConfig = field(default_factory=lambda: ModelConfig(
        provider="openai",
        name="text-embedding-ada-002",
        ctx_length=8191,
        limit_requests=100,
        limit_input=8191,
        limit_output=1536,
        kwargs={}
    ))
    
    # Enhancement system configurations
    pattern_recognition: PatternConfig = field(default_factory=PatternConfig)
    resource_optimization: ResourceConfig = field(default_factory=ResourceConfig)
    learning_integration: LearningConfig = field(default_factory=LearningConfig)
    multi_agent_cooperation: CooperationConfig = field(default_factory=CooperationConfig)
    system_evolution: EvolutionConfig = field(default_factory=EvolutionConfig)
    analytics_system: AnalyticsConfig = field(default_factory=AnalyticsConfig)
    interface_system: InterfaceConfig = field(default_factory=InterfaceConfig)
    
    # General settings
    prompts_subdir: str = "default"
    memory_subdir: str = ""
    debug: bool = False
    log_level: str = "INFO"
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert configuration to dictionary format.
        
        Returns:
            Dictionary representation of configuration
        """
        return {
            "chat_model": vars(self.chat_model),
            "utility_model": vars(self.utility_model),
            "embeddings_model": vars(self.embeddings_model),
            "pattern_recognition": vars(self.pattern_recognition),
            "resource_optimization": vars(self.resource_optimization),
            "learning_integration": vars(self.learning_integration),
            "multi_agent_cooperation": vars(self.multi_agent_cooperation),
            "system_evolution": vars(self.system_evolution),
            "analytics_system": vars(self.analytics_system),
            "interface_system": vars(self.interface_system),
            "prompts_subdir": self.prompts_subdir,
            "memory_subdir": self.memory_subdir,
            "debug": self.debug,
            "log_level": self.log_level
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AgentConfig":
        """
        Create configuration from dictionary format.
        
        Args:
            data: Dictionary containing configuration data
            
        Returns:
            New AgentConfig instance
        """
        # Create model configs
        chat_model = ModelConfig(**data.get("chat_model", {}))
        utility_model = ModelConfig(**data.get("utility_model", {}))
        embeddings_model = ModelConfig(**data.get("embeddings_model", {}))
        
        # Create system configs
        pattern_recognition = PatternConfig(**data.get("pattern_recognition", {}))
        resource_optimization = ResourceConfig(**data.get("resource_optimization", {}))
        learning_integration = LearningConfig(**data.get("learning_integration", {}))
        multi_agent_cooperation = CooperationConfig(**data.get("multi_agent_cooperation", {}))
        system_evolution = EvolutionConfig(**data.get("system_evolution", {}))
        analytics_system = AnalyticsConfig(**data.get("analytics_system", {}))
        interface_system = InterfaceConfig(**data.get("interface_system", {}))
        
        return cls(
            chat_model=chat_model,
            utility_model=utility_model,
            embeddings_model=embeddings_model,
            pattern_recognition=pattern_recognition,
            resource_optimization=resource_optimization,
            learning_integration=learning_integration,
            multi_agent_cooperation=multi_agent_cooperation,
            system_evolution=system_evolution,
            analytics_system=analytics_system,
            interface_system=interface_system,
            prompts_subdir=data.get("prompts_subdir", "default"),
            memory_subdir=data.get("memory_subdir", ""),
            debug=data.get("debug", False),
            log_level=data.get("log_level", "INFO")
        )
