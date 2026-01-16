#!/bin/bash
# © 2026 Tony Ray Macier III. All rights reserved.
#
# Thalos Prime v3.0 - Automatic Web Deployment (Linux/macOS)
# One-click web interface launcher

echo ""
echo "========================================================================"
echo ""
echo "    ████████╗██╗  ██╗ █████╗ ██╗      ██████╗ ███████╗"
echo "    ╚══██╔══╝██║  ██║██╔══██╗██║     ██╔═══██╗██╔════╝"
echo "       ██║   ███████║███████║██║     ██║   ██║███████╗"
echo "       ██║   ██╔══██║██╔══██║██║     ██║   ██║╚════██║"
echo "       ██║   ██║  ██║██║  ██║███████╗╚██████╔╝███████║"
echo "       ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚══════╝"
echo ""
echo "       SYNTHETIC BIOLOGICAL INTELLIGENCE v3.0"
echo "           AUTOMATIC WEB DEPLOYMENT"
echo ""
echo "========================================================================"
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python 3 is not installed"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

# Run the Python deployment script
echo "[INFO] Launching Python deployment script..."
echo ""

python3 auto_web_deploy.py

# Exit with the same code as the Python script
exit $?
