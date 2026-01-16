# Thalos Prime - API Reference

**Version:** 1.0.0  
**Copyright © 2026 Tony Ray Macier III. All rights reserved.**

---

## Table of Contents

1. [Core System API](#core-system-api)
2. [Memory API](#memory-api)
3. [Code Generation API](#code-generation-api)
4. [CLI API](#cli-api)
5. [REST API](#rest-api)
6. [Configuration API](#configuration-api)
7. [Logging API](#logging-api)
8. [Utilities API](#utilities-api)

---

## Core System API

### CIS (Central Intelligence System)

The primary system orchestrator. All subsystems are owned and managed by CIS.

#### Class: `CIS`

**Location:** `src/core/cis/controller.py`

**Lifecycle Methods (Required):**

```python
def __init__() -> None
    """Initialize CIS control unit"""

def initialize() -> bool
    """
    Initialize CIS - allocate resources, verify preconditions
    Returns: True if successful
    """

def validate() -> bool
    """
    Validate configuration and dependencies
    Blocks startup if invalid
    Returns: True if valid
    """

def boot() -> bool
    """
    Boot system - initialize all subsystems
    Returns: True if successful
    """

def operate() -> Dict[str, Any]
    """
    Perform operations - return current status
    Returns: Operational status dictionary
    """

def reconcile() -> bool
    """
    Reconcile internal state - fix inconsistencies
    Returns: True if successful
    """

def checkpoint() -> Dict[str, Any]
    """
    Checkpoint state - persist for recovery
    Returns: Serialized state dictionary
    """

def terminate() -> bool
    """
    Terminate cleanly - leave system restartable
    Returns: True if successful
    """
```

**Subsystem Access Methods:**

```python
def get_memory() -> Optional[MemoryModule]
    """Get CIS-owned memory subsystem"""

def get_codegen() -> Optional[CodeGenerator]
    """Get CIS-owned codegen subsystem"""

def get_cli() -> Optional[CLI]
    """Get CIS-owned CLI interface"""

def get_api() -> Optional[API]
    """Get CIS-owned REST API interface"""
```

**State Query Methods:**

```python
def status() -> Dict[str, Any]
    """
    Get system status
    
    Returns:
        {
            'version': str,
            'status': str,  # 'created', 'operational', 'error'
            'booted': bool,
            'subsystems': {
                'memory': bool,
                'codegen': bool,
                'cli': bool,
                'api': bool
            }
        }
    """

def shutdown() -> bool
    """
    Shutdown system cleanly
    Returns: True if successful
    """
```

**Example Usage:**

```python
from src.core.cis import CIS

# Create and boot
cis = CIS()
if cis.boot():
    # Access subsystems
    memory = cis.get_memory()
    
    # Check status
    status = cis.status()
    
    # Checkpoint
    state = cis.checkpoint()
    
    # Cleanup
    cis.shutdown()
```

---

## Memory API

### MemoryModule

Key-value storage with persistence support.

**Location:** `src/core/memory/storage.py`

#### Methods:

```python
def store(key: str, value: Any) -> None
    """
    Store value with key
    
    Args:
        key: Storage key
        value: Value to store
        
    Raises:
        KeyExistsError: If key already exists
    """

def retrieve(key: str) -> Any
    """
    Retrieve value by key
    
    Args:
        key: Storage key
        
    Returns:
        Stored value
        
    Raises:
        KeyNotFoundError: If key not found
    """

def update(key: str, value: Any) -> None
    """
    Update existing key
    
    Args:
        key: Storage key
        value: New value
        
    Raises:
        KeyNotFoundError: If key not found
    """

def delete(key: str) -> None
    """
    Delete key
    
    Args:
        key: Storage key
        
    Raises:
        KeyNotFoundError: If key not found
    """

def list_keys() -> List[str]
    """
    List all keys
    
    Returns:
        List of key names
    """

def exists(key: str) -> bool
    """
    Check if key exists
    
    Args:
        key: Storage key
        
    Returns:
        True if key exists
    """

def clear() -> None
    """Clear all stored data"""
```

**Example Usage:**

```python
memory = cis.get_memory()

# Store data
memory.store("user_name", "Alice")
memory.store("count", 42)

# Retrieve data
name = memory.retrieve("user_name")  # "Alice"

# Update
memory.update("count", 43)

# Check existence
if memory.exists("user_name"):
    print("User found")

# List keys
keys = memory.list_keys()

# Delete
memory.delete("count")
```

---

## Code Generation API

### CodeGenerator

Generate Python code from templates.

**Location:** `src/codegen/generator.py`

#### Methods:

```python
def generate_class(name: str, methods: List[str] = None,
                   attributes: List[str] = None) -> str
    """
    Generate Python class
    
    Args:
        name: Class name
        methods: List of method names
        attributes: List of attribute names
        
    Returns:
        Generated Python code
        
    Raises:
        ValidationError: If name is invalid
    """

def generate_function(name: str, parameters: List[str] = None,
                     return_type: str = None) -> str
    """
    Generate Python function
    
    Args:
        name: Function name
        parameters: List of parameter names
        return_type: Return type annotation
        
    Returns:
        Generated Python code
    """

def clear_history() -> None
    """Clear generation history"""
```

**Example Usage:**

```python
codegen = cis.get_codegen()

# Generate class
code = codegen.generate_class(
    name="UserManager",
    methods=["create", "read", "update", "delete"],
    attributes=["users", "database"]
)

# Generate function
func_code = codegen.generate_function(
    name="calculate_total",
    parameters=["items", "tax_rate"],
    return_type="float"
)
```

---

## CLI API

### CLI Interface

Command-line interface for system interaction.

**Location:** `src/interfaces/cli/cli.py`

#### Methods:

```python
def execute(args: List[str]) -> str
    """
    Execute CLI command
    
    Args:
        args: Command arguments
        
    Returns:
        Command output
    """
```

**Available Commands:**

```bash
# System commands
status                    # Show system status
boot                      # Boot system
shutdown                  # Shutdown system

# Memory commands
memory create <key> <value>   # Create entry
memory read <key>             # Read entry
memory update <key> <value>   # Update entry
memory delete <key>           # Delete entry
memory list                   # List all keys

# Codegen commands
codegen class <name> --methods <m1> <m2>
codegen function <name> --params <p1> <p2>
```

**Example Usage:**

```python
cli = cis.get_cli()

# Execute command
result = cli.execute(['status'])
print(result)

result = cli.execute(['memory', 'create', 'key1', 'value1'])
```

---

## REST API

### API Endpoints

HTTP REST interface for remote access.

**Location:** `src/interfaces/api/server.py`

**Base URL:** `http://localhost:5000`

#### Endpoints:

**Health Check:**
```http
GET /health
```
Response:
```json
{"status": "healthy", "version": "1.0"}
```

**System Status:**
```http
GET /api/status
```
Response:
```json
{
    "version": "1.0",
    "status": "operational",
    "booted": true,
    "subsystems": {
        "memory": true,
        "codegen": true,
        "cli": true,
        "api": true
    }
}
```

**Memory Operations:**

Create:
```http
POST /api/memory
Content-Type: application/json

{
    "key": "user_id",
    "value": "12345"
}
```

Read:
```http
GET /api/memory/<key>
```

Update:
```http
PUT /api/memory/<key>
Content-Type: application/json

{
    "value": "new_value"
}
```

Delete:
```http
DELETE /api/memory/<key>
```

List:
```http
GET /api/memory
```

**Code Generation:**

Generate Class:
```http
POST /api/codegen/class
Content-Type: application/json

{
    "name": "MyClass",
    "methods": ["method1", "method2"],
    "attributes": ["attr1"]
}
```

Generate Function:
```http
POST /api/codegen/function
Content-Type: application/json

{
    "name": "my_function",
    "parameters": ["param1", "param2"],
    "return_type": "str"
}
```

---

## Configuration API

### ConfigManager

Configuration management with INI file support.

**Location:** `src/core/config.py`

#### Methods:

```python
def get(section: str, key: str, default: Any = None,
        type_cast: type = str) -> Any
    """
    Get configuration value
    
    Precedence: ENV > File > Defaults > Parameter
    
    Args:
        section: Config section
        key: Config key
        default: Default value
        type_cast: Type to cast to (str, int, float, bool)
        
    Returns:
        Configuration value
    """

def get_section(section: str) -> Dict[str, Any]
    """Get all values in section"""

def set(section: str, key: str, value: Any) -> None
    """Set configuration value"""

def save(config_path: Optional[str] = None) -> None
    """Save configuration to file"""

def validate() -> bool
    """
    Validate configuration
    
    Returns:
        True if valid
        
    Raises:
        ValidationError: If invalid
    """
```

**Example Usage:**

```python
from src.core.config import get_config, initialize_config

# Get global config
config = get_config()

# Get values
debug = config.get('system', 'debug', default=False, type_cast=bool)
log_level = config.get('system', 'log_level', default='INFO')

# Get section
memory_config = config.get_section('memory')

# Initialize with custom file
config = initialize_config('./my_config.ini')
```

---

## Logging API

### ThalosLogger

Singleton logger with structured logging.

**Location:** `src/core/logging.py`

#### Methods:

```python
def configure(level: str = 'INFO', log_file: Optional[str] = None,
             console: bool = True, format_string: Optional[str] = None) -> None
    """Configure logger settings"""

def debug(message: str, **kwargs) -> None
    """Log debug message"""

def info(message: str, **kwargs) -> None
    """Log info message"""

def warning(message: str, **kwargs) -> None
    """Log warning message"""

def error(message: str, **kwargs) -> None
    """Log error message"""

def critical(message: str, **kwargs) -> None
    """Log critical message"""

def exception(message: str, exc_info=True, **kwargs) -> None
    """Log exception with traceback"""

def log_lifecycle(subsystem: str, event: str, success: bool = True,
                 details: Optional[dict] = None) -> None
    """Log lifecycle event"""

def log_state_transition(subsystem: str, from_state: str,
                        to_state: str, reason: Optional[str] = None) -> None
    """Log state transition"""
```

**Example Usage:**

```python
from src.core.logging import get_logger, configure_logging

# Get logger
logger = get_logger()

# Configure
logger.configure(level='DEBUG', log_file='./logs/thalos.log')

# Log messages
logger.info("System starting")
logger.debug("Debug information")
logger.error("An error occurred")

# Log lifecycle
logger.log_lifecycle('CIS', 'boot', success=True)

# Log state transition
logger.log_state_transition('CIS', 'created', 'operational', 'Boot complete')
```

---

## Utilities API

### Result Type

Deterministic error handling without exceptions.

**Location:** `src/core/utils.py`

```python
# Create results
result = Result.ok(value)
result = Result.err("error message")

# Check status
if result.success:
    value = result.value

# Unwrap
value = result.unwrap_or(default_value)

# Map
new_result = result.map(lambda x: x * 2)
```

### Validators

```python
from src.core.utils import Validator

# Validate
result = Validator.is_not_empty("value", "field_name")
result = Validator.is_valid_identifier("my_var")
result = Validator.is_in_range(5, 0, 10)
result = Validator.is_positive(42)

if result.valid:
    print("Valid")
else:
    print(f"Errors: {result.errors}")
```

### State Management

```python
from src.core.utils import (
    serialize_state,
    deserialize_state,
    version_state,
    timestamp
)

# Serialize
state = {'key': 'value'}
json_str = serialize_state(state)

# Deserialize
state = deserialize_state(json_str)

# Version
versioned = version_state(state, version="1.0")

# Timestamp
ts = timestamp()
```

---

## Exception Hierarchy

**Location:** `src/core/exceptions.py`

```
ThalosError (base)
├── CISError
├── SubsystemError
│   ├── MemoryError
│   │   ├── KeyNotFoundError
│   │   └── KeyExistsError
│   └── CodeGenError
├── ValidationError
├── StateError
├── ConfigurationError
├── InitializationError
├── OperationError
├── InterfaceError
├── LifecycleError
├── ReconciliationError
└── CheckpointError
```

**Usage:**

```python
from src.core.exceptions import (
    ThalosError,
    CISError,
    MemoryError,
    KeyNotFoundError,
    ValidationError
)

try:
    memory.retrieve("nonexistent")
except KeyNotFoundError as e:
    print(f"Key not found: {e}")
except MemoryError as e:
    print(f"Memory error: {e}")
```

---

## Complete Example

```python
#!/usr/bin/env python3
"""
Complete Thalos Prime example showing proper CIS ownership pattern
"""

from src.core.cis import CIS
from src.core.logging import configure_logging
from src.core.config import initialize_config
from src.core.exceptions import ThalosError

def main():
    # Configure logging
    configure_logging(level='INFO', log_file='./logs/thalos.log')
    
    # Load configuration
    config = initialize_config('./config/thalos.ini')
    
    # Create and boot CIS
    cis = CIS()
    
    if not cis.boot():
        print("Boot failed")
        return 1
        
    try:
        # Access CIS-owned subsystems
        memory = cis.get_memory()
        codegen = cis.get_codegen()
        
        # Use memory
        memory.store("app_name", "Thalos Prime")
        memory.store("version", "1.0.0")
        
        # Use codegen
        code = codegen.generate_class(
            "DataProcessor",
            methods=["process", "validate", "export"]
        )
        print(code)
        
        # Check status
        status = cis.status()
        print(f"System: {status['status']}")
        
        # Checkpoint
        checkpoint = cis.checkpoint()
        print(f"State checkpointed: {len(checkpoint)} keys")
        
    except ThalosError as e:
        print(f"Error: {e}")
        return 1
        
    finally:
        # Always cleanup
        cis.shutdown()
        
    return 0

if __name__ == "__main__":
    exit(main())
```

---

**For more information, see:**
- [README.md](../README.md) - System overview and quick start
- [IMPLEMENTATION_SUMMARY.md](./IMPLEMENTATION_SUMMARY.md) - Implementation details
- [ARCHITECTURE.md](./ARCHITECTURE.md) - System architecture

**Copyright © 2026 Tony Ray Macier III. All rights reserved.**
