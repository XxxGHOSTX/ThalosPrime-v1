"""
© 2026 Tony Ray Macier III. All rights reserved.

Thalos Prime™ is a proprietary system.
"""

"""
Thalos Prime Exception Hierarchy

Complete exception hierarchy for deterministic error handling.
No catch-all exceptions allowed - all errors must be explicit and recoverable.
"""


class ThalosError(Exception):
    """Base exception for all Thalos Prime errors"""
    
    def __init__(self, message: str, details: dict = None):
        super().__init__(message)
        self.message = message
        self.details = details or {}
        
    def to_dict(self):
        """Convert exception to dictionary for serialization"""
        return {
            'type': self.__class__.__name__,
            'message': self.message,
            'details': self.details
        }


class CISError(ThalosError):
    """Errors related to CIS (Central Intelligence System)"""
    pass


class BootError(CISError):
    """System boot failure - cannot proceed"""
    pass


class ShutdownError(CISError):
    """System shutdown failure - state may be inconsistent"""
    pass


class SubsystemError(CISError):
    """Subsystem initialization or operation failure"""
    pass


class KeyNotFoundError(ThalosError):
    """Key does not exist in storage"""
    pass


class KeyExistsError(ThalosError):
    """Key already exists in storage"""
    pass


class ValidationError(ThalosError):
    """Data validation failure"""
    
    def __init__(self, message: str, field: str = None, value=None, details: dict = None):
        super().__init__(message, details)
        self.field = field
        self.value = value
        
    def to_dict(self):
        result = super().to_dict()
        result['field'] = self.field
        result['value'] = str(self.value) if self.value is not None else None
        return result


class StateError(ThalosError):
    """Invalid state transition or operation in current state"""
    
    def __init__(self, message: str, current_state: str = None, expected_state: str = None, details: dict = None):
        super().__init__(message, details)
        self.current_state = current_state
        self.expected_state = expected_state
        
    def to_dict(self):
        result = super().to_dict()
        result['current_state'] = self.current_state
        result['expected_state'] = self.expected_state
        return result


class ConfigurationError(ThalosError):
    """Configuration file or setting error"""
    pass


class MemoryError(ThalosError):
    """Memory subsystem errors"""
    pass


class CodeGenError(ThalosError):
    """Code generation errors"""
    pass


class TemplateError(CodeGenError):
    """Template not found or invalid"""
    pass


class InterfaceError(ThalosError):
    """CLI or API interface errors"""
    pass


class LifecycleError(ThalosError):
    """Lifecycle method execution error"""
    
    def __init__(self, message: str, phase: str = None, subsystem: str = None, details: dict = None):
        super().__init__(message, details)
        self.phase = phase
        self.subsystem = subsystem
        
    def to_dict(self):
        result = super().to_dict()
        result['phase'] = self.phase
        result['subsystem'] = self.subsystem
        return result


class ReconciliationError(ThalosError):
    """State reconciliation failure - system cannot restore consistency"""
    pass


class CheckpointError(ThalosError):
    """Checkpoint save/restore failure"""
    pass


class DeterminismError(ThalosError):
    """Non-deterministic behavior detected"""
    pass


class ResourceError(ThalosError):
    """Resource allocation or access error"""
    pass


class TimeoutError(ThalosError):
    """Operation timeout"""
    pass


class DependencyError(ThalosError):
    """Missing or incompatible dependency"""
    pass


# Security exceptions
class SecurityError(ThalosError):
    """Security-related errors"""
    pass


class AuthenticationError(SecurityError):
    """Authentication failure"""
    pass


class AuthorizationError(SecurityError):
    """Authorization failure"""
    pass


class InputValidationError(SecurityError):
    """Input validation failure for security"""
    pass
