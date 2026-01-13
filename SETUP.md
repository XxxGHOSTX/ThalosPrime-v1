# Thalos Prime v2.0 - Setup and Installation Guide

## 🚀 Quick Start (Easiest Method)

### Auto Web Deployment (Recommended for New Users)

**One-command deployment** that handles everything:

**Linux/macOS:**
```bash
./auto_web_deploy.sh
```

**Windows:**
```bash
auto_web_deploy.bat
```

**Universal (all platforms):**
```bash
python auto_web_deploy.py
```

This script automatically:
1. ✅ Checks Python version (3.8+ required)
2. ✅ Creates virtual environment
3. ✅ Installs all dependencies
4. ✅ Sets up .env configuration
5. ✅ Creates data directories
6. ✅ Verifies installation
7. ✅ Launches web interface on http://localhost:8000

**Perfect for getting started in under 2 minutes!**

---

## Manual Installation

### 1. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment (Optional)

Copy the example environment file and customize it:

```bash
cp .env.example .env
# Edit .env with your preferred settings
```

### 4. Run Tests

```bash
# Run all unit tests
cd tests/unit
for test in *.py; do python "$test"; done

# Or use pytest if installed
pytest tests/
```

### 5. Run the Application

```bash
# Show help
python src/main.py --help

# Check system status
python src/main.py status

# Example commands
python src/main.py memory create mykey myvalue
python src/main.py codegen class MyClass --methods process validate
```

## Production Deployment

### Using Docker

Build and run using Docker:

```bash
# Build the image
docker build -t thalos-prime:1.0 .

# Run the container
docker run -it thalos-prime:1.0

# Or use docker-compose
docker-compose up
```

### Using Docker with Persistence

To enable data persistence across container restarts:

```bash
docker run -it -v $(pwd)/data:/app/data \
  -e THALOS_STORAGE_TYPE=file \
  -e THALOS_STORAGE_PATH=/app/data/storage.json \
  thalos-prime:1.0
```

## Configuration Options

### Memory Persistence

By default, the Memory Module uses in-memory storage (data is lost on restart). To enable persistence:

**Option 1: File-based Storage**
```python
from core.memory import MemoryModule

# Initialize with file persistence
memory = MemoryModule(persistence_path="/app/data/storage.json")
```

**Option 2: Environment Variable**
```bash
export THALOS_STORAGE_TYPE=file
export THALOS_STORAGE_PATH=/app/data/storage.json
```

### Production Web Server

For API deployment in production, update the Dockerfile CMD to use a production server:

**For WSGI applications (Flask):**
```dockerfile
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "src.interfaces.api.server:app"]
```

**For ASGI applications (FastAPI):**
```dockerfile
CMD ["uvicorn", "src.interfaces.api.server:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

## Security Considerations

1. **Change default secrets**: Update `THALOS_SECRET_KEY` and `THALOS_API_KEY` in `.env`
2. **Use environment variables**: Never commit `.env` files to version control
3. **Enable HTTPS**: Use a reverse proxy (nginx, traefik) with SSL/TLS in production
4. **Limit permissions**: Run containers with non-root users when possible

## Troubleshooting

### Bootstrap Script Not Executable

```bash
chmod +x create_thalos_bootstrap.sh
./create_thalos_bootstrap.sh
```

### Import Errors

Ensure PYTHONPATH is set:
```bash
export PYTHONPATH=/path/to/ThalosPrime-v1/src
```

### Persistence Issues

Check that the storage directory exists and has write permissions:
```bash
mkdir -p /app/data
chmod 755 /app/data
```

## Next Steps

1. Review the architecture documentation in `docs/ARCHITECTURE.md`
2. Check the roadmap in `docs/ROADMAP.md`
3. Read contributing guidelines in `CONTRIBUTING.md`
4. Explore the module dependencies in `docs/MODULE_DEPENDENCIES.md`
