# Thalos Prime - Module Dependency Graph

## System Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                    User Interface Layer                  │
├─────────────────────────────────────────────────────────┤
│                                                           │
│  ┌─────────────┐              ┌─────────────┐          │
│  │     CLI     │              │     API     │          │
│  │  (thin)     │              │  (thin)     │          │
│  └──────┬──────┘              └──────┬──────┘          │
│         │                            │                  │
│         └────────────┬───────────────┘                  │
│                      │                                  │
└──────────────────────┼──────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│                  Orchestration Layer                     │
├─────────────────────────────────────────────────────────┤
│                                                           │
│              ┌─────────────────────┐                    │
│              │        CIS          │                    │
│              │  (orchestrator)     │                    │
│              │                     │                    │
│              │  - boot()           │                    │
│              │  - shutdown()       │                    │
│              │  - status()         │                    │
│              │  - get_memory()     │                    │
│              │  - get_codegen()    │                    │
│              │  - get_cli()        │                    │
│              │  - get_api()        │                    │
│              └──────────┬──────────┘                    │
│                         │                                │
└─────────────────────────┼────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│                   Subsystem Layer                        │
├─────────────────────────────────────────────────────────┤
│                                                           │
│  ┌────────────────┐              ┌─────────────────┐   │
│  │     Memory     │              │    CodeGen      │   │
│  │   Subsystem    │              │   Subsystem     │   │
│  │                │              │                 │   │
│  │  - create()    │              │  - generate()   │   │
│  │  - read()      │              │  - generate_    │   │
│  │  - update()    │              │    class()      │   │
│  │  - delete()    │              │  - generate_    │   │
│  │  - exists()    │              │    function()   │   │
│  │  - list_keys() │              │  - register_    │   │
│  │  - count()     │              │    template()   │   │
│  │  - clear()     │              │                 │   │
│  └────────────────┘              └─────────────────┘   │
│                                                           │
└───────────────────────────────────────────────────────────┘
```

## Detailed Dependency Map

### CIS (Central Intelligence System)

**Location**: `src/core/cis/controller.py`

**Dependencies**:
```
CIS
├── imports (during boot())
│   ├── core.memory.storage.MemoryModule
│   ├── codegen.generator.CodeGenerator
│   ├── interfaces.cli.cli.CLI
│   └── interfaces.api.server.API
└── manages
    ├── memory: MemoryModule instance
    ├── codegen: CodeGenerator instance
    ├── cli: CLI instance
    └── api: API instance
```

**Dependents**:
- CLI (receives CIS instance)
- API (receives CIS instance)
- Main entry point (creates and boots CIS)

### Memory Module

**Location**: `src/core/memory/storage.py`

**Dependencies**:
```
MemoryModule
├── Python stdlib: typing, Dict, Any, Optional
└── No external dependencies
```

**Dependents**:
- CIS (initializes during boot)
- CLI (accesses via CIS)
- API (accesses via CIS)

**Interface**:
```python
MemoryModule
├── create(key: str, value: Any) -> bool
├── read(key: str) -> Optional[Any]
├── update(key: str, value: Any) -> bool
├── delete(key: str) -> bool
├── exists(key: str) -> bool
├── list_keys() -> list
├── count() -> int
└── clear() -> None
```

### Code Generator

**Location**: `src/codegen/generator.py`

**Dependencies**:
```
CodeGenerator
├── Python stdlib: typing, Dict, Any, Optional
└── No external dependencies
```

**Dependents**:
- CIS (initializes during boot)
- CLI (accesses via CIS)
- API (accesses via CIS)

**Interface**:
```python
CodeGenerator
├── __init__(track_history: bool = False)
├── register_template(name: str, content: str) -> bool
├── generate(template_name: str, context: Dict) -> Optional[str]
├── generate_class(name: str, methods: list = None) -> str
├── generate_function(name: str, parameters: list = None) -> str
├── list_templates() -> list
├── get_history() -> list
└── clear_history() -> None
```

### CLI Interface

**Location**: `src/interfaces/cli/cli.py`

**Dependencies**:
```
CLI
├── Python stdlib: argparse, sys
├── CIS (passed during initialization)
└── Delegates to:
    ├── CIS.boot()
    ├── CIS.shutdown()
    ├── CIS.status()
    ├── CIS.get_memory() -> MemoryModule
    └── CIS.get_codegen() -> CodeGenerator
```

**Dependents**:
- Main entry point (creates with CIS)
- Users via command line

**Interface**:
```python
CLI
├── __init__(cis: Optional[CIS] = None)
├── set_cis(cis: CIS) -> None
├── execute(args: list = None) -> str
└── _create_parser() -> ArgumentParser
```

### API Interface

**Location**: `src/interfaces/api/server.py`

**Dependencies**:
```
API
├── Python stdlib: typing, Dict, Any, Optional, json
├── CIS (passed during initialization)
└── Delegates to:
    ├── CIS.boot()
    ├── CIS.shutdown()
    ├── CIS.status()
    ├── CIS.get_memory() -> MemoryModule
    └── CIS.get_codegen() -> CodeGenerator
