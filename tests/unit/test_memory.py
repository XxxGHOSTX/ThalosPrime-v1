"""
Thalos Prime v1.0 - Unit Tests for Memory Module

Tests for deterministic in-memory storage with explicit CRUD operations
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from core.memory import MemoryModule


def test_memory_initialization():
    """Test Memory Module initialization"""
    memory = MemoryModule()
    assert memory is not None
    assert len(memory.list_keys()) == 0
    assert memory.count() == 0
    print("✓ Memory initialization test passed")


def test_crud_create():
    """Test Create operation (explicit CRUD)"""
    memory = MemoryModule()
    
    # Successful create
    result = memory.create('key1', 'value1')
    assert result is True
    assert memory.exists('key1') is True
    
    # Duplicate create should fail
    result = memory.create('key1', 'value2')
    assert result is False
    
    print("✓ CRUD Create test passed")


def test_crud_read():
    """Test Read operation (explicit CRUD)"""
    memory = MemoryModule()
    
    # Create then read
    memory.create('key1', 'value1')
    value = memory.read('key1')
    assert value == 'value1'
    
    # Read non-existent key
    value = memory.read('nonexistent')
    assert value is None
    
    print("✓ CRUD Read test passed")


def test_crud_update():
    """Test Update operation (explicit CRUD)"""
    memory = MemoryModule()
    
    # Create then update
    memory.create('key1', 'value1')
    result = memory.update('key1', 'value2')
    assert result is True
    assert memory.read('key1') == 'value2'
    
    # Update non-existent key should fail
    result = memory.update('nonexistent', 'value')
    assert result is False
    
    print("✓ CRUD Update test passed")


def test_crud_delete():
    """Test Delete operation (explicit CRUD)"""
    memory = MemoryModule()
    
    # Create then delete
    memory.create('key1', 'value1')
    assert memory.exists('key1') is True
    
    result = memory.delete('key1')
    assert result is True
    assert memory.exists('key1') is False
    
    # Delete non-existent key should fail
    result = memory.delete('nonexistent')
    assert result is False
    
    print("✓ CRUD Delete test passed")


def test_exists():
    """Test key existence check"""
    memory = MemoryModule()
    
    # Key doesn't exist
    assert memory.exists('key1') is False
    
    # Create key
    memory.create('key1', 'value1')
    assert memory.exists('key1') is True
    
    # Delete key
    memory.delete('key1')
    assert memory.exists('key1') is False
    
    print("✓ Exists test passed")


def test_list_keys():
    """Test listing all keys"""
    memory = MemoryModule()
    
    # Empty storage
    assert memory.list_keys() == []
    
    # Add keys
    memory.create('key1', 'value1')
    memory.create('key2', 'value2')
    memory.create('key3', 'value3')
    
    keys = memory.list_keys()
    assert len(keys) == 3
    assert 'key1' in keys
    assert 'key2' in keys
    assert 'key3' in keys
    
    print("✓ List keys test passed")


def test_count():
    """Test counting stored items"""
    memory = MemoryModule()
    
    assert memory.count() == 0
    
    memory.create('key1', 'value1')
    assert memory.count() == 1
    
    memory.create('key2', 'value2')
    assert memory.count() == 2
    
    memory.delete('key1')
    assert memory.count() == 1
    
    print("✓ Count test passed")


def test_clear():
    """Test clearing all data"""
    memory = MemoryModule()
    
    memory.create('key1', 'value1')
    memory.create('key2', 'value2')
    assert memory.count() == 2
    
    memory.clear()
    assert memory.count() == 0
    assert len(memory.list_keys()) == 0
    
    print("✓ Clear test passed")


def test_deterministic_behavior():
    """Test that memory operations are deterministic"""
    memory1 = MemoryModule()
    memory2 = MemoryModule()
    
    # Same operations should produce same results
    operations = [
        ('create', 'k1', 'v1'),
        ('create', 'k2', 'v2'),
        ('update', 'k1', 'v1_updated'),
        ('delete', 'k2', None)
    ]
    
    for op, key, value in operations:
        if op == 'create':
            memory1.create(key, value)
            memory2.create(key, value)
        elif op == 'update':
            memory1.update(key, value)
            memory2.update(key, value)
        elif op == 'delete':
            memory1.delete(key)
            memory2.delete(key)
    
    # Both should have same state
    assert memory1.list_keys() == memory2.list_keys()
    assert memory1.count() == memory2.count()
    assert memory1.read('k1') == memory2.read('k1')
    
    print("✓ Deterministic behavior test passed")


def test_no_side_effects():
    """Test that operations have no side effects"""
    memory = MemoryModule()
    
    # Create key
    memory.create('key1', 'value1')
    
    # Reading should not modify state
    value1 = memory.read('key1')
    value2 = memory.read('key1')
    assert value1 == value2
    assert memory.count() == 1
    
    # Failed operations should not modify state
    result = memory.create('key1', 'other')  # Duplicate, should fail
    assert result is False
    assert memory.read('key1') == 'value1'  # Value unchanged
    
    result = memory.update('nonexistent', 'value')  # Update missing key
    assert result is False
    assert memory.count() == 1  # Count unchanged
    
    print("✓ No side effects test passed")


def test_persistence():
    """Test file-based persistence"""
    import tempfile
    
    # Create temporary file for testing
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        temp_path = f.name
    
    try:
        # Create memory with persistence and add data
        memory1 = MemoryModule(persistence_path=temp_path)
        memory1.create('key1', 'value1')
        memory1.create('key2', {'nested': 'data'})
        
        # Save to disk
        result = memory1.save_to_disk()
        assert result is True
        
        # Create new memory instance and verify data loads
        memory2 = MemoryModule(persistence_path=temp_path)
        assert memory2.read('key1') == 'value1'
        assert memory2.read('key2') == {'nested': 'data'}
        assert memory2.count() == 2
        
        print("✓ Persistence test passed")
    finally:
        # Clean up temp file
        if os.path.exists(temp_path):
            os.remove(temp_path)


if __name__ == '__main__':
    print("Running Memory Module Unit Tests...")
    test_memory_initialization()
    test_crud_create()
    test_crud_read()
    test_crud_update()
    test_crud_delete()
    test_exists()
    test_list_keys()
    test_count()
    test_clear()
    test_deterministic_behavior()
    test_no_side_effects()
    test_persistence()
    print("\nAll Memory Module tests passed!")
