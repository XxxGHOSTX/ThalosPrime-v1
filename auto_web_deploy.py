#!/usr/bin/env python3
"""
© 2026 Tony Ray Macier III. All rights reserved.

Thalos Prime v2.0 - Automatic Web Deployment
One-click deployment directly to web interface
"""

import os
import sys
import subprocess
import platform
import time
import socket
from pathlib import Path


class Colors:
    """ANSI color codes for terminal output"""
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    RESET = '\033[0m'


def print_banner():
    """Print Thalos Prime Web Deployment banner"""
    print(f"\n{Colors.CYAN}{'='*70}")
    print(f"""
    ████████╗██╗  ██╗ █████╗ ██╗      ██████╗ ███████╗
    ╚══██╔══╝██║  ██║██╔══██╗██║     ██╔═══██╗██╔════╝
       ██║   ███████║███████║██║     ██║   ██║███████╗
       ██║   ██╔══██║██╔══██║██║     ██║   ██║╚════██║
       ██║   ██║  ██║██║  ██║███████╗╚██████╔╝███████║
       ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚══════╝
    
      SYNTHETIC BIOLOGICAL INTELLIGENCE v2.0
             AUTOMATIC WEB DEPLOYMENT
             
         Matrix-Style Chatbot Interface
          with Wetware Integration
    """)
    print(f"{'='*70}{Colors.RESET}\n")


def print_step(message):
    """Print step message"""
    print(f"{Colors.GREEN}[STEP]{Colors.RESET} {message}")


def print_info(message):
    """Print info message"""
    print(f"{Colors.BLUE}[INFO]{Colors.RESET} {message}")


def print_success(message):
    """Print success message"""
    print(f"{Colors.GREEN}✓ {Colors.BOLD}{message}{Colors.RESET}")


def print_warning(message):
    """Print warning message"""
    print(f"{Colors.YELLOW}[WARN]{Colors.RESET} {message}")


def print_error(message):
    """Print error message"""
    print(f"{Colors.RED}[ERROR]{Colors.RESET} {message}")


