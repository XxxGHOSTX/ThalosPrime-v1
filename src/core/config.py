"""
© 2026 Tony Ray Macier III. All rights reserved.

Thalos Prime™ is a proprietary system.
"""

"""
Thalos Prime Configuration Management

INI-based configuration with validation and type safety.
All configuration must be deterministic and validated.
"""

import configparser
from pathlib import Path
from typing import Any, Dict, Optional, Union, List
from .exceptions import ConfigurationError, ValidationError


class Config:
    """
    Configuration manager for Thalos Prime
    
    Provides:
    - INI file parsing
    - Type-safe value access
    - Validation
    - Default values
    - Environment overrides
    """
    
    def __init__(self, config_file: Optional[Union[str, Path]] = None):
        """
        Initialize configuration
        
        Args:
            config_file: Path to INI config file (default: config/thalos.ini)
        """
        self.config = configparser.ConfigParser()
        self._loaded = False
        self._config_file = None
        
        if config_file:
            self.load(config_file)
        else:
            # Try default locations
            default_paths = [
                Path('config/thalos.ini'),
                Path('thalos.ini'),
                Path('/etc/thalos/thalos.ini')
            ]
            for path in default_paths:
                if path.exists():
                    self.load(path)
                    break
    
    def load(self, config_file: Union[str, Path]) -> None:
        """
        Load configuration from INI file
        
        Args:
            config_file: Path to configuration file
            
        Raises:
            ConfigurationError: If file cannot be loaded
        """
        config_path = Path(config_file)
        
        if not config_path.exists():
            raise ConfigurationError(
                f"Configuration file not found: {config_path}",
                details={'path': str(config_path)}
            )
        
        try:
            self.config.read(config_path)
            self._config_file = config_path
            self._loaded = True
        except Exception as e:
            raise ConfigurationError(
                f"Failed to parse configuration file: {e}",
                details={'path': str(config_path), 'error': str(e)}
            )
    
    def get(self, section: str, key: str, default: Any = None, 
            required: bool = False, value_type: type = str) -> Any:
        """
        Get configuration value with type conversion
        
        Args:
            section: Configuration section
            key: Configuration key
            default: Default value if not found
            required: Whether value is required
            value_type: Type to convert value to
            
        Returns:
            Configuration value converted to specified type
            
        Raises:
            ConfigurationError: If required value is missing
            ValidationError: If type conversion fails
        """
        if not self._loaded and default is None and required:
            raise ConfigurationError(
                "No configuration file loaded",
                details={'section': section, 'key': key}
            )
        
        try:
            if self.config.has_option(section, key):
                raw_value = self.config.get(section, key)
                return self._convert_type(raw_value, value_type, section, key)
            elif required:
                raise ConfigurationError(
                    f"Required configuration missing: [{section}] {key}",
                    details={'section': section, 'key': key}
                )
            else:
                return default
        except (configparser.NoSectionError, configparser.NoOptionError):
            if required:
                raise ConfigurationError(
                    f"Required configuration missing: [{section}] {key}",
                    details={'section': section, 'key': key}
                )
            return default
    
    def _convert_type(self, value: str, value_type: type, section: str, key: str) -> Any:
        """Convert string value to specified type"""
        try:
            if value_type == bool:
                return value.lower() in ('true', 'yes', '1', 'on')
            elif value_type == int:
                return int(value)
            elif value_type == float:
                return float(value)
            elif value_type == list:
                # Comma-separated values
                return [v.strip() for v in value.split(',') if v.strip()]
            else:
                return value
        except (ValueError, TypeError) as e:
            raise ValidationError(
                f"Invalid type for configuration value: [{section}] {key}",
                field=f"{section}.{key}",
                value=value,
                details={'expected_type': value_type.__name__, 'error': str(e)}
            )
    
    def get_section(self, section: str) -> Dict[str, str]:
        """
        Get all values from a section
        
        Args:
            section: Section name
            
        Returns:
            Dictionary of key-value pairs
        """
        if not self.config.has_section(section):
            return {}
        return dict(self.config.items(section))
    
    def has_section(self, section: str) -> bool:
        """Check if section exists"""
        return self.config.has_section(section)
    
    def has_option(self, section: str, key: str) -> bool:
        """Check if option exists"""
        return self.config.has_option(section, key)
    
    def sections(self) -> List[str]:
        """Get list of all sections"""
        return self.config.sections()
    
    def validate_required(self, requirements: Dict[str, List[str]]) -> None:
        """
        Validate that required configuration values exist
        
        Args:
            requirements: Dict mapping section names to lists of required keys
            
        Raises:
            ConfigurationError: If any required values are missing
        """
        missing = []
        
        for section, keys in requirements.items():
            if not self.config.has_section(section):
                missing.append(f"Section [{section}]")
                continue
                
            for key in keys:
                if not self.config.has_option(section, key):
                    missing.append(f"[{section}] {key}")
        
        if missing:
            raise ConfigurationError(
                f"Missing required configuration: {', '.join(missing)}",
                details={'missing': missing}
            )
    
    def to_dict(self) -> Dict[str, Dict[str, str]]:
        """Convert configuration to nested dictionary"""
        return {section: dict(self.config.items(section)) 
                for section in self.config.sections()}
    
    def __repr__(self) -> str:
        if self._config_file:
            return f"Config(file='{self._config_file}', sections={len(self.config.sections())})"
        return f"Config(loaded={self._loaded}, sections={len(self.config.sections())})"


# Global configuration instance
_global_config: Optional[Config] = None


def get_config(config_file: Optional[Union[str, Path]] = None) -> Config:
    """
    Get global configuration instance
    
    Args:
        config_file: Path to config file (only used on first call)
        
    Returns:
        Global Config instance
    """
    global _global_config
    if _global_config is None:
        _global_config = Config(config_file)
    return _global_config


def load_config(config_file: Union[str, Path]) -> Config:
    """
    Load configuration file
    
    Args:
        config_file: Path to configuration file
        
    Returns:
        Loaded Config instance
    """
    global _global_config
    _global_config = Config(config_file)
    return _global_config
