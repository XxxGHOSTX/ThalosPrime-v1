"""
© 2026 Tony Ray Macier III. All rights reserved.

Thalos Prime™ is a proprietary system.
"""

"""
Unit tests for core utility modules.

Tests config, logging, exceptions, and utils modules.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

import pytest
from core.config import ConfigManager
from core.logging import ThalosLogger
from core.exceptions import (
    ThalosError, CISError, MemoryError, KeyNotFoundError, 
    ValidationError, StateError
)
from core.utils import (
    Result, Validator, ValidationResult, 
    serialize_state, deserialize_state, version_state,
    clamp, format_bytes, truncate_string
)


class TestConfigManager:
    """Test configuration management"""
    
    def test_config_creation(self):
        """Test creating config manager"""
        config = ConfigManager()
        assert config is not None
        
    def test_get_default_values(self):
        """Test getting default configuration values"""
        config = ConfigManager()
        
        version = config.get('system', 'version', default='0.0.0')
        assert version == '1.0'
        
        debug = config.get('system', 'debug', default=False, type_cast=bool)
        assert debug is False
        
    def test_get_section(self):
        """Test getting entire configuration section"""
        config = ConfigManager()
        
        system_config = config.get_section('system')
        assert 'version' in system_config
        assert 'debug' in system_config
        assert 'log_level' in system_config
        
    def test_set_and_get(self):
        """Test setting and getting configuration values"""
        config = ConfigManager()
        
        config.set('test', 'key', 'value')
        value = config.get('test', 'key')
        assert value == 'value'
        
    def test_type_casting(self):
        """Test configuration value type casting"""
        config = ConfigManager()
        
        # Boolean casting
        config.set('test', 'bool_true', 'true')
        assert config.get('test', 'bool_true', type_cast=bool) is True
        
        config.set('test', 'bool_false', 'false')
        assert config.get('test', 'bool_false', type_cast=bool) is False
        
        # Integer casting
        config.set('test', 'int_val', '42')
        assert config.get('test', 'int_val', type_cast=int) == 42
        
        # Float casting
        config.set('test', 'float_val', '3.14')
        assert config.get('test', 'float_val', type_cast=float) == 3.14
        
    def test_validation(self):
        """Test configuration validation"""
        config = ConfigManager()
        
        # Should validate successfully with defaults
        assert config.validate() is True


class TestThalosLogger:
    """Test logging system"""
    
    def test_logger_creation(self):
        """Test creating logger"""
        logger = ThalosLogger()
        assert logger is not None
        
    def test_logger_singleton(self):
        """Test logger singleton pattern"""
        logger1 = ThalosLogger()
        logger2 = ThalosLogger()
        assert logger1 is logger2
        
    def test_logging_methods(self):
        """Test basic logging methods"""
        logger = ThalosLogger()
        
        # Should not raise exceptions
        logger.debug("Debug message")
        logger.info("Info message")
        logger.warning("Warning message")
        logger.error("Error message")
        logger.critical("Critical message")
        
    def test_lifecycle_logging(self):
        """Test lifecycle event logging"""
        logger = ThalosLogger()
        
        # Should not raise exceptions
        logger.log_lifecycle('CIS', 'initialize', success=True)
        logger.log_lifecycle('Memory', 'validate', success=False)
        
    def test_state_transition_logging(self):
        """Test state transition logging"""
        logger = ThalosLogger()
        
        # Should not raise exceptions
        logger.log_state_transition('CIS', 'created', 'initialized', 'Preconditions met')


class TestExceptions:
    """Test exception hierarchy"""
    
    def test_base_exception(self):
        """Test base ThalosError"""
        error = ThalosError("Test error")
        assert str(error) == "Test error"
        
        error_with_state = ThalosError("Test error", state={'key': 'value'})
        assert 'State:' in str(error_with_state)
        
    def test_exception_hierarchy(self):
        """Test exception inheritance"""
        # CISError is a ThalosError
        assert issubclass(CISError, ThalosError)
        
        # MemoryError is a ThalosError
        assert issubclass(MemoryError, ThalosError)
        
        # KeyNotFoundError is a MemoryError
        assert issubclass(KeyNotFoundError, MemoryError)
        
    def test_raising_exceptions(self):
        """Test raising and catching exceptions"""
        with pytest.raises(ThalosError):
            raise ThalosError("Test")
            
        with pytest.raises(CISError):
            raise CISError("CIS error")
            
        with pytest.raises(KeyNotFoundError):
            raise KeyNotFoundError("Key not found")


class TestResult:
    """Test Result type for error handling"""
    
    def test_ok_result(self):
        """Test successful result"""
        result = Result.ok(42)
        
        assert result.success is True
        assert result.failure is False
        assert result.value == 42
        assert result.error is None
        
    def test_err_result(self):
        """Test failed result"""
        result = Result.err("Something went wrong")
        
        assert result.success is False
        assert result.failure is True
        assert result.error == "Something went wrong"
        
    def test_unwrap_or(self):
        """Test unwrapping with default"""
        ok_result = Result.ok(42)
        assert ok_result.unwrap_or(0) == 42
        
        err_result = Result.err("Error")
        assert err_result.unwrap_or(0) == 0
        
    def test_map(self):
        """Test mapping over result"""
        result = Result.ok(5)
        mapped = result.map(lambda x: x * 2)
        
        assert mapped.success is True
        assert mapped.value == 10


class TestValidator:
    """Test validation utilities"""
    
    def test_is_not_empty(self):
        """Test empty string validation"""
        result = Validator.is_not_empty("hello")
        assert result.valid is True
        
        result = Validator.is_not_empty("")
        assert result.valid is False
        
        result = Validator.is_not_empty("   ")
        assert result.valid is False
        
    def test_is_valid_identifier(self):
        """Test Python identifier validation"""
        result = Validator.is_valid_identifier("my_var")
        assert result.valid is True
        
        result = Validator.is_valid_identifier("123abc")
        assert result.valid is False
        
        result = Validator.is_valid_identifier("class")
        assert result.valid is False
        
    def test_is_in_range(self):
        """Test range validation"""
        result = Validator.is_in_range(5, 0, 10)
        assert result.valid is True
        
        result = Validator.is_in_range(15, 0, 10)
        assert result.valid is False
        
    def test_is_positive(self):
        """Test positive number validation"""
        result = Validator.is_positive(42)
        assert result.valid is True
        
        result = Validator.is_positive(-5)
        assert result.valid is False
        
        result = Validator.is_positive(0)
        assert result.valid is False
        
    def test_has_keys(self):
        """Test dictionary key validation"""
        data = {'name': 'Alice', 'age': 30}
        
        result = Validator.has_keys(data, ['name', 'age'])
        assert result.valid is True
        
        result = Validator.has_keys(data, ['name', 'email'])
        assert result.valid is False


class TestValidationResult:
    """Test ValidationResult type"""
    
    def test_valid_result(self):
        """Test valid validation result"""
        result = ValidationResult(valid=True)
        assert result.valid is True
        assert len(result.errors) == 0
        assert bool(result) is True
        
    def test_invalid_result(self):
        """Test invalid validation result"""
        result = ValidationResult(valid=False, errors=["Error 1", "Error 2"])
        assert result.valid is False
        assert len(result.errors) == 2
        assert bool(result) is False
        
    def test_add_error(self):
        """Test adding errors"""
        result = ValidationResult()
        assert result.valid is True
        
        result.add_error("Test error")
        assert result.valid is False
        assert len(result.errors) == 1
        
    def test_merge_results(self):
        """Test merging validation results"""
        result1 = ValidationResult(valid=True)
        result2 = ValidationResult(valid=False, errors=["Error"])
        
        merged = result1.merge(result2)
        assert merged.valid is False
        assert len(merged.errors) == 1


class TestStateUtils:
    """Test state management utilities"""
    
    def test_serialize_deserialize(self):
        """Test state serialization and deserialization"""
        state = {'key': 'value', 'count': 42, 'flag': True}
        
        # Serialize
        json_str = serialize_state(state)
        assert isinstance(json_str, str)
        
        # Deserialize
        restored = deserialize_state(json_str)
        assert restored == state
        
    def test_version_state(self):
        """Test state versioning"""
        state = {'data': 'value'}
        
        versioned = version_state(state, version='1.0')
        
        assert '_version' in versioned
        assert '_timestamp' in versioned
        assert 'data' in versioned
        assert versioned['_version'] == '1.0'


class TestMiscUtils:
    """Test miscellaneous utility functions"""
    
    def test_clamp(self):
        """Test value clamping"""
        assert clamp(5, 0, 10) == 5
        assert clamp(-5, 0, 10) == 0
        assert clamp(15, 0, 10) == 10
        
    def test_format_bytes(self):
        """Test byte formatting"""
        assert "B" in format_bytes(100)
        assert "KB" in format_bytes(2048)
        assert "MB" in format_bytes(2 * 1024 * 1024)
        
    def test_truncate_string(self):
        """Test string truncation"""
        text = "This is a long text"
        truncated = truncate_string(text, 10)
        
        assert len(truncated) <= 10
        assert "..." in truncated
        
        # Short text should not be truncated
        short = "Short"
        assert truncate_string(short, 10) == "Short"