def check_port(port):
    """Check if port is available"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.bind(('', port))
        sock.close()
        return True
    except OSError:
        return False


def check_python():
    """Check Python version"""
    print_step("Checking Python installation...")
    
    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print_error(f"Python {version_str} detected. Python 3.8+ required.")
        sys.exit(1)
    else:
        print_success(f"Python {version_str} detected")


def setup_venv():
    """Create and activate virtual environment"""
    print_step("Setting up virtual environment...")
    
    venv_path = Path("venv")
    
    if not venv_path.exists():
        print_info("Creating virtual environment...")
        try:
            subprocess.run([sys.executable, "-m", "venv", "venv"], 
                         check=True, capture_output=True)
            print_success("Virtual environment created")
        except subprocess.CalledProcessError as e:
            print_error(f"Failed to create virtual environment: {e}")
            sys.exit(1)
    else:
        print_info("Virtual environment already exists")
    
    # Get python executable in venv
    if platform.system() == "Windows":
        python_exe = venv_path / "Scripts" / "python.exe"
    else:
        python_exe = venv_path / "bin" / "python"
    
    if not python_exe.exists():
        print_error("Could not find Python in virtual environment")
        sys.exit(1)
    
    print_success("Virtual environment ready")
    return str(python_exe)


def install_dependencies(python_exe):
    """Install required dependencies"""
    print_step("Installing dependencies...")
    
    requirements = Path("requirements.txt")
    if not requirements.exists():
        print_error("requirements.txt not found")
        sys.exit(1)
    
    print_info("Upgrading pip...")
    subprocess.run([python_exe, "-m", "pip", "install", "--upgrade", "pip"],
                   capture_output=True, check=True)
    
    print_info("Installing Python packages...")
    result = subprocess.run([python_exe, "-m", "pip", "install", "-r", "requirements.txt"],
                          capture_output=True, text=True)
    
    if result.returncode != 0:
        print_error("Failed to install dependencies")
        print(result.stderr)
        sys.exit(1)
    
    print_success("Dependencies installed")


def setup_env():
    """Setup environment configuration"""
    print_step("Setting up environment configuration...")
    
    env_file = Path(".env")
    env_example = Path(".env.example")
    
    if not env_file.exists() and env_example.exists():
        print_info("Creating .env file from template...")
        env_file.write_text(env_example.read_text())
        print_success(".env file created")
        print_warning("Using default configuration (you can customize .env later)")
    elif env_file.exists():
        print_info(".env file already exists")
    else:
        print_warning("No .env file found, using default configuration")


def create_data_directories():
    """Create necessary data directories"""
    print_step("Creating data directories...")
    
    directories = ['data', 'logs', 'data/storage']
    for dir_name in directories:
        dir_path = Path(dir_name)
        if not dir_path.exists():
            dir_path.mkdir(parents=True)
            print_info(f"Created {dir_name}/")
    
    print_success("Data directories ready")


def verify_installation(python_exe):
    """Verify the installation is complete"""
    print_step("Verifying installation...")
    
    # Check if main launcher exists
    if not Path("thalos_prime.py").exists():
        print_error("thalos_prime.py not found")
        return False
    
    # Check if web server exists
    web_server = Path("src/interfaces/web/web_server.py")
    if not web_server.exists():
        print_error("Web server not found")
        return False
    
    # Check critical dependencies
    print_info("Checking Flask installation...")
    result = subprocess.run([python_exe, "-c", "import flask"],
                          capture_output=True)
    if result.returncode != 0:
        print_error("Flask not installed properly")
        return False
    
    print_success("Installation verified")
    return True


def display_web_info(port=8000):
    """Display web interface information"""
    print(f"\n{Colors.PURPLE}{'='*70}")
    print(f"{Colors.CYAN}{Colors.BOLD}WEB INTERFACE READY{Colors.RESET}")
    print(f"{Colors.PURPLE}{'='*70}{Colors.RESET}\n")
    
    print(f"{Colors.GREEN}✓ Server Status:{Colors.RESET} Starting...")
    print(f"{Colors.GREEN}✓ Port:{Colors.RESET} {port}")
    print(f"{Colors.GREEN}✓ Local URL:{Colors.RESET} {Colors.CYAN}http://localhost:{port}{Colors.RESET}")
    print(f"{Colors.GREEN}✓ Network URL:{Colors.RESET} {Colors.CYAN}http://127.0.0.1:{port}{Colors.RESET}")
    print()
    
    print(f"{Colors.YELLOW}Features:{Colors.RESET}")
    print(f"  • Matrix-style code rain background (DNA sequences)")
    print(f"  • Real-time chatbot with NLP")
    print(f"  • Wetware biological processing (3 organoid lobes)")
    print(f"  • Neural activity visualization")
    print(f"  • System metrics dashboard")
    print(f"  • 20,000 channel MEA interface")
    print()
    
    print(f"{Colors.YELLOW}Capabilities:{Colors.RESET}")
    print(f"  • Natural language understanding (11 intent types)")
    print(f"  • Action execution (18 command types)")
    print(f"  • Knowledge base (7 domains, 40+ concepts)")
    print(f"  • Memory operations (CRUD)")
    print(f"  • Mathematical calculations")
    print(f"  • Code generation")
    print()
    
    print(f"{Colors.RED}To stop the server:{Colors.RESET} Press Ctrl+C")
    print(f"{Colors.PURPLE}{'='*70}{Colors.RESET}\n")


def launch_web_interface(python_exe, port=8000):
    """Launch the web interface"""
    print_step(f"Launching web interface on port {port}...")
    
    # Check if port is available
    if not check_port(port):
        print_warning(f"Port {port} is already in use")
        response = input(f"Try port 8080 instead? (y/n): ").strip().lower()
        if response == 'y':
            port = 8080
            if not check_port(port):
                print_error(f"Port {port} is also in use")
                sys.exit(1)
        else:
            sys.exit(1)
    
    display_web_info(port)
    
    # Set environment variable for port
    env = os.environ.copy()
    env['THALOS_PORT'] = str(port)
    env['FLASK_ENV'] = 'production'
    
    print_info("Starting Thalos Prime Web Server...")
    print_info("Initializing synthetic biological intelligence...")
    print()
    
    try:
        # Launch the web server
        subprocess.run([python_exe, "thalos_prime.py", "web"], env=env)
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Server stopped by user{Colors.RESET}")
    except Exception as e:
        print_error(f"Failed to start web server: {e}")
        sys.exit(1)


def main():
    """Main deployment function"""
    print_banner()
    
    print(f"{Colors.CYAN}Starting automatic web deployment...{Colors.RESET}\n")
    
    try:
        # Step 1: Check Python
        check_python()
        print()
        
        # Step 2: Setup virtual environment
        python_exe = setup_venv()
        print()
        
        # Step 3: Install dependencies
        install_dependencies(python_exe)
        print()
        
        # Step 4: Setup environment
        setup_env()
        print()
        
        # Step 5: Create data directories
        create_data_directories()
        print()
        
        # Step 6: Verify installation
        if not verify_installation(python_exe):
            print_error("Installation verification failed")
            sys.exit(1)
        print()
        
        # Step 7: Launch web interface
        print_success("Deployment complete! Launching web interface...")
        print()
        time.sleep(1)
        
        launch_web_interface(python_exe)
        
        print()
        print_success("Web deployment session ended")
        print()
        
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Deployment interrupted by user{Colors.RESET}")
        sys.exit(0)
    except Exception as e:
        print_error(f"Deployment failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
