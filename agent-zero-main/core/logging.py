#!/usr/bin/env python3
"""
Logging system for Agent Zero.

This module provides structured logging capabilities with:
- Multiple output formats (text, JSON)
- Log level filtering
- Rotation support
- Context tracking
"""

import json
import logging
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from logging.handlers import RotatingFileHandler

class LogEntry:
    """Represents a single log entry with metadata."""
    
    def __init__(
        self,
        message: str,
        level: str = "INFO",
        context_id: Optional[str] = None,
        timestamp: Optional[datetime] = None,
        **kwargs
    ):
        self.message = message
        self.level = level.upper()
        self.context_id = context_id
        self.timestamp = timestamp or datetime.now()
        self.metadata = kwargs
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert entry to dictionary format."""
        return {
            "timestamp": self.timestamp.isoformat(),
            "level": self.level,
            "message": self.message,
            "context_id": self.context_id,
            **self.metadata
        }
        
    def to_string(self) -> str:
        """Convert entry to formatted string."""
        timestamp = self.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        context = f"[{self.context_id}]" if self.context_id else ""
        metadata = " ".join(f"{k}={v}" for k, v in self.metadata.items())
        return f"{timestamp} {self.level} {context} {self.message} {metadata}".strip()

class Log:
    """
    Main logging class supporting multiple outputs and formats.
    
    Features:
    - Multiple output handlers
    - Log level filtering
    - Context tracking
    - Structured data logging
    """
    
    def __init__(
        self,
        name: str = "agent-zero",
        level: str = "INFO",
        log_dir: Optional[Union[str, Path]] = None,
        max_size: int = 10 * 1024 * 1024,  # 10MB
        backup_count: int = 5,
        context_id: Optional[str] = None
    ):
        self.name = name
        self.level = level.upper()
        self.context_id = context_id
        self.entries: List[LogEntry] = []
        
        # Set up Python logger
        self.logger = logging.getLogger(name)
        self.logger.setLevel(self.level)
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(
            logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        )
        self.logger.addHandler(console_handler)
        
        # File handler if log_dir specified
        if log_dir:
            log_dir = Path(log_dir)
            log_dir.mkdir(parents=True, exist_ok=True)
            
            # Text log
            text_handler = RotatingFileHandler(
                log_dir / f"{name}.log",
                maxBytes=max_size,
                backupCount=backup_count
            )
            text_handler.setFormatter(
                logging.Formatter('%(asctime)s %(levelname)s %(message)s')
            )
            self.logger.addHandler(text_handler)
            
            # JSON log
            json_handler = RotatingFileHandler(
                log_dir / f"{name}.json",
                maxBytes=max_size,
                backupCount=backup_count
            )
            json_handler.setFormatter(JsonFormatter())
            self.logger.addHandler(json_handler)

    def add(
        self,
        message: str,
        level: str = "INFO",
        context_id: Optional[str] = None,
        **kwargs
    ) -> None:
        """
        Add a new log entry.
        
        Args:
            message: The log message
            level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            context_id: Optional context identifier
            **kwargs: Additional metadata to include
        """
        # Create entry
        entry = LogEntry(
            message=message,
            level=level,
            context_id=context_id or self.context_id,
            **kwargs
        )
        
        # Store entry
        self.entries.append(entry)
        
        # Log through Python logger
        log_level = getattr(logging, entry.level)
        self.logger.log(log_level, entry.to_string())

    def debug(self, message: str, **kwargs) -> None:
        """Add debug level entry."""
        self.add(message, "DEBUG", **kwargs)

    def info(self, message: str, **kwargs) -> None:
        """Add info level entry."""
        self.add(message, "INFO", **kwargs)

    def warning(self, message: str, **kwargs) -> None:
        """Add warning level entry."""
        self.add(message, "WARNING", **kwargs)

    def error(self, message: str, **kwargs) -> None:
        """Add error level entry."""
        self.add(message, "ERROR", **kwargs)

    def critical(self, message: str, **kwargs) -> None:
        """Add critical level entry."""
        self.add(message, "CRITICAL", **kwargs)

    def get_entries(
        self,
        level: Optional[str] = None,
        context_id: Optional[str] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None
    ) -> List[LogEntry]:
        """
        Get filtered log entries.
        
        Args:
            level: Filter by log level
            context_id: Filter by context ID
            start_time: Filter entries after this time
            end_time: Filter entries before this time
            
        Returns:
            List of matching LogEntry objects
        """
        entries = self.entries
        
        if level:
            entries = [e for e in entries if e.level == level.upper()]
            
        if context_id:
            entries = [e for e in entries if e.context_id == context_id]
            
        if start_time:
            entries = [e for e in entries if e.timestamp >= start_time]
            
        if end_time:
            entries = [e for e in entries if e.timestamp <= end_time]
            
        return entries

    def clear(self) -> None:
        """Clear all stored log entries."""
        self.entries = []

    def to_dict(self) -> Dict[str, Any]:
        """Convert all entries to dictionary format."""
        return {
            "name": self.name,
            "level": self.level,
            "context_id": self.context_id,
            "entries": [entry.to_dict() for entry in self.entries]
        }

    def to_json(self) -> str:
        """Convert all entries to JSON format."""
        return json.dumps(self.to_dict(), default=str)

class JsonFormatter(logging.Formatter):
    """Custom formatter for JSON log output."""
    
    def format(self, record: logging.LogRecord) -> str:
        """Format record as JSON string."""
        data = {
            "timestamp": datetime.fromtimestamp(record.created).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage()
        }
        
        if hasattr(record, "context_id"):
            data["context_id"] = record.context_id
            
        return json.dumps(data)
