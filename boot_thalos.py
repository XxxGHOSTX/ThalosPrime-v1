#!/usr/bin/env python3
"""
© 2026 Tony Ray Macier III. All rights reserved.

Thalos Prime™ is a proprietary system.
"""

"""
Thalos Prime Boot Launcher

Launches Thalos Prime with the immersive Matrix interface.
Automatically starts web server and opens browser.
"""

import sys
import os
import time
import webbrowser
import subprocess
from pathlib import Path


def print_banner():
    """Print Thalos Prime boot banner"""
    banner = """
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║  ████████╗██╗  ██╗ █████╗ ██╗      ██████╗ ███████╗            ║
║  ╚══██╔══╝██║  ██║██╔══██╗██║     ██╔═══██╗██╔════╝            ║
║     ██║   ███████║███████║██║     ██║   ██║███████╗            ║
║     ██║   ██╔══██║██╔══██║██║     ██║   ██║╚════██║            ║
║     ██║   ██║  ██║██║  ██║███████╗╚██████╔╝███████║            ║
║     ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚══════╝            ║
║                                                                  ║
║              PRIME v1.5 - LIVE IMMERSIVE EDITION                 ║
║          Synthetic Biological Intelligence System                ║
║                                                                  ║
║        © 2026 Tony Ray Macier III. All rights reserved.         ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
"""
    print(banner)


def check_dependencies():
    """Check if all required dependencies are installed"""
    print("\n[SYSTEM] Checking dependencies...")
    
    required = ['flask', 'flask_cors', 'numpy', 'scipy']
    missing = []
    
    for package in required:
        try:
            __import__(package)
            print(f"  ✓ {package}")
        except ImportError:
            print(f"  ✗ {package} - MISSING")
            missing.append(package)
    
    if missing:
        print(f"\n[ERROR] Missing dependencies: {', '.join(missing)}")
        print("[INFO] Installing missing dependencies...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-q"] + missing)
        print("[INFO] Dependencies installed")
    
    return True


def initialize_system():
    """Initialize Thalos Prime system"""
    print("\n[SYSTEM] Initializing Thalos Prime Core...")
    
    # Add src to path
    sys.path.insert(0, str(Path(__file__).parent / "src"))
    
    try:
        from core.cis.controller import CIS
        
        print("  [1/5] Loading CIS Controller...")
        cis = CIS()
        
        print("  [2/5] Booting subsystems...")
        if cis.boot():
            print("  ✓ CIS operational")
        else:
            print("  ✗ CIS boot failed")
            return None
        
        print("  [3/5] Initializing memory systems...")
        memory = cis.get_memory()
        if memory:
            print(f"  ✓ Memory online ({memory.count()} entries)")
        
        print("  [4/5] Loading code generation...")
        codegen = cis.get_codegen()
        if codegen:
            print("  ✓ CodeGen ready")
        
        print("  [5/5] Preparing interfaces...")
        cli = cis.get_cli()
        api = cis.get_api()
        print("  ✓ CLI and API initialized")
        
        return cis
        
    except Exception as e:
        print(f"\n[ERROR] System initialization failed: {e}")
        import traceback
        traceback.print_exc()
        return None


def start_web_server(port=8000):
    """Start the immersive web interface"""
    print(f"\n[WEB] Starting immersive interface on port {port}...")
    
    # Create server process
    server_script = Path(__file__).parent / "src" / "interfaces" / "web" / "immersive_server.py"
    
    if not server_script.exists():
        print(f"[ERROR] Server script not found: {server_script}")
        return None
    
    # Start server in background
    env = os.environ.copy()
    env['FLASK_ENV'] = 'production'
    
    process = subprocess.Popen(
        [sys.executable, str(server_script)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=env
    )
    
    # Wait for server to start
    print("  [WEB] Waiting for server to start...")
    time.sleep(3)
    
    if process.poll() is None:
        print("  ✓ Web server running")
        return process
    else:
        print("  ✗ Web server failed to start")
        return None


def open_browser(url="http://localhost:8000"):
    """Open browser to the interface"""
    print(f"\n[BROWSER] Opening interface at {url}...")
    
    try:
        webbrowser.open(url)
        print("  ✓ Browser launched")
        return True
    except Exception as e:
        print(f"  ! Could not open browser automatically: {e}")
        print(f"  → Please open manually: {url}")
        return False


def main():
    """Main boot sequence"""
    print_banner()
    
    print("\n" + "="*70)
    print("BOOT SEQUENCE INITIATED")
    print("="*70)
    
    # Check dependencies
    if not check_dependencies():
        print("\n[ABORT] Dependency check failed")
        return 1
    
    # Initialize system
    cis = initialize_system()
    if not cis:
        print("\n[ABORT] System initialization failed")
        return 1
    
    # Start web server
    server_process = start_web_server()
    if not server_process:
        print("\n[ABORT] Web server failed to start")
        return 1
    
    # Open browser
    open_browser()
    
    print("\n" + "="*70)
    print("THALOS PRIME - FULLY OPERATIONAL")
    print("="*70)
    print("\n[STATUS] System Status:")
    status = cis.status()
    print(f"  • Version: {status['version']}")
    print(f"  • State: {status['status'].upper()}")
    print(f"  • Subsystems: {sum(1 for v in status['subsystems'].values() if v)}/{len(status['subsystems'])}")
    print(f"\n[ACCESS] Immersive Interface: http://localhost:8000")
    print("\n[CONTROL] Press Ctrl+C to shutdown")
    print("="*70 + "\n")
    
    # Keep running
    try:
        while True:
            time.sleep(1)
            
            # Check if server is still running
            if server_process.poll() is not None:
                print("\n[WARNING] Web server stopped unexpectedly")
                break
                
    except KeyboardInterrupt:
        print("\n\n[SHUTDOWN] Initiating graceful shutdown...")
        
        # Shutdown CIS
        print("  [1/2] Shutting down CIS...")
        if cis.shutdown():
            print("  ✓ CIS terminated cleanly")
        
        # Stop web server
        print("  [2/2] Stopping web server...")
        server_process.terminate()
        server_process.wait(timeout=5)
        print("  ✓ Web server stopped")
        
        print("\n[COMPLETE] Thalos Prime shut down successfully")
        print("="*70 + "\n")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
