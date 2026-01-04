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
Command Line Interface for Thalos Prime

Thin interface layer:
- Delegates logic to CIS
- Uses argparse
- No business logic inside CLI
"""

import argparse
import sys
from typing import Optional, Any


class CLI:
    """
    Command Line Interface for Thalos Prime
    
    Principles:
    - Thin interface layer only
    - All business logic delegated to CIS
    - Uses argparse for command parsing
    - No business logic in CLI itself
    """
    
    def __init__(self, cis: Optional[Any] = None):
        """
        Initialize the CLI
        
        Args:
            cis: CIS instance to delegate to (optional, can be set later)
        """
        self.cis = cis
        self.parser = self._create_parser()
        
    def set_cis(self, cis: Any) -> None:
        """
        Set the CIS instance to delegate to
        
        Args:
            cis: CIS instance
        """
        self.cis = cis
        
    def _create_parser(self) -> argparse.ArgumentParser:
        """Create argument parser"""
        parser = argparse.ArgumentParser(
            prog='thalos',
            description='Thalos Prime v1.0 - Command Line Interface'
        )
        
        subparsers = parser.add_subparsers(dest='command', help='Available commands')
        
        # Boot command
        subparsers.add_parser('boot', help='Boot the system')
        
        # Shutdown command
        subparsers.add_parser('shutdown', help='Shutdown the system')
        
        # Status command
        subparsers.add_parser('status', help='Get system status')
        
        # Memory commands
        memory_parser = subparsers.add_parser('memory', help='Memory operations')
        memory_subparsers = memory_parser.add_subparsers(dest='memory_cmd')
        
        mem_create = memory_subparsers.add_parser('create', help='Create memory entry')
        mem_create.add_argument('key', help='Key name')
        mem_create.add_argument('value', help='Value to store')
        
        mem_read = memory_subparsers.add_parser('read', help='Read memory entry')
        mem_read.add_argument('key', help='Key name')
        
        mem_update = memory_subparsers.add_parser('update', help='Update memory entry')
        mem_update.add_argument('key', help='Key name')
        mem_update.add_argument('value', help='New value')
        
        mem_delete = memory_subparsers.add_parser('delete', help='Delete memory entry')
        mem_delete.add_argument('key', help='Key name')
        
        memory_subparsers.add_parser('list', help='List all keys')
        memory_subparsers.add_parser('count', help='Get count of stored items')
        
        # Codegen commands
        codegen_parser = subparsers.add_parser('codegen', help='Code generation')
        codegen_subparsers = codegen_parser.add_subparsers(dest='codegen_cmd')
        
        gen_class = codegen_subparsers.add_parser('class', help='Generate class')
        gen_class.add_argument('name', help='Class name')
        gen_class.add_argument('--methods', nargs='*', help='Method names')
        
        gen_func = codegen_subparsers.add_parser('function', help='Generate function')
        gen_func.add_argument('name', help='Function name')
        gen_func.add_argument('--params', nargs='*', help='Parameter names')
        
        return parser
        
    def execute(self, args: list = None) -> str:
        """
        Execute CLI command - delegates to CIS
        
        Args:
            args: Command line arguments (defaults to sys.argv[1:])
            
        Returns:
            Result message
        """
        if args is None:
            args = sys.argv[1:]
            
        if not args:
            return self.parser.format_help()
            
        parsed = self.parser.parse_args(args)
        
        if not self.cis:
            return "Error: CIS not initialized"
            
        # Delegate to CIS based on command
        if parsed.command == 'boot':
            result = self.cis.boot()
            return "System booted successfully" if result else "System already booted"
            
        elif parsed.command == 'shutdown':
            result = self.cis.shutdown()
            return "System shutdown successfully" if result else "System not booted"
            
        elif parsed.command == 'status':
            status = self.cis.status()
            return self._format_status(status)
            
        elif parsed.command == 'memory':
            return self._handle_memory_command(parsed)
            
        elif parsed.command == 'codegen':
            return self._handle_codegen_command(parsed)
            
        return "Unknown command"
        
    def _handle_memory_command(self, parsed: argparse.Namespace) -> str:
        """Delegate memory commands to CIS memory subsystem"""
        memory = self.cis.get_memory()
        if not memory:
            return "Error: Memory subsystem not initialized. Run 'boot' first."
            
        if parsed.memory_cmd == 'create':
            result = memory.create(parsed.key, parsed.value)
            return f"Created: {parsed.key}" if result else f"Key already exists: {parsed.key}"
            
        elif parsed.memory_cmd == 'read':
            value = memory.read(parsed.key)
            return f"{parsed.key}: {value}" if value is not None else f"Key not found: {parsed.key}"
            
        elif parsed.memory_cmd == 'update':
            result = memory.update(parsed.key, parsed.value)
            return f"Updated: {parsed.key}" if result else f"Key not found: {parsed.key}"
            
        elif parsed.memory_cmd == 'delete':
            result = memory.delete(parsed.key)
            return f"Deleted: {parsed.key}" if result else f"Key not found: {parsed.key}"
            
        elif parsed.memory_cmd == 'list':
            keys = memory.list_keys()
            return f"Keys: {', '.join(keys)}" if keys else "No keys stored"
            
        elif parsed.memory_cmd == 'count':
            count = memory.count()
            return f"Total items: {count}"
            
        return "Unknown memory command"
        
    def _handle_codegen_command(self, parsed: argparse.Namespace) -> str:
        """Delegate codegen commands to CIS codegen subsystem"""
        codegen = self.cis.get_codegen()
        if not codegen:
            return "Error: Codegen subsystem not initialized. Run 'boot' first."
            
        if parsed.codegen_cmd == 'class':
            methods = parsed.methods or ['__init__']
            code = codegen.generate_class(parsed.name, methods)
            return f"Generated class:\n{code}"
            
        elif parsed.codegen_cmd == 'function':
            params = parsed.params or []
            code = codegen.generate_function(parsed.name, params)
            return f"Generated function:\n{code}"
            
        return "Unknown codegen command"
        
    def _format_status(self, status: dict) -> str:
        """Format status dictionary for display"""
        lines = [
            "=== Thalos Prime System Status ===",
            f"Version: {status['version']}",
            f"Status: {status['status']}",
            f"Booted: {status['booted']}",
            "Subsystems:"
        ]
        for subsystem, active in status['subsystems'].items():
            lines.append(f"  {subsystem}: {'active' if active else 'inactive'}")
        return '\n'.join(lines)
