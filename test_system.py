#!/usr/bin/env python3
"""
Thalos Prime v2.0 - Quick Start Test
Tests all major components to ensure system is working
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_core_systems():
    """Test core CIS system"""
    print("Testing Core CIS...")
    from core.cis import CIS
    
    cis = CIS()
    assert cis.boot(), "CIS boot failed"
    status = cis.status()
    assert status['status'] == 'operational', "CIS not operational"
    print("✓ Core CIS working")
    return True

def test_wetware():
    """Test wetware components"""
    print("\nTesting Wetware Components...")
    try:
        from wetware.organoid_core import OrganoidCore
        from wetware.mea_interface import MEAInterface
        from wetware.life_support import LifeSupport
        
        # Test Organoid
        organoid = OrganoidCore("test_org", "logic")
        assert organoid.initialize(), "Organoid init failed"
        print("✓ Organoid Core working")
        
        # Test MEA
        mea = MEAInterface(channels=100)
        assert mea.initialize(), "MEA init failed"
        print("✓ MEA Interface working")
        
        # Test Life Support
        life_support = LifeSupport()
        assert life_support.initialize(), "Life support init failed"
        print("✓ Life Support working")
        
        return True
    except Exception as e:
        print(f"⚠️  Wetware test failed: {e}")
        return False

def test_ai_systems():
    """Test AI components"""
    print("\nTesting AI Systems...")
    try:
        from ai.neural.bio_neural_network import BioNeuralNetwork
        from ai.learning.reinforcement_learner import ReinforcementLearner
        
        # Test Neural Network
        net = BioNeuralNetwork("test_net")
        input_layer = net.create_layer(5, "input")
        output_layer = net.create_layer(3, "output")
        net.connect_layers(input_layer, output_layer, 0.5)
        print("✓ Bio Neural Network working")
        
        # Test RL Agent
        rl = ReinforcementLearner(state_dim=5, action_dim=3)
        action = rl.get_action([0.1, 0.2, 0.3, 0.4, 0.5])
        print("✓ Reinforcement Learner working")
        
        return True
    except Exception as e:
        print(f"⚠️  AI test failed: {e}")
        return False

def test_database():
    """Test database manager"""
    print("\nTesting Database Manager...")
    try:
        from database.connection_manager import DatabaseManager
        
        db = DatabaseManager(db_type="memory")
        with db.get_connection() as conn:
            assert conn is not None, "Connection failed"
        print("✓ Database Manager working")
        return True
    except Exception as e:
        print(f"⚠️  Database test failed: {e}")
        return False

def test_interfaces():
    """Test interfaces"""
    print("\nTesting Interfaces...")
    try:
        from core.cis import CIS
        from interfaces.cli import CLI
        from interfaces.api import API
        
        cis = CIS()
        cis.boot()
        
        cli = CLI(cis)
        result = cli.execute(['status'])
        print("✓ CLI Interface working")
        
        api = API(cis)
        response = api.handle_request('GET', '/health')
        assert response['status'] == 'success', "API health check failed"
        print("✓ API Interface working")
        
        return True
    except Exception as e:
        print(f"⚠️  Interface test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("THALOS PRIME v2.0 - SYSTEM TEST")
    print("=" * 60)
    
    results = []
    
    results.append(("Core Systems", test_core_systems()))
    results.append(("Wetware", test_wetware()))
    results.append(("AI Systems", test_ai_systems()))
    results.append(("Database", test_database()))
    results.append(("Interfaces", test_interfaces()))
    
    print("\n" + "=" * 60)
    print("TEST RESULTS")
    print("=" * 60)
    
    for name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{name:20s}: {status}")
    
    passed_count = sum(1 for _, p in results if p)
    total_count = len(results)
    
    print("\n" + "=" * 60)
    print(f"Total: {passed_count}/{total_count} tests passed")
    print("=" * 60)
    
    if passed_count == total_count:
        print("\n🎉 All systems operational!")
        return 0
    else:
        print(f"\n⚠️  {total_count - passed_count} system(s) need attention")
        return 1

if __name__ == "__main__":
    sys.exit(main())
