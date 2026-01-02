# Thalos Prime - Deployment Guide

## Overview

This guide covers various deployment methods for Thalos Prime v1.0, from local development to containerized production environments.

## Prerequisites

- Python 3.12 or higher
- Git
- Docker (for containerized deployment)
- Docker Compose (for orchestrated deployment)

## Deployment Methods

### 1. Local Development Deployment

#### Quick Start

```bash
# Clone repository
git clone https://github.com/XxxGHOSTX/ThalosPrime-v1.git
cd ThalosPrime-v1

# Run bootstrap script
chmod +x create_thalos_bootstrap.sh
./create_thalos_bootstrap.sh

# Run application
python src/main.py status
```

#### Testing

```bash
# Run all unit tests
for test in tests/unit/*.py; do python "$test"; done

# Run integration tests
python tests/integration/test_system.py

# Test CLI commands
python src/main.py --help
python src/main.py memory create test value
python src/main.py codegen class MyClass
```

### 2. Docker Deployment

#### Build Image

```bash
# Build Docker image
docker build -t thalos-prime:1.0 .

# Verify build
docker images | grep thalos-prime
```

#### Run Container

```bash
# Run with default command (help)
docker run --rm thalos-prime:1.0

# Run status command
docker run --rm thalos-prime:1.0 python src/main.py status

# Run interactive mode
docker run -it --rm thalos-prime:1.0 /bin/bash
```

#### With Volume Mounting

```bash
# Mount local directory for persistence
docker run --rm \
  -v $(pwd)/data:/app/data \
  thalos-prime:1.0 \
  python src/main.py status
```

### 3. Docker Compose Deployment

#### Start Services

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f thalos-prime

# Check health
docker-compose ps
```

#### Stop Services

```bash
# Stop services
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

### 4. Kubernetes Deployment (Future)

Coming in v1.2 - See ROADMAP.md

## Configuration

### Environment Variables

```bash
# Python path
export PYTHONPATH=/path/to/ThalosPrime-v1/src

# Environment (development/production)
export THALOS_ENV=development

# Log level (optional, future)
export THALOS_LOG_LEVEL=INFO
```

### Configuration File

Edit `config/thalos.conf`:

```ini
[system]
version=1.0
name=ThalosPrime

[cis]
enabled=true

[memory]
enabled=true

[interfaces]
cli_enabled=true
api_enabled=true

[codegen]
deterministic=true
```

## Health Checks

### Local Health Check

```bash
# Check system status
python src/main.py status

# Expected output:
# === Thalos Prime System Status ===
# Version: 1.0
# Status: operational
# Booted: True
# Subsystems: ...
```

### Docker Health Check

```bash
# Check container health
docker ps --filter name=thalos-prime --format "{{.Status}}"

# Manual health check
docker exec thalos-prime python -c "
import sys
sys.path.insert(0, '/app/src')
from core.cis import CIS
cis = CIS()
cis.boot()
print(cis.status())
"
```

## Monitoring

### Basic Monitoring

```bash
# Watch logs
tail -f logs/thalos.log  # (future)

# Monitor resource usage
docker stats thalos-prime
```

### Health Endpoint (API)

```python
from interfaces.api import API
from core.cis import CIS

cis = CIS()
cis.boot()
api = API(cis)

# Health check
response = api.handle_request('GET', '/health')
print(response)  # {'status': 'success', 'data': {'healthy': True, ...}}
```

## Troubleshooting

### Common Issues

#### Import Errors

```bash
# Ensure PYTHONPATH is set
export PYTHONPATH=/path/to/ThalosPrime-v1/src

# Or use absolute imports
cd ThalosPrime-v1
python -m src.main
```

#### Bootstrap Script Fails

```bash
# Make executable
chmod +x create_thalos_bootstrap.sh

# Check for errors
bash -x create_thalos_bootstrap.sh
```

#### Docker Build Fails

```bash
# Clean build
docker build --no-cache -t thalos-prime:1.0 .

# Check logs
docker build -t thalos-prime:1.0 . 2>&1 | tee build.log
```

#### Tests Fail

```bash
# Run specific test
python tests/unit/test_cis.py

# Check Python version
python --version  # Should be 3.12+
```

### Debug Mode

```bash
# Enable Python debug output
python -v src/main.py status

# Check module imports
python -c "import sys; sys.path.insert(0, 'src'); from core.cis import CIS; print('OK')"
```

## Production Deployment

### Best Practices

1. **Use Docker**: Containerize for consistency
2. **Set Resource Limits**: Configure memory/CPU limits
3. **Enable Health Checks**: Ensure auto-recovery
4. **Log to External Storage**: Mount log volumes
5. **Monitor Metrics**: Track system performance
6. **Backup Configuration**: Version control config files

### Resource Requirements

#### Minimum
- CPU: 1 core
- Memory: 512 MB
- Disk: 100 MB

#### Recommended
- CPU: 2 cores
- Memory: 1 GB
- Disk: 500 MB

### Security Considerations

1. **Run as Non-Root**: Use unprivileged user in container
2. **Read-Only Filesystem**: Mount only necessary volumes
3. **Network Isolation**: Use Docker networks
4. **Secrets Management**: Use environment variables or secrets manager
5. **Regular Updates**: Keep base images updated

## CI/CD Integration

### GitHub Actions

The repository includes CI/CD workflows in `.github/workflows/ci.yml`:

- Automated testing on push/PR
- Code quality checks
- Build verification
- Test report generation

### Manual Trigger

```bash
# Run CI locally (requires act)
act push

# Or use GitHub CLI
gh workflow run ci.yml
```

## Scaling (Future)

### Horizontal Scaling

Coming in v2.0 with Kubernetes support:

```bash
# Scale replicas
kubectl scale deployment thalos-prime --replicas=3

# Auto-scaling
kubectl autoscale deployment thalos-prime --min=2 --max=10 --cpu-percent=80
```

### Load Balancing

Future implementation will support:
- Multiple CIS instances
- Distributed memory layer
- API gateway

## Backup & Recovery

### Current (v1.0)

Data is in-memory only. No persistence required.

### Future (v2.0+)

```bash
# Backup data
docker exec thalos-prime tar czf /app/data/backup.tar.gz /app/data

# Restore data
docker cp thalos-prime:/app/data/backup.tar.gz .
tar xzf backup.tar.gz
```

## Next Steps

1. Review [ROADMAP.md](ROADMAP.md) for planned features
2. Check [ARCHITECTURE.md](ARCHITECTURE.md) for system design
3. Read [README.md](../README.md) for usage examples
4. Explore [tests/](../tests/) for validation examples

## Support

- **Issues**: GitHub Issues
- **Documentation**: `docs/` directory
- **Examples**: `tests/integration/test_system.py`

---

**Version**: 1.0  
**Last Updated**: 2026-01-02  
**Status**: Production Ready
