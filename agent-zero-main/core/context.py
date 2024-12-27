#!/usr/bin/env python3
"""
Context management for Agent Zero.

This module handles agent context and maintains the context hierarchy.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, Optional
import uuid

from core.config import AgentConfig
from core.logging import Log

@dataclass
class AgentContext:
    """
    Manages context for an agent instance.
    
    This class handles:
    - Context hierarchy and relationships
    - Agent configuration
    - Logging
    - State management
    """
    
    # Class-level storage
    _contexts: Dict[str, "AgentContext"] = field(default_factory=dict)
    _counter: int = 0
    
    # Instance attributes
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: Optional[str] = None
    config: AgentConfig = field(default_factory=AgentConfig)
    log: Log = field(default_factory=Log)
    
    # Relationship management
    parent: Optional["AgentContext"] = None
    children: Dict[str, "AgentContext"] = field(default_factory=dict)
    
    # State
    paused: bool = False
    active: bool = True
    data: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """Initialize context after creation."""
        # Increment counter
        AgentContext._counter += 1
        self.number = AgentContext._counter
        
        # Register context
        existing = self._contexts.get(self.id)
        if existing:
            AgentContext.remove(self.id)
        self._contexts[self.id] = self

    def add_child(self, child: "AgentContext") -> None:
        """
        Add a child context.
        
        Args:
            child: The child context to add
        """
        child.parent = self
        self.children[child.id] = child

    def remove_child(self, child_id: str) -> None:
        """
        Remove a child context.
        
        Args:
            child_id: ID of the child context to remove
        """
        if child_id in self.children:
            child = self.children[child_id]
            child.parent = None
            del self.children[child_id]

    def get_current_context(self) -> Dict[str, Any]:
        """
        Get the current context state.
        
        Returns:
            Dictionary containing current context data
        """
        return {
            'id': self.id,
            'name': self.name,
            'number': self.number,
            'parent_id': self.parent.id if self.parent else None,
            'child_ids': list(self.children.keys()),
            'data': self.data.copy(),
            'paused': self.paused,
            'active': self.active
        }

    def get_full_context(self) -> Dict[str, Any]:
        """
        Get the complete context including parent and children.
        
        Returns:
            Dictionary containing full context hierarchy
        """
        context = self.get_current_context()
        
        # Add parent context if exists
        if self.parent:
            context['parent'] = self.parent.get_current_context()
            
        # Add children contexts
        context['children'] = {
            child_id: child.get_current_context()
            for child_id, child in self.children.items()
        }
        
        return context

    @classmethod
    def get(cls, id: str) -> Optional["AgentContext"]:
        """
        Get a context by ID.
        
        Args:
            id: The context ID to retrieve
            
        Returns:
            The context if found, None otherwise
        """
        return cls._contexts.get(id)

    @classmethod
    def remove(cls, id: str) -> None:
        """
        Remove a context by ID.
        
        Args:
            id: The context ID to remove
        """
        if id in cls._contexts:
            context = cls._contexts[id]
            
            # Remove parent relationship
            if context.parent:
                context.parent.remove_child(id)
                
            # Remove child relationships
            for child_id in list(context.children.keys()):
                context.remove_child(child_id)
                
            # Remove from storage
            del cls._contexts[id]

    def pause(self) -> None:
        """Pause this context."""
        self.paused = True
        self.log.add(f"Context {self.id} paused")

    def resume(self) -> None:
        """Resume this context."""
        self.paused = False
        self.log.add(f"Context {self.id} resumed")

    def deactivate(self) -> None:
        """Deactivate this context."""
        self.active = False
        self.log.add(f"Context {self.id} deactivated")
        
        # Deactivate children
        for child in self.children.values():
            child.deactivate()

    def activate(self) -> None:
        """Activate this context."""
        self.active = True
        self.log.add(f"Context {self.id} activated")
