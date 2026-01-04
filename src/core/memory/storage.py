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
Memory Module - Data Storage and Management

Deterministic storage interface:
- In-memory dict-based storage
- Explicit CRUD semantics
- No side effects, no magic
"""

from typing import Any, Dict, Optional


class MemoryModule:
    """
    Memory Module for data storage and management
    
    Provides deterministic key-value storage:
    - In-memory dict-based implementation
    - Explicit CRUD operations
    - No automatic timestamps or side effects
    """
    
    def __init__(self):
        """Initialize the Memory Module"""
        self.storage: Dict[str, Any] = {}
        
    def create(self, key: str, value: Any) -> bool:
        """
        Create a new entry in storage (explicit CRUD - Create)
        
        Args:
            key: Unique identifier for the data
            value: Data to store
            
        Returns:
            bool: True if creation successful, False if key already exists
        """
        if key in self.storage:
            return False
        self.storage[key] = value
        return True
        
    def read(self, key: str) -> Optional[Any]:
        """
        Read data from storage (explicit CRUD - Read)
        
        Args:
            key: Unique identifier for the data
            
        Returns:
            Stored data if found, None otherwise
        """
        return self.storage.get(key)
        
    def update(self, key: str, value: Any) -> bool:
        """
        Update existing data in storage (explicit CRUD - Update)
        
        Args:
            key: Unique identifier for the data
            value: New data value
            
        Returns:
            bool: True if update successful, False if key doesn't exist
        """
        if key not in self.storage:
            return False
        self.storage[key] = value
        return True
        
    def delete(self, key: str) -> bool:
        """
        Delete data from storage (explicit CRUD - Delete)
        
        Args:
            key: Unique identifier for the data
            
        Returns:
            bool: True if deletion successful, False if key doesn't exist
        """
        if key not in self.storage:
            return False
        del self.storage[key]
        return True
        
    def exists(self, key: str) -> bool:
        """
        Check if a key exists in storage
        
        Args:
            key: Unique identifier for the data
            
        Returns:
            bool: True if key exists, False otherwise
        """
        return key in self.storage
        
    def list_keys(self) -> list:
        """
        List all stored keys
        
        Returns:
            List of all keys in storage
        """
        return list(self.storage.keys())
        
    def clear(self) -> None:
        """Clear all data from storage"""
        self.storage.clear()
        
    def count(self) -> int:
        """
        Get count of stored items
        
        Returns:
            Number of items in storage
        """
        return len(self.storage)
