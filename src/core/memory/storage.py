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
- Optional file-based persistence
"""

from typing import Any, Dict, Optional
import json
import os


class MemoryModule:
    """
    Memory Module for data storage and management
    
    Provides deterministic key-value storage:
    - In-memory dict-based implementation
    - Explicit CRUD operations
    - No automatic timestamps or side effects
    - Optional file-based persistence for data durability
    """
    
    def __init__(self, persistence_path: Optional[str] = None):
        """
        Initialize the Memory Module
        
        Args:
            persistence_path: Optional path to JSON file for persistent storage.
                            If provided, data will be loaded from and saved to this file.
        """
        self.storage: Dict[str, Any] = {}
        self.persistence_path = persistence_path
        self._initialized = False
        self._validated = False
        self._state = 'created'
        
        # Load existing data from file if persistence is enabled
        if self.persistence_path:
            self.load_from_disk()
            
    def initialize(self) -> bool:
        """
        Initialize memory module - Lifecycle hook
        
        Allocates resources and verifies preconditions.
        
        Returns:
            bool: True if initialization successful
        """
        if self._initialized:
            return True
            
        try:
            # Ensure storage is initialized
            if self.storage is None:
                self.storage = {}
                
            self._initialized = True
            self._state = 'initialized'
            return True
        except Exception:
            self._state = 'error'
            return False
            
    def validate(self) -> bool:
        """
        Validate memory module - Lifecycle hook
        
        Blocks startup if configuration invalid.
        
        Returns:
            bool: True if validation successful
        """
        if not self._initialized:
            return False
            
        if self._validated:
            return True
            
        try:
            # Validate persistence path if configured
            if self.persistence_path:
                import os
                directory = os.path.dirname(self.persistence_path)
                if directory and not os.path.exists(directory):
                    os.makedirs(directory, exist_ok=True)
                    
            # Validate storage is a dict
            if not isinstance(self.storage, dict):
                return False
                
            self._validated = True
            self._state = 'validated'
            return True
        except Exception:
            self._state = 'error'
            return False
            
    def operate(self) -> Dict[str, Any]:
        """
        Perform memory operations - Lifecycle hook
        
        Returns current operational status.
        
        Returns:
            dict: Operational status
        """
        return {
            'state': self._state,
            'initialized': self._initialized,
            'validated': self._validated,
            'item_count': len(self.storage),
            'persistence_enabled': self.persistence_path is not None
        }
        
    def reconcile(self) -> bool:
        """
        Reconcile internal state - Lifecycle hook
        
        Corrects any internal inconsistencies.
        
        Returns:
            bool: True if reconciliation successful
        """
        # Ensure storage is a dict
        if not isinstance(self.storage, dict):
            self.storage = {}
            
        # Remove any None keys
        keys_to_remove = [k for k in self.storage.keys() if k is None]
        for k in keys_to_remove:
            del self.storage[k]
            
        return True
        
    def checkpoint(self) -> Dict[str, Any]:
        """
        Checkpoint memory state - Lifecycle hook
        
        Persists full deterministic state for recovery.
        
        Returns:
            dict: Serialized state
        """
        state = {
            'version': '1.0',
            'state': self._state,
            'initialized': self._initialized,
            'validated': self._validated,
            'item_count': len(self.storage),
            'persistence_path': self.persistence_path,
            'data': self.storage.copy()
        }
        
        # Also save to disk if persistence enabled
        if self.persistence_path:
            self.save_to_disk()
            
        return state
        
    def terminate(self) -> bool:
        """
        Terminate memory module - Lifecycle hook
        
        Leaves system restartable and coherent.
        
        Returns:
            bool: True if termination successful
        """
        # Save to disk before terminating
        if self.persistence_path:
            self.save_to_disk()
            
        # Clear state but don't destroy storage (allows restart)
        self._state = 'terminated'
        return True
        
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
        
    def save_to_disk(self) -> bool:
        """
        Save current storage to disk (if persistence is enabled)
        
        Returns:
            bool: True if save successful or persistence disabled, False on error
        """
        if not self.persistence_path:
            return True  # No persistence configured, nothing to do
            
        try:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(self.persistence_path), exist_ok=True)
            
            # Write storage to JSON file
            with open(self.persistence_path, 'w') as f:
                json.dump(self.storage, f, indent=2)
            return True
        except Exception as e:
            # In production, you'd log this error
            print(f"Error saving to disk: {e}")
            return False
            
    def load_from_disk(self) -> bool:
        """
        Load storage from disk (if persistence is enabled and file exists)
        
        Returns:
            bool: True if load successful or file doesn't exist, False on error
        """
        if not self.persistence_path:
            return True  # No persistence configured, nothing to do
            
        if not os.path.exists(self.persistence_path):
            return True  # File doesn't exist yet, start with empty storage
            
        try:
            with open(self.persistence_path, 'r') as f:
                self.storage = json.load(f)
            return True
        except Exception as e:
            # In production, you'd log this error
            print(f"Error loading from disk: {e}")
            return False
