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
Thalos Prime - Utility Functions

Validators, Result class, and deterministic helpers.
"""

import re
import json
from typing import Any, Dict, List, Optional, Union, Callable, TypeVar, Generic
from datetime import datetime
from enum import Enum


T = TypeVar('T')


class Result(Generic[T]):
    """
    Result type for deterministic error handling.
    
    Replaces exceptions with explicit success/failure returns.
    Inspired by Rust's Result<T, E> type.
    """
    
    def __init__(self, value: Optional[T] = None, error: Optional[str] = None,
                 success: bool = True):
        """
        Initialize result.
        
        Args:
            value: Success value
            error: Error message
            success: Whether operation succeeded
        """
        self._success = success
        self._value = value
        self._error = error
        
    @property
    def success(self) -> bool:
        """Check if result is successful"""
        return self._success
        
    @property
    def failure(self) -> bool:
        """Check if result is failure"""
        return not self._success
        
    @property
    def value(self) -> T:
        """Get success value (raises if failure)"""
        if self._success:
            return self._value
        raise ValueError(f"Cannot get value from failed result: {self._error}")
        
    @property
    def error(self) -> Optional[str]:
        """Get error message"""
        return self._error
        
    def unwrap(self) -> T:
        """Unwrap value (raises if failure) - alias for .value"""
        return self.value
        
    def unwrap_or(self, default: T) -> T:
        """Unwrap value or return default"""
        return self._value if self._success else default
        
    def map(self, func: Callable[[T], Any]) -> 'Result':
        """Apply function to value if successful"""
        if self._success:
            try:
                new_value = func(self._value)
                return Result(value=new_value, success=True)
            except Exception as e:
                return Result(error=str(e), success=False)
        return self
        
    def __repr__(self) -> str:
        """String representation"""
        if self._success:
            return f"Result(success=True, value={self._value})"
        return f"Result(success=False, error={self._error})"
        
    @staticmethod
    def ok(value: T) -> 'Result[T]':
        """Create successful result"""
        return Result(value=value, success=True)
        
    @staticmethod
    def err(error: str) -> 'Result[T]':
        """Create failed result"""
        return Result(error=error, success=False)


class ValidationResult:
    """
    Validation result with detailed error information.
    """
    
    def __init__(self, valid: bool = True, errors: Optional[List[str]] = None):
        """
        Initialize validation result.
        
        Args:
            valid: Whether validation passed
            errors: List of validation errors
        """
        self.valid = valid
        self.errors = errors or []
        
    def add_error(self, error: str) -> None:
        """Add validation error"""
        self.valid = False
        self.errors.append(error)
        
    def merge(self, other: 'ValidationResult') -> 'ValidationResult':
        """Merge with another validation result"""
        return ValidationResult(
            valid=self.valid and other.valid,
            errors=self.errors + other.errors
        )
        
    def __bool__(self) -> bool:
        """Allow use in boolean context"""
        return self.valid
        
    def __repr__(self) -> str:
        """String representation"""
        if self.valid:
            return "ValidationResult(valid=True)"
        return f"ValidationResult(valid=False, errors={self.errors})"


class Validator:
    """
    Static validators for common validation tasks.
    """
    
    @staticmethod
    def is_not_empty(value: str, field_name: str = "value") -> ValidationResult:
        """Validate string is not empty"""
        if not value or not value.strip():
            return ValidationResult(valid=False, 
                                  errors=[f"{field_name} cannot be empty"])
        return ValidationResult(valid=True)
        
    @staticmethod
    def is_valid_identifier(value: str, field_name: str = "identifier") -> ValidationResult:
        """Validate string is valid Python identifier"""
        if not value:
            return ValidationResult(valid=False, 
                                  errors=[f"{field_name} cannot be empty"])
        
        # Check Python identifier rules
        if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', value):
            return ValidationResult(valid=False, 
                                  errors=[f"{field_name} must be a valid Python identifier"])
        
        # Check not a keyword
        import keyword
        if keyword.iskeyword(value):
            return ValidationResult(valid=False, 
                                  errors=[f"{field_name} cannot be a Python keyword"])
        
        return ValidationResult(valid=True)
        
    @staticmethod
    def is_in_range(value: Union[int, float], min_val: Union[int, float], 
                   max_val: Union[int, float], field_name: str = "value") -> ValidationResult:
        """Validate number is in range"""
        if value < min_val or value > max_val:
            return ValidationResult(valid=False, 
                                  errors=[f"{field_name} must be between {min_val} and {max_val}"])
        return ValidationResult(valid=True)
        
    @staticmethod
    def is_positive(value: Union[int, float], field_name: str = "value") -> ValidationResult:
        """Validate number is positive"""
        if value <= 0:
            return ValidationResult(valid=False, 
                                  errors=[f"{field_name} must be positive"])
        return ValidationResult(valid=True)
        
    @staticmethod
    def is_dict(value: Any, field_name: str = "value") -> ValidationResult:
        """Validate value is a dictionary"""
        if not isinstance(value, dict):
            return ValidationResult(valid=False, 
                                  errors=[f"{field_name} must be a dictionary"])
        return ValidationResult(valid=True)
        
    @staticmethod
    def is_list(value: Any, field_name: str = "value") -> ValidationResult:
        """Validate value is a list"""
        if not isinstance(value, list):
            return ValidationResult(valid=False, 
                                  errors=[f"{field_name} must be a list"])
        return ValidationResult(valid=True)
        
    @staticmethod
    def has_keys(value: dict, required_keys: List[str], 
                field_name: str = "dictionary") -> ValidationResult:
        """Validate dictionary has required keys"""
        missing_keys = [k for k in required_keys if k not in value]
        if missing_keys:
            return ValidationResult(valid=False, 
                                  errors=[f"{field_name} missing required keys: {missing_keys}"])
        return ValidationResult(valid=True)


def serialize_state(state: Dict[str, Any]) -> str:
    """
    Serialize state to JSON string.
    
    Args:
        state: State dictionary
        
    Returns:
        JSON string representation
    """
    return json.dumps(state, default=str, sort_keys=True, indent=2)


def deserialize_state(state_str: str) -> Dict[str, Any]:
    """
    Deserialize state from JSON string.
    
    Args:
        state_str: JSON string
        
    Returns:
        State dictionary
    """
    return json.loads(state_str)


def timestamp() -> str:
    """
    Get current timestamp in ISO format.
    
    Returns:
        ISO formatted timestamp string
    """
    return datetime.utcnow().isoformat() + 'Z'


def version_state(state: Dict[str, Any], version: str = "1.0") -> Dict[str, Any]:
    """
    Add version and timestamp to state.
    
    Args:
        state: State dictionary
        version: Version string
        
    Returns:
        Versioned state dictionary
    """
    return {
        '_version': version,
        '_timestamp': timestamp(),
        'data': state
    }


def safe_dict_get(d: dict, key: str, default: Any = None) -> Any:
    """
    Safely get value from dictionary with default.
    
    Args:
        d: Dictionary
        key: Key to get
        default: Default value if key not found
        
    Returns:
        Value or default
    """
    return d.get(key, default)


def merge_dicts(*dicts: dict) -> dict:
    """
    Merge multiple dictionaries.
    
    Later dictionaries override earlier ones.
    
    Args:
        *dicts: Dictionaries to merge
        
    Returns:
        Merged dictionary
    """
    result = {}
    for d in dicts:
        result.update(d)
    return result


def deep_merge_dicts(base: dict, override: dict) -> dict:
    """
    Deep merge two dictionaries.
    
    Recursively merges nested dictionaries.
    
    Args:
        base: Base dictionary
        override: Override dictionary
        
    Returns:
        Merged dictionary
    """
    result = base.copy()
    
    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_merge_dicts(result[key], value)
        else:
            result[key] = value
            
    return result


def clamp(value: Union[int, float], min_val: Union[int, float], 
         max_val: Union[int, float]) -> Union[int, float]:
    """
    Clamp value to range.
    
    Args:
        value: Value to clamp
        min_val: Minimum value
        max_val: Maximum value
        
    Returns:
        Clamped value
    """
    return max(min_val, min(max_val, value))


def format_bytes(bytes_value: int) -> str:
    """
    Format bytes to human-readable string.
    
    Args:
        bytes_value: Number of bytes
        
    Returns:
        Formatted string (e.g., "1.5 MB")
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_value < 1024.0:
            return f"{bytes_value:.1f} {unit}"
        bytes_value /= 1024.0
    return f"{bytes_value:.1f} PB"


