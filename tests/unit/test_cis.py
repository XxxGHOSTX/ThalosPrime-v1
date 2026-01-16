"""
Thalos Prime v1.0 - Unit Tests for CIS Module

Tests for the Central Intelligence System (primary authority and orchestrator)
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from core.cis import CIS


def test_cis_initialization():
    """Test CIS initialization"""
    cis = CIS()
    assert cis is not None
    assert cis.memory is None
    assert cis.codegen is None
    assert cis.cli is None
    assert cis.api is None
    status = cis.status()
    assert status['status'] == 'created'
    assert status['booted'] is False
    print("✓ CIS initialization test passed")


def test_boot_lifecycle():
    """Test system boot lifecycle hook"""
    cis = CIS()
    
    # Test successful boot
    result = cis.boot()
    assert result is True
    
    status = cis.status()
    assert status['booted'] is True
    assert status['status'] == 'operational'
    assert status['subsystems']['memory'] is True
    assert status['subsystems']['codegen'] is True
    assert status['subsystems']['cli'] is True
    assert status['subsystems']['api'] is True
    
    # Test duplicate boot fails
    result = cis.boot()
    assert result is False
    
    print("✓ Boot lifecycle test passed")


def test_shutdown_lifecycle():
    """Test system shutdown lifecycle hook"""
    cis = CIS()
    
    # Cannot shutdown before boot
    result = cis.shutdown()
    assert result is False
    
    # Boot then shutdown
    cis.boot()
    result = cis.shutdown()
    assert result is True
    
    status = cis.status()
    assert status['booted'] is False
    assert status['status'] == 'shutdown'
    assert status['subsystems']['memory'] is False
    
    print("✓ Shutdown lifecycle test passed")


def test_status_lifecycle():
    """Test status lifecycle hook"""
    cis = CIS()
    
    # Initial status
    status = cis.status()
    assert 'version' in status
    assert 'status' in status
    assert 'booted' in status
    assert 'subsystems' in status
    
    # After boot
    cis.boot()
    status = cis.status()
    assert status['version'] == '1.0'
    assert status['status'] == 'operational'
    assert status['booted'] is True
    
    print("✓ Status lifecycle test passed")


def test_subsystem_access():
    """Test accessing subsystems through CIS"""
    cis = CIS()
    cis.boot()
    
    # Access subsystems
    memory = cis.get_memory()
    assert memory is not None
    
    codegen = cis.get_codegen()
    assert codegen is not None
    
    cli = cis.get_cli()
    assert cli is not None
    
    api = cis.get_api()
    assert api is not None
    
    print("✓ Subsystem access test passed")


def test_interfaces_bound_to_cis():
    """Ensure interfaces initialized by CIS are bound to the CIS instance"""
    cis = CIS()
    cis.boot()
    
    cli = cis.get_cli()
    api = cis.get_api()
    
    assert cli is not None and cli.cis is cis
    assert api is not None and api.cis is cis
    
    print("✓ Interfaces bound to CIS test passed")


def test_subsystem_initialization_order():
    """Test that CIS initializes subsystems in correct order"""
    cis = CIS()
    
    # Before boot, subsystems should be None
    assert cis.get_memory() is None
    assert cis.get_codegen() is None
    
    # After boot, all should be initialized
    cis.boot()
    assert cis.get_memory() is not None
    assert cis.get_codegen() is not None
    assert cis.get_cli() is not None
    assert cis.get_api() is not None
    
    print("✓ Subsystem initialization order test passed")


if __name__ == '__main__':
    print("Running CIS Unit Tests...")
    test_cis_initialization()
    test_boot_lifecycle()
    test_shutdown_lifecycle()
    test_status_lifecycle()
    test_subsystem_access()
    test_interfaces_bound_to_cis()
    test_subsystem_initialization_order()
    print("\nAll CIS tests passed!")
