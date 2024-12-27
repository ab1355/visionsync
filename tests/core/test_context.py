#!/usr/bin/env python3
"""
Tests for the AgentContext implementation.
"""

import pytest
from unittest.mock import MagicMock

from core.config import AgentConfig
from core.context import AgentContext
from core.logging import Log

@pytest.fixture
def config():
    """Create a test configuration."""
    return AgentConfig()

@pytest.fixture
def context(config):
    """Create a test context."""
    return AgentContext(config=config)

def test_context_initialization(context):
    """Test context initialization."""
    assert isinstance(context.id, str)
    assert isinstance(context.config, AgentConfig)
    assert isinstance(context.log, Log)
    assert context.parent is None
    assert isinstance(context.children, dict)
    assert not context.paused
    assert context.active
    assert isinstance(context.data, dict)

def test_context_registration(config):
    """Test context registration in class storage."""
    context = AgentContext(config=config)
    assert AgentContext.get(context.id) == context

def test_context_hierarchy(config):
    """Test parent-child relationship management."""
    parent = AgentContext(config=config)
    child = AgentContext(config=config)
    
    # Add child
    parent.add_child(child)
    assert child.id in parent.children
    assert parent.children[child.id] == child
    assert child.parent == parent
    
    # Remove child
    parent.remove_child(child.id)
    assert child.id not in parent.children
    assert child.parent is None

def test_context_removal(config):
    """Test context removal and cleanup."""
    parent = AgentContext(config=config)
    child = AgentContext(config=config)
    parent.add_child(child)
    
    # Remove parent
    AgentContext.remove(parent.id)
    assert AgentContext.get(parent.id) is None
    assert AgentContext.get(child.id) is not None
    assert child.parent is None

def test_get_current_context(context):
    """Test current context data retrieval."""
    data = context.get_current_context()
    
    assert isinstance(data, dict)
    assert data['id'] == context.id
    assert data['name'] == context.name
    assert data['number'] == context.number
    assert data['parent_id'] is None
    assert isinstance(data['child_ids'], list)
    assert isinstance(data['data'], dict)
    assert isinstance(data['paused'], bool)
    assert isinstance(data['active'], bool)

def test_get_full_context(config):
    """Test full context hierarchy retrieval."""
    parent = AgentContext(config=config)
    child = AgentContext(config=config)
    parent.add_child(child)
    
    data = parent.get_full_context()
    
    assert isinstance(data, dict)
    assert data['id'] == parent.id
    assert 'children' in data
    assert child.id in data['children']
    assert data['children'][child.id]['id'] == child.id
    assert data['parent'] is None

    child_data = child.get_full_context()
    assert child_data['parent']['id'] == parent.id

def test_context_state_management(context):
    """Test context state management."""
    # Test pause/resume
    context.pause()
    assert context.paused
    assert "Context {} paused".format(context.id) in [e.message for e in context.log.entries]
    
    context.resume()
    assert not context.paused
    assert "Context {} resumed".format(context.id) in [e.message for e in context.log.entries]
    
    # Test activation/deactivation
    context.deactivate()
    assert not context.active
    assert "Context {} deactivated".format(context.id) in [e.message for e in context.log.entries]
    
    context.activate()
    assert context.active
    assert "Context {} activated".format(context.id) in [e.message for e in context.log.entries]

def test_context_deactivation_hierarchy(config):
    """Test hierarchical context deactivation."""
    parent = AgentContext(config=config)
    child1 = AgentContext(config=config)
    child2 = AgentContext(config=config)
    
    parent.add_child(child1)
    parent.add_child(child2)
    
    # Deactivate parent
    parent.deactivate()
    
    assert not parent.active
    assert not child1.active
    assert not child2.active

def test_context_data_isolation(config):
    """Test data isolation between contexts."""
    context1 = AgentContext(config=config)
    context2 = AgentContext(config=config)
    
    context1.data['test'] = 'value1'
    context2.data['test'] = 'value2'
    
    assert context1.data['test'] == 'value1'
    assert context2.data['test'] == 'value2'

def test_context_counter(config):
    """Test context counter incrementation."""
    initial_counter = AgentContext._counter
    
    context1 = AgentContext(config=config)
    context2 = AgentContext(config=config)
    
    assert context2.number == context1.number + 1
    assert AgentContext._counter == initial_counter + 2

def test_context_logging(context):
    """Test context logging functionality."""
    test_message = "Test log message"
    context.log.add(test_message)
    
    assert test_message in [entry.message for entry in context.log.entries]

def test_duplicate_context_handling(config):
    """Test handling of duplicate context IDs."""
    context1 = AgentContext(config=config)
    original_id = context1.id
    
    # Create context with same ID
    context2 = AgentContext(config=config)
    context2.id = original_id
    
    # Initialize should replace old context
    context2.__post_init__()
    
    assert AgentContext.get(original_id) == context2
    assert AgentContext.get(original_id) != context1
