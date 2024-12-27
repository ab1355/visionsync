#!/usr/bin/env python3
"""
Core Agent implementation providing the base agent functionality.
"""

import asyncio
import uuid
from typing import Any, List, Optional

from ..core.context import AgentContext
from ..core.config import AgentConfig
from ..systems.base import InterfaceSystem
from ..systems.pattern import PatternEngine
from ..systems.base import ResourceSystem as ResourceManager
from ..systems.base import LearningSystem as LearningEngine
from ..systems.base import CooperationSystem as CoordinationEngine
from ..systems.base import EvolutionSystem as EvolutionEngine
from ..systems.base import AnalyticsSystem as AnalyticsEngine

class Agent:
    """
    Core Agent class handling primary agent functionality.
    
    This class coordinates between different enhancement systems and handles
    the main conversation loop and response generation.
    """
    
    def __init__(self, number: int, config: AgentConfig, context: Optional[AgentContext] = None):
        """
        Initialize a new Agent instance.
        
        Args:
            number: Unique identifier for this agent
            config: Configuration settings for the agent
            context: Optional context for the agent
        """
        # Core initialization
        self.number = number
        self.config = config
        self.context = context or AgentContext(config=config)
        self.agent_name = f"Agent {self.number}"
        self.id = str(uuid.uuid4())
        
        # Enhancement systems
        self.pattern_engine = PatternEngine(self.config.pattern_recognition)
        self.resource_manager = ResourceManager(self.config.resource_optimization)
        self.learning_engine = LearningEngine(self.config.learning_integration)
        self.cooperation_engine = CoordinationEngine(self.config.multi_agent_cooperation)
        self.evolution_engine = EvolutionEngine(self.config.system_evolution)
        self.analytics_engine = AnalyticsEngine(self.config.analytics_system)
        self.interface_engine = InterfaceSystem(self.config.interface_system)
        
        # State management
        self.history: List[Any] = []
        self.last_user_message = None
        self.intervention = None
        self.data = {}

    async def monologue(self) -> Any:
        """
        Main agent loop handling the conversation flow.
        
        Returns:
            Result of the conversation or None if interrupted
        """
        while True:
            try:
                # Initialize loop
                self.loop_data = await self.initialize_loop()
                
                # Process through enhancement systems
                await self.process_through_systems()
                
                # Main conversation loop
                while True:
                    try:
                        # Prepare prompt
                        prompt = await self.prepare_prompt()
                        
                        # Generate response
                        response = await self.generate_response(prompt)
                        
                        # Process response
                        result = await self.process_response(response)
                        
                        if result:
                            return result
                            
                    except Exception as e:
                        await self.handle_exception(e)
                        
            except Exception as e:
                await self.handle_critical_exception(e)

    async def initialize_loop(self) -> dict:
        """
        Initialize data for a new conversation loop.
        
        Returns:
            Dictionary containing loop initialization data
        """
        return {
            'start_time': asyncio.get_event_loop().time(),
            'context': self.context.get_current_context(),
            'history': self.history.copy()
        }

    async def process_through_systems(self) -> None:
        """Process the current state through all enhancement systems."""
        # Pattern recognition
        patterns = await self.pattern_engine.process_patterns(self.loop_data)
        
        # Resource optimization
        resources = await self.resource_manager.optimize_resources()
        
        # Learning integration
        learning = await self.learning_engine.process_learning()
        
        # Multi-agent cooperation
        cooperation = await self.cooperation_engine.coordinate_agents()
        
        # System evolution
        evolution = await self.evolution_engine.evolve_system()
        
        # Analytics processing
        analytics = await self.analytics_engine.analyze_system()
        
        # Interface enhancement
        interface = await self.interface_engine.process_interaction()
        
        # Integrate results
        await self.integrate_system_results(
            patterns, resources, learning, cooperation,
            evolution, analytics, interface
        )

    async def prepare_prompt(self) -> str:
        """
        Prepare the prompt for the next interaction.
        
        Returns:
            Formatted prompt string
        """
        # Get system prompt
        system_prompt = await self.get_system_prompt()
        
        # Get enhancement data
        system_data = await self.get_system_enhancements()
        
        # Combine prompts
        return "\n\n".join(system_prompt + system_data)

    async def generate_response(self, prompt: str) -> str:
        """
        Generate a response using the configured model.
        
        Args:
            prompt: The input prompt
            
        Returns:
            Generated response string
        """
        # Process through interface
        formatted_prompt = await self.interface_engine.format_prompt(prompt)
        
        # Generate response
        response = await self.call_model(formatted_prompt)
        
        # Analyze response
        await self.analytics_engine.analyze_response(response)
        
        return response

    async def process_response(self, response: str) -> Any:
        """
        Process the generated response.
        
        Args:
            response: The response to process
            
        Returns:
            Processing result or None
        """
        # Process through interface
        formatted_response = await self.interface_engine.format_response(response)
        
        # Extract and execute tools
        result = await self.process_tools(formatted_response)
        
        # Learn from execution
        await self.learning_engine.learn_from_execution(result)
        
        return result

    async def handle_exception(self, error: Exception) -> None:
        """
        Handle non-critical exceptions during execution.
        
        Args:
            error: The exception to handle
        """
        await self.analytics_engine.log_error(error)
        self.context.log.add(f"Error: {str(error)}")

    async def handle_critical_exception(self, error: Exception) -> None:
        """
        Handle critical exceptions that require loop termination.
        
        Args:
            error: The critical exception to handle
        """
        await self.analytics_engine.log_critical_error(error)
        self.context.log.add(f"Critical Error: {str(error)}")
        raise error  # Re-raise to terminate the loop
