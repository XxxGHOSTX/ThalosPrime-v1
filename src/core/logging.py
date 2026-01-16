"""
© 2026 Tony Ray Macier III. All rights reserved.

Thalos Prime is an original proprietary software system, including but not limited to
its source code, system architecture, internal logic descriptions, documentation,
interfaces, diagrams, and design materials.

Unauthorized reproduction, modification, distribution, public display, or use of
this software or its associated materials is strictly prohibited without the
express written permission of the copyright holder.

Thalos Prime™ is a proprietary system.
"""

"""
Thalos Prime - Logging System

Singleton logger with deterministic output and structured logging.
Provides consistent logging across all subsystems.
"""

import logging
import sys
from typing import Optional
from pathlib import Path
from datetime import datetime


class ThalosLogger:
    """
    Singleton logger for Thalos Prime.
    
    Provides deterministic, structured logging with:
    - Consistent format across all subsystems
    - File and console output
    - Log level control
    - Automatic log rotation
    """
    
    _instance: Optional['ThalosLogger'] = None
    _initialized: bool = False
    
    def __new__(cls):
        """Ensure singleton pattern"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
        
    def __init__(self):
        """Initialize logger (only once)"""
        if ThalosLogger._initialized:
            return
            
        self.logger = logging.getLogger('ThalosP rime')
        self.logger.setLevel(logging.DEBUG)  # Capture all levels
        self.logger.propagate = False  # Don't propagate to root logger
        
        # Remove any existing handlers
        self.logger.handlers.clear()
        
        # Default format
        self.format_string = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        self.formatter = logging.Formatter(self.format_string)
        
        # Console handler (default: INFO level)
        self.console_handler = logging.StreamHandler(sys.stdout)
        self.console_handler.setLevel(logging.INFO)
        self.console_handler.setFormatter(self.formatter)
        self.logger.addHandler(self.console_handler)
        
        # File handler will be added when configured
        self.file_handler: Optional[logging.FileHandler] = None
        
        ThalosLogger._initialized = True
        
    def configure(self, level: str = 'INFO', log_file: Optional[str] = None,
                 console: bool = True, format_string: Optional[str] = None) -> None:
        """
        Configure logger settings.
        
        Args:
            level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            log_file: Path to log file (if None, no file logging)
            console: Enable console output
            format_string: Custom format string
        """
        # Update log level
        log_level = getattr(logging, level.upper(), logging.INFO)
        self.logger.setLevel(log_level)
        
        # Update format if provided
        if format_string:
            self.format_string = format_string
            self.formatter = logging.Formatter(format_string)
            
        # Update console handler
        if console:
            if self.console_handler not in self.logger.handlers:
                self.logger.addHandler(self.console_handler)
            self.console_handler.setLevel(log_level)
            self.console_handler.setFormatter(self.formatter)
        else:
            if self.console_handler in self.logger.handlers:
                self.logger.removeHandler(self.console_handler)
                
        # Configure file handler
        if log_file:
            # Remove existing file handler
            if self.file_handler:
                self.logger.removeHandler(self.file_handler)
                self.file_handler.close()
                
            # Create log directory if needed
            log_path = Path(log_file)
            log_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Add new file handler
            self.file_handler = logging.FileHandler(log_file)
            self.file_handler.setLevel(log_level)
            self.file_handler.setFormatter(self.formatter)
            self.logger.addHandler(self.file_handler)
            
    def debug(self, message: str, **kwargs) -> None:
        """Log debug message"""
        self.logger.debug(message, extra=kwargs)
        
    def info(self, message: str, **kwargs) -> None:
        """Log info message"""
        self.logger.info(message, extra=kwargs)
        
    def warning(self, message: str, **kwargs) -> None:
        """Log warning message"""
        self.logger.warning(message, extra=kwargs)
        
    def error(self, message: str, **kwargs) -> None:
        """Log error message"""
        self.logger.error(message, extra=kwargs)
        
    def critical(self, message: str, **kwargs) -> None:
        """Log critical message"""
        self.logger.critical(message, extra=kwargs)
        
    def exception(self, message: str, exc_info=True, **kwargs) -> None:
        """Log exception with traceback"""
        self.logger.exception(message, exc_info=exc_info, extra=kwargs)
        
    def log_lifecycle(self, subsystem: str, event: str, success: bool = True,
                     details: Optional[dict] = None) -> None:
        """
        Log lifecycle event for a subsystem.
        
        Args:
            subsystem: Name of subsystem (e.g., 'CIS', 'Memory')
            event: Lifecycle event (e.g., 'initialize', 'validate', 'operate')
            success: Whether event was successful
            details: Optional additional details
        """
        status = "SUCCESS" if success else "FAILED"
        message = f"[{subsystem}] Lifecycle event '{event}': {status}"
        
        if details:
            message += f" | Details: {details}"
            
        if success:
            self.info(message)
        else:
            self.error(message)
            
    def log_state_transition(self, subsystem: str, from_state: str,
                            to_state: str, reason: Optional[str] = None) -> None:
        """
        Log state transition.
        
        Args:
            subsystem: Name of subsystem
            from_state: Previous state
            to_state: New state
            reason: Optional reason for transition
        """
        message = f"[{subsystem}] State transition: {from_state} -> {to_state}"
        if reason:
            message += f" | Reason: {reason}"
        self.info(message)
        
    def log_operation(self, subsystem: str, operation: str, 
                     params: Optional[dict] = None, result: Optional[dict] = None) -> None:
        """
        Log subsystem operation.
        
        Args:
            subsystem: Name of subsystem
            operation: Operation name
            params: Operation parameters
            result: Operation result
        """
        message = f"[{subsystem}] Operation: {operation}"
        if params:
            message += f" | Params: {params}"
        if result:
            message += f" | Result: {result}"
        self.debug(message)
        
    def get_logger(self) -> logging.Logger:
        """
        Get underlying logger instance.
        
        Returns:
            Python logging.Logger instance
        """
        return self.logger
        
    def shutdown(self) -> None:
        """Shutdown logger and close handlers"""
        if self.file_handler:
            self.file_handler.close()
            self.logger.removeHandler(self.file_handler)
            
        if self.console_handler:
            self.console_handler.close()
            self.logger.removeHandler(self.console_handler)
            
        logging.shutdown()


# Global logger instance
_logger_instance: Optional[ThalosLogger] = None


def get_logger() -> ThalosLogger:
    """
    Get global logger instance.
    
    Returns:
        Global ThalosLogger instance
    """
    global _logger_instance
    if _logger_instance is None:
        _logger_instance = ThalosLogger()
    return _logger_instance


def configure_logging(level: str = 'INFO', log_file: Optional[str] = None,
                     console: bool = True, format_string: Optional[str] = None) -> ThalosLogger:
    """
    Configure global logging.
    
    Args:
        level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Path to log file
        console: Enable console output
        format_string: Custom format string
        
    Returns:
        Configured ThalosLogger instance
    """
    logger = get_logger()
    logger.configure(level=level, log_file=log_file, console=console, 
                    format_string=format_string)
    return logger
