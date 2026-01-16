#!/usr/bin/env python3
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
Thalos Prime v1.0 - Utility Functions

Common utility functions used across the Thalos Prime system.
All utilities maintain deterministic behavior.
"""

import re
from typing import Any, Dict, List, Optional, TypeVar, Callable

T = TypeVar('T')


def validate_key(key: str) -> bool:
    """
    Validate a storage key format
    
    Keys must:
    - Be non-empty strings
    - Contain only alphanumeric characters, underscores, and hyphens
    - Not start with a number
    
    Args:
        key: Key string to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not key or not isinstance(key, str):
        return False
    
    pattern = r'^[a-zA-Z_][a-zA-Z0-9_-]*$'
    return bool(re.match(pattern, key))


def validate_class_name(name: str) -> bool:
    """
    Validate a Python class name format
    
    Class names must:
    - Start with an uppercase letter
    - Contain only alphanumeric characters and underscores
    
    Args:
        name: Class name to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not name or not isinstance(name, str):
        return False
    
    pattern = r'^[A-Z][a-zA-Z0-9_]*$'
    return bool(re.match(pattern, name))


def validate_function_name(name: str) -> bool:
    """
    Validate a Python function name format
    
    Function names must:
    - Start with a lowercase letter or underscore
    - Contain only alphanumeric characters and underscores
    
    Args:
        name: Function name to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not name or not isinstance(name, str):
        return False
    
    pattern = r'^[a-z_][a-zA-Z0-9_]*$'
    return bool(re.match(pattern, name))


def validate_identifier(name: str) -> bool:
    """
    Validate a Python identifier (variable/parameter name)
    
    Args:
        name: Identifier to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not name or not isinstance(name, str):
        return False
    
    pattern = r'^[a-zA-Z_][a-zA-Z0-9_]*$'
    return bool(re.match(pattern, name))


def safe_get(dictionary: Dict, *keys: str, default: Any = None) -> Any:
    """
    Safely get a nested dictionary value
    
    Args:
        dictionary: Source dictionary
        *keys: Keys to traverse
        default: Default value if not found
        
    Returns:
        Value at the nested path or default
    """
    result = dictionary
    for key in keys:
        if isinstance(result, dict) and key in result:
            result = result[key]
        else:
            return default
    return result


def flatten_dict(d: Dict, parent_key: str = '', sep: str = '.') -> Dict[str, Any]:
    """
    Flatten a nested dictionary
    
    Args:
        d: Dictionary to flatten
        parent_key: Parent key prefix
        sep: Separator for nested keys
        
    Returns:
        Flattened dictionary
    """
    items: List[tuple] = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def truncate_string(s: str, max_length: int = 100, suffix: str = '...') -> str:
    """
    Truncate a string to maximum length
    
    Args:
        s: String to truncate
        max_length: Maximum length (including suffix)
        suffix: Suffix to append when truncated
        
    Returns:
        Truncated string
    """
    if len(s) <= max_length:
        return s
    return s[:max_length - len(suffix)] + suffix


def format_dict_for_display(d: Dict, indent: int = 0) -> str:
    """
    Format a dictionary for human-readable display
    
    Args:
        d: Dictionary to format
        indent: Indentation level
        
    Returns:
        Formatted string representation
    """
    lines = []
    prefix = '  ' * indent
    
    for key, value in sorted(d.items()):
        if isinstance(value, dict):
            lines.append(f"{prefix}{key}:")
            lines.append(format_dict_for_display(value, indent + 1))
        else:
            lines.append(f"{prefix}{key}: {value}")
    
    return '\n'.join(lines)


def ensure_list(value: Any) -> List:
    """
    Ensure a value is a list
    
    Args:
        value: Any value
        
    Returns:
        Value wrapped in list if not already a list
    """
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def first_or_default(items: List[T], predicate: Optional[Callable[[T], bool]] = None, default: Optional[T] = None) -> Optional[T]:
    """
    Get first item matching predicate or default
    
    Args:
        items: List of items
        predicate: Optional filter function
        default: Default value if not found
        
    Returns:
        First matching item or default
    """
    if predicate is None:
        return items[0] if items else default
    
    for item in items:
        if predicate(item):
            return item
    return default


def deduplicate(items: List[T]) -> List[T]:
    """
    Remove duplicates while preserving order
    
    Args:
        items: List with potential duplicates
        
    Returns:
        List with duplicates removed
    """
    seen = set()
    result = []
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result


def chunk_list(items: List[T], chunk_size: int) -> List[List[T]]:
    """
    Split a list into chunks of specified size
    
    Args:
        items: List to chunk
        chunk_size: Size of each chunk
        
    Returns:
        List of chunks
    """
    return [items[i:i + chunk_size] for i in range(0, len(items), chunk_size)]


class Result:
    """
    Result wrapper for operations that can succeed or fail
    
    Provides a consistent pattern for returning operation results
    with success/failure status and optional error messages.
    """
    
    def __init__(self, success: bool, value: Any = None, error: Optional[str] = None):
        """
        Create a Result
        
        Args:
            success: Whether the operation succeeded
            value: Result value (on success)
            error: Error message (on failure)
        """
        self.success = success
        self.value = value
        self.error = error
    
    @classmethod
    def ok(cls, value: Any = None) -> 'Result':
        """Create a successful result"""
        return cls(True, value=value)
    
    @classmethod
    def fail(cls, error: str) -> 'Result':
        """Create a failed result"""
        return cls(False, error=error)
    
    def __bool__(self) -> bool:
        """Allow truthiness check"""
        return self.success
    
    def __repr__(self) -> str:
        if self.success:
            return f"Result.ok({self.value!r})"
        return f"Result.fail({self.error!r})"