```

**Dependents**:
- Main entry point (creates with CIS)
- External API clients

**Interface**:
```python
API
├── __init__(cis: Optional[CIS] = None)
├── set_cis(cis: CIS) -> None
└── handle_request(method: str, path: str, body: Optional[Dict]) -> Dict
```

## Data Flow Diagrams

### System Boot Sequence

```
1. main.py creates CIS
   └─> CIS.__init__()
       └─> sets status='created', booted=False

2. main.py calls CIS.boot()
   └─> CIS.boot()
       ├─> imports MemoryModule
       ├─> imports CodeGenerator
       ├─> imports CLI
       ├─> imports API
       ├─> instantiates all subsystems
       └─> sets status='operational', booted=True

3. main.py creates CLI(cis) and API(cis)
   └─> Interfaces receive CIS reference

4. System ready for operations
```

### Memory Operation Flow

```
User Command: "python src/main.py memory create key value"
   │
   ├─> main.py creates CIS and boots
   ├─> main.py creates CLI(cis)
   ├─> CLI.execute(['memory', 'create', 'key', 'value'])
   │   │
   │   ├─> CLI parses arguments (argparse)
   │   ├─> CLI calls _handle_memory_command()
   │   ├─> CLI.cis.get_memory() -> MemoryModule
   │   ├─> memory.create('key', 'value') -> bool
   │   └─> CLI formats response string
   │
   └─> main.py prints result
```

### Code Generation Flow

```
User Command: "python src/main.py codegen class MyClass --methods m1 m2"
   │
   ├─> main.py creates CIS and boots
   ├─> main.py creates CLI(cis)
   ├─> CLI.execute(['codegen', 'class', 'MyClass', '--methods', 'm1', 'm2'])
   │   │
   │   ├─> CLI parses arguments (argparse)
   │   ├─> CLI calls _handle_codegen_command()
   │   ├─> CLI.cis.get_codegen() -> CodeGenerator
   │   ├─> codegen.generate_class('MyClass', ['m1', 'm2']) -> str
   │   └─> CLI formats response string
   │
   └─> main.py prints generated code
```

### API Request Flow

```
API Request: POST /memory {"key": "k1", "value": "v1"}
   │
   ├─> API.handle_request('POST', '/memory', {...})
   │   │
   │   ├─> API identifies endpoint
   │   ├─> API calls _handle_memory_request()
   │   ├─> API.cis.get_memory() -> MemoryModule
   │   ├─> memory.create('k1', 'v1') -> bool
   │   └─> API formats response dict
   │
   └─> Returns: {'status': 'success', 'code': 200, 'data': {...}}
```

## Import Graph

```
main.py
├── imports core.cis.CIS
├── imports interfaces.cli.CLI
└── imports interfaces.api.API

core.cis.controller
├── dynamically imports (in boot()):
│   ├── core.memory.storage.MemoryModule
│   ├── codegen.generator.CodeGenerator
│   ├── interfaces.cli.cli.CLI
│   └── interfaces.api.server.API

core.memory.storage
└── (no internal imports)

codegen.generator
└── (no internal imports)

interfaces.cli.cli
├── imports argparse
└── imports sys

interfaces.api.server
├── imports typing
└── imports json
```

## Testing Dependencies

```
tests/unit/test_cis.py
└── imports core.cis.CIS

tests/unit/test_memory.py
└── imports core.memory.MemoryModule

tests/unit/test_codegen.py
└── imports codegen.CodeGenerator

tests/unit/test_cli.py
├── imports core.cis.CIS
└── imports interfaces.cli.CLI

tests/unit/test_api.py
├── imports core.cis.CIS
└── imports interfaces.api.API

tests/integration/test_system.py
├── imports core.cis.CIS
├── imports interfaces.cli.CLI
├── imports interfaces.api.API
└── imports codegen.CodeGenerator
```

## Module Isolation

### Independently Testable Modules

✅ **MemoryModule**: No dependencies, pure key-value storage
✅ **CodeGenerator**: No dependencies, stateless generation
⚠️ **CLI**: Requires CIS instance (can be mocked)
⚠️ **API**: Requires CIS instance (can be mocked)
❌ **CIS**: Orchestrator, depends on all subsystems

### Coupling Analysis

**Low Coupling**:
- MemoryModule (zero dependencies)
- CodeGenerator (zero dependencies)

**Medium Coupling**:
- CLI (depends on CIS, but thin delegation)
- API (depends on CIS, but thin delegation)

**High Coupling**:
- CIS (by design, orchestrator pattern)

## Future Module Additions

### Planned Modules (See ROADMAP.md)

```
thalos-prime/
├── modules/
│   ├── analytics/          # Telemetry & metrics
│   ├── persistence/        # Database layer
│   ├── monitoring/         # Health & performance
│   └── security/          # Auth & compliance
└── interfaces/
    └── web/               # Web UI
```

### Integration Points

New modules will integrate via:
1. CIS orchestration (add to boot sequence)
2. Interface exposure (CLI/API endpoints)
3. Event hooks (future: pub/sub pattern)

---

**Version**: 1.0  
**Last Updated**: 2026-01-02  
**Status**: Current Architecture
