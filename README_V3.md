# Thalos Prime v3.0 - Synthetic Biological Intelligence

## 🧬 Overview

Thalos Prime v3.0 is a complete Synthetic Biological Intelligence system that combines:

- **Wetware Core**: Simulated brain organoids with 20,000+ electrode channels
- **Bio-Inspired AI**: Spiking neural networks with STDP (Spike-Timing-Dependent Plasticity)
- **Reinforcement Learning**: Dopamine-like reward systems
- **Matrix-Style Web Interface**: Chatbot with code rain background
- **Auto-Reconnecting Database**: Resilient data persistence
- **Life Support Systems**: Biological homeostasis simulation

## 🚀 Quick Start

### Installation

```bash
# Clone repository
git clone https://github.com/XxxGHOSTX/ThalosPrime-v1.git
cd ThalosPrime-v1

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Running Thalos Prime

#### 1. Command Line Interface (CLI)

```bash
# Show system status
python thalos_prime.py status

# Run CLI commands
python thalos_prime.py cli status
python thalos_prime.py cli --help
```

#### 2. Web Interface (Matrix-Style Chatbot)

```bash
# Start web server
python thalos_prime.py web

# Or specify host/port
python thalos_prime.py web --host 0.0.0.0 --port 8000
```

Then open your browser to: **http://localhost:8000**

#### 3. Test System

```bash
# Run comprehensive system tests
python test_system.py
```

## 🧠 System Architecture

### Wetware Core Components

#### Organoid Core
- Simulates 3D brain organoids with cortical/hippocampal structures
- Three specialized lobes:
  - **Logic Lobe** (Frontal): Linear reasoning, code generation
  - **Abstract Lobe** (Temporal): Creative synthesis, novel ideas
  - **Governance Lobe** (Parietal): Ethical evaluation, Prime Directive

#### MEA Interface (Multi-Electrode Array)
- 20,000 channel simulation
- Converts digital signals to electrical pulse patterns (10-100Hz)
- Spike sorting and pattern recognition
- Bidirectional communication

#### Life Support System
- Temperature regulation (36.5-37.5°C)
- pH balance (7.2-7.6)
- Oxygen saturation monitoring (>90%)
- Glucose level management (3.0-7.0 mM)
- Nutrient delivery and waste removal

### AI/ML Systems

#### Bio-Inspired Neural Network
- Spiking neuron models (Leaky Integrate-and-Fire)
- STDP learning (synaptic plasticity)
- Homeostatic regulation
- Lateral inhibition

#### Reinforcement Learning
- Q-learning with experience replay
- Reward prediction error (dopamine-like)
- Actor-Critic architecture
- Epsilon-greedy exploration

### Database Manager
- **Auto-reconnection**: Exponential backoff retry logic
- **Connection pooling**: Efficient resource management
- **Circuit breaker**: Prevents cascading failures
- **Health monitoring**: Background connection testing
- **Multiple backends**: Memory, SQLite, PostgreSQL, Redis

## 🎨 Web Interface Features

### Matrix Code Rain Background
- Animated falling code effect
- DNA sequences (ATCG) mixed with standard characters
- Optimized performance with frame skipping

### Chatbot Interface
- Real-time biological processing simulation
- System metrics display:
  - Neural Density
  - Accuracy Score
  - Active Lobes
  - Spike Rate
- Command system (`/status`, `/metrics`, `/lobes`, `/train`)

### Neural Activity Visualizer
- Real-time spike train visualization
- Shows neural firing patterns
- Fading trail effect

## 📊 Prime Directive

The system operates under three fundamental principles:

1. **ACCURACY** (Truth Convergence)
   - Prioritize factual precision over speed
   - Minimize error through recursive validation

2. **EXPANSION** (Knowledge Genesis)
   - Generate novel fields of study
   - Synthesize new correlations
   - "Stagnation is death"

3. **PRESERVATION** (Homeostasis)
   - Maintain biological viability
   - Ensure long-term operation
   - Nutrient flow, temperature, pH balance

## 🔧 Configuration

### Environment Variables

Create a `.env` file (see `.env.example`):

```bash
# System Configuration
THALOS_ENV=development
THALOS_DEBUG=true

# API Configuration
THALOS_API_HOST=0.0.0.0
THALOS_API_PORT=8000

