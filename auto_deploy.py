#!/usr/bin/env python3
"""
Thalos Prime v3.0 - Universal Auto Deploy Script
Cross-platform Python-based auto-deployment
Works on Windows, Linux, macOS without shell dependencies
"""

import os
import sys
import subprocess
import platform
import time
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
    """Print Thalos Prime banner"""
    print(f"\n{Colors.CYAN}{'='*70}")
    print(f"""
    ████████╗██╗  ██╗ █████╗ ██╗      ██████╗ ███████╗
    ╚══██╔══╝██║  ██║██╔══██╗██║     ██╔═══██╗██╔════╝
       ██║   ███████║███████║██║     ██║   ██║███████╗
       ██║   ██╔══██║██╔══██║██║     ██║   ██║╚════██║
       ██║   ██║  ██║██║  ██║███████╗╚██████╔╝███████║
       ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚══════╝
    
         SYNTHETIC BIOLOGICAL INTELLIGENCE v3.0
                AUTO DEPLOYMENT SYSTEM
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
    print(f"{Colors.GREEN}[SUCCESS]{Colors.RESET} {message}")


def print_warning(message):
    """Print warning message"""
    print(f"{Colors.YELLOW}[WARN]{Colors.RESET} {message}")


def print_error(message):
    """Print error message"""
    print(f"{Colors.RED}[ERROR]{Colors.RESET} {message}")


def check_python():
    """Check Python version"""
    print_step("Checking Python installation...")
    
    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"
    
    if version.major < 3 or (version.major == 3 and version.minor < 12):
        print_warning(f"Python {version_str} detected. Python 3.12+ recommended.")
        response = input("Continue anyway? (y/n): ").strip().lower()
        if response != 'y':
            sys.exit(1)
    else:
        print_success(f"Python {version_str} detected")


def setup_venv():
    """Create and activate virtual environment"""
    print_step("Setting up virtual environment...")
    
    venv_path = Path("venv")
    
    if not venv_path.exists():
        print_info("Creating virtual environment...")
        subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
        print_success("Virtual environment created")
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
        print_warning("requirements.txt not found")
        return
    
    print_info("Upgrading pip...")
    subprocess.run([python_exe, "-m", "pip", "install", "--upgrade", "pip", "-q"], 
                   check=True)
    
    print_info("Installing Python packages...")
    subprocess.run([python_exe, "-m", "pip", "install", "-r", "requirements.txt", "-q"],
                   check=True)
    
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
        print_warning("Remember to update .env with your settings")
    elif env_file.exists():
        print_info(".env file already exists")


def run_tests(python_exe):
    """Run system tests"""
    print_step("Running system tests...")
    
    test_file = Path("test_system.py")
    if test_file.exists():
        result = subprocess.run([python_exe, "test_system.py"])
        return result.returncode == 0
    else:
        print_warning("test_system.py not found")
        return True


def show_launch_menu():
    """Display launch options menu"""
    print(f"\n{Colors.PURPLE}{'='*70}")
    print(f"{Colors.RESET}                    {Colors.CYAN}LAUNCH OPTIONS{Colors.RESET}")
    print(f"{Colors.PURPLE}{'='*70}{Colors.RESET}\n")
    
    print(f"{Colors.GREEN}1){Colors.RESET} Web Interface (Matrix Chatbot) {Colors.YELLOW}[RECOMMENDED]{Colors.RESET}")
    print("   - Matrix code rain background")
    print("   - Interactive chatbot interface")
    print("   - Real-time neural visualization")
    print(f"   {Colors.CYAN}URL: http://localhost:8000{Colors.RESET}")
    print()
    
    print(f"{Colors.GREEN}2){Colors.RESET} Command Line Interface (CLI)")
    print("   - Terminal-based interaction")
    print("   - Direct system access")
    print()
    
    print(f"{Colors.GREEN}3){Colors.RESET} System Status")
    print("   - View comprehensive system status")
    print("   - Check all components")
    print()
    
    print(f"{Colors.GREEN}4){Colors.RESET} Run Tests")
    print("   - Verify system integrity")
    print("   - Test all components")
    print()
    
    print(f"{Colors.GREEN}5){Colors.RESET} Exit")
    print()


def launch_system(python_exe):
    """Launch system based on user choice"""
    while True:
        show_launch_menu()
        
        try:
            choice = input("Enter your choice (1-5): ").strip()
            
            if choice == '1':
                print_step("Launching Web Interface...")
                print_info("Starting server on http://localhost:8000")
                print_info("Press Ctrl+C to stop\n")
                subprocess.run([python_exe, "thalos_prime.py", "web"])
                break
                
            elif choice == '2':
                print_step("Launching CLI Interface...")
                subprocess.run([python_exe, "thalos_prime.py", "cli", "--help"])
                print()
                cli_cmd = input("Enter CLI command (or 'exit'): ").strip()
                if cli_cmd and cli_cmd != 'exit':
                    subprocess.run([python_exe, "thalos_prime.py", "cli"] + cli_cmd.split())
                
            elif choice == '3':
                print_step("Getting System Status...")
                subprocess.run([python_exe, "thalos_prime.py", "status"])
                input("\nPress Enter to continue...")
                
            elif choice == '4':
                run_tests(python_exe)
                input("\nPress Enter to continue...")
                
            elif choice == '5':
                print_info("Exiting...")
                break
                
            else:
                print_error("Invalid choice. Please select 1-5.")
                time.sleep(1)
                
        except KeyboardInterrupt:
            print("\n\nInterrupted by user")
            break
        except Exception as e:
            print_error(f"Error: {e}")
            time.sleep(2)


def main():
    """Main deployment function"""
    print_banner()
    
    print(f"{Colors.CYAN}Starting automatic deployment...{Colors.RESET}\n")
    
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
        
        # Step 5: Optional tests
        response = input("Run system tests before launch? (y/n): ").strip().lower()
        if response == 'y':
            run_tests(python_exe)
        print()
        
        print_success("Deployment complete!")
        print()
        
        # Step 6: Launch system
        launch_system(python_exe)
        
        print()
        print_success("Thalos Prime deployment finished")
        print()
        
    except KeyboardInterrupt:
        print("\n\nDeployment interrupted by user")
        sys.exit(1)
    except Exception as e:
        print_error(f"Deployment failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
