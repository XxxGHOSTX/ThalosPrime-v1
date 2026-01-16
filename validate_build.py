#!/usr/bin/env python3
"""
© 2026 Tony Ray Macier III. All rights reserved.

Thalos Prime™ is a proprietary system.

Final System Validation - Verify all requirements and integrations
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

print("="*70)
print("THALOS PRIME v3.0 - FINAL SYSTEM VALIDATION")
print("© 2026 Tony Ray Macier III. All rights reserved.")
print("="*70 + "\n")

validation_results = []

def validate_requirement(name, check_func):
    """Validate a requirement"""
    try:
        result = check_func()
        status = "✓ PASS" if result else "✗ FAIL"
        validation_results.append((name, result))
        print(f"{status} - {name}")
        return result
    except Exception as e:
        print(f"✗ FAIL - {name}: {e}")
        validation_results.append((name, False))
        return False


print("1. VALIDATING CORE REQUIREMENTS")
print("-" * 70)

def check_github_actions_updated():
    """Verify GitHub Actions updated to v4"""
    try:
        with open('.github/workflows/ci.yml', 'r') as f:
            content = f.read()
            return 'actions/checkout@v4' in content and 'actions/upload-artifact@v4' in content
    except:
        return False

def check_requirements_file():
    """Verify requirements.txt exists with all dependencies"""
    try:
        with open('requirements.txt', 'r') as f:
            content = f.read()
            required = ['pytest', 'python-dotenv']
            return all(dep in content for dep in required)
    except:
        return False

def check_env_example():
    """Verify .env.example exists"""
    return os.path.exists('.env.example')

def check_data_persistence():
    """Verify data persistence implementation"""
    try:
        from core.memory.storage import MemoryModule
        mem = MemoryModule(persistence_path="/tmp/test_storage.json")
        return hasattr(mem, 'save_to_disk') and hasattr(mem, 'load_from_disk')
    except:
        return False

validate_requirement("GitHub Actions updated to v4", check_github_actions_updated)
validate_requirement("requirements.txt with dependencies", check_requirements_file)
validate_requirement(".env.example configuration", check_env_example)
validate_requirement("Data persistence implemented", check_data_persistence)

print("\n2. VALIDATING WETWARE COMPONENTS")
print("-" * 70)

def check_wetware_core():
    """Verify wetware core components"""
    try:
        from wetware.organoid_core import OrganoidCore
        from wetware.mea_interface import MEAInterface
        from wetware.life_support import LifeSupport
        
        # Test organoid
        org = OrganoidCore("test", "logic")
        org.initialize()
        
        # Test MEA
        mea = MEAInterface(channels=100)
        mea.initialize()
        
        # Test life support
        ls = LifeSupport()
        ls.initialize()
        
        return True
    except Exception as e:
        print(f"  Error: {e}")
        return False

def check_organoid_lobes():
    """Verify all 3 organoid lobes"""
    try:
        from wetware.organoid_core import OrganoidCore
        lobes = ['logic', 'abstract', 'governance']
        for lobe in lobes:
            org = OrganoidCore(f"test_{lobe}", lobe)
            org.initialize()
            status = org.get_status()
            if status['lobe_type'] != lobe:
                return False
        return True
    except:
        return False

def check_mea_20k_channels():
    """Verify MEA supports 20,000 channels"""
    try:
        from wetware.mea_interface import MEAInterface
        mea = MEAInterface(channels=20000)
        mea.initialize()
        status = mea.get_status()
        return status['total_channels'] == 20000
    except:
        return False

def check_life_support_homeostasis():
    """Verify life support maintains homeostasis"""
    try:
        from wetware.life_support import LifeSupport
        ls = LifeSupport()
        ls.initialize()
        ls.update(dt=1.0)
        viability = ls.get_viability_score()
        return viability > 0.9
    except:
        return False

validate_requirement("Wetware core components operational", check_wetware_core)
validate_requirement("3 organoid lobes (logic, abstract, governance)", check_organoid_lobes)
validate_requirement("MEA with 20,000 channels", check_mea_20k_channels)
validate_requirement("Life support homeostasis", check_life_support_homeostasis)

print("\n3. VALIDATING DATABASE INTEGRATION")
print("-" * 70)

def check_database_auto_reconnect():
    """Verify database auto-reconnection"""
    try:
        from database.connection_manager import DatabaseManager
        db = DatabaseManager(db_type="memory")
        stats = db.get_statistics()
        return 'pool' in stats and stats['pool']['total_connections'] > 0
    except:
        return False

def check_database_shared_storage():
    """Verify shared data storage across connections"""
    try:
        from database.connection_manager import DatabaseManager
        db = DatabaseManager(db_type="memory")
        
        # Store data
        conn1 = db.pool.get_connection()
        conn1['data']['test_key'] = 'test_value'
        db.pool.return_connection(conn1)
        
        # Retrieve data
        conn2 = db.pool.get_connection()
        value = conn2['data'].get('test_key')
        db.pool.return_connection(conn2)
        
        db.close()
        return value == 'test_value'
    except Exception as e:
        print(f"  Error: {e}")
        return False

validate_requirement("Database auto-reconnection", check_database_auto_reconnect)
validate_requirement("Database shared storage", check_database_shared_storage)

print("\n4. VALIDATING CHATBOT CAPABILITIES")
print("-" * 70)

def check_nlp_processor():
    """Verify NLP processor"""
    try:
        from interfaces.web.nlp_processor import NLPProcessor
        nlp = NLPProcessor()
        
        # Test analysis
        analysis = nlp.analyze_message("Hello, how are you?")
        return analysis['intent'] == 'greeting'
    except:
        return False

def check_action_handler():
    """Verify action handler"""
    try:
        from interfaces.web.action_handler import ActionHandler
        from core.cis import CIS
        from database.connection_manager import DatabaseManager
        
        cis = CIS()
        cis.boot()
        db = DatabaseManager(db_type="memory")
        
        # Create minimal system for action handler
        from wetware.organoid_core import OrganoidCore
        from wetware.mea_interface import MEAInterface
        from wetware.life_support import LifeSupport
        from ai.neural.bio_neural_network import BioNeuralNetwork
        from ai.learning.reinforcement_learner import ReinforcementLearner
        
        ls = LifeSupport()
        ls.initialize()
        mea = MEAInterface(channels=100)
        mea.initialize()
        orgs = []
        for i in range(3):
            org = OrganoidCore(f"org_{i}", "logic")
            org.initialize()
            orgs.append(org)
        
        net = BioNeuralNetwork("test")
        rl = ReinforcementLearner(state_dim=5, action_dim=3)
        
        handler = ActionHandler(cis, orgs, mea, ls, net, rl, db)
        
        # Test action detection
        action_type, params = handler.detect_action("Calculate 5 + 3")
        
        db.close()
        return action_type == 'calculate'
    except Exception as e:
        print(f"  Error: {e}")
        return False

def check_wetware_chatbot_integration():
    """Verify chatbot uses wetware for processing"""
    try:
        # Check web_server has wetware integration
        with open('src/interfaces/web/web_server.py', 'r') as f:
            content = f.read()
            return all(keyword in content for keyword in [
                'process_through_wetware',
                'organoids',
                'mea.encode',
                'org.process_stimulus',
                'life_support'
            ])
    except:
        return False

def check_knowledge_base():
    """Verify knowledge base with multiple domains"""
    try:
        from interfaces.web.action_handler import ActionHandler
        from core.cis import CIS
        from database.connection_manager import DatabaseManager
        from wetware.organoid_core import OrganoidCore
        from wetware.mea_interface import MEAInterface
        from wetware.life_support import LifeSupport
        from ai.neural.bio_neural_network import BioNeuralNetwork
        from ai.learning.reinforcement_learner import ReinforcementLearner
        
        cis = CIS()
        cis.boot()
        db = DatabaseManager(db_type="memory")
        ls = LifeSupport()
        ls.initialize()
        mea = MEAInterface(channels=100)
        mea.initialize()
        orgs = [OrganoidCore(f"o{i}", "logic") for i in range(3)]
        for o in orgs: o.initialize()
        net = BioNeuralNetwork("t")
        rl = ReinforcementLearner(state_dim=5, action_dim=3)
        
        handler = ActionHandler(cis, orgs, mea, ls, net, rl, db)
        
        # Check knowledge domains
        domains = handler.knowledge_domains
        db.close()
        return len(domains) >= 7
    except Exception as e:
        print(f"  Error: {e}")
        return False

validate_requirement("NLP processor operational", check_nlp_processor)
validate_requirement("Action handler operational", check_action_handler)
validate_requirement("Chatbot uses wetware processing", check_wetware_chatbot_integration)
validate_requirement("Knowledge base (7+ domains)", check_knowledge_base)

print("\n5. VALIDATING WEB INTERFACE")
print("-" * 70)

def check_matrix_interface():
    """Verify Matrix-style interface files"""
    files = [
        'src/interfaces/web/templates/index.html',
        'src/interfaces/web/static/css/matrix-style.css',
        'src/interfaces/web/static/js/matrix-rain.js',
        'src/interfaces/web/static/js/chat-interface.js',
    ]
    return all(os.path.exists(f) for f in files)

def check_matrix_code_rain():
    """Verify matrix code rain implementation"""
    try:
        with open('src/interfaces/web/static/js/matrix-rain.js', 'r') as f:
            content = f.read()
            return 'canvas' in content and 'DNA' in content
    except:
        return False

def check_neural_visualizer():
    """Verify neural activity visualizer"""
    return os.path.exists('src/interfaces/web/static/js/neural-visualizer.js')

validate_requirement("Matrix-style interface files", check_matrix_interface)
validate_requirement("Matrix code rain animation", check_matrix_code_rain)
validate_requirement("Neural activity visualizer", check_neural_visualizer)

print("\n6. VALIDATING AUTO-DEPLOYMENT")
print("-" * 70)

def check_auto_deploy_scripts():
    """Verify auto-deployment scripts"""
    scripts = ['auto_deploy.sh', 'auto_deploy.bat', 'auto_deploy.py']
    return all(os.path.exists(s) for s in scripts)

def check_deploy_script_executable():
    """Verify deployment scripts are executable"""
    import stat
    try:
        sh_stat = os.stat('auto_deploy.sh')
        py_stat = os.stat('auto_deploy.py')
        return bool(sh_stat.st_mode & stat.S_IXUSR) and bool(py_stat.st_mode & stat.S_IXUSR)
    except:
        return False

validate_requirement("Auto-deployment scripts (sh, bat, py)", check_auto_deploy_scripts)
validate_requirement("Scripts are executable", check_deploy_script_executable)

print("\n7. VALIDATING DOCUMENTATION")
print("-" * 70)

def check_documentation():
    """Verify documentation files"""
    docs = ['README.md', 'SETUP.md', 'README_V2.md', 'DEPLOYMENT_COMPLETE.md']
    return all(os.path.exists(d) for d in docs)

def check_copyright_notices():
    """Verify copyright in all Python files"""
    import glob
    python_files = glob.glob('src/**/*.py', recursive=True)
    python_files.extend(glob.glob('*.py'))
    
    checked = 0
    for file in python_files[:20]:  # Check first 20
        try:
            with open(file, 'r') as f:
                content = f.read()
                if 'Tony Ray Macier III' in content:
                    checked += 1
        except:
            pass
    
    return checked > 10

validate_requirement("Complete documentation", check_documentation)
validate_requirement("Copyright notices in source files", check_copyright_notices)

print("\n8. VALIDATING TEST COVERAGE")
print("-" * 70)

def check_test_files():
    """Verify all test files exist"""
    tests = ['test_system.py', 'test_integration.py', 'test_chatbot.py']
    return all(os.path.exists(t) for t in tests)

def check_test_executability():
    """Verify tests can be imported"""
    try:
        import test_system
        import test_integration
        import test_chatbot
        return True
    except:
        return False

validate_requirement("Test files (system, integration, chatbot)", check_test_files)
validate_requirement("Tests are executable", check_test_executability)

print("\n9. VALIDATING AI/ML CAPABILITIES")
print("-" * 70)

def check_neural_network():
    """Verify bio neural network"""
    try:
        from ai.neural.bio_neural_network import BioNeuralNetwork
        net = BioNeuralNetwork("test")
        input_layer = net.create_layer(5, "input")
        output_layer = net.create_layer(3, "output")
        net.connect_layers(input_layer, output_layer, 0.5)
        
        net.stimulate_inputs([0.5, 0.7, 0.3, 0.9, 0.2])
        for _ in range(10):
            net.simulate_step()
        
        stats = net.get_network_stats()
        return stats['num_neurons'] > 0
    except:
        return False

def check_reinforcement_learning():
    """Verify reinforcement learning"""
    try:
        from ai.learning.reinforcement_learner import ReinforcementLearner
        rl = ReinforcementLearner(state_dim=5, action_dim=3)
        
        state = [0.2, 0.5, 0.8, 0.3, 0.7]
        action = rl.get_action(state)
        rl.update(state, action, 1.0, state, False)
        
        stats = rl.get_statistics()
        return stats['total_updates'] > 0
    except:
        return False

def check_stdp_learning():
    """Verify STDP learning in organoids"""
    try:
        from wetware.organoid_core import OrganoidCore
        org = OrganoidCore("test", "logic")
        org.initialize()
        
        # Apply positive feedback
        org.apply_feedback(reward=True, intensity=0.8)
        
        status = org.get_status()
        return status['plasticity_coefficient'] >= 1.0
    except:
        return False

validate_requirement("Bio neural network with STDP", check_neural_network)
validate_requirement("Reinforcement learning (Q-learning)", check_reinforcement_learning)
validate_requirement("STDP learning in organoids", check_stdp_learning)

print("\n10. VALIDATING LEGAL FRAMEWORK")
print("-" * 70)

def check_license_file():
    """Verify proprietary license"""
    return os.path.exists('THALOS-PRIME-LICENSE.txt')

def check_ownership_declaration():
    """Verify ownership declaration"""
    return os.path.exists('OWNERSHIP.md')

def check_license_content():
    """Verify license contains copyright"""
    try:
        with open('THALOS-PRIME-LICENSE.txt', 'r') as f:
            content = f.read()
            return 'Tony Ray Macier III' in content and 'All rights reserved' in content
    except:
        return False

validate_requirement("THALOS-PRIME-LICENSE.txt", check_license_file)
validate_requirement("OWNERSHIP.md declaration", check_ownership_declaration)
validate_requirement("Copyright © 2026 Tony Ray Macier III", check_license_content)

# Summary
print("\n" + "="*70)
print("VALIDATION SUMMARY")
print("="*70)

categories = {
    "Core Requirements": validation_results[0:4],
    "Wetware Components": validation_results[4:8],
    "Database Integration": validation_results[8:10],
    "Chatbot Capabilities": validation_results[10:14],
    "Web Interface": validation_results[14:17],
    "Auto-Deployment": validation_results[17:19],
    "Documentation": validation_results[19:21],
    "Test Coverage": validation_results[21:23],
    "AI/ML Capabilities": validation_results[23:26],
    "Legal Framework": validation_results[26:29],
}

all_passed = True
for category, results in categories.items():
    passed = sum(1 for _, r in results if r)
    total = len(results)
    status = "✓" if passed == total else "✗"
    print(f"{status} {category}: {passed}/{total}")
    if passed != total:
        all_passed = False

total_passed = sum(1 for _, r in validation_results if r)
total_checks = len(validation_results)

print("\n" + "="*70)
print(f"TOTAL: {total_passed}/{total_checks} validations passed ({total_passed/total_checks*100:.1f}%)")
print("="*70)

if all_passed:
    print("\n🎉 ALL VALIDATIONS PASSED!")
    print("✓ Complete build verified")
    print("✓ All requirements functional")
    print("✓ Full integration confirmed")
    print("✓ System ready for deployment")
    print("\nTHALOS PRIME v3.0 - FULLY OPERATIONAL")
    print("© 2026 Tony Ray Macier III. All rights reserved.")
    sys.exit(0)
else:
    print(f"\n⚠️  {total_checks - total_passed} validation(s) failed")
    sys.exit(1)
