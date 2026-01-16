#!/usr/bin/env python3
"""
© 2026 Tony Ray Macier III. All rights reserved.

Thalos Prime™ is a proprietary system.
"""

"""
Custom Test Runner for Thalos Prime

Provides deterministic test execution with detailed reporting.
"""

import sys
import subprocess
from pathlib import Path


def main():
    """Run all tests with coverage"""
    print("=" * 70)
    print("THALOS PRIME - TEST SUITE")
    print("=" * 70)
    print()
    
    # Run pytest with coverage
    cmd = [
        sys.executable, "-m", "pytest",
        "tests/",
        "-v",
        "--tb=short",
        "--cov=src",
        "--cov-report=term-missing",
        "--cov-report=html",
        "-x"  # Stop on first failure
    ]
    
    print(f"Running: {' '.join(cmd)}")
    print()
    
    result = subprocess.run(cmd)
    
    print()
    print("=" * 70)
    if result.returncode == 0:
        print("✓ ALL TESTS PASSED")
    else:
        print("✗ SOME TESTS FAILED")
    print("=" * 70)
    
    return result.returncode


if __name__ == "__main__":
    sys.exit(main())
