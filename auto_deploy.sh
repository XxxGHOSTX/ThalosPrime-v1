#!/bin/bash
################################################################################
# Thalos Prime v3.0 - Auto Deploy & Launch Script
# 
# This script automatically sets up and runs Thalos Prime after extraction
# Works on Linux, macOS, and Windows (via Git Bash/WSL)
################################################################################

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Banner
print_banner() {
    echo -e "${CYAN}"
    echo "╔═══════════════════════════════════════════════════════════════════╗"
    echo "║                                                                   ║"
    echo "║   ████████╗██╗  ██╗ █████╗ ██╗      ██████╗ ███████╗            ║"
    echo "║   ╚══██╔══╝██║  ██║██╔══██╗██║     ██╔═══██╗██╔════╝            ║"
    echo "║      ██║   ███████║███████║██║     ██║   ██║███████╗            ║"
    echo "║      ██║   ██╔══██║██╔══██║██║     ██║   ██║╚════██║            ║"
    echo "║      ██║   ██║  ██║██║  ██║███████╗╚██████╔╝███████║            ║"
    echo "║      ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚══════╝            ║"
    echo "║                                                                   ║"
    echo "║              SYNTHETIC BIOLOGICAL INTELLIGENCE v3.0              ║"
    echo "║                    AUTO DEPLOYMENT SYSTEM                        ║"
    echo "║                                                                   ║"
    echo "╚═══════════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

# Check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Print step
print_step() {
    echo -e "${GREEN}[STEP]${NC} $1"
}

# Print info
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

# Print warning
print_warning() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

# Print error
print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Print success
print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

# Check Python version
check_python() {
    print_step "Checking Python installation..."
    
    if command_exists python3; then
        PYTHON_CMD="python3"
    elif command_exists python; then
        PYTHON_CMD="python"
    else
        print_error "Python not found! Please install Python 3.12 or higher."
        echo "Download from: https://www.python.org/downloads/"
        exit 1
    fi
    
    # Check version
    PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | awk '{print $2}')
    PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
    PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)
    
    if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 12 ]); then
        print_warning "Python $PYTHON_VERSION detected. Python 3.12+ recommended."
        read -p "Continue anyway? (y/n) " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    else
        print_success "Python $PYTHON_VERSION detected"
    fi
}

# Create virtual environment
setup_venv() {
    print_step "Setting up virtual environment..."
    
    if [ ! -d "venv" ]; then
        print_info "Creating virtual environment..."
        $PYTHON_CMD -m venv venv
        print_success "Virtual environment created"
    else
        print_info "Virtual environment already exists"
    fi
    
    # Activate virtual environment
    if [ -f "venv/bin/activate" ]; then
        source venv/bin/activate
    elif [ -f "venv/Scripts/activate" ]; then
        source venv/Scripts/activate
    else
        print_error "Could not find activation script"
        exit 1
    fi
    
    print_success "Virtual environment activated"
}

# Install dependencies
install_dependencies() {
    print_step "Installing dependencies..."
    
    if [ -f "requirements.txt" ]; then
        print_info "Installing Python packages..."
        pip install --upgrade pip -q
        pip install -r requirements.txt -q
        print_success "Dependencies installed"
    else
        print_warning "requirements.txt not found"
    fi
}

# Run system test
run_tests() {
    print_step "Running system tests..."
    
    if [ -f "test_system.py" ]; then
        $PYTHON_CMD test_system.py
    else
        print_warning "test_system.py not found, skipping tests"
    fi
}

# Create .env from example
setup_env() {
    print_step "Setting up environment configuration..."
    
    if [ ! -f ".env" ] && [ -f ".env.example" ]; then
        print_info "Creating .env file from template..."
        cp .env.example .env
        print_success ".env file created"
        print_warning "Remember to update .env with your settings"
    elif [ -f ".env" ]; then
        print_info ".env file already exists"
    fi
}

# Display launch options
show_launch_menu() {
    echo ""
    echo -e "${PURPLE}╔═══════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${PURPLE}║${NC}                    ${CYAN}LAUNCH OPTIONS${NC}                               ${PURPLE}║${NC}"
    echo -e "${PURPLE}╚═══════════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "${GREEN}1)${NC} Web Interface (Matrix Chatbot) ${YELLOW}[RECOMMENDED]${NC}"
    echo -e "   - Matrix code rain background"
    echo -e "   - Interactive chatbot interface"
    echo -e "   - Real-time neural visualization"
    echo -e "   ${CYAN}URL: http://localhost:8000${NC}"
    echo ""
    echo -e "${GREEN}2)${NC} Command Line Interface (CLI)"
    echo -e "   - Terminal-based interaction"
    echo -e "   - Direct system access"
    echo ""
    echo -e "${GREEN}3)${NC} System Status"
    echo -e "   - View comprehensive system status"
    echo -e "   - Check all components"
    echo ""
    echo -e "${GREEN}4)${NC} Run Tests"
    echo -e "   - Verify system integrity"
    echo -e "   - Test all components"
    echo ""
    echo -e "${GREEN}5)${NC} Exit"
    echo ""
}

# Launch based on choice
launch_system() {
    while true; do
        show_launch_menu
        read -p "Enter your choice (1-5): " choice
        
        case $choice in
            1)
                print_step "Launching Web Interface..."
                print_info "Starting server on http://localhost:8000"
                print_info "Press Ctrl+C to stop"
                echo ""
                $PYTHON_CMD thalos_prime.py web
                break
                ;;
            2)
                print_step "Launching CLI Interface..."
                $PYTHON_CMD thalos_prime.py cli --help
                echo ""
                read -p "Enter CLI command (or 'exit'): " cli_cmd
                if [ "$cli_cmd" != "exit" ]; then
                    $PYTHON_CMD thalos_prime.py cli $cli_cmd
                fi
                ;;
            3)
                print_step "Getting System Status..."
                $PYTHON_CMD thalos_prime.py status
                read -p "Press Enter to continue..."
                ;;
            4)
                run_tests
                read -p "Press Enter to continue..."
                ;;
            5)
                print_info "Exiting..."
                break
                ;;
            *)
                print_error "Invalid choice. Please select 1-5."
                ;;
        esac
    done
}

# Main deployment flow
main() {
    print_banner
    
    echo -e "${CYAN}Starting automatic deployment...${NC}"
    echo ""
    
    # Step 1: Check Python
    check_python
    
    # Step 2: Setup virtual environment
    setup_venv
    
    # Step 3: Install dependencies
    install_dependencies
    
    # Step 4: Setup environment
    setup_env
    
    # Step 5: Run initial tests (optional)
    echo ""
    read -p "Run system tests before launch? (y/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        run_tests
    fi
    
    echo ""
    print_success "Deployment complete!"
    echo ""
    
    # Step 6: Launch system
    launch_system
    
    echo ""
    print_success "Thalos Prime deployment finished"
    echo ""
}

# Run main function
main
