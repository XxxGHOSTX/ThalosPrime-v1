# Thalos Prime v1.0 - Architecture Documentation

---

**© 2026 Tony Ray Macier III. All rights reserved.**

This document is part of Thalos Prime, an original proprietary software system. Unauthorized reproduction, modification, distribution, or use is strictly prohibited without express written permission.

**Thalos Prime™ is a proprietary system.**

---



## System Overview

Thalos Prime is a deterministic system framework built on principles of explicit control, separation of concerns, and predictable behavior.

## Core Architecture Principles

### 1. Determinism
- **Predictable Behavior**: Same inputs always produce same outputs
- **Repeatable Outcomes**: Operations can be replayed with identical results  
- **State-Controlled Flow**: All state changes are explicit and traceable
- **No Randomness**: No timestamps, UUIDs, or random values in core logic

### 2. Authority Hierarchy

```
CIS (Central Intelligence System) - Primary Authority
├── Memory Subsystem - Data storage operations
├── CodeGen Subsystem - Code generation logic
└── Interface Layer - User interaction only
    ├── CLI - Command routing (no business logic)
    └── API - Protocol translation (no business logic)
```

### 3. Separation of Concerns

- **CIS**: System orchestration, lifecycle management, dependency ownership
- **Memory**: CRUD operations on in-memory key-value store
- **CodeGen**: Deterministic code generation from templates/specs
- **CLI/API**: Thin delegation layer with zero business logic

## Component Details

### CIS (Central Intelligence System)

**File**: `src/core/cis/controller.py`

**Responsibilities**:
- Initialize all subsystems in proper order
- Maintain system state
- Provide lifecycle hooks (boot, shutdown, status)
- Act as single source of truth
- Own all dependencies

**Key Methods**:
- `boot()` - Initialize all subsystems
- `shutdown()` - Clean shutdown of all subsystems
- `status()` - Get current system state
- `get_memory()`, `get_codegen()`, `get_cli()`, `get_api()` - Access subsystems

**Principles**:
- CIS owns all subsystem instances
- Interfaces access subsystems only through CIS
- No circular dependencies
- Top-down control flow

### Memory Subsystem

**File**: `src/core/memory/storage.py`

**Responsibilities**:
- Provide deterministic key-value storage
- Implement explicit CRUD semantics
- Maintain in-memory state

**Key Methods**:
- `create(key, value)` - Create new entry (fails if exists)
- `read(key)` - Read value (returns None if missing)
- `update(key, value)` - Update existing (fails if missing)
- `delete(key)` - Delete entry (fails if missing)
- `exists(key)` - Check existence
- `list_keys()` - List all keys
- `count()` - Get item count
- `clear()` - Clear all data

**Principles**:
- No implicit behavior or side effects
- No automatic timestamps or metadata
- Explicit success/failure return values
- No global state

### CodeGen Subsystem

**File**: `src/codegen/generator.py`

**Responsibilities**:
- Generate code deterministically
- Support template-based generation
- Provide structure generators (class, function)

**Key Methods**:
- `register_template(name, content)` - Register code template
- `generate(template_name, context)` - Generate from template
- `generate_class(name, methods)` - Generate class structure
- `generate_function(name, parameters)` - Generate function structure
- `list_templates()` - List registered templates (sorted)
- `get_history()`, `clear_history()` - Optional history tracking

**Principles**:
- Pure functions, stateless operation
- No randomness (no timestamps, no UUIDs)
- Same input → same output (deterministic)
- Testable in isolation without CIS
- History tracking is optional explicit state

### CLI Interface

**File**: `src/interfaces/cli/cli.py`

**Responsibilities**:
- Parse command-line arguments
- Route commands to CIS subsystems
- Format output for display
- **NO business logic**

**Key Commands**:
- `boot` - Boot the system
- `shutdown` - Shutdown the system
- `status` - Get system status
- `memory create|read|update|delete|list|count` - Memory operations
- `codegen class|function` - Code generation

**Principles**:
- Thin delegation layer only
- Uses argparse for command parsing
- All logic delegated to CIS subsystems
- No state ownership
- CLI instances are interchangeable

### API Interface

**File**: `src/interfaces/api/server.py`

**Responsibilities**:
- Provide REST HTTP endpoints
- Translate HTTP to CIS calls
- **NO business logic**
- **NO persistence assumptions**

