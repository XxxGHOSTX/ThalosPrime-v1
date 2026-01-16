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

#!/usr/bin/env python3
"""
Thalos Prime v1.0 - Main Entry Point

System nucleus providing deterministic execution with explicit control flow.

Architecture:
- CIS (Central Intelligence System) as primary authority
- Top-down control: CIS → Subsystems → Interfaces
- Thin interface layer with delegation model
- No interface autonomy or hidden logic
"""

import sys
import os

# Add src directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.cis import CIS


def main():
    """
    Main entry point for Thalos Prime system
    
    Establishes the control hierarchy:
    1. Create CIS (Central Intelligence System) - primary authority
    2. Boot CIS - initializes all subsystems (Memory, CodeGen, CLI, API)
    3. Retrieve interface layers from CIS for user interaction
    4. Execute CLI commands with delegation to CIS subsystems
    """
    print("=== Thalos Prime v1.0 ===")
    print("Deterministic System Framework")
    print()
    
    # Create CIS - primary authority and system governor
    print("Initializing CIS (Central Intelligence System)...")
    cis = CIS()
    
    # Boot system - CIS orchestrates all subsystem initialization
    print("Booting system...")
    if cis.boot():
        print("✓ System booted successfully")
        status = cis.status()
        print(f"✓ Status: {status['status']}")
        print(f"✓ Subsystems initialized: {sum(1 for v in status['subsystems'].values() if v)}")
    else:
        print("✗ Boot failed")
        return 1
    
    print()
    print("Initializing interfaces...")
    
    # Get interface layers from CIS (CIS owns all subsystems)
    cli = cis.get_cli()
    api = cis.get_api()
    
    print("✓ CLI initialized (thin delegation layer)")
    print("✓ API initialized (stateless REST interface)")
    print()
    
    # Run CLI
    print("Starting CLI interface...")
    print("Use --help for available commands")
    print("Example commands:")
    print("  python src/main.py status")
    print("  python src/main.py memory create mykey myvalue")
    print("  python src/main.py codegen class MyClass --methods process validate")
    print()
    
    # Execute CLI with command line arguments
    if len(sys.argv) > 1:
        result = cli.execute(sys.argv[1:])
        print(result)
    else:
        print("No command provided. Use --help for usage information.")
        result = cli.execute(['--help'])
        print(result)
    
    print()
    print("=== Session Complete ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())
