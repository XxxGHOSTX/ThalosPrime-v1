"""
© 2026 Tony Ray Macier III. All rights reserved.

Thalos Prime™ is a proprietary system.
"""

"""
Pytest configuration and fixtures for Thalos Prime tests.

Provides common fixtures for deterministic testing.
"""

import pytest
import sys
import os
from pathlib import Path

# Add src directory to path
src_path = Path(__file__).parent / 'src'
sys.path.insert(0, str(src_path))


@pytest.fixture
def cis_instance():
    """
    Provide a fresh CIS instance for testing.
    
    Returns:
        CIS: Fresh CIS instance
    """
    from core.cis import CIS
    cis = CIS()
    yield cis
    # Cleanup
    if cis.system_state.get('booted'):
        cis.shutdown()


@pytest.fixture
def booted_cis():
    """
    Provide a booted CIS instance for testing.
    
    Returns:
        CIS: Booted CIS instance
    """
    from core.cis import CIS
    cis = CIS()
    cis.boot()
    yield cis
    # Cleanup
    cis.shutdown()


@pytest.fixture
def memory_module():
    """
    Provide a fresh Memory module for testing.
    
    Returns:
        MemoryModule: Fresh memory instance
    """
    from core.memory.storage import MemoryModule
    memory = MemoryModule()
    yield memory
    # Cleanup
    memory.clear()


@pytest.fixture
def config_manager():
    """
    Provide a ConfigManager instance for testing.
    
    Returns:
        ConfigManager: Fresh config manager
    """
    from core.config import ConfigManager
    config = ConfigManager()
    yield config


@pytest.fixture
def logger():
    """
    Provide a ThalosLogger instance for testing.
    
    Returns:
        ThalosLogger: Fresh logger instance
    """
    from core.logging import ThalosLogger
    logger = ThalosLogger()
    yield logger
    # Cleanup
    logger.shutdown()


@pytest.fixture
def temp_config_file(tmp_path):
    """
    Provide a temporary config file for testing.
    
    Args:
        tmp_path: Pytest temporary directory fixture
        
    Returns:
        Path: Path to temporary config file
    """
    config_file = tmp_path / "test_config.ini"
    config_content = """
[system]
version = 1.0
debug = true
log_level = DEBUG

[memory]
type = dict
max_size = 1000
persistence = false

[codegen]
templates_dir = ./templates
output_dir = ./output
validate_syntax = true
"""
    config_file.write_text(config_content)
    yield config_file


@pytest.fixture
def sample_state():
    """
    Provide sample system state for testing.
    
    Returns:
        dict: Sample state dictionary
    """
    return {
        'version': '1.0',
        'status': 'operational',
        'booted': True,
        'subsystems': {
            'memory': True,
            'codegen': True,
            'cli': True,
            'api': True
        }
    }


# Configure pytest
def pytest_configure(config):
    """Configure pytest with custom markers"""
    config.addinivalue_line("markers", "unit: mark test as a unit test")
    config.addinivalue_line("markers", "integration: mark test as an integration test")
    config.addinivalue_line("markers", "slow: mark test as slow running")


def pytest_collection_modifyitems(config, items):
    """Modify test collection - add markers automatically"""
    for item in items:
        # Auto-mark tests based on path
        if "unit" in str(item.fspath):
            item.add_marker(pytest.mark.unit)
        elif "integration" in str(item.fspath):
            item.add_marker(pytest.mark.integration)
