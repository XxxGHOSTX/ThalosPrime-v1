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
Thalos Prime - Configuration Management

INI-based configuration with validation and type coercion.
Supports environment variable overrides and defaults.
"""

import os
import configparser
from typing import Any, Dict, Optional, Union
from pathlib import Path

from .exceptions import ConfigurationError, ValidationError


class ConfigManager:
    """
    Configuration manager for Thalos Prime.
    
    Loads configuration from INI files with support for:
    - Environment variable overrides (THALOS_SECTION_KEY)
    - Type coercion (str, int, float, bool)
    - Default values
    - Validation
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize configuration manager.
        
        Args:
            config_path: Path to config file. If None, uses default locations:
                         1. ./config/thalos.ini
                         2. ./thalos.ini
                         3. Built-in defaults only
        """
        self.config = configparser.ConfigParser()
        self.config_path: Optional[Path] = None
        self._defaults = self._get_builtin_defaults()
        
        # Try to load from file
        if config_path:
            self._load_from_file(config_path)
        else:
            self._load_default_locations()
            
    def _get_builtin_defaults(self) -> Dict[str, Dict[str, Any]]:
        """
        Get built-in default configuration.
        
        Returns:
            Dictionary of default values
        """
        return {
            'system': {
                'version': '1.0',
                'debug': False,
                'log_level': 'INFO',
            },
            'memory': {
                'type': 'dict',
                'max_size': 10000,
                'persistence': False,
                'persistence_path': './data/memory.json',
            },
            'codegen': {
                'templates_dir': './templates',
                'output_dir': './output',
                'validate_syntax': True,
            },
            'cli': {
                'prompt': 'thalos> ',
                'history_size': 1000,
            },
            'api': {
                'host': '0.0.0.0',
                'port': 5000,
                'debug': False,
            },
            'logging': {
                'level': 'INFO',
                'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                'file': './logs/thalos.log',
                'console': True,
            }
        }
        
    def _load_from_file(self, config_path: str) -> None:
        """
        Load configuration from file.
        
        Args:
            config_path: Path to config file
            
        Raises:
            ConfigurationError: If file cannot be read
        """
        path = Path(config_path)
        if not path.exists():
            raise ConfigurationError(f"Configuration file not found: {config_path}")
            
        try:
            self.config.read(config_path)
            self.config_path = path
        except Exception as e:
            raise ConfigurationError(f"Failed to read configuration file: {e}")
            
    def _load_default_locations(self) -> None:
        """Load configuration from default locations"""
        default_paths = [
            Path('./config/thalos.ini'),
            Path('./thalos.ini'),
        ]
        
        for path in default_paths:
            if path.exists():
                try:
                    self.config.read(str(path))
                    self.config_path = path
                    return
                except Exception:
                    continue  # Try next location
                    
        # No config file found - use defaults only
        
    def get(self, section: str, key: str, default: Any = None, 
            type_cast: type = str) -> Any:
        """
        Get configuration value with environment override support.
        
        Precedence order:
        1. Environment variable (THALOS_SECTION_KEY)
        2. Config file value
        3. Built-in default
        4. Provided default parameter
        
        Args:
            section: Configuration section
            key: Configuration key
            default: Default value if not found
            type_cast: Type to cast value to (str, int, float, bool)
            
        Returns:
            Configuration value with appropriate type
        """
        # Check environment variable first
        env_key = f"THALOS_{section.upper()}_{key.upper()}"
        env_value = os.environ.get(env_key)
        if env_value is not None:
            return self._cast_value(env_value, type_cast)
            
        # Check config file
        if self.config.has_option(section, key):
            value = self.config.get(section, key)
            return self._cast_value(value, type_cast)
            
        # Check built-in defaults
        if section in self._defaults and key in self._defaults[section]:
            return self._defaults[section][key]
            
        # Use provided default
        return default
        
    def get_section(self, section: str) -> Dict[str, Any]:
        """
        Get all values in a section.
        
        Args:
            section: Configuration section name
            
        Returns:
            Dictionary of key-value pairs
        """
        result = {}
        
        # Start with defaults
        if section in self._defaults:
            result.update(self._defaults[section])
            
        # Override with config file values
        if self.config.has_section(section):
            for key in self.config.options(section):
                result[key] = self.config.get(section, key)
                
        # Apply environment overrides
        env_prefix = f"THALOS_{section.upper()}_"
        for env_key, env_value in os.environ.items():
            if env_key.startswith(env_prefix):
                key = env_key[len(env_prefix):].lower()
                result[key] = env_value
                
        return result
        
    def set(self, section: str, key: str, value: Any) -> None:
        """
        Set configuration value.
        
        Args:
            section: Configuration section
            key: Configuration key
            value: Value to set
        """
        if not self.config.has_section(section):
            self.config.add_section(section)
            
        self.config.set(section, key, str(value))
        
    def save(self, config_path: Optional[str] = None) -> None:
        """
        Save configuration to file.
        
        Args:
            config_path: Path to save to. If None, uses loaded path.
            
        Raises:
            ConfigurationError: If no path specified and no file was loaded
        """
        path = config_path or self.config_path
        if path is None:
            raise ConfigurationError("No configuration file path specified")
            
        try:
            path = Path(path)
            path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(path, 'w') as f:
                self.config.write(f)
                
        except Exception as e:
            raise ConfigurationError(f"Failed to save configuration: {e}")
            
    def validate(self) -> bool:
        """
        Validate configuration.
        
        Ensures all required values are present and valid.
        
        Returns:
            True if valid
            
        Raises:
            ValidationError: If configuration is invalid
        """
        # Check required sections
        required_sections = ['system', 'memory', 'codegen']
        for section in required_sections:
            # Section can be in defaults or config file
            has_section = (section in self._defaults or 
                          self.config.has_section(section))
            if not has_section:
                raise ValidationError(f"Missing required section: {section}")
                
        # Validate specific values
        log_level = self.get('system', 'log_level', type_cast=str)
        valid_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        if log_level not in valid_levels:
            raise ValidationError(
                f"Invalid log_level: {log_level}. Must be one of {valid_levels}"
            )
            
        return True
        
    def _cast_value(self, value: str, type_cast: type) -> Any:
        """
        Cast string value to specified type.
        
        Args:
            value: String value to cast
            type_cast: Target type
            
        Returns:
            Casted value
            
        Raises:
            ValidationError: If cast fails
        """
        try:
            if type_cast == bool:
                # Handle boolean specially
                if isinstance(value, bool):
                    return value
                return value.lower() in ('true', '1', 'yes', 'on')
            elif type_cast == int:
                return int(value)
            elif type_cast == float:
                return float(value)
            else:
                return str(value)
        except (ValueError, AttributeError) as e:
            raise ValidationError(
                f"Failed to cast '{value}' to {type_cast.__name__}: {e}"
            )
            
    def __repr__(self) -> str:
        """String representation"""
        path = self.config_path or "defaults"
        sections = list(self._defaults.keys())
        if self.config.sections():
            sections.extend(self.config.sections())
        sections = sorted(set(sections))
        return f"ConfigManager(path={path}, sections={sections})"


# Global config instance
_config_instance: Optional[ConfigManager] = None


def get_config() -> ConfigManager:
    """
    Get global configuration instance.
    
    Returns:
        Global ConfigManager instance
    """
    global _config_instance
    if _config_instance is None:
        _config_instance = ConfigManager()
    return _config_instance


def initialize_config(config_path: Optional[str] = None) -> ConfigManager:
    """
    Initialize global configuration with specific path.
    
    Args:
        config_path: Path to configuration file
        
    Returns:
        Initialized ConfigManager instance
    """
    global _config_instance
    _config_instance = ConfigManager(config_path)
    return _config_instance