def truncate_string(s: str, max_length: int, suffix: str = "...") -> str:
    """
    Truncate string to maximum length.
    
    Args:
        s: String to truncate
        max_length: Maximum length
        suffix: Suffix to append if truncated
        
    Returns:
        Truncated string
    """
    if len(s) <= max_length:
        return s
    return s[:max_length - len(suffix)] + suffix


def ensure_list(value: Union[Any, List[Any]]) -> List[Any]:
    """
    Ensure value is a list.
    
    Args:
        value: Value to convert
        
    Returns:
        List containing value, or value if already a list
    """
    if isinstance(value, list):
        return value
    return [value]


def parse_key_value_pairs(text: str, separator: str = "=") -> Dict[str, str]:
    """
    Parse key=value pairs from text.
    
    Args:
        text: Text containing key=value pairs
        separator: Separator character
        
    Returns:
        Dictionary of key-value pairs
    """
    result = {}
    for line in text.strip().split('\n'):
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        if separator in line:
            key, value = line.split(separator, 1)
            result[key.strip()] = value.strip()
    return result


class StateTransition:
    """
    State transition descriptor for logging.
    """
    
    def __init__(self, subsystem: str, from_state: str, to_state: str,
                 reason: Optional[str] = None, data: Optional[Dict] = None):
        """
        Initialize state transition.
        
        Args:
            subsystem: Subsystem name
            from_state: Previous state
            to_state: New state
            reason: Transition reason
            data: Additional data
        """
        self.subsystem = subsystem
        self.from_state = from_state
        self.to_state = to_state
        self.reason = reason
        self.data = data or {}
        self.timestamp = timestamp()
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'subsystem': self.subsystem,
            'from_state': self.from_state,
            'to_state': self.to_state,
            'reason': self.reason,
            'data': self.data,
            'timestamp': self.timestamp
        }
        
    def __repr__(self) -> str:
        """String representation"""
        return f"StateTransition({self.subsystem}: {self.from_state} -> {self.to_state})"
