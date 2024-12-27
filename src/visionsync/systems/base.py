#!/usr/bin/env python3
"""
Base interfaces for Agent Zero enhancement systems.

This module defines the core protocols that all enhancement systems must implement,
ensuring consistent behavior and integration across the framework.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

class EnhancementSystem(ABC):
    """Base class for all enhancement systems."""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the enhancement system.
        
        Args:
            config: Configuration dictionary for the system
        """
        self.config = config
        self.enabled = config.get('enabled', True)
        self.debug = config.get('debug', False)
        self._initialize_system()

    @abstractmethod
    def _initialize_system(self) -> None:
        """Initialize system-specific components."""
        pass

    @abstractmethod
    async def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process data through the enhancement system.
        
        Args:
            data: Input data to process
            
        Returns:
            Processed data
        """
        pass

    @abstractmethod
    async def analyze(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze data for insights.
        
        Args:
            data: Data to analyze
            
        Returns:
            Analysis results
        """
        pass

    @abstractmethod
    async def adapt(self, feedback: Dict[str, Any]) -> None:
        """
        Adapt system behavior based on feedback.
        
        Args:
            feedback: Feedback data for adaptation
        """
        pass

class PatternSystem(EnhancementSystem):
    """Base interface for pattern recognition systems."""
    
    @abstractmethod
    async def detect_patterns(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Detect patterns in input data.
        
        Args:
            data: Data to analyze for patterns
            
        Returns:
            Detected patterns
        """
        pass

    @abstractmethod
    async def apply_patterns(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Apply detected patterns to new data.
        
        Args:
            data: Data to apply patterns to
            
        Returns:
            Data with patterns applied
        """
        pass

class ResourceSystem(EnhancementSystem):
    """Base interface for resource optimization systems."""
    
    @abstractmethod
    async def allocate_resources(self, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """
        Allocate resources based on requirements.
        
        Args:
            requirements: Resource requirements
            
        Returns:
            Resource allocation plan
        """
        pass

    @abstractmethod
    async def monitor_usage(self) -> Dict[str, float]:
        """
        Monitor current resource usage.
        
        Returns:
            Current resource usage metrics
        """
        pass

class LearningSystem(EnhancementSystem):
    """Base interface for learning integration systems."""
    
    @abstractmethod
    async def learn(self, experience: Dict[str, Any]) -> None:
        """
        Learn from new experience.
        
        Args:
            experience: Experience data to learn from
        """
        pass

    @abstractmethod
    async def apply_learning(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Apply learned knowledge to new context.
        
        Args:
            context: Context to apply learning to
            
        Returns:
            Enhanced context with learning applied
        """
        pass

class CooperationSystem(EnhancementSystem):
    """Base interface for multi-agent cooperation systems."""
    
    @abstractmethod
    async def coordinate(self, agents: Dict[str, Any]) -> Dict[str, Any]:
        """
        Coordinate between multiple agents.
        
        Args:
            agents: Agents to coordinate
            
        Returns:
            Coordination plan
        """
        pass

    @abstractmethod
    async def delegate(self, task: Dict[str, Any]) -> Optional[str]:
        """
        Delegate task to appropriate agent.
        
        Args:
            task: Task to delegate
            
        Returns:
            ID of agent task was delegated to, or None if no delegation
        """
        pass

class EvolutionSystem(EnhancementSystem):
    """Base interface for system evolution."""
    
    @abstractmethod
    async def evaluate(self) -> Dict[str, float]:
        """
        Evaluate current system performance.
        
        Returns:
            Performance metrics
        """
        pass

    @abstractmethod
    async def evolve(self, metrics: Dict[str, float]) -> None:
        """
        Evolve system based on performance metrics.
        
        Args:
            metrics: Performance metrics to base evolution on
        """
        pass

class AnalyticsSystem(EnhancementSystem):
    """Base interface for analytics systems."""
    
    @abstractmethod
    async def collect_metrics(self) -> Dict[str, Any]:
        """
        Collect current system metrics.
        
        Returns:
            Current metrics
        """
        pass

    @abstractmethod
    async def analyze_trends(self) -> Dict[str, Any]:
        """
        Analyze metric trends.
        
        Returns:
            Trend analysis results
        """
        pass

class InterfaceSystem(EnhancementSystem):
    """Base interface for interface systems."""
    
    @abstractmethod
    async def format_input(self, data: Any) -> Any:
        """
        Format input data for processing.
        
        Args:
            data: Input data to format
            
        Returns:
            Formatted input data
        """
        pass

    @abstractmethod
    async def format_output(self, data: Any) -> Any:
        """
        Format output data for presentation.
        
        Args:
            data: Output data to format
            
        Returns:
            Formatted output data
        """
        pass
