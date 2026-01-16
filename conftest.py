"""
© 2026 Tony Ray Macier III. All rights reserved.

Thalos Prime™ is a proprietary system.
"""

"""
Pytest Configuration and Fixtures for Thalos Prime
"""

import pytest
import sys
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))


@pytest.fixture
def cis_instance():
    """Fixture providing a fresh CIS instance"""
    from core.cis.controller import CIS
    cis = CIS()
    yield cis
    # Cleanup
    if cis.system_state.get('booted'):
        cis.shutdown()


@pytest.fixture
def booted_cis():
    """Fixture providing a booted CIS instance"""
    from core.cis.controller import CIS
    cis = CIS()
    cis.boot()
    yield cis
    cis.shutdown()


@pytest.fixture
def memory_module():
    """Fixture providing a fresh memory module"""
    from core.memory.storage import MemoryModule
    mem = MemoryModule()
    yield mem
    mem.clear()


@pytest.fixture
def codegen_module():
    """Fixture providing a code generator"""
    from codegen.generator import CodeGenerator
    gen = CodeGenerator()
    yield gen
    gen.clear_history()


@pytest.fixture
def cli_instance():
    """Fixture providing a CLI instance"""
    from interfaces.cli.cli import CLI
    cli = CLI()
    return cli


@pytest.fixture
def api_instance():
    """Fixture providing an API instance"""
    from interfaces.api.server import API
    api = API()
    return api


@pytest.fixture(autouse=True)
def reset_singletons():
    """Reset singleton instances between tests"""
    yield
    # Reset logging singleton
    try:
        from core.logging import ThalosLogger
        ThalosLogger._instance = None
        ThalosLogger._initialized = False
    except ImportError:
        pass


@pytest.fixture
def sample_config_file(tmp_path):
    """Create a sample config file for testing"""
    config_file = tmp_path / "test_config.ini"
    config_file.write_text("""
[system]
name = Thalos Prime Test
version = 3.0.0
debug = true

[memory]
max_size = 1000
persistence = false

[logging]
level = DEBUG
file = logs/test.log
""")
    return config_file
