import logging
import uuid
from typing import Optional, Dict, Any
from dataclasses import dataclass
from flask import Response
import traceback
from datetime import datetime

@dataclass
class ErrorContext:
    component: str
    operation: str
    user_id: Optional[str] = None
    additional_data: Optional[Dict[str, Any]] = None

class ErrorHandler:
    def __init__(self):
        self._configure_logging()
        
    def _configure_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('errors.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger('AgentZero')
    
    def generate_error_id(self) -> str:
        """Generate a unique error ID for tracking."""
        return str(uuid.uuid4())
    
    def log_error(self, error_id: str, error: Exception, context: ErrorContext):
        """Log error details with context."""
        error_details = {
            'error_id': error_id,
            'timestamp': datetime.utcnow().isoformat(),
            'error_type': type(error).__name__,
            'error_message': str(error),
            'component': context.component,
            'operation': context.operation,
            'traceback': traceback.format_exc(),
            'user_id': context.user_id,
            'additional_data': context.additional_data
        }
        
        self.logger.error(
            f"Error ID: {error_id}\n"
            f"Component: {context.component}\n"
            f"Operation: {context.operation}\n"
            f"Error: {str(error)}\n"
            f"Details: {error_details}"
        )
        return error_details
    
    def create_error_response(self, error_id: str, error: Exception, status_code: int = 500) -> Response:
        """Create a standardized error response."""
        if status_code >= 500:
            # Don't expose internal error details to client
            message = "An internal server error occurred"
        else:
            # For 4xx errors, we can be more specific
            message = str(error)
            
        return Response(
            response={
                'error': {
                    'id': error_id,
                    'message': message,
                    'status_code': status_code
                }
            },
            status=status_code,
            mimetype='application/json'
        )
    
    def handle_error(self, error: Exception, context: ErrorContext) -> Response:
        """Main error handling method combining logging and response creation."""
        error_id = self.generate_error_id()
        error_details = self.log_error(error_id, error, context)
        
        # Determine appropriate status code based on error type
        if isinstance(error, ValueError):
            status_code = 400
        elif isinstance(error, PermissionError):
            status_code = 403
        elif isinstance(error, FileNotFoundError):
            status_code = 404
        else:
            status_code = 500
            
        return self.create_error_response(error_id, error, status_code)

# Global error handler instance
error_handler = ErrorHandler()
