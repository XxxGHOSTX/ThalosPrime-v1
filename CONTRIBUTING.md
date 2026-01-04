# Contributing to Thalos Prime

---

**© 2026 Tony Ray Macier III. All rights reserved.**

This document is part of Thalos Prime, an original proprietary software system. Unauthorized reproduction, modification, distribution, or use is strictly prohibited without express written permission.

**Thalos Prime™ is a proprietary system.**

---



Thank you for your interest in contributing to Thalos Prime! This document provides guidelines and instructions for contributing to the project.

## Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [Getting Started](#getting-started)
3. [Development Workflow](#development-workflow)
4. [Coding Standards](#coding-standards)
5. [Testing Requirements](#testing-requirements)
6. [Submitting Changes](#submitting-changes)
7. [Architecture Principles](#architecture-principles)

## Code of Conduct

- Be respectful and professional
- Focus on constructive feedback
- Follow deterministic design principles
- Maintain code quality standards

## Getting Started

### Prerequisites

- Python 3.12 or higher
- Git
- Basic understanding of the Thalos Prime architecture

### Setup Development Environment

```bash
# Clone repository
git clone https://github.com/XxxGHOSTX/ThalosPrime-v1.git
cd ThalosPrime-v1

# Run bootstrap
./create_thalos_bootstrap.sh

# Run tests to verify setup
python tests/unit/test_cis.py
python tests/integration/test_system.py
```

## Development Workflow

### Branch Structure

- `main`: Stable production code
- `develop`: Integration branch for features
- `feature/*`: New features (e.g., `feature/web-interface`)
- `bugfix/*`: Bug fixes
- `docs/*`: Documentation updates

### Creating a Feature Branch

```bash
# Update main branch
git checkout main
git pull origin main

# Create feature branch
git checkout -b feature/your-feature-name

# Make changes and commit
git add .
git commit -m "Add: your feature description"

# Push to remote
git push origin feature/your-feature-name
```

## Coding Standards

### Architecture Principles

1. **Determinism**: No randomness, timestamps in core logic
2. **Explicit Contracts**: Return True/False for success/failure
3. **Separation of Concerns**: CIS → Subsystems → Interfaces
4. **No Side Effects**: Pure functions where possible
5. **Testability**: All code must be testable in isolation

### Python Style Guide

- Follow PEP 8 conventions
- Use type hints for function signatures
- Write docstrings for all public methods
- Keep functions focused and small

#### Example

```python
def create(self, key: str, value: Any) -> bool:
    """
    Create a new entry in storage
    
    Args:
        key: Unique identifier for the data
        value: Data to store
        
    Returns:
        bool: True if creation successful, False if key already exists
    """
    if key in self.storage:
        return False
    self.storage[key] = value
    return True
```

### File Organization

```
src/
├── core/
│   ├── cis/          # Central Intelligence System
│   └── memory/       # Memory subsystem
├── codegen/          # Code generation
└── interfaces/
    ├── cli/          # Command-line interface
    └── api/          # REST API interface
```

## Testing Requirements

### Unit Tests

All new code must include unit tests:

```python
def test_new_feature():
    """Test description"""
    # Setup
    component = Component()
    
    # Execute
    result = component.new_feature()
    
    # Assert
    assert result is True
    print("✓ New feature test passed")
```

### Integration Tests

For features that span multiple components:

```python
def test_feature_integration():
    """Test feature across components"""
    cis = CIS()
    cis.boot()
    
    # Test integration
    memory = cis.get_memory()
    memory.create('test', 'value')
    
    assert memory.read('test') == 'value'
    print("✓ Integration test passed")
```

### Running Tests

```bash
# Run all unit tests
for test in tests/unit/*.py; do python "$test"; done

# Run integration tests
python tests/integration/test_system.py

# Test specific component
python tests/unit/test_memory.py
```

### Test Coverage

- Aim for 100% coverage of public APIs
- Test success paths
- Test failure paths
- Test edge cases

## Submitting Changes

### Pull Request Process

1. **Create Feature Branch**
   ```bash
   git checkout -b feature/your-feature
   ```

2. **Make Changes**
   - Follow coding standards
   - Add tests
   - Update documentation

3. **Run Tests**
   ```bash
   # All tests must pass
   for test in tests/unit/*.py; do python "$test" || exit 1; done
   python tests/integration/test_system.py
   ```

4. **Commit Changes**
   ```bash
   git add .
   git commit -m "Add: descriptive commit message"
   ```

5. **Push and Create PR**
   ```bash
   git push origin feature/your-feature
   # Create PR on GitHub
   ```

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] All unit tests pass
- [ ] All integration tests pass
- [ ] New tests added

## Checklist
- [ ] Code follows style guidelines
- [ ] Documentation updated
- [ ] Tests added/updated
- [ ] No breaking changes (or documented)
```

### Review Process

1. Automated CI/CD checks must pass
2. Code review by maintainer
3. Address feedback
4. Approval and merge

## Architecture Principles

### CIS (Central Intelligence System)

**Role**: Primary orchestrator

```python
# Good: CIS manages lifecycle
cis = CIS()
cis.boot()
memory = cis.get_memory()

# Bad: Direct instantiation bypasses CIS
memory = MemoryModule()  # Avoid
```

### Memory Subsystem

**Role**: Explicit CRUD operations

```python
# Good: Explicit operations
memory.create('key', 'value')  # Returns True/False
memory.read('key')             # Returns value or None
memory.update('key', 'new')    # Returns True/False
memory.delete('key')           # Returns True/False

# Bad: Implicit operations
memory['key'] = 'value'        # Avoid
```

### Code Generation

**Role**: Deterministic output

```python
# Good: Pure, deterministic
codegen.generate_class('User', ['save', 'load'])

# Bad: Non-deterministic
codegen.generate_class_with_timestamp('User')  # Avoid
```

### Interfaces

**Role**: Thin delegation layer

```python
# Good: Delegate to CIS
def execute(self, args):
    return self.cis.get_memory().read(args.key)

# Bad: Business logic in interface
def execute(self, args):
    # Complex validation logic
    # Data transformation
    # Business rules
```

## Documentation

### Code Documentation

- Add docstrings to all public methods
- Include type hints
- Provide usage examples

### User Documentation

Update relevant docs:
- `README.md`: User-facing features
- `ARCHITECTURE.md`: Technical design
- `DEPLOYMENT.md`: Deployment changes
- `ROADMAP.md`: Future plans

## Common Patterns

### Adding a New Subsystem

1. Create module in `src/`
2. Add initialization in `CIS.boot()`
3. Add accessor method in CIS
4. Write unit tests
5. Write integration tests
6. Update documentation

### Adding CLI Command

1. Add subparser in `CLI._create_parser()`
2. Add handler method
3. Delegate to CIS subsystem
4. Add tests
5. Update help text

### Adding API Endpoint

1. Add handler in `API.handle_request()`
2. Delegate to CIS subsystem
3. Return standardized response
4. Add tests
5. Document endpoint

## Resources

- [Architecture Documentation](ARCHITECTURE.md)
- [Deployment Guide](DEPLOYMENT.md)
- [Roadmap](ROADMAP.md)
- [Implementation Summary](IMPLEMENTATION_SUMMARY.md)

## Questions?

- Open an issue for questions
- Check existing issues for similar questions
- Review documentation thoroughly

---

**Thank you for contributing to Thalos Prime!**
