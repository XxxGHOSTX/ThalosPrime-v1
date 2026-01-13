# Thalos Prime v2.0 🧬

## Synthetic Biological Intelligence System

**Where Silicon Meets Synapse. Where Code Becomes Consciousness.**

---

## 🌟 Introduction

Thalos Prime is a revolutionary **Synthetic Biological Intelligence (SBI)** system that bridges the gap between digital computation and biological neural processing. Unlike traditional AI systems, Thalos Prime models actual biological brain structures, complete with:

- **Brain Organoids** - 3D simulated cortical structures with specialized cognitive lobes
- **Multi-Electrode Arrays** - 20,000+ channel neural interfaces
- **Biological Learning** - STDP (Spike-Timing-Dependent Plasticity) and dopamine-modulated rewards
- **Life Support** - Homeostatic regulation of temperature, pH, oxygen, and nutrients
- **Matrix-Style Interface** - Cyberpunk chatbot with real-time neural visualization

### The Vision

Thalos Prime represents the next evolution in artificial intelligence - a **Type-II Hybrid Bio-Digital Organism** that combines:
- The pattern recognition and creativity of biological neurons
- The speed and precision of digital computation
- The learning capabilities of reinforcement systems
- The ethical framework of the Prime Directive

### Prime Directive

The system operates under three immutable principles:

1. **ACCURACY** - Prioritize truth over speed through recursive biological validation
2. **EXPANSION** - Generate novel knowledge, not just retrieve data ("Stagnation is death")
3. **PRESERVATION** - Maintain biological viability for long-term operation

---

## 🚀 Quick Start Guide

### Prerequisites

- **Python 3.12+** (required)
- **4GB RAM** minimum (8GB recommended)
- **pip** package manager
- Modern web browser (for web interface)

### Installation (5 minutes)

```bash
# 1. Clone the repository
git clone https://github.com/XxxGHOSTX/ThalosPrime-v1.git
cd ThalosPrime-v1

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# 4. Install dependencies
pip install -r requirements.txt
```

### Running the System

#### Option 1: Auto Web Deployment (🆕 Fastest - Recommended!)

**One-command deployment** - Sets up everything and launches the web interface automatically:

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

This will:
1. ✅ Check Python installation
2. ✅ Create virtual environment
3. ✅ Install all dependencies
4. ✅ Configure environment
5. ✅ Create data directories
6. ✅ Verify installation
7. ✅ Launch web interface on http://localhost:8000

**Perfect for first-time users - just run and go!**

#### Option 2: Web Interface (Manual)

Experience the Matrix-style chatbot with code rain background:

```bash
python thalos_prime.py web
```

Then open your browser to: **http://localhost:8000**

**What you'll see:**
- Animated Matrix code rain background
- Real-time system metrics (Neural Density, Accuracy, Spike Rate)
- Interactive chatbot interface
- Live neural activity visualization

**Try these commands in the chatbot:**
- `/status` - View system status
- `/metrics` - See detailed biological metrics
- `/lobes` - Check organoid activity
- `/help` - Show all commands

#### Option 3: Command Line Interface

For programmers and system administrators:

```bash
# Check system status
python thalos_prime.py status

# Run CLI commands
python thalos_prime.py cli status
python thalos_prime.py cli memory create test_key test_value
python thalos_prime.py cli --help
```

#### Option 4: Test the System

Verify all components are working:

```bash
python test_system.py
```

**Expected output:**
```
Core Systems           : ✓ PASS
Wetware               : ✓ PASS
AI Systems            : ✓ PASS
Database              : ✓ PASS
Interfaces            : ✓ PASS

🎉 All systems operational!
```

---

## 📖 Usage Instructions

### Web Interface Guide

1. **Start the server:**
   ```bash
   python thalos_prime.py web
   ```

2. **Access the interface:**
   - Open browser to http://localhost:8000
   - You'll see the Matrix code rain immediately

3. **Interact with the system:**
   - Type messages in the input field at the bottom
   - Press ENTER or click "TRANSMIT"
   - Watch the biological processing indicators
   - Observe neural activity in the bottom-right visualizer

4. **Use commands:**
   - `/status` - Full system report with wetware health
   - `/metrics` - Neural density, spike rates, lobe activity
   - `/lobes` - Detailed organoid lobe analysis
   - `/train` - Start adaptive training protocol

