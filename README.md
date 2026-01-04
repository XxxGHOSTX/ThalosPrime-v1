# Thalos Prime v1.0

**System Nucleus** - Deterministic Foundational Architecture

---

**© 2026 Tony Ray Macier III. All rights reserved.**

Thalos Prime is an original proprietary software system, including but not limited to its source code, system architecture, internal logic descriptions, documentation, interfaces, diagrams, and design materials.

Unauthorized reproduction, modification, distribution, public display, or use of this software or its associated materials is strictly prohibited without the express written permission of the copyright holder.

**Thalos Prime™ is a proprietary system.**

See [THALOS-PRIME-LICENSE.txt](THALOS-PRIME-LICENSE.txt) for complete license terms.  
See [OWNERSHIP.md](OWNERSHIP.md) for ownership declaration.

---

Thalos Prime is a deterministic system framework providing predictable behavior, repeatable outcomes, and explicit control flow.

## Core Principles

- **Determinism**: Predictable, repeatable execution
- **Explicit Control**: No implicit behavior or hidden logic
- **Separation of Concerns**: Clear authority boundaries
- **Top-Down Control**: CIS → Subsystems → Interfaces
- **No Side Effects**: Pure, traceable operations

## Architecture

### CIS (Central Intelligence System)
**Primary Authority** - System governor and orchestration layer

- Lifecycle management (boot, shutdown, status)
- Dependency ownership and execution arbitration
- Single source of truth for system state
- Initializes and coordinates all subsystems

### Memory
**Storage Layer** - In-memory key-value store

- Explicit CRUD operations (Create, Read, Update, Delete)
- No implicit behavior or side effects
- Deterministic storage interface
- No global state

### Code Generation
**Transform Engine** - Deterministic code generation

- Pure functions, stateless generator
- Config-driven, reproducible output
- Isolated from CIS, testable independently
- No randomness

### Interfaces
**Thin Delegation Layer** - System access points

#### CLI (Command-Line Interface)
- Argument parsing with argparse
- Command routing to CIS
- No domain logic or state ownership
- Pure delegation model

#### API (REST Interface)
- Minimal HTTP endpoints
- Health, status, and control endpoints
- Stateless, no persistence assumptions
- Protocol adapter only

## Directory Structure

```
.
├── create_thalos_bootstrap.sh    # Bootstrap script (idempotent)
├── config/
│   └── thalos.conf               # System configuration
├── src/
│   ├── core/
│   │   ├── cis/                  # Central Intelligence System
│   │   │   └── controller.py     # System orchestrator
│   │   └── memory/               # Memory subsystem
│   │       └── storage.py        # In-memory storage
│   ├── codegen/                  # Code generation
│   │   └── generator.py          # Deterministic generator
│   ├── interfaces/
│   │   ├── cli/                  # Command-line interface
│   │   │   └── cli.py            # Thin CLI layer
│   │   └── api/                  # REST API
│   │       └── server.py         # Minimal REST surface
│   └── main.py                   # System entry point
├── tests/
│   ├── unit/                     # Unit tests (isolated)
│   └── integration/              # Integration tests
└── docs/                         # Documentation
```

## Quick Start

### Bootstrap

Run the bootstrap script to set up the directory structure:

```bash
chmod +x create_thalos_bootstrap.sh
./create_thalos_bootstrap.sh
```

### Usage

#### Command Line

```bash
# Get system status
python src/main.py status

# Memory operations
python src/main.py memory create mykey myvalue
python src/main.py memory read mykey
python src/main.py memory update mykey newvalue
python src/main.py memory delete mykey
python src/main.py memory list
python src/main.py memory count

# Code generation
python src/main.py codegen class MyClass --methods process validate
python src/main.py codegen function my_function --params arg1 arg2

# System control
python src/main.py boot
python src/main.py shutdown
```

#### Programmatic API

```python
from core.cis import CIS
from interfaces.api import API

# Create and boot CIS
cis = CIS()
cis.boot()

# Get status
status = cis.status()

# Access subsystems through CIS
memory = cis.get_memory()
memory.create('key', 'value')
value = memory.read('key')

codegen = cis.get_codegen()
code = codegen.generate_class('MyClass', ['method1', 'method2'])

# Use API interface
api = API(cis)
response = api.handle_request('GET', '/status')
response = api.handle_request('POST', '/memory', {'key': 'k1', 'value': 'v1'})
response = api.handle_request('GET', '/memory/k1')
```

## Testing

Run unit tests:

```bash
# Test CIS
python tests/unit/test_cis.py

# Test Memory
python tests/unit/test_memory.py

# Test CodeGen
python tests/unit/test_codegen.py

# Test CLI
python tests/unit/test_cli.py

# Test API
python tests/unit/test_api.py
```

## Governance Model

### Authority Hierarchy

```
CIS (Central Intelligence System)
 ├── Memory Subsystem
 ├── CodeGen Subsystem
 └── Interfaces
     ├── CLI (delegates to CIS)
     └── API (delegates to CIS)
```

### Decision Ownership

- **CIS**: System lifecycle, state management, subsystem coordination
- **Memory**: Data storage operations (CRUD)
- **CodeGen**: Code generation logic
- **Interfaces**: User interaction and protocol translation only

### No Interface Autonomy

Interfaces (CLI/API) have **no domain logic** and **no state ownership**. All business logic resides in CIS and subsystems. Interfaces are pure delegation layers.

## Design Patterns

### Explicit Contracts

All interfaces use explicit method signatures with clear inputs and outputs. No hidden state or side effects.

### Deterministic Execution

- No random number generation
- No timestamps in core logic
- Reproducible outputs for same inputs
- State changes are explicit and traceable

### Testability

- Each component testable in isolation
- CodeGen works without CIS
- Memory is independent
- Deterministic tests with predictable results

## Extensibility

The system is designed for controlled growth:

- **Stable Core**: CIS provides unchanging foundation
- **Composable Systems**: Add new subsystems via CIS
- **Interface Adapters**: Add new interfaces (GraphQL, gRPC, etc.)
- **Plugin Architecture**: Extend CodeGen with templates

## Inspection and Traceability

- All operations are explicit and traceable
- Status endpoint provides system visibility
- No hidden behavior or implicit state changes
- Mechanical transparency for debugging

## Version

**1.0** - Initial Release

## License

See project repository for license information.