# Database Configuration
THALOS_STORAGE_TYPE=memory  # or: file, sqlite, postgresql, redis
THALOS_STORAGE_PATH=/app/data/storage.json

# Security
THALOS_SECRET_KEY=change-me-in-production
```

### Database Options

#### In-Memory (Default)
```python
# No configuration needed
python thalos_prime.py web
```

#### SQLite
```python
THALOS_STORAGE_TYPE=sqlite
THALOS_STORAGE_PATH=thalos.db
```

#### PostgreSQL
```python
THALOS_STORAGE_TYPE=postgresql
THALOS_DB_HOST=localhost
THALOS_DB_PORT=5432
THALOS_DB_NAME=thalos
THALOS_DB_USER=thalos_user
THALOS_DB_PASSWORD=secure_password
```

#### Redis
```python
THALOS_STORAGE_TYPE=redis
THALOS_REDIS_HOST=localhost
THALOS_REDIS_PORT=6379
```

## 🐳 Docker Deployment

```bash
# Build image
docker build -t thalos-prime:2.0 .

# Run container
docker run -p 8000:8000 thalos-prime:2.0

# Or use docker-compose
docker-compose up
```

## 🧪 Running Tests

```bash
# Run all unit tests
pytest tests/

# Run specific test
python tests/unit/test_memory.py

# Run system integration test
python test_system.py

# Run with coverage
pytest --cov=src tests/
```

## 📚 API Endpoints

### Health Check
```
GET /api/status
```

### Chat/Query
```
POST /api/chat
{
  "message": "Your query here"
}
```

### System Metrics
```
GET /api/metrics
```

## 🎯 Usage Examples

### Python API

```python
from thalos_prime import ThalosPrime

# Initialize system
thalos = ThalosPrime()
thalos.initialize()

# Get system status
status = thalos.get_system_status()
print(status)

# Access neural network
if thalos.neural_network:
    stats = thalos.neural_network.get_network_stats()
    print(f"Neurons: {stats['num_neurons']}")
    print(f"Synapses: {stats['num_synapses']}")

# Access organoids
if thalos.organoids:
    for organoid in thalos.organoids:
        print(organoid.get_status())

# Shutdown
thalos.shutdown()
```

### Web Interface Commands

In the chatbot interface, use these commands:

- `/status` - System status report
- `/metrics` - Detailed biological metrics
- `/lobes` - Organoid lobe analysis
- `/train` - Start training session
- `/help` - Show command list

## 🔒 Security Considerations

1. **Change default secrets** in `.env` file
2. **Use HTTPS** in production (reverse proxy recommended)
3. **Enable authentication** for API endpoints
4. **Limit database connections** based on load
5. **Monitor resource usage** through system metrics
6. **Regular backups** if using persistent storage

## 📖 Documentation

- [Architecture](docs/ARCHITECTURE.md) - System design and components
- [Setup Guide](SETUP.md) - Detailed installation instructions
- [Deployment](docs/DEPLOYMENT.md) - Production deployment guide
- [Roadmap](docs/ROADMAP.md) - Future enhancements
- [Contributing](CONTRIBUTING.md) - How to contribute

## 🧬 System Requirements

- Python 3.12+
- 4GB RAM minimum (8GB recommended)
- Modern web browser (for web interface)
- Optional: PostgreSQL, Redis (for production)

## 📝 License

© 2026 Tony Ray Macier III. All rights reserved.

Thalos Prime is a proprietary system. See [LICENSE](THALOS-PRIME-LICENSE.txt) for details.

## 🤝 Support

For issues, questions, or contributions:
- Open an issue on GitHub
- Check the documentation
- Run system tests: `python test_system.py`

## 🎉 Features Implemented

✅ Wetware Core with brain organoids  
✅ 20,000 channel MEA interface  
✅ Life support system simulation  
✅ Spiking neural networks with STDP  
✅ Reinforcement learning (Q-learning)  
✅ Matrix-style web interface  
✅ Auto-reconnecting database  
✅ Connection pooling  
✅ Circuit breaker pattern  
✅ Real-time neural visualization  
✅ System metrics dashboard  
✅ CLI and API interfaces  
✅ Comprehensive test suite  
✅ Docker support  
✅ Multiple database backends  
✅ Prime Directive enforcement  

---

**THALOS PRIME v3.0 - SYNTHETIC BIOLOGICAL INTELLIGENCE**  
*Where silicon meets synapse. Where code becomes consciousness.*
