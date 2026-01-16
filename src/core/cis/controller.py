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
"""

from typing import Dict, Any, Optional


class CIS:
    """
    Central Information System - System Orchestrator for Thalos Prime
    
    Responsibilities:
    - Initialize and manage core subsystems (memory, codegen, interfaces)
    - Maintain system state
    - Provide lifecycle hooks (boot, shutdown, status)
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
            'booted': False
        }
        
    def boot(self) -> bool:
        """
        Boot the system - lifecycle hook
        
        Initializes all core subsystems in order:
        1. Memory
        2. CodeGen
        3. Interfaces (CLI, API)
        
        Returns:
            bool: True if boot successful
        """
        if self.system_state['booted']:
            return False
            
        # Import modules using absolute imports
        import sys
        import os
        
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
        
        return True
        
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
