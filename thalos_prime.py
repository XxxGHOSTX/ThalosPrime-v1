#!/usr/bin/env python3
"""
© 2026 Tony Ray Macier III. All rights reserved.

Thalos Prime v3.0 - Synthetic Biological Intelligence
Main System Launcher

Complete system initialization and orchestration
"""

import sys
import os
import argparse
import signal
from typing import Optional

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Core imports
from core.cis import CIS

# Wetware imports
try:
    from wetware.organoid_core import OrganoidCore
    from wetware.mea_interface import MEAInterface
    from wetware.life_support import LifeSupport
    WETWARE_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Wetware components not fully available: {e}")
    WETWARE_AVAILABLE = False

# AI imports
try:
    from ai.neural.bio_neural_network import BioNeuralNetwork
    from ai.learning.reinforcement_learner import ReinforcementLearner
    AI_AVAILABLE = True
except ImportError as e:
    print(f"Warning: AI components not fully available: {e}")
    AI_AVAILABLE = False

# Database imports
try:
    from database.connection_manager import DatabaseManager
    DATABASE_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Database components not fully available: {e}")
    DATABASE_AVAILABLE = False

# Interface imports
from interfaces.cli import CLI
from interfaces.api import API


class ThalosPrime:
    """
    Main Thalos Prime System Controller
    
    Orchestrates all subsystems:
    - CIS (Central Intelligence System)
    - Wetware Core (Biological Computing)
    - AI/ML Systems (Neural Networks, Learning)
    - Database (Persistent Storage)
    - Interfaces (CLI, API, Web)
    """
    
    def __init__(self):
        self.version = "2.0"
        self.name = "Thalos Prime"
        self.initialized = False
        
        # Core components
        self.cis = None
        self.cli = None
        self.api = None
        
        # Wetware components
        self.organoids = []
        self.mea = None
        self.life_support = None
        
        # AI components
        self.neural_network = None
        self.rl_agent = None
        
        # Database
        self.db_manager = None
        
        # Status
        self.status = "dormant"
        
    def initialize(self, config: Optional[dict] = None) -> bool:
        """
        Initialize all subsystems
        
        Args:
            config: Configuration dictionary
            
        Returns:
            bool: True if initialization successful
        """
        config = config or {}
        
        print("=" * 70)
        print(f"{self.name} v{self.version} - SYNTHETIC BIOLOGICAL INTELLIGENCE")
        print("=" * 70)
        print()
        
        # Initialize CIS (Central Intelligence System)
        print("🔧 Initializing CIS (Central Intelligence System)...")
        self.cis = CIS()
        if not self.cis.boot():
            print("❌ CIS initialization failed")
            return False
        print("✓ CIS operational")
        
        # Initialize Wetware Core
        if WETWARE_AVAILABLE and config.get('enable_wetware', True):
            print("\n🧬 Initializing Wetware Core...")
            success = self._initialize_wetware()
            if success:
                print("✓ Wetware Core operational")
            else:
                print("⚠️  Wetware Core initialization failed (non-critical)")
        
        # Initialize AI Systems
        if AI_AVAILABLE and config.get('enable_ai', True):
            print("\n🤖 Initializing AI Systems...")
            success = self._initialize_ai()
            if success:
                print("✓ AI Systems operational")
            else:
                print("⚠️  AI Systems initialization failed (non-critical)")
        
        # Initialize Database
        if DATABASE_AVAILABLE and config.get('enable_database', True):
            print("\n💾 Initializing Database...")
            success = self._initialize_database(config.get('database', {}))
            if success:
                print("✓ Database operational")
            else:
                print("⚠️  Database initialization failed (non-critical)")
        
        # Initialize Interfaces
        print("\n🖥️  Initializing Interfaces...")
        self.cli = CLI(self.cis)
        self.api = API(self.cis)
        print("✓ CLI initialized")
        print("✓ API initialized")
        
        self.initialized = True
        self.status = "operational"
        
        print("\n" + "=" * 70)
        print("✓ SYSTEM INITIALIZATION COMPLETE")
        print("=" * 70)
        
        return True
    
    def _initialize_wetware(self) -> bool:
        """Initialize wetware components"""
        try:
            # Initialize Life Support
            self.life_support = LifeSupport()
            if not self.life_support.initialize():
                return False
            
            # Initialize MEA Interface
            self.mea = MEAInterface(channels=20000)
            if not self.mea.initialize():
                return False
            
            # Initialize Organoid Clusters
            lobe_types = ['logic', 'abstract', 'governance']
            for i, lobe_type in enumerate(lobe_types):
                organoid = OrganoidCore(f"organoid_{i}", lobe_type)
                if organoid.initialize():
                    self.organoids.append(organoid)
            
            return len(self.organoids) > 0
            
        except Exception as e:
            print(f"Wetware initialization error: {e}")
            return False
    
    def _initialize_ai(self) -> bool:
        """Initialize AI systems"""
        try:
            # Create Bio-inspired Neural Network
            self.neural_network = BioNeuralNetwork("thalos_main")
            
            # Build network architecture
            input_layer = self.neural_network.create_layer(10, "input")
            hidden1 = self.neural_network.create_layer(20, "hidden")
            hidden2 = self.neural_network.create_layer(15, "hidden")
            output_layer = self.neural_network.create_layer(5, "output")
            
            # Connect layers
            self.neural_network.connect_layers(input_layer, hidden1, 0.6)
            self.neural_network.connect_layers(hidden1, hidden2, 0.6)
            self.neural_network.connect_layers(hidden2, output_layer, 0.7)
            
            # Initialize Reinforcement Learner
            self.rl_agent = ReinforcementLearner(
                state_dim=10,
                action_dim=5,
                learning_rate=0.01
            )
            
            return True
            
        except Exception as e:
            print(f"AI initialization error: {e}")
            return False
    
    def _initialize_database(self, db_config: dict) -> bool:
        """Initialize database manager"""
        try:
            db_type = db_config.get('type', 'memory')
            self.db_manager = DatabaseManager(db_type=db_type, config=db_config)
            return True
        except Exception as e:
            print(f"Database initialization error: {e}")
            return False
    
    def run_cli(self, args: list) -> int:
        """
        Run CLI interface
        
        Args:
            args: Command line arguments
            
        Returns:
            Exit code
        """
        if not self.initialized:
            print("Error: System not initialized")
            return 1
        
        if args:
            result = self.cli.execute(args)
            print(result)
        else:
            print("\nNo command provided. Use --help for usage information.")
            result = self.cli.execute(['--help'])
            print(result)
        
        return 0
    
    def run_web_server(self, host: str = '0.0.0.0', port: int = 8000) -> int:
        """
        Run web server interface
        
        Args:
            host: Server host
            port: Server port
            
        Returns:
            Exit code
        """
        if not self.initialized:
            print("Error: System not initialized")
            return 1
        
        try:
            # Import web server
            from interfaces.web.web_server import app
            
            print(f"\n🌐 Starting Web Interface on http://{host}:{port}")
            print("   Matrix-style chatbot interface with bio-intelligence")
            print("   Press Ctrl+C to stop\n")
            
            app.run(host=host, port=port, debug=False)
            return 0
            
        except ImportError:
            print("Error: Flask not installed. Run: pip install flask")
            return 1
        except Exception as e:
            print(f"Error starting web server: {e}")
            return 1
    
    def get_system_status(self) -> dict:
        """Get comprehensive system status"""
        status = {
            "name": self.name,
            "version": self.version,
            "status": self.status,
            "initialized": self.initialized
        }
        
        if self.cis:
            status["cis"] = self.cis.status()
        
        if self.neural_network:
            status["neural_network"] = self.neural_network.get_network_stats()
        
        if self.rl_agent:
            status["reinforcement_learning"] = self.rl_agent.get_statistics()
        
        if self.life_support:
            status["life_support"] = self.life_support.get_status()
        
        if self.organoids:
            status["organoids"] = [org.get_status() for org in self.organoids]
        
        if self.mea:
            status["mea"] = self.mea.get_status()
        
        if self.db_manager:
            status["database"] = self.db_manager.get_statistics()
        
        return status
    
    def shutdown(self) -> bool:
        """Gracefully shutdown all systems"""
        print("\n🔄 Initiating system shutdown...")
        
        # Shutdown organoids
        if self.organoids:
            for organoid in self.organoids:
                organoid.shutdown()
        
        # Shutdown MEA
        if self.mea:
            self.mea.shutdown()
        
        # Shutdown Life Support
        if self.life_support:
            self.life_support.shutdown()
        
        # Shutdown CIS
        if self.cis:
            self.cis.shutdown()
        
        # Close database
        if self.db_manager:
            self.db_manager.close()
        
        self.status = "dormant"
        print("✓ System shutdown complete")
        return True


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Thalos Prime v3.0 - Synthetic Biological Intelligence'
    )
    
    parser.add_argument(
        'mode',
        nargs='?',
        default='cli',
        choices=['cli', 'web', 'status'],
        help='Operating mode (default: cli)'
    )
    
    parser.add_argument(
        '--host',
        default='0.0.0.0',
        help='Web server host (default: 0.0.0.0)'
    )
    
    parser.add_argument(
        '--port',
        type=int,
        default=8000,
        help='Web server port (default: 8000)'
    )
    
    parser.add_argument(
        '--no-wetware',
        action='store_true',
        help='Disable wetware components'
    )
    
    parser.add_argument(
        '--no-ai',
        action='store_true',
        help='Disable AI systems'
    )
    
    parser.add_argument(
        'command',
        nargs='*',
        help='Command for CLI mode'
    )
    
    args = parser.parse_args()
    
    # Initialize system
    thalos = ThalosPrime()
    
    config = {
        'enable_wetware': not args.no_wetware,
        'enable_ai': not args.no_ai,
        'enable_database': True
    }
    
    if not thalos.initialize(config):
        print("Failed to initialize system")
        return 1
    
    # Set up signal handlers
    def signal_handler(sig, frame):
        print("\n\nReceived interrupt signal...")
        thalos.shutdown()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Run requested mode
    try:
        if args.mode == 'web':
            return thalos.run_web_server(args.host, args.port)
        elif args.mode == 'status':
            import json
            status = thalos.get_system_status()
            print(json.dumps(status, indent=2))
            return 0
        else:  # cli
            return thalos.run_cli(args.command)
    finally:
        thalos.shutdown()


if __name__ == "__main__":
    sys.exit(main())
