"""
© 2026 Tony Ray Macier III. All rights reserved.

Thalos Prime™ is a proprietary system.
"""

"""
Thalos Prime Logging System

Singleton logger with deterministic output.
All logging must be observable, serializable, and reproducible.
"""

import logging
import sys
from pathlib import Path
from typing import Optional
from datetime import datetime


class ThalosLogger:
    """
    Singleton logger for Thalos Prime
    
    Provides deterministic, structured logging with:
    - Single instance across application
    - Consistent format
    - Multiple output destinations
    - Structured data support
    """
    
    _instance: Optional['ThalosLogger'] = None
    _initialized: bool = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize logger (only once)"""
        if self._initialized:
            return
            
        self.logger = logging.getLogger('thalos_prime')
        self.logger.setLevel(logging.DEBUG)
        
        # Clear any existing handlers
        self.logger.handlers.clear()
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_format = logging.Formatter(
            '%(asctime)s [%(levelname)s] %(name)s: %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_handler.setFormatter(console_format)
        self.logger.addHandler(console_handler)
        
        # File handler (if logs directory exists)
        log_dir = Path('logs')
        if log_dir.exists() or self._create_log_dir(log_dir):
            log_file = log_dir / f'thalos_{datetime.now().strftime("%Y%m%d")}.log'
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(logging.DEBUG)
            file_format = logging.Formatter(
                '%(asctime)s [%(levelname)s] %(name)s - %(filename)s:%(lineno)d - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            file_handler.setFormatter(file_format)
            self.logger.addHandler(file_handler)
        
        self._initialized = True
        
    def _create_log_dir(self, log_dir: Path) -> bool:
        """Create log directory if possible"""
        try:
            log_dir.mkdir(parents=True, exist_ok=True)
            return True
        except (PermissionError, OSError):
            return False
    
    def debug(self, message: str, **kwargs):
        """Log debug message"""
        self.logger.debug(message, extra=kwargs)
        
    def info(self, message: str, **kwargs):
        """Log info message"""
        self.logger.info(message, extra=kwargs)
        
    def warning(self, message: str, **kwargs):
        """Log warning message"""
        self.logger.warning(message, extra=kwargs)
        
    def error(self, message: str, **kwargs):
        """Log error message"""
        self.logger.error(message, extra=kwargs)
        
    def critical(self, message: str, **kwargs):
        """Log critical message"""
        self.logger.critical(message, extra=kwargs)
        
    def exception(self, message: str, exc_info=True, **kwargs):
        """Log exception with traceback"""
        self.logger.exception(message, exc_info=exc_info, extra=kwargs)
        
    def lifecycle(self, phase: str, subsystem: str, status: str, **kwargs):
        """Log lifecycle event"""
        message = f"[LIFECYCLE] {subsystem}.{phase}() -> {status}"
        self.logger.info(message, extra={'phase': phase, 'subsystem': subsystem, 'status': status, **kwargs})
        
    def state_transition(self, subsystem: str, from_state: str, to_state: str, **kwargs):
        """Log state transition"""
        message = f"[STATE] {subsystem}: {from_state} -> {to_state}"
        self.logger.info(message, extra={'subsystem': subsystem, 'from_state': from_state, 'to_state': to_state, **kwargs})
        
    def set_level(self, level: str):
        """Set logging level"""
        level_map = {
            'DEBUG': logging.DEBUG,
            'INFO': logging.INFO,
            'WARNING': logging.WARNING,
            'ERROR': logging.ERROR,
            'CRITICAL': logging.CRITICAL
        }
        self.logger.setLevel(level_map.get(level.upper(), logging.INFO))


# Global singleton instance
def get_logger() -> ThalosLogger:
    """Get the singleton logger instance"""
    return ThalosLogger()


# Module-level convenience functions
def debug(message: str, **kwargs):
    """Log debug message"""
    get_logger().debug(message, **kwargs)


def info(message: str, **kwargs):
    """Log info message"""
    get_logger().info(message, **kwargs)


def warning(message: str, **kwargs):
    """Log warning message"""
    get_logger().warning(message, **kwargs)


def error(message: str, **kwargs):
    """Log error message"""
    get_logger().error(message, **kwargs)


def critical(message: str, **kwargs):
    """Log critical message"""
    get_logger().critical(message, **kwargs)


def exception(message: str, **kwargs):
    """Log exception with traceback"""
    get_logger().exception(message, **kwargs)


def lifecycle(phase: str, subsystem: str, status: str, **kwargs):
    """Log lifecycle event"""
    get_logger().lifecycle(phase, subsystem, status, **kwargs)


def state_transition(subsystem: str, from_state: str, to_state: str, **kwargs):
    """Log state transition"""
    get_logger().state_transition(subsystem, from_state, to_state, **kwargs)
