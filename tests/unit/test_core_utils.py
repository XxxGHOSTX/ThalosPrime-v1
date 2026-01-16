"""
© 2026 Tony Ray Macier III. All rights reserved.

Thalos Prime™ is a proprietary system.
"""

"""
Tests for Core Utility Modules
"""

import pytest
from pathlib import Path
from core.config import Config
from core.logging import get_logger, ThalosLogger
from core.exceptions import *
from core.utils import *


class TestConfig:
    """Test configuration management"""
    
    def test_config_creation(self):
        """Test config instance creation"""
        config = Config()
        assert config is not None
    
    def test_config_get_with_default(self):
        """Test getting value with default"""
        config = Config()
        value = config.get("nonexistent", "key", default="default_value")
        assert value == "default_value"
    
    def test_config_type_conversion(self):
        """Test type conversion"""
        config = Config()
        # These will use defaults since no file loaded
        assert config.get("test", "bool", default=True, value_type=bool) == True
        assert config.get("test", "int", default=42, value_type=int) == 42


class TestLogging:
    """Test logging system"""
    
    def test_logger_singleton(self):
        """Test logger is singleton"""
        logger1 = get_logger()
        logger2 = get_logger()
        assert logger1 is logger2
    
    def test_logger_methods(self):
        """Test logger methods exist"""
        logger = get_logger()
        assert hasattr(logger, 'debug')
        assert hasattr(logger, 'info')
        assert hasattr(logger, 'warning')
        assert hasattr(logger, 'error')
        assert hasattr(logger, 'lifecycle')
        assert hasattr(logger, 'state_transition')


class TestExceptions:
    """Test exception hierarchy"""
    
    def test_base_exception(self):
        """Test ThalosError base exception"""
        error = ThalosError("Test error", details={'key': 'value'})
        assert str(error) == "Test error"
        assert error.details['key'] == 'value'
    
    def test_exception_to_dict(self):
        """Test exception serialization"""
        error = ValidationError("Invalid value", field="username", value="x")
        error_dict = error.to_dict()
        assert error_dict['type'] == 'ValidationError'
        assert error_dict['message'] == 'Invalid value'
        assert error_dict['field'] == 'username'
    
    def test_exception_hierarchy(self):
        """Test exception inheritance"""
        assert issubclass(CISError, ThalosError)
        assert issubclass(ValidationError, ThalosError)
        assert issubclass(StateError, ThalosError)


class TestResult:
    """Test Result type"""
    
    def test_result_ok(self):
        """Test successful result"""
        result = Result.ok(42)
        assert result.is_ok()
        assert not result.is_err()
        assert result.unwrap() == 42
    
    def test_result_fail(self):
        """Test failed result"""
        result = Result.fail("Error message")
        assert result.is_err()
        assert not result.is_ok()
        assert result.error() == "Error message"
    
    def test_result_unwrap_or(self):
        """Test unwrap with default"""
        result = Result.fail("Error")
        assert result.unwrap_or(100) == 100


class TestValidator:
    """Test validation functions"""
    
    def test_not_empty(self):
        """Test not_empty validator"""
        result = Validator.not_empty("hello", field="test")
        assert result == "hello"
        
        with pytest.raises(ValidationError):
            Validator.not_empty("", field="test")
    
    def test_min_length(self):
        """Test min_length validator"""
        result = Validator.min_length("hello", 3, field="test")
        assert result == "hello"
        
        with pytest.raises(ValidationError):
            Validator.min_length("hi", 5, field="test")
    
    def test_in_range(self):
        """Test in_range validator"""
        result = Validator.in_range(5, 0, 10, field="test")
        assert result == 5
        
        with pytest.raises(ValidationError):
            Validator.in_range(15, 0, 10, field="test")
    
    def test_one_of(self):
        """Test one_of validator"""
        result = Validator.one_of("red", ["red", "green", "blue"], field="color")
        assert result == "red"
        
        with pytest.raises(ValidationError):
            Validator.one_of("yellow", ["red", "green", "blue"], field="color")


class TestUtilityFunctions:
    """Test utility helper functions"""
    
    def test_generate_id(self):
        """Test ID generation"""
        id1 = generate_id(prefix="test")
        id2 = generate_id(prefix="test")
        assert id1.startswith("test_")
        assert id1 != id2  # Should be unique
    
    def test_sanitize_filename(self):
        """Test filename sanitization"""
        result = sanitize_filename("my file@#$.txt")
        assert "@" not in result
        assert "#" not in result
    
    def test_truncate_string(self):
        """Test string truncation"""
        result = truncate_string("Hello World", max_length=8)
        assert len(result) <= 8
        assert result.endswith("...")
    
    def test_deep_merge(self):
        """Test dictionary deep merge"""
        base = {"a": 1, "b": {"c": 2}}
        override = {"b": {"d": 3}, "e": 4}
        result = deep_merge(base, override)
        assert result["a"] == 1
        assert result["b"]["c"] == 2
        assert result["b"]["d"] == 3
        assert result["e"] == 4
    
    def test_ensure_list(self):
        """Test ensure_list"""
        assert ensure_list(None) == []
        assert ensure_list(5) == [5]
        assert ensure_list([1, 2]) == [1, 2]
    
    def test_safe_divide(self):
        """Test safe division"""
        assert safe_divide(10, 2) == 5.0
        assert safe_divide(10, 0, default=0) == 0
    
    def test_clamp(self):
        """Test value clamping"""
        assert clamp(5, 0, 10) == 5
        assert clamp(-5, 0, 10) == 0
        assert clamp(15, 0, 10) == 10
