"""
© 2026 Tony Ray Macier III. All rights reserved.

Thalos Prime is an original proprietary software system, including but not limited to
its source code, system architecture, internal logic descriptions, documentation,
interfaces, diagrams, and design materials.

Unauthorized reproduction, modification, distribution, public display, or use of
this software or its associated materials is strictly prohibited without the
express written permission of the copyright holder.

Thalos Prime™ is a proprietary system.
"""

"""
CIS (Primary Control Unit) - Central Information System

Acts as the system orchestrator:
- Initializes memory, codegen, interfaces
- Maintains system state
- Exposes lifecycle hooks (boot, shutdown, status)
- Enforces deterministic lifecycle: initialize -> validate -> operate -> reconcile -> checkpoint -> terminate
"""

from typing import Dict, Any, Optional
import sys
import os


class CIS:
    """
    Central Information System - System Orchestrator for Thalos Prime
    
    Responsibilities:
    - Initialize and manage core subsystems (memory, codegen, interfaces)
    - Maintain system state
    - Provide lifecycle hooks (initialize, validate, operate, reconcile, checkpoint, terminate)
    - Enforce deterministic execution
    """
    
    def __init__(self):
        """Initialize the CIS control unit"""
        self.memory = None
        self.codegen = None
        self.cli = None
        self.api = None
        self.system_state: Dict[str, Any] = {
            'status': 'created',
            'version': '1.0',
            'booted': False,
            'initialized': False,
            'validated': False
        }
        self._state_history: list = []
        
    def initialize(self) -> bool:
        """
        Initialize CIS - Lifecycle hook
        
        Allocates resources and verifies preconditions.
        
        Returns:
            bool: True if initialization successful
        """
        if self.system_state['initialized']:
            return True
            
        try:
            # Verify Python version
            if sys.version_info < (3, 8):
                raise RuntimeError("Python 3.8+ required")
                
            # Mark as initialized
            self.system_state['initialized'] = True
            self._log_state_transition('created', 'initialized', 'Preconditions verified')
            return True
        except Exception as e:
            self.system_state['status'] = 'error'
            self.system_state['error'] = str(e)
            return False
            
    def validate(self) -> bool:
        """
        Validate CIS configuration and dependencies - Lifecycle hook
        
        Blocks startup if configuration is invalid or dependencies are missing.
        
        Returns:
            bool: True if validation successful
        """
        if not self.system_state['initialized']:
            return False
            
        if self.system_state['validated']:
            return True
            
        try:
            # Verify required imports are available
            from core.memory.storage import MemoryModule
            from codegen.generator import CodeGenerator
            from interfaces.cli.cli import CLI
            from interfaces.api.server import API
            
            # Mark as validated
            self.system_state['validated'] = True
            self._log_state_transition('initialized', 'validated', 'Dependencies verified')
            return True
        except ImportError as e:
            self.system_state['status'] = 'error'
            self.system_state['error'] = f"Missing dependency: {e}"
            return False
    def boot(self) -> bool:
        """
        Boot the system - lifecycle hook
        
        Initializes all core subsystems in order:
        1. Initialize CIS
        2. Validate CIS
        3. Initialize Memory
        4. Initialize CodeGen
        5. Initialize Interfaces (CLI, API)
        
        Returns:
            bool: True if boot successful
        """
        if self.system_state['booted']:
            return False
            
        # Run initialization and validation first
        if not self.initialize():
            return False
        if not self.validate():
            return False
            
        # Get the src directory path
        src_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        if src_dir not in sys.path:
            sys.path.insert(0, src_dir)
        
        from core.memory.storage import MemoryModule
        from codegen.generator import CodeGenerator
        from interfaces.cli.cli import CLI
        from interfaces.api.server import API
        
        # Initialize subsystems
        self.memory = MemoryModule()
        self.codegen = CodeGenerator()
        self.cli = CLI(self)
        self.api = API(self)
        
        # Update state
        self.system_state['status'] = 'operational'
        self.system_state['booted'] = True
        self._log_state_transition('validated', 'operational', 'All subsystems initialized')
        
        return True
        
    def operate(self) -> Dict[str, Any]:
        """
        Perform CIS operations - Lifecycle hook
        
        Returns current system status and allows subsystems to operate.
        
        Returns:
            dict: Current operational status
        """
        if not self.system_state['booted']:
            return {'error': 'System not booted'}
            
        return self.status()
        
    def reconcile(self) -> bool:
        """
        Reconcile internal state - Lifecycle hook
        
        Corrects any internal inconsistencies detected.
        
        Returns:
            bool: True if reconciliation successful
        """
        if not self.system_state['booted']:
            return False
            
        # Check for inconsistencies
        inconsistencies = []
        
        # Verify subsystems are initialized if booted
        if self.system_state['booted']:
            if self.memory is None:
                inconsistencies.append('memory')
            if self.codegen is None:
                inconsistencies.append('codegen')
            if self.cli is None:
                inconsistencies.append('cli')
            if self.api is None:
                inconsistencies.append('api')
                
        if inconsistencies:
            # Attempt to re-initialize missing subsystems
            return self.boot()
            
        return True
        
    def checkpoint(self) -> Dict[str, Any]:
        """
        Checkpoint system state - Lifecycle hook
        
        Persists full deterministic state for recovery.
        
        Returns:
            dict: Serialized system state
        """
        state = {
            'version': self.system_state['version'],
            'status': self.system_state['status'],
            'booted': self.system_state['booted'],
            'initialized': self.system_state['initialized'],
            'validated': self.system_state['validated'],
            'subsystems': {
                'memory': self.memory is not None,
                'codegen': self.codegen is not None,
                'cli': self.cli is not None,
                'api': self.api is not None
            },
            'state_history': self._state_history
        }
        
        return state
        
    def terminate(self) -> bool:
        """
        Terminate system cleanly - Lifecycle hook
        
        Leaves system in restartable and coherent state.
        Alias for shutdown() for lifecycle compliance.
        
        Returns:
            bool: True if termination successful
        """
        return self.shutdown()
        
    def shutdown(self) -> bool:
        """
        Shutdown the system - lifecycle hook
        
        Cleanly shuts down all subsystems in reverse order.
        
        Returns:
            bool: True if shutdown successful
        """
        if not self.system_state['booted']:
            return False
            
        # Clear memory
        if self.memory:
            self.memory.clear()
            
        # Clear codegen history
        if self.codegen:
            self.codegen.clear_history()
            
        # Update state
        self.system_state['status'] = 'shutdown'
        self.system_state['booted'] = False
        
        # Clear references
        self.memory = None
        self.codegen = None
        self.cli = None
        self.api = None
        
        return True
        
    def status(self) -> Dict[str, Any]:
        """
        Get system status - lifecycle hook
        
        Returns:
            Dictionary containing current system status
        """
        return {
            'version': self.system_state['version'],
            'status': self.system_state['status'],
            'booted': self.system_state['booted'],
            'subsystems': {
                'memory': self.memory is not None,
                'codegen': self.codegen is not None,
                'cli': self.cli is not None,
                'api': self.api is not None
            }
        }
        
    def get_memory(self) -> Optional[Any]:
        """Get the memory subsystem"""
        return self.memory
        
    def get_codegen(self) -> Optional[Any]:
        """Get the codegen subsystem"""
        return self.codegen
        
    def get_cli(self) -> Optional[Any]:
        """Get the CLI subsystem"""
        return self.cli
        
    def get_api(self) -> Optional[Any]:
        """Get the API subsystem"""
        return self.api
        
    def _log_state_transition(self, from_state: str, to_state: str, reason: str) -> None:
        """
        Log state transition for observability.
        
        Args:
            from_state: Previous state
            to_state: New state
            reason: Reason for transition
        """
        transition = {
            'from': from_state,
            'to': to_state,
            'reason': reason,
            'timestamp': self._get_timestamp()
        }
        self._state_history.append(transition)
        
    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.utcnow().isoformat() + 'Z'
