"""
© 2026 Tony Ray Macier III. All rights reserved.

Thalos Prime™ is a proprietary system.
"""

"""
Thalos Prime Utility Functions

Common utilities including validators, Result class, and deterministic helpers.
"""

import re
import hashlib
from typing import Any, Optional, Union, List, Dict, TypeVar, Generic
from datetime import datetime
from .exceptions import ValidationError


T = TypeVar('T')


class Result(Generic[T]):
    """
    Result type for explicit success/failure handling
    
    Forces explicit error handling instead of exceptions for expected failures.
    """
    
    def __init__(self, value: Optional[T] = None, error: Optional[str] = None, 
                 success: bool = True, details: Optional[Dict] = None):
        """
        Create a Result
        
        Args:
            value: The successful value
            error: Error message if failed
            success: Whether operation succeeded
            details: Additional details
        """
        self._value = value
        self._error = error
        self._success = success
        self._details = details or {}
    
    @classmethod
    def ok(cls, value: T) -> 'Result[T]':
        """Create a successful Result"""
        return cls(value=value, success=True)
    
    @classmethod
    def fail(cls, error: str, details: Optional[Dict] = None) -> 'Result[T]':
        """Create a failed Result"""
        return cls(error=error, success=False, details=details)
    
    def is_ok(self) -> bool:
        """Check if result is successful"""
        return self._success
    
    def is_err(self) -> bool:
        """Check if result is an error"""
        return not self._success
    
    def unwrap(self) -> T:
        """
        Get the value, raising exception if failed
        
        Raises:
            ValueError: If result is an error
        """
        if not self._success:
            raise ValueError(f"Called unwrap on error Result: {self._error}")
        return self._value
    
    def unwrap_or(self, default: T) -> T:
        """Get the value or return default if failed"""
        return self._value if self._success else default
    
    def expect(self, message: str) -> T:
        """
        Get the value or raise with custom message
        
        Args:
            message: Custom error message
            
        Raises:
            ValueError: If result is an error
        """
        if not self._success:
            raise ValueError(f"{message}: {self._error}")
        return self._value
    
    def error(self) -> Optional[str]:
        """Get error message"""
        return self._error
    
    def details(self) -> Dict:
        """Get additional details"""
        return self._details
    
    def __repr__(self) -> str:
        if self._success:
            return f"Result.ok({self._value})"
        return f"Result.fail({self._error})"


class Validator:
    """
    Collection of validation functions
    
    All validators raise ValidationError on failure.
    """
    
    @staticmethod
    def not_empty(value: str, field: str = "value") -> str:
        """Validate string is not empty"""
        if not value or not value.strip():
            raise ValidationError(
                f"{field} cannot be empty",
                field=field,
                value=value
            )
        return value.strip()
    
    @staticmethod
    def min_length(value: str, min_len: int, field: str = "value") -> str:
        """Validate minimum string length"""
        if len(value) < min_len:
            raise ValidationError(
                f"{field} must be at least {min_len} characters",
                field=field,
                value=value,
                details={'min_length': min_len, 'actual_length': len(value)}
            )
        return value
    
    @staticmethod
    def max_length(value: str, max_len: int, field: str = "value") -> str:
        """Validate maximum string length"""
        if len(value) > max_len:
            raise ValidationError(
                f"{field} must be at most {max_len} characters",
                field=field,
                value=value,
                details={'max_length': max_len, 'actual_length': len(value)}
            )
        return value
    
    @staticmethod
    def matches_pattern(value: str, pattern: str, field: str = "value") -> str:
        """Validate string matches regex pattern"""
        if not re.match(pattern, value):
            raise ValidationError(
                f"{field} does not match required pattern",
                field=field,
                value=value,
                details={'pattern': pattern}
            )
        return value
    
    @staticmethod
    def is_alpha(value: str, field: str = "value") -> str:
        """Validate string contains only letters"""
        if not value.isalpha():
            raise ValidationError(
                f"{field} must contain only letters",
                field=field,
                value=value
            )
        return value
    
    @staticmethod
    def is_alphanumeric(value: str, field: str = "value") -> str:
        """Validate string contains only letters and numbers"""
        if not value.isalnum():
            raise ValidationError(
                f"{field} must contain only letters and numbers",
                field=field,
                value=value
            )
        return value
    
    @staticmethod
    def in_range(value: Union[int, float], min_val: Union[int, float], 
                 max_val: Union[int, float], field: str = "value") -> Union[int, float]:
        """Validate numeric value is in range"""
        if not min_val <= value <= max_val:
            raise ValidationError(
                f"{field} must be between {min_val} and {max_val}",
                field=field,
                value=value,
                details={'min': min_val, 'max': max_val}
            )
        return value
    
    @staticmethod
    def is_positive(value: Union[int, float], field: str = "value") -> Union[int, float]:
        """Validate value is positive"""
        if value <= 0:
            raise ValidationError(
                f"{field} must be positive",
                field=field,
                value=value
            )
        return value
    
    @staticmethod
    def one_of(value: Any, allowed: List[Any], field: str = "value") -> Any:
        """Validate value is in allowed list"""
        if value not in allowed:
            raise ValidationError(
                f"{field} must be one of {allowed}",
                field=field,
                value=value,
                details={'allowed': allowed}
            )
        return value


