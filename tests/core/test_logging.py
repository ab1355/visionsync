#!/usr/bin/env python3
"""
Tests for the logging system.
"""

import json
import logging
import os
import pytest
from datetime import datetime, timedelta
from pathlib import Path
from typing import Generator
from unittest.mock import patch, MagicMock

from core.logging import Log, LogEntry, JsonFormatter

@pytest.fixture
def temp_log_dir(tmp_path) -> Generator[Path, None, None]:
    """Create a temporary directory for log files."""
    log_dir = tmp_path / "logs"
    log_dir.mkdir()
    yield log_dir

@pytest.fixture
def log_entry() -> LogEntry:
    """Create a test log entry."""
    return LogEntry(
        message="Test message",
        level="INFO",
        context_id="test-context",
        metadata={"key": "value"}
    )

@pytest.fixture
def log(temp_log_dir) -> Log:
    """Create a test logger."""
    return Log(
        name="test-logger",
        level="DEBUG",
        log_dir=temp_log_dir,
        max_size=1024,
        backup_count=2
    )

def test_log_entry_initialization(log_entry):
    """Test LogEntry initialization."""
    assert log_entry.message == "Test message"
    assert log_entry.level == "INFO"
    assert log_entry.context_id == "test-context"
    assert isinstance(log_entry.timestamp, datetime)
    assert log_entry.metadata == {"key": "value"}

def test_log_entry_to_dict(log_entry):
    """Test LogEntry serialization to dictionary."""
    data = log_entry.to_dict()
    
    assert isinstance(data, dict)
    assert data["message"] == "Test message"
    assert data["level"] == "INFO"
    assert data["context_id"] == "test-context"
    assert isinstance(data["timestamp"], str)
    assert data["key"] == "value"

def test_log_entry_to_string(log_entry):
    """Test LogEntry string formatting."""
    text = log_entry.to_string()
    
    assert "Test message" in text
    assert "INFO" in text
    assert "test-context" in text
    assert "key=value" in text

def test_log_initialization(log, temp_log_dir):
    """Test Log initialization."""
    assert log.name == "test-logger"
    assert log.level == "DEBUG"
    assert isinstance(log.logger, logging.Logger)
    assert len(log.logger.handlers) == 3  # console, text file, and JSON file
    
    # Check log files were created
    assert (temp_log_dir / "test-logger.log").exists()
    assert (temp_log_dir / "test-logger.json").exists()

def test_log_add_entry(log):
    """Test adding log entries."""
    log.add("Test message", level="INFO", context_id="test-context")
    
    assert len(log.entries) == 1
    entry = log.entries[0]
    assert entry.message == "Test message"
    assert entry.level == "INFO"
    assert entry.context_id == "test-context"

def test_log_level_methods(log):
    """Test convenience methods for different log levels."""
    log.debug("Debug message")
    log.info("Info message")
    log.warning("Warning message")
    log.error("Error message")
    log.critical("Critical message")
    
    assert len(log.entries) == 5
    assert [e.level for e in log.entries] == [
        "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"
    ]

def test_log_filtering(log):
    """Test log entry filtering."""
    # Add entries with different levels and contexts
    log.info("Info 1", context_id="ctx1")
    log.debug("Debug 1", context_id="ctx1")
    log.warning("Warning 1", context_id="ctx2")
    log.error("Error 1", context_id="ctx2")
    
    # Filter by level
    info_entries = log.get_entries(level="INFO")
    assert len(info_entries) == 1
    assert info_entries[0].message == "Info 1"
    
    # Filter by context
    ctx1_entries = log.get_entries(context_id="ctx1")
    assert len(ctx1_entries) == 2
    assert all(e.context_id == "ctx1" for e in ctx1_entries)
    
    # Filter by time
    now = datetime.now()
    recent_entries = log.get_entries(
        start_time=now - timedelta(seconds=1),
        end_time=now + timedelta(seconds=1)
    )
    assert len(recent_entries) == 4

def test_log_clear(log):
    """Test clearing log entries."""
    log.info("Test message")
    assert len(log.entries) == 1
    
    log.clear()
    assert len(log.entries) == 0

def test_log_serialization(log):
    """Test log serialization to dictionary and JSON."""
    log.info("Test message", context_id="test-context")
    
    # Test to_dict
    data = log.to_dict()
    assert isinstance(data, dict)
    assert data["name"] == "test-logger"
    assert data["level"] == "DEBUG"
    assert len(data["entries"]) == 1
    
    # Test to_json
    json_data = log.to_json()
    assert isinstance(json_data, str)
    parsed = json.loads(json_data)
    assert parsed["name"] == "test-logger"

def test_json_formatter():
    """Test JSON formatter for log records."""
    formatter = JsonFormatter()
    record = MagicMock()
    record.created = datetime.now().timestamp()
    record.levelname = "INFO"
    record.name = "test-logger"
    record.getMessage.return_value = "Test message"
    record.context_id = "test-context"
    
    output = formatter.format(record)
    data = json.loads(output)
    
    assert isinstance(data, dict)
    assert "timestamp" in data
    assert data["level"] == "INFO"
    assert data["logger"] == "test-logger"
    assert data["message"] == "Test message"
    assert data["context_id"] == "test-context"

def test_log_file_rotation(temp_log_dir):
    """Test log file rotation."""
    # Create logger with small max_size
    log = Log(
        name="rotation-test",
        level="DEBUG",
        log_dir=temp_log_dir,
        max_size=50,  # Small size to trigger rotation
        backup_count=2
    )
    
    # Write enough entries to trigger rotation
    for i in range(10):
        log.info("X" * 10)  # Each entry is larger than max_size/2
    
    # Check that backup files were created
    log_files = list(temp_log_dir.glob("rotation-test.log*"))
    assert len(log_files) > 1

def test_log_with_exception(log):
    """Test logging with exception information."""
    try:
        raise ValueError("Test error")
    except ValueError as e:
        log.error("Error occurred", exc_info=e)
    
    assert len(log.entries) == 1
    entry = log.entries[0]
    assert entry.level == "ERROR"
    assert "Error occurred" in entry.message
    assert "exc_info" in entry.metadata

def test_log_context_inheritance(log):
    """Test context ID inheritance in nested logging."""
    log.context_id = "parent-context"
    
    # Log without explicit context_id
    log.info("Parent message")
    assert log.entries[-1].context_id == "parent-context"
    
    # Log with explicit context_id
    log.info("Child message", context_id="child-context")
    assert log.entries[-1].context_id == "child-context"

def test_invalid_log_level(temp_log_dir):
    """Test handling of invalid log level."""
    with pytest.raises(ValueError):
        Log(name="test", level="INVALID", log_dir=temp_log_dir)

def test_log_dir_creation(tmp_path):
    """Test automatic log directory creation."""
    log_dir = tmp_path / "nested" / "log" / "dir"
    
    # Directory shouldn't exist yet
    assert not log_dir.exists()
    
    # Creating log should create directory
    log = Log(name="test", log_dir=log_dir)
    
    assert log_dir.exists()
    assert log_dir.is_dir()
