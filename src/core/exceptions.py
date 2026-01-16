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
Thalos Prime - Exception Hierarchy

Complete exception hierarchy for deterministic error handling.
No catch-all exceptions permitted - all errors must be explicit and recoverable.
"""


class ThalosError(Exception):
    """
    Base exception for all Thalos Prime errors.
    
    All exceptions in Thalos Prime inherit from this base class,
    enabling consistent error handling and state capture.
    """
    
    def __init__(self, message: str, state: dict = None):
        """
        Initialize exception with message and optional state.
        
        Args:
            message: Human-readable error description
            state: Optional system state at time of error for debugging
        """
        super().__init__(message)
        self.message = message
        self.state = state or {}
        
    def __str__(self) -> str:
        """String representation of the exception"""
        if self.state:
            return f"{self.message} | State: {self.state}"
        return self.message


class CISError(ThalosError):
    """
    Central Intelligence System errors.
    
    Raised when CIS operations fail - boot, shutdown, or orchestration issues.
    """
    pass


class SubsystemError(ThalosError):
    """
    General subsystem errors.
    
    Base class for errors in specific subsystems (memory, codegen, etc.)
    """
    pass


class MemoryError(SubsystemError):
    """
    Memory subsystem errors.
    
    Raised when memory operations fail - storage, retrieval, or persistence issues.
    """
    pass


class KeyNotFoundError(MemoryError):
    """
    Key not found in memory storage.
    
    Raised when attempting to retrieve or delete a non-existent key.
    """
    pass


class KeyExistsError(MemoryError):
    """
    Key already exists in memory storage.
    
    Raised when attempting to create a key that already exists.
    """
    pass


class ValidationError(ThalosError):
    """
    Validation errors.
    
    Raised when input validation fails or system state is invalid.
    """
    pass


class StateError(ThalosError):
    """
    System state errors.
    
    Raised when system is in an invalid state for requested operation.
    """
    pass


class ConfigurationError(ThalosError):
    """
    Configuration errors.
    
    Raised when configuration is invalid or missing required values.
    """
    pass


class InitializationError(ThalosError):
    """
    Initialization errors.
    
    Raised when subsystem initialization fails.
    """
    pass


class OperationError(ThalosError):
    """
    Operation errors.
    
    Raised when a subsystem operation fails during execution.
    """
    pass


class CodeGenError(SubsystemError):
    """
    Code generation errors.
    
    Raised when code generation fails or produces invalid output.
    """
    pass


class InterfaceError(ThalosError):
    """
    Interface layer errors.
    
    Raised when CLI, API, or web interface operations fail.
    """
    pass


class LifecycleError(ThalosError):
    """
    Lifecycle errors.
    
    Raised when lifecycle transitions fail (initialize, validate, operate, etc.)
    """
    pass


class ReconciliationError(ThalosError):
    """
    State reconciliation errors.
    
    Raised when system cannot reconcile internal inconsistencies.
    """
    pass


class CheckpointError(ThalosError):
    """
    Checkpoint errors.
    
    Raised when state persistence (checkpoint) operations fail.
    """
    pass
