"""
© 2026 Tony Ray Macier III. All rights reserved.

Thalos Prime™ is a proprietary system.
"""

"""
Integration tests for Thalos Prime complete system lifecycle.

Tests the full system boot, operation, and shutdown cycle.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

import pytest
from core.cis import CIS


class TestSystemLifecycle:
    """Test complete system lifecycle"""
    
    def test_cis_initialization(self):
        """Test CIS initialization"""
        cis = CIS()
        
        assert cis.system_state['status'] == 'created'
        assert not cis.system_state['booted']
        
    def test_cis_lifecycle_sequence(self):
        """Test CIS lifecycle: initialize -> validate -> boot"""
        cis = CIS()
        
        # Initialize
        assert cis.initialize() is True
        assert cis.system_state['initialized'] is True
        
        # Validate
        assert cis.validate() is True
        assert cis.system_state['validated'] is True
        
        # Boot
        assert cis.boot() is True
        assert cis.system_state['booted'] is True
        assert cis.system_state['status'] == 'operational'
        
        # Cleanup
        cis.shutdown()
        
    def test_cis_subsystem_ownership(self):
        """Test that CIS owns all subsystem instances"""
        cis = CIS()
        assert cis.boot() is True
        
        # All subsystems must be CIS-owned (not None)
        assert cis.get_memory() is not None, "Memory subsystem not initialized by CIS"
        assert cis.get_codegen() is not None, "CodeGen subsystem not initialized by CIS"
        assert cis.get_cli() is not None, "CLI subsystem not initialized by CIS"
        assert cis.get_api() is not None, "API subsystem not initialized by CIS"
        
        # Cleanup
        cis.shutdown()
        
    def test_cis_status(self):
        """Test CIS status reporting"""
        cis = CIS()
        cis.boot()
        
        status = cis.status()
        
        assert 'version' in status
        assert 'status' in status
        assert 'booted' in status
        assert 'subsystems' in status
        
        assert status['version'] == '1.0'
        assert status['status'] == 'operational'
        assert status['booted'] is True
        
        subsystems = status['subsystems']
        assert subsystems['memory'] is True
        assert subsystems['codegen'] is True
        assert subsystems['cli'] is True
        assert subsystems['api'] is True
        
        # Cleanup
        cis.shutdown()
        
    def test_cis_checkpoint(self):
        """Test CIS state checkpointing"""
        cis = CIS()
        cis.boot()
        
        checkpoint = cis.checkpoint()
        
        assert 'version' in checkpoint
        assert 'status' in checkpoint
        assert 'booted' in checkpoint
        assert 'subsystems' in checkpoint
        assert 'state_history' in checkpoint
        
        # Should have state transitions recorded
        assert len(checkpoint['state_history']) > 0
        
        # Cleanup
        cis.shutdown()
        
    def test_cis_reconcile(self):
        """Test CIS state reconciliation"""
        cis = CIS()
        cis.boot()
        
        # Reconcile should succeed
        assert cis.reconcile() is True
        
        # System should still be operational
        status = cis.status()
        assert status['status'] == 'operational'
        
        # Cleanup
        cis.shutdown()
        
    def test_cis_shutdown(self):
        """Test CIS clean shutdown"""
        cis = CIS()
        cis.boot()
        
        assert cis.shutdown() is True
        
        status = cis.status()
        assert status['status'] == 'shutdown'
        assert status['booted'] is False
        
        # Subsystems should be cleared
        assert cis.get_memory() is None
        assert cis.get_codegen() is None
        assert cis.get_cli() is None
        assert cis.get_api() is None
        
    def test_memory_subsystem_lifecycle(self):
        """Test Memory subsystem lifecycle methods"""
        cis = CIS()
        cis.boot()
        
        memory = cis.get_memory()
        
        # Test initialization (already done by CIS)
        assert memory.initialize() is True
        
        # Test validation
        assert memory.validate() is True
        
        # Test operation
        status = memory.operate()
        assert status['state'] in ['initialized', 'validated']
        assert status['initialized'] is True
        
        # Test data operations
        memory.create('test_key', 'test_value')
        assert memory.read('test_key') == 'test_value'
        
        # Test checkpoint
        checkpoint = memory.checkpoint()
        assert checkpoint['version'] == '1.0'
        assert checkpoint['item_count'] > 0
        
        # Test reconcile
        assert memory.reconcile() is True
        
        # Test terminate
        assert memory.terminate() is True
        
        # Cleanup
        cis.shutdown()
        
    def test_codegen_subsystem_lifecycle(self):
        """Test CodeGen subsystem lifecycle methods"""
        cis = CIS()
        cis.boot()
        
        codegen = cis.get_codegen()
        
        # Test initialization (already done by CIS)
        assert codegen.initialize() is True
        
        # Test validation
        assert codegen.validate() is True
        
        # Test operation
        status = codegen.operate()
        assert status['state'] in ['initialized', 'validated']
        assert status['initialized'] is True
        
        # Test code generation
        code = codegen.generate_class('TestClass', methods=['test'])
        assert code is not None
        assert 'TestClass' in code
        
        # Test checkpoint
        checkpoint = codegen.checkpoint()
        assert checkpoint['version'] == '1.0'
        assert 'templates' in checkpoint
        
        # Test reconcile
        assert codegen.reconcile() is True
        
        # Test terminate
        assert codegen.terminate() is True
        
        # Cleanup
        cis.shutdown()
        
    def test_full_system_boot_operate_shutdown(self):
        """Test complete system lifecycle from boot to shutdown"""
        # Create
        cis = CIS()
        
        # Boot
        assert cis.boot() is True
        
        # Operate - use memory
        memory = cis.get_memory()
        memory.create('app_name', 'Thalos Prime')
        memory.create('version', '1.0.0')
        
        assert memory.read('app_name') == 'Thalos Prime'
        
        # Operate - use codegen
        codegen = cis.get_codegen()
        code = codegen.generate_function('my_func', parameters=['x', 'y'])
        assert code is not None
        assert 'my_func' in code
        
        # Checkpoint entire system
        checkpoint = cis.checkpoint()
        assert checkpoint['booted'] is True
        
        # Reconcile
        assert cis.reconcile() is True
        
        # Shutdown cleanly
        assert cis.shutdown() is True
        assert cis.status()['booted'] is False


class TestStateObservability:
    """Test that all state is observable, serializable, versioned, reconstructible"""
    
    def test_state_is_observable(self):
        """Test that state can be observed at any time"""
        cis = CIS()
        cis.boot()
        
        # Status should always be available
        status = cis.status()
        assert status is not None
        assert isinstance(status, dict)
        
        # Memory status
        memory = cis.get_memory()
        mem_status = memory.operate()
        assert mem_status is not None
        assert isinstance(mem_status, dict)
        
        cis.shutdown()
        
    def test_state_is_serializable(self):
        """Test that state can be serialized"""
        cis = CIS()
        cis.boot()
        
        # CIS checkpoint should be serializable
        checkpoint = cis.checkpoint()
        assert isinstance(checkpoint, dict)
        
        # Should be JSON-serializable
        import json
        json_str = json.dumps(checkpoint, default=str)
        assert json_str is not None
        
        cis.shutdown()
        
    def test_state_is_versioned(self):
        """Test that state includes version information"""
        cis = CIS()
        cis.boot()
        
        # Memory checkpoint includes version
        memory = cis.get_memory()
        checkpoint = memory.checkpoint()
        assert 'version' in checkpoint
        assert checkpoint['version'] == '1.0'
        
        # CodeGen checkpoint includes version
        codegen = cis.get_codegen()
        checkpoint = codegen.checkpoint()
        assert 'version' in checkpoint
        assert checkpoint['version'] == '1.0'
        
        cis.shutdown()
        
    def test_state_transitions_are_logged(self):
        """Test that state transitions are recorded"""
        cis = CIS()
        cis.boot()
        
        checkpoint = cis.checkpoint()
        assert 'state_history' in checkpoint
        
        # Should have recorded transitions
        history = checkpoint['state_history']
        assert len(history) > 0
        
        # Each transition should have required fields
        for transition in history:
            assert 'from' in transition
            assert 'to' in transition
            assert 'reason' in transition
            assert 'timestamp' in transition
        
        cis.shutdown()