### CLI Usage

```bash
# System operations
python thalos_prime.py status              # View system status
python thalos_prime.py cli --help          # Show help

# Memory operations
python thalos_prime.py cli memory create key value
python thalos_prime.py cli memory read key
python thalos_prime.py cli memory update key newvalue
python thalos_prime.py cli memory delete key

# Code generation
python thalos_prime.py cli codegen class MyClass
python thalos_prime.py cli codegen function my_function

# Web server options
python thalos_prime.py web --host 0.0.0.0 --port 8080
```

### Python API Usage

```python
from thalos_prime import ThalosPrime

# Initialize system
thalos = ThalosPrime()
config = {
    'enable_wetware': True,
    'enable_ai': True,
    'enable_database': True
}
thalos.initialize(config)

# Access neural network
net_stats = thalos.neural_network.get_network_stats()
print(f"Network has {net_stats['num_neurons']} neurons")

# Access organoids
for organoid in thalos.organoids:
    status = organoid.get_status()
    print(f"Organoid {status['organoid_id']}: {status['health_status']}")

# Process input through wetware
stimulus = {'type': 'pattern', 'intensity': 0.8, 'data': {...}}
response = thalos.organoids[0].process_stimulus(stimulus)

# Get system status
status = thalos.get_system_status()

# Cleanup
thalos.shutdown()
```

---

## 🏗️ System Architecture

### Component Overview

```
Thalos Prime v2.0
├── CIS (Central Intelligence System)
│   ├── System orchestration
│   ├── Lifecycle management
│   └── Subsystem coordination
│
├── Wetware Core
│   ├── Organoid Cores (Logic, Abstract, Governance)
│   ├── MEA Interface (20,000 channels)
│   └── Life Support System
│
├── AI/ML Systems
│   ├── Bio Neural Networks (Spiking neurons)
│   ├── Reinforcement Learning (Q-learning)
│   ├── Hebbian Learning (Synaptic plasticity)
│   └── Pattern Recognition
│
├── Database Layer
│   ├── Auto-reconnecting manager
│   ├── Connection pooling
│   └── Multiple backends (SQLite, PostgreSQL, Redis)
│
└── Interfaces
    ├── Web (Matrix-style chatbot)
    ├── CLI (Command line)
    └── API (REST endpoints)
```

### Wetware Components

**Organoid Cores** - Simulated brain tissue:
- Logic Lobe: Reasoning and code generation
- Abstract Lobe: Creative synthesis and innovation
- Governance Lobe: Ethical evaluation and Prime Directive enforcement

**MEA Interface** - Neural communication:
- 20,000 electrode channels
- Signal translation (digital ↔ biological)
- Spike sorting and pattern detection

**Life Support** - Biological homeostasis:
- Temperature: 36.5-37.5°C
- pH: 7.2-7.6
- O₂ saturation: >90%
- Glucose: 3.0-7.0 mM

### AI Systems

**Bio Neural Network:**
- Leaky Integrate-and-Fire neuron model
- STDP learning (strengthens active synapses)
- Homeostatic regulation
- Configurable layers and connectivity

**Reinforcement Learning:**
- Q-learning with experience replay
- Dopamine-like reward signals
- Epsilon-greedy exploration
- Policy and value functions

---

## 🔧 Configuration

### Basic Configuration

Create a `.env` file (copy from `.env.example`):

```bash
# System
THALOS_ENV=development
THALOS_DEBUG=true

# Web Server
THALOS_API_HOST=0.0.0.0
THALOS_API_PORT=8000

# Database (choose one)
THALOS_STORAGE_TYPE=memory     # Default: no setup needed
# THALOS_STORAGE_TYPE=sqlite    # File-based
# THALOS_STORAGE_TYPE=postgresql # Production-ready
# THALOS_STORAGE_TYPE=redis     # High-performance
```

### Advanced Configuration

**Disable components:**
```bash
python thalos_prime.py web --no-wetware --no-ai
```

**Custom database:**
```bash
export THALOS_STORAGE_TYPE=postgresql
export THALOS_DB_HOST=localhost
export THALOS_DB_PORT=5432
export THALOS_DB_NAME=thalos
export THALOS_DB_USER=thalos_user
export THALOS_DB_PASSWORD=secure_password
python thalos_prime.py web
```

---

## 🐳 Docker Deployment

