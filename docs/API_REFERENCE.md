# Thalos Prime API Reference

**© 2026 Tony Ray Macier III. All rights reserved.**

Complete API documentation for Thalos Prime v1.5 - Synthetic Biological Intelligence System.

---

## Table of Contents

1. [Python API](#python-api)
2. [REST API](#rest-api)
3. [CLI Interface](#cli-interface)
4. [Chatbot Commands](#chatbot-commands)

---

## Python API

### Core System (CIS)

#### CIS Controller

```python
from core.cis.controller import CIS

# Initialize system
cis = CIS()

# Boot all subsystems
success = cis.boot()  # Returns: bool

# Get system status
status = cis.status()
# Returns: {
#     'version': str,
#     'status': str,
#     'booted': bool,
#     'subsystems': dict
# }

# Shutdown system
cis.shutdown()  # Returns: bool

# Access subsystems
memory = cis.get_memory()
codegen = cis.get_codegen()
cli = cis.get_cli()
api = cis.get_api()
```

#### System Orchestrator

```python
from core.cis.orchestrator import SystemOrchestrator, SubsystemProtocol

# Create orchestrator
orchestrator = SystemOrchestrator()

# Register subsystem
orchestrator.register_subsystem(
    name="my_subsystem",
    subsystem=my_subsystem_instance,
    depends_on=["dependency1", "dependency2"]
)

# Initialize all subsystems
orchestrator.initialize_all()

# Validate all subsystems
orchestrator.validate_all()

# Create checkpoint
orchestrator.checkpoint_all()

# Get system state
state = orchestrator.get_system_state()

# Monitor health
health = orchestrator.monitor_health()

# Terminate gracefully
orchestrator.terminate_all()
```

### Memory Systems

#### Basic Memory

```python
from core.memory.storage import MemoryModule

memory = MemoryModule()

# CRUD operations
memory.create(key="username", value="alice")
value = memory.read(key="username")  # Returns: "alice"
memory.update(key="username", value="bob")
memory.delete(key="username")

# List operations
keys = memory.list()  # Returns: dict of all entries
count = memory.count()  # Returns: int
exists = memory.exists(key="username")  # Returns: bool

# Clear all
memory.clear()
```

#### Advanced Memory

```python
from core.memory.advanced_memory import AdvancedMemorySystem

memory = AdvancedMemorySystem(storage_path="data/memory")

# Create with metadata
memory.create(
    key="user_profile",
    value={"name": "Alice", "role": "admin"},
    tags=["user", "admin"],
    related_keys=["user_settings", "user_logs"]
)

# Full-text search
results = memory.search(query="admin user", limit=10)
# Returns: [(key, value, score), ...]

# Find by tag
entries = memory.find_by_tag(tag="admin")

# Find related entries
related = memory.find_related(key="user_profile", depth=2)

# Get version history
history = memory.get_version_history(key="user_profile")

# Restore version
memory.restore_version(key="user_profile", version=2)

# Export as graph
graph = memory.export_graph()
# Returns: {'nodes': [...], 'edges': [...]}

# Get statistics
stats = memory.get_statistics()

# Optimize indexes
results = memory.optimize()
```

### Code Generation

```python
from codegen.generator import CodeGenerator

codegen = CodeGenerator()

# Generate code from template
code = codegen.generate(
    template_name="class",
    params={
        "name": "DataProcessor",
        "methods": ["process", "validate"]
    }
)

# List available templates
templates = codegen.list_templates()

# Get generation history
history = codegen.get_history()

# Clear history
codegen.clear_history()
```

### AI Modules

#### Neural Pathway Optimizer

```python
from ai.optimization.neural_optimizer import NeuralPathwayOptimizer

optimizer = NeuralPathwayOptimizer(
    learning_rate=0.01,
    prune_threshold=0.1
)

# Optimize entire network
results = optimizer.optimize_network(neural_network)
# Returns: {
#     'initial_connections': int,
#     'final_connections': int,
#     'pruned': int,
#     'consolidated': int,
#     'energy_saved': float
# }

# Optimize single synapse
new_weight = optimizer.optimize_synapse(synapse, activity=0.8)

# Get statistics
stats = optimizer.get_pathway_statistics()
metrics = optimizer.get_optimization_metrics()
```

#### Advanced Reasoning Engine

```python
from ai.reasoning.advanced_reasoning import AdvancedReasoningEngine

reasoning = AdvancedReasoningEngine()

# Add facts
reasoning.add_fact("sky is blue")
reasoning.add_fact("grass is green")

# Add rules
reasoning.add_rule(
    conditions=["it is raining", "sky is cloudy"],
    conclusion="use umbrella",
    confidence=0.95
)

# Forward chaining inference
new_facts = reasoning.forward_chain()

# Backward chaining (prove goal)
provable = reasoning.backward_chain(goal="use umbrella")

# Abductive reasoning (find explanations)
explanations = reasoning.abductive_reasoning(observation="wet ground")

# Causal inference
effects = reasoning.causal_inference(cause="rain", max_depth=3)

# Analogical reasoning
inferred = reasoning.analogical_reasoning(
    source="bird",
    target="airplane",
    mapping={"wings": "wings", "flies": "flies"}
)

# Query
answer = reasoning.query("why is the sky blue?")

# Get statistics
stats = reasoning.get_reasoning_statistics()
```

#### Predictive Analytics

```python
from ai.optimization.predictive_analytics import PredictiveAnalyticsEngine

analytics = PredictiveAnalyticsEngine(window_size=50)

# Add data points
analytics.add_data_point(series_name="temperature", value=72.5)
analytics.add_data_point(series_name="temperature", value=73.1)

# Predict future values
predictions = analytics.predict_next(series_name="temperature", steps=5)
# Returns: [
#     {
#         'value': float,
#         'lower_bound': float,
#         'upper_bound': float,
#         'confidence': float,
#         'step': int
#     },
#     ...
# ]

# Detect trend
trend = analytics.detect_trend(series_name="temperature")
# Returns: {
#     'trend': str,  # 'increasing', 'decreasing', 'stable'
#     'slope': float,
#     'strength': float,
#     'change_percent': float
# }

# Detect anomalies
anomalies = analytics.detect_anomalies(series_name="temperature", threshold=2.5)

# Forecast probability
probability = analytics.forecast_probability(
    series_name="temperature",
    target_value=80.0,
    horizon=10
)

# Analyze correlation
correlation = analytics.analyze_correlation("temperature", "humidity")

# Get summary
summary = analytics.get_analytics_summary()
```

### Utilities

#### Configuration

```python
from core.config import Config, get_config

# Load configuration
config = Config(config_file="config/thalos.ini")

# Get values with type conversion
name = config.get("system", "name", value_type=str)
port = config.get("server", "port", value_type=int, default=8000)
debug = config.get("system", "debug", value_type=bool, default=False)

# Validate required config
config.validate_required({
    "system": ["name", "version"],
    "server": ["port"]
})

# Get entire section
server_config = config.get_section("server")

# Global config instance
config = get_config()
```

#### Logging

```python
from core.logging import get_logger

logger = get_logger()

# Standard logging
logger.debug("Debug message")
logger.info("Info message")
logger.warning("Warning message")
logger.error("Error message")
logger.critical("Critical message")
logger.exception("Exception occurred")

# Lifecycle logging
logger.lifecycle(
    phase="initialize",
    subsystem="memory",
    status="success"
)

# State transition logging
logger.state_transition(
    subsystem="cis",
    from_state="initializing",
    to_state="operational"
)
```

#### Validators

```python
from core.utils import Validator, Result

# Validate inputs
username = Validator.not_empty("alice", field="username")
password = Validator.min_length("secret123", min_len=8, field="password")
age = Validator.in_range(25, min_val=0, max_val=150, field="age")
email = Validator.matches_pattern("user@example.com", r"^[\w\.-]+@[\w\.-]+\.\w+$")

# Use Result type for explicit error handling
result = Result.ok(42)
if result.is_ok():
    value = result.unwrap()

result = Result.fail("Operation failed")
if result.is_err():
    error = result.error()
```

---

## REST API

Base URL: `http://localhost:8000`

### Chat Endpoint

**POST** `/api/chat`

Unrestricted conversational AI with full system access.

**Request:**
```json
{
  "message": "execute code: print(2+2)"
}
```

**Response:**
```json
{
  "response": "Code executed successfully:\n4",
  "status": "success",
  "timestamp": "2026-01-16T22:30:00.000Z"
}
```

### System Status

**GET** `/api/status`

Get complete system status.

**Response:**
```json
{
  "cis": {
    "version": "1.5.0",
    "status": "operational",
    "booted": true,
    "subsystems": {
      "memory": true,
      "codegen": true,
      "cli": true,
      "api": true
    }
  },
  "memory_entries": 42,
  "system_health": "OPERATIONAL",
  "version": "1.5.0"
}
```

### Memory Operations

**GET** `/api/memory`

Get all memory entries.

**Response:**
```json
{
  "entries": {
    "key1": "value1",
    "key2": "value2"
  },
  "count": 2
}
```

### Code Execution

**POST** `/api/execute`

Execute arbitrary Python code (unrestricted).

**Request:**
```json
{
  "code": "result = 2 + 2\nprint(f'Result: {result}')"
}
```

**Response:**
```json
{
  "output": "Result: 4\n",
  "status": "success"
}
```

---

## CLI Interface

```bash
# Boot system
python src/main.py

# Get status
python src/main.py status

# Memory operations
python src/main.py memory create mykey myvalue
python src/main.py memory read mykey
python src/main.py memory update mykey newvalue
python src/main.py memory delete mykey
python src/main.py memory list

# Code generation
python src/main.py codegen class MyClass --methods process validate
python src/main.py codegen function my_function

# Help
python src/main.py --help
```

---

## Chatbot Commands

The immersive interface supports natural language commands:

### Code Execution
```
execute this code: print("Hello World")
run code: for i in range(5): print(i)
```

### System Commands
```
run command ls -la
shell: pwd
bash: echo "Hello"
```

### Memory Operations
```
remember username as Alice
store api_key as xyz123
recall username
get memory key
list all memory
```

### Code Generation
```
generate a Python class named DataProcessor
create a function called process_data
generate class MyClass with methods init and run
```

### Data Analysis
```
analyze system status
examine current state
show system metrics
```

### System Control
```
status
boot
restart
shutdown
```

### File Operations
```
read file config.txt
list files
```

### Questions
```
what are you?
how do you work?
what can you do?
```

---

## Error Handling

All APIs use consistent error responses:

```json
{
  "error": "Error message",
  "status": "error",
  "details": {}
}
```

Exceptions follow the hierarchy in `core.exceptions`:
- `ThalosError` - Base exception
- `CISError` - CIS-related errors
- `ValidationError` - Validation failures
- `StateError` - Invalid state transitions
- `LifecycleError` - Lifecycle violations

---

## Advanced Features

### Self-Healing
The system automatically recovers from failures:
- Automatic reconciliation
- Checkpoint restoration
- Subsystem reinitialization

### Lifecycle Management
All subsystems implement:
- `initialize()` - Setup and resource allocation
- `validate()` - State validation
- `operate()` - Core functionality
- `reconcile()` - Consistency restoration
- `checkpoint()` - State persistence
- `terminate()` - Graceful shutdown

### State Management
All state is:
- Observable via APIs
- Serializable to JSON
- Versioned with history
- Reconstructible from checkpoints

---

**For more information, visit the repository or contact the author.**

**Thalos Prime™ - Where Silicon Meets Synapse. Where Code Becomes Consciousness.**
