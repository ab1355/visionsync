from typing import Optional, List, Any
import logging
from contextlib import contextmanager
from threading import Lock
from datetime import datetime

class ResourceManager:
    def __init__(self):
        self._resources: List[Any] = []
        self._lock = Lock()
        self.logger = logging.getLogger('VisionSync.ResourceManager')
        self._metrics = {
            'processing_rate': 0,
            'accuracy': 0,
            'scope': 0,
            'plan': 0,
            'analyze': 0,
            'create': 0,
            'execute': 0,
            'cognitive': {
                'discover': 0,
                'space': 0
            }
        }
        self._last_update = datetime.now()
        self._success_count = 0
        self._total_count = 0
    
    def add_resource(self, resource: Any):
        """Add a resource to be managed."""
        with self._lock:
            self._resources.append(resource)
            self._total_count += 1
            self._success_count += 1
            self._update_metrics()
    
    def remove_resource(self, resource: Any):
        """Remove a resource from management."""
        with self._lock:
            try:
                self._resources.remove(resource)
                self._update_metrics()
            except ValueError:
                self.logger.warning(f"Attempted to remove non-existent resource: {resource}")
                self._total_count += 1
    
    def _update_metrics(self):
        """Update internal metrics based on current state."""
        now = datetime.now()
        time_diff = (now - self._last_update).total_seconds()
        if time_diff > 0:
            self._metrics['processing_rate'] = int(self._success_count / time_diff * 60)
            self._last_update = now
            self._success_count = 0

        active_count = len(self._resources)
        self._metrics['accuracy'] = int((self._success_count / max(1, self._total_count)) * 100)
        
        # Update space metrics based on resource utilization
        total_capacity = max(1, active_count * 100)
        self._metrics['scope'] = min(100, int((active_count / total_capacity) * 100))
        self._metrics['plan'] = min(100, int((self._success_count / max(1, self._total_count)) * 100))
        self._metrics['analyze'] = min(100, int((active_count / max(1, total_capacity)) * 100))
        self._metrics['create'] = min(100, int((self._success_count / max(1, active_count)) * 100))
        self._metrics['execute'] = min(100, int((active_count / max(1, total_capacity)) * 100))
        
        # Update cognitive levels
        self._metrics['cognitive']['discover'] = min(100, 60 + int((self._success_count / max(1, self._total_count)) * 40))
        self._metrics['cognitive']['space'] = min(100, 60 + int((active_count / max(1, total_capacity)) * 40))
    
    def cleanup_resources(self):
        """Clean up all managed resources."""
        with self._lock:
            for resource in reversed(self._resources):
                try:
                    if hasattr(resource, 'close'):
                        resource.close()
                    elif hasattr(resource, 'cleanup'):
                        resource.cleanup()
                    elif hasattr(resource, '__del__'):
                        resource.__del__()
                except Exception as e:
                    self.logger.error(f"Error cleaning up resource {resource}: {e}")
                    self._total_count += 1
            self._resources.clear()
            self._update_metrics()
    
    @contextmanager
    def manage_resource(self, resource: Any):
        """Context manager for automatic resource management."""
        try:
            self.add_resource(resource)
            yield resource
        finally:
            self.remove_resource(resource)
            if hasattr(resource, 'close'):
                try:
                    resource.close()
                except Exception as e:
                    self.logger.error(f"Error closing resource {resource}: {e}")
                    self._total_count += 1

    def get_processing_rate(self) -> int:
        """Get the current processing rate."""
        with self._lock:
            return self._metrics['processing_rate']

    def get_accuracy(self) -> int:
        """Get the current accuracy level."""
        with self._lock:
            return self._metrics['accuracy']

    def get_metric(self, metric_name: str) -> int:
        """Get a specific metric value."""
        with self._lock:
            if metric_name in self._metrics:
                return self._metrics[metric_name]
            return 0

    def get_cognitive_level(self, system: str) -> int:
        """Get the cognitive level for a specific system."""
        with self._lock:
            if system in self._metrics['cognitive']:
                return self._metrics['cognitive'][system]
            return 0

    def update_metric(self, metric_name: str, value: int):
        """Update a specific metric value."""
        with self._lock:
            if metric_name in self._metrics:
                self._metrics[metric_name] = value
                self._update_metrics()

    def get_active_resources_count(self) -> int:
        """Get the count of currently active resources."""
        with self._lock:
            return len(self._resources)

    def record_success(self):
        """Record a successful operation."""
        with self._lock:
            self._success_count += 1
            self._total_count += 1
            self._update_metrics()

    def record_failure(self):
        """Record a failed operation."""
        with self._lock:
            self._total_count += 1
            self._update_metrics()

    def __enter__(self):
        """Enter context manager."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit context manager and cleanup resources."""
        self.cleanup_resources()
        if exc_type is not None:
            self.logger.error(f"Error during resource management: {exc_val}")
            return False  # Re-raise the exception
        return True

# Global resource manager instance
resource_manager = ResourceManager()