**Key Endpoints**:
- `GET /health` - Health check (doesn't require CIS)
- `GET /status` - System status (delegates to CIS)
- `POST /boot` - Boot system
- `POST /shutdown` - Shutdown system
- `POST /memory` - Create memory entry
- `GET /memory/{key}` - Read memory entry
- `PUT /memory/{key}` - Update memory entry
- `DELETE /memory/{key}` - Delete memory entry
- `GET /memory` - List all keys
- `POST /codegen/class` - Generate class
- `POST /codegen/function` - Generate function

**Principles**:
- Stateless REST API
- Minimal surface area
- Protocol adapter only
- All logic delegated to CIS subsystems
- API instances are interchangeable

## Data Flow

### Command Execution Flow

```
User Input (CLI/API)
    ↓
Interface Layer (parse/validate)
    ↓
CIS (route to subsystem)
    ↓
Subsystem (execute operation)
    ↓
Return result
    ↓
Interface Layer (format output)
    ↓
User Output
```

### Lifecycle Flow

```
1. Create CIS instance
2. CIS.boot()
   - Initialize Memory
   - Initialize CodeGen
   - Initialize CLI
   - Initialize API
   - Set status to 'operational'
3. Use system through interfaces
4. CIS.shutdown()
   - Clear Memory
   - Clear CodeGen history
   - Clear references
   - Set status to 'shutdown'
```

## Testing Strategy

### Unit Tests
- Test each component in isolation
- Verify deterministic behavior
- Validate explicit contracts
- Ensure no side effects

**Test Files**:
- `tests/unit/test_cis.py` - CIS lifecycle and orchestration
- `tests/unit/test_memory.py` - Memory CRUD operations
- `tests/unit/test_codegen.py` - Code generation
- `tests/unit/test_cli.py` - CLI command routing
- `tests/unit/test_api.py` - API endpoint delegation

### Integration Tests
- Test full system lifecycle
- Verify component interactions
- Validate authority hierarchy
- Ensure CLI/API interoperability

**Test File**:
- `tests/integration/test_system.py` - Full system integration

## Design Patterns

### 1. Command Pattern
CLI and API use command pattern to route operations to CIS subsystems.

### 2. Facade Pattern
CIS acts as a facade providing unified interface to subsystems.

### 3. Delegation Pattern
Interfaces delegate all logic to CIS, maintaining no state.

### 4. Factory Pattern
CIS factory-creates all subsystems during boot.

## Extension Points

### Adding New Subsystems
1. Create subsystem module in `src/`
2. Add initialization in `CIS.boot()`
3. Add accessor method in CIS
4. Update interfaces to expose new functionality

### Adding New Interface Methods
1. Add command/endpoint in CLI/API
2. Delegate to existing CIS subsystems
3. NO business logic in interface

### Adding Code Templates
1. Register template with CodeGen
2. Use `generate()` method with context
3. Ensure deterministic output

## Governance Model

### Decision Ownership
- **CIS**: System-level decisions (boot, shutdown, coordination)
- **Subsystems**: Domain-specific decisions (memory ops, code gen)
- **Interfaces**: NO decisions (pure delegation)

### Execution Control
- All execution flows through CIS
- Interfaces cannot bypass CIS
- No hidden autonomous behavior

### State Management
- CIS owns system-level state
- Subsystems own domain state
- Interfaces own NO state

## Best Practices

1. **Always use CIS as entry point** for system operations
2. **Never put business logic in interfaces** - delegate to CIS
3. **Keep subsystems isolated** - testable without CIS
4. **Maintain deterministic behavior** - no random values
5. **Use explicit return values** - True/False for success/failure
6. **Document all state changes** - make them traceable
7. **Test in isolation** - unit test each component
8. **Test integration** - verify component interactions

## Troubleshooting

### System won't boot
- Check that CIS.boot() is called before operations
- Verify no circular import dependencies
- Check src directory is in Python path

### Interface operations fail
- Ensure system is booted (CIS.boot())
- Check CIS instance is passed to interface
- Verify subsystem initialization

### Determinism issues
- Check for timestamps in logic
- Verify no random number generation
- Ensure sorted outputs where order matters

### Memory operations fail
- Verify explicit CRUD semantics
- Check key existence before update/delete
- Use create() not update() for new keys

## Version Information

**Version**: 1.0  
**Release**: Initial Release  
**Status**: Stable

## References

- Main entry point: `src/main.py`
- Bootstrap script: `create_thalos_bootstrap.sh`
- Configuration: `config/thalos.conf`
- Tests: `tests/unit/` and `tests/integration/`
