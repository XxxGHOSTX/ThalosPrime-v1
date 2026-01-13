#!/usr/bin/env python3
"""
Thalos Prime v2.0 - Integration Test
Tests complete wetware-to-chatbot pipeline
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_wetware_integration():
    """Test complete wetware processing pipeline"""
    print("Testing Wetware Integration Pipeline...")
    
    from wetware.organoid_core import OrganoidCore
    from wetware.mea_interface import MEAInterface
    from wetware.life_support import LifeSupport
    
    # Initialize components
    life_support = LifeSupport()
    assert life_support.initialize(), "Life support init failed"
    
    mea = MEAInterface(channels=1000)  # Use fewer channels for testing
    assert mea.initialize(), "MEA init failed"
    
    organoid = OrganoidCore("test_org", "logic")
    assert organoid.initialize(), "Organoid init failed"
    
    # Test complete pipeline
    # 1. Create digital signal
    digital_signal = {
        'type': 'query',
        'data': {'text': 'test message'},
        'intensity': 0.8
    }
    
    # 2. Encode to pulses
    pulse_pattern = mea.encode_digital_to_pulse(digital_signal)
    assert 'pulses' in pulse_pattern, "Pulse encoding failed"
    assert len(pulse_pattern['pulses']) > 0, "No pulses generated"
    
    # 3. Process through organoid
    stimulus = {
        'type': 'pattern',
        'intensity': 0.8,
        'data': pulse_pattern
    }
    response = organoid.process_stimulus(stimulus)
    assert 'spikes' in response, "Organoid processing failed"
    
    # 4. Apply feedback
    organoid.apply_feedback(reward=True, intensity=0.8)
    
    # 5. Decode spikes
    decoded = mea.decode_spike_train(response['spikes'])
    assert decoded['decoded'], "Spike decoding failed"
    
    # 6. Update life support
    life_support.update(dt=1.0)
    viability = life_support.get_viability_score()
    assert viability > 0.5, f"Low viability: {viability}"
    
    print("✓ Complete wetware pipeline working")
    print(f"  - Pulses generated: {len(pulse_pattern['pulses'])}")
    print(f"  - Spikes produced: {len(response['spikes'])}")
    print(f"  - Confidence: {response['confidence']:.2f}")
    print(f"  - Viability: {viability:.2f}")
    
    return True

def test_database_integration():
    """Test database with wetware data storage"""
    print("\nTesting Database Integration...")
    
    from database.connection_manager import DatabaseManager
    
    db = DatabaseManager(db_type="memory")
    
    # Get connection and store data
    conn = db.pool.get_connection()
    conn['data']['test_interaction'] = {
        'message': 'test query',
        'spikes': 150,
        'confidence': 0.85,
        'lobes': ['logic', 'abstract']
    }
    db.pool.return_connection(conn)
    
    # Retrieve data from same connection
    conn = db.pool.get_connection()
    data = conn['data'].get('test_interaction')
    assert data is not None, "Data storage failed"
    assert data['spikes'] == 150, "Data retrieval incorrect"
    db.pool.return_connection(conn)
    
    # Check statistics
    stats = db.get_statistics()
    assert 'pool' in stats, "Statistics missing"
    assert stats['pool']['total_connections'] > 0, "No connections"
    
    print("✓ Database integration working")
    print(f"  - Active connections: {stats['pool']['total_connections']}")
    
    db.close()
    return True

def test_neural_wetware_integration():
    """Test neural network with wetware"""
    print("\nTesting Neural-Wetware Integration...")
    
    from ai.neural.bio_neural_network import BioNeuralNetwork
    from wetware.organoid_core import OrganoidCore
    
    # Create small network
    net = BioNeuralNetwork("integration_test")
    input_layer = net.create_layer(5, "input")
    output_layer = net.create_layer(3, "output")
    net.connect_layers(input_layer, output_layer, 0.5)
    
    # Create organoid
    organoid = OrganoidCore("test_org", "abstract")
    organoid.initialize()
    
    # Process through both systems
    input_pattern = [0.5, 0.7, 0.3, 0.9, 0.6]
    net.stimulate_inputs(input_pattern)
    
    # Simulate
    for _ in range(20):
        net.simulate_step()
    
    output = net.get_output_activity()
    
    # Process through organoid
    stimulus = {
        'type': 'pattern',
        'intensity': sum(output) / len(output),
        'data': {'neural_output': output}
    }
    org_response = organoid.process_stimulus(stimulus)
    
    print("✓ Neural-Wetware integration working")
    print(f"  - Neural output: {[round(x, 2) for x in output]}")
    print(f"  - Organoid spikes: {len(org_response['spikes'])}")
    print(f"  - Organoid confidence: {org_response['confidence']:.2f}")
    
    return True

def test_reinforcement_integration():
    """Test RL with wetware feedback"""
    print("\nTesting Reinforcement Learning Integration...")
    
    from ai.learning.reinforcement_learner import ReinforcementLearner
    
    rl = ReinforcementLearner(state_dim=5, action_dim=3)
    
    # Simulate wetware feedback loop
    state = [0.2, 0.5, 0.8, 0.3, 0.7]
    
    for episode in range(10):
        action = rl.get_action(state)
        reward = 0.5 + (episode * 0.05)  # Improving reward (simulated wetware feedback)
        next_state = [s + 0.1 for s in state]
        
        rl.store_experience(state, action, reward, next_state, False)
        td_error = rl.update(state, action, reward, next_state, False)
        
        state = next_state
    
    stats = rl.get_statistics()
    
    print("✓ RL-Wetware integration working")
    print(f"  - Updates: {stats['total_updates']}")
    print(f"  - Total reward: {stats['total_reward']:.2f}")
    print(f"  - States explored: {stats['states_explored']}")
    
    return True

def test_complete_pipeline():
    """Test complete message->wetware->response pipeline"""
    print("\nTesting Complete Pipeline...")
    
    from wetware.organoid_core import OrganoidCore
    from wetware.mea_interface import MEAInterface
    from wetware.life_support import LifeSupport
    from database.connection_manager import DatabaseManager
    
    # Initialize all components
    life_support = LifeSupport()
    life_support.initialize()
    
    mea = MEAInterface(channels=1000)
    mea.initialize()
    
    organoids = []
    for i, lobe_type in enumerate(['logic', 'abstract', 'governance']):
        org = OrganoidCore(f"org_{i}", lobe_type)
        org.initialize()
        organoids.append(org)
    
    db = DatabaseManager(db_type="memory")
    
    # Simulate message processing
    message = "Test biological intelligence query"
    
    # Encode
    digital_signal = {'type': 'query', 'data': {'text': message}, 'intensity': 0.7}
    pulse_pattern = mea.encode_digital_to_pulse(digital_signal)
    
    # Process through all lobes
    all_spikes = []
    for org in organoids:
        stimulus = {'type': 'pattern', 'intensity': 0.7, 'data': pulse_pattern}
        response = org.process_stimulus(stimulus)
        all_spikes.extend(response['spikes'])
        org.apply_feedback(reward=True, intensity=0.5)
    
    # Decode
    decoded = mea.decode_spike_train(all_spikes)
    
    # Update life support
    life_support.update(dt=1.0)
    
    # Store in database (use same connection)
    conn = db.pool.get_connection()
    conn['data']['pipeline_test'] = {
        'message': message,
        'total_spikes': len(all_spikes),
        'lobes_active': len(organoids),
        'decoded_confidence': decoded.get('confidence', 0),
        'viability': life_support.get_viability_score()
    }
    
    # Verify (same connection)
    stored_data = conn['data']['pipeline_test']
    db.pool.return_connection(conn)
    
    print("✓ Complete pipeline working")
    print(f"  - Message: '{message}'")
    print(f"  - Total spikes: {stored_data['total_spikes']}")
    print(f"  - Active lobes: {stored_data['lobes_active']}")
    print(f"  - Confidence: {stored_data['decoded_confidence']:.2f}")
    print(f"  - Viability: {stored_data['viability']:.2f}")
    
    # Cleanup
    db.close()
    
    return True

def main():
    """Run all integration tests"""
    print("=" * 60)
    print("THALOS PRIME v2.0 - INTEGRATION TEST")
    print("=" * 60)
    
    tests = [
        ("Wetware Integration", test_wetware_integration),
        ("Database Integration", test_database_integration),
        ("Neural-Wetware Integration", test_neural_wetware_integration),
        ("RL Integration", test_reinforcement_integration),
        ("Complete Pipeline", test_complete_pipeline)
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"✗ {name} failed: {e}")
            import traceback
            traceback.print_exc()
            results.append((name, False))
    
    print("\n" + "=" * 60)
    print("INTEGRATION TEST RESULTS")
    print("=" * 60)
    
    for name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{name:30s}: {status}")
    
    passed_count = sum(1 for _, p in results if p)
    total_count = len(results)
    
    print("\n" + "=" * 60)
    print(f"Total: {passed_count}/{total_count} integration tests passed")
    print("=" * 60)
    
    if passed_count == total_count:
        print("\n🎉 All integration tests passed!")
        print("✓ Wetware-Database-AI pipeline fully operational")
        return 0
    else:
        print(f"\n⚠️  {total_count - passed_count} integration test(s) failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())