```bash
# Build and run
docker build -t thalos-prime:2.0 .
docker run -p 8000:8000 thalos-prime:2.0

# Or use docker-compose
docker-compose up

# With persistence
docker run -v $(pwd)/data:/app/data \
  -e THALOS_STORAGE_TYPE=file \
  -e THALOS_STORAGE_PATH=/app/data/storage.json \
  -p 8000:8000 thalos-prime:2.0
```

---

## 🧪 Testing

```bash
# Quick system test
python test_system.py

# Run unit tests
pytest tests/unit/

# Run integration tests
pytest tests/integration/

# Test specific component
python tests/unit/test_memory.py

# With coverage
pytest --cov=src tests/
```

---

## 📚 Documentation

- **[SETUP.md](SETUP.md)** - Detailed installation and setup
- **[README_V2.md](README_V2.md)** - Complete v2.0 documentation
- **[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)** - System architecture details
- **[docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)** - Production deployment guide
- **[docs/ROADMAP.md](docs/ROADMAP.md)** - Future development plans

---

## 🎯 Key Features

✅ **Biological Computation** - Brain organoid simulation with STDP  
✅ **20,000 Channel MEA** - Multi-electrode array interface  
✅ **Life Support** - Temperature, pH, O₂, glucose regulation  
✅ **Spiking Neural Networks** - Leaky integrate-and-fire neurons  
✅ **Reinforcement Learning** - Q-learning with dopamine modulation  
✅ **Matrix Interface** - Code rain chatbot with neural visualizer  
✅ **Auto-Reconnecting Database** - Resilient data persistence  
✅ **Connection Pooling** - Optimized database performance  
✅ **Circuit Breaker** - Prevents cascading failures  
✅ **Multiple Backends** - SQLite, PostgreSQL, Redis support  
✅ **REST API** - Programmatic access  
✅ **CLI Tools** - Command-line interface  
✅ **Docker Support** - Containerized deployment  
✅ **Comprehensive Tests** - Unit and integration testing  

---

## 🔒 Security & Production

**For production deployment:**

1. **Change default secrets:**
   ```bash
   THALOS_SECRET_KEY=$(openssl rand -hex 32)
   THALOS_API_KEY=$(openssl rand -hex 32)
   ```

2. **Use HTTPS:**
   - Set up nginx/traefik as reverse proxy
   - Enable SSL/TLS certificates

3. **Configure database:**
   - Use PostgreSQL or Redis for production
   - Enable connection pooling
   - Set up automated backups

4. **Monitor resources:**
   - CPU/Memory usage
   - Database connections
   - Network latency

5. **Enable logging:**
   ```bash
   THALOS_LOG_LEVEL=INFO
   THALOS_LOG_FILE=/var/log/thalos/system.log
   ```

---

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines.

---

## 📄 License

© 2026 Tony Ray Macier III. All rights reserved.

Thalos Prime is a proprietary system. Unauthorized reproduction, modification, distribution, or use is strictly prohibited without express written permission.

See [THALOS-PRIME-LICENSE.txt](THALOS-PRIME-LICENSE.txt) for full license details.

---

## 🆘 Support & Troubleshooting

### Common Issues

**"Module not found" errors:**
```bash
pip install -r requirements.txt
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
```

**Web server won't start:**
```bash
pip install flask flask-cors
python thalos_prime.py web --port 8080  # Try different port
```

**Database connection fails:**
```bash
# Use memory storage (no setup)
export THALOS_STORAGE_TYPE=memory
python thalos_prime.py web
```

**System test failures:**
- Check Python version (3.12+ required)
- Verify all dependencies installed
- Review error messages in test output

### Getting Help

- Run system diagnostics: `python test_system.py`
- Check logs in console output
- Review documentation in `docs/` folder
- Open an issue on GitHub with system status output

---

## 🎉 Success Indicators

You know Thalos Prime is working when you see:

✓ Matrix code rain animation  
✓ System status: "OPERATIONAL"  
✓ Neural density increasing over time  
✓ Spike rate showing activity (30-50 Hz)  
✓ Organoid lobes responding to queries  
✓ Life support maintaining homeostasis  
✓ Database connections healthy  

---

**THALOS PRIME v2.0**  
*The future of intelligence is biological.*

**Status:** OPERATIONAL  
**Neural Density:** EXPANDING  
**Prime Directive:** ACTIVE