def generate_id(prefix: str = "", data: Optional[str] = None) -> str:
    """
    Generate deterministic ID
    
    Args:
        prefix: Optional prefix
        data: Data to hash (if None, uses timestamp)
        
    Returns:
        Unique ID string
    """
    if data is None:
        data = f"{datetime.utcnow().isoformat()}_{id(object())}"
    
    hash_obj = hashlib.sha256(data.encode())
    hash_hex = hash_obj.hexdigest()[:16]
    
    if prefix:
        return f"{prefix}_{hash_hex}"
    return hash_hex


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename for safe filesystem use
    
    Args:
        filename: Input filename
        
    Returns:
        Sanitized filename
    """
    # Remove or replace unsafe characters
    sanitized = re.sub(r'[^\w\s\-\.]', '_', filename)
    # Remove leading/trailing spaces and dots
    sanitized = sanitized.strip('. ')
    # Collapse multiple underscores
    sanitized = re.sub(r'_+', '_', sanitized)
    return sanitized


def truncate_string(text: str, max_length: int, suffix: str = "...") -> str:
    """
    Truncate string to max length
    
    Args:
        text: Input text
        max_length: Maximum length
        suffix: Suffix to add if truncated
        
    Returns:
        Truncated string
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def deep_merge(base: Dict, override: Dict) -> Dict:
    """
    Deep merge two dictionaries
    
    Args:
        base: Base dictionary
        override: Dictionary to merge in
        
    Returns:
        Merged dictionary
    """
    result = base.copy()
    
    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = value
    
    return result


def format_timestamp(dt: Optional[datetime] = None, format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
    """
    Format timestamp in deterministic way
    
    Args:
        dt: Datetime to format (default: now)
        format_str: Format string
        
    Returns:
        Formatted timestamp
    """
    if dt is None:
        dt = datetime.utcnow()
    return dt.strftime(format_str)


def ensure_list(value: Any) -> List:
    """
    Ensure value is a list
    
    Args:
        value: Input value
        
    Returns:
        List containing value(s)
    """
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def safe_divide(numerator: Union[int, float], denominator: Union[int, float], 
                default: Union[int, float] = 0) -> Union[int, float]:
    """
    Safe division that returns default on division by zero
    
    Args:
        numerator: Numerator
        denominator: Denominator
        default: Default value if denominator is zero
        
    Returns:
        Division result or default
    """
    try:
        return numerator / denominator if denominator != 0 else default
    except (ZeroDivisionError, TypeError):
        return default


def clamp(value: Union[int, float], min_val: Union[int, float], 
          max_val: Union[int, float]) -> Union[int, float]:
    """
    Clamp value between min and max
    
    Args:
        value: Input value
        min_val: Minimum value
        max_val: Maximum value
        
    Returns:
        Clamped value
    """
    return max(min_val, min(value, max_val))
