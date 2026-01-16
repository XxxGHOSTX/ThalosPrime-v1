#!/usr/bin/env python3
"""
© 2026 Tony Ray Macier III. All rights reserved.

Thalos Prime™ is a proprietary system.
"""

"""
Custom test runner for Thalos Prime.

Provides deterministic test execution with detailed output.
"""

import sys
import os
import subprocess
import argparse
from pathlib import Path
from datetime import datetime


class ThalosTestRunner:
    """
    Custom test runner with deterministic output.
    """
    
    def __init__(self, verbose: bool = True, coverage: bool = False):
        """
        Initialize test runner.
        
        Args:
            verbose: Enable verbose output
            coverage: Enable coverage reporting
        """
        self.verbose = verbose
        self.coverage = coverage
        self.root_dir = Path(__file__).parent
        
    def run_tests(self, test_path: str = "tests/", markers: str = None) -> int:
        """
        Run tests with pytest.
        
        Args:
            test_path: Path to tests directory or file
            markers: Pytest markers to filter (e.g., "unit", "integration")
            
        Returns:
            Exit code (0 = success, non-zero = failure)
        """
        print("=" * 70)
        print("THALOS PRIME - TEST RUNNER")
        print("=" * 70)
        print(f"Timestamp: {datetime.now().isoformat()}")
        print(f"Test Path: {test_path}")
        print(f"Markers: {markers or 'all'}")
        print(f"Coverage: {'enabled' if self.coverage else 'disabled'}")
        print("=" * 70)
        print()
        
        # Build pytest command
        cmd = ["pytest", test_path]
        
        if self.verbose:
            cmd.append("-v")
            
        if markers:
            cmd.extend(["-m", markers])
            
        if self.coverage:
            cmd.extend([
                "--cov=src",
                "--cov-report=term-missing",
                "--cov-report=html",
                "--cov-report=xml"
            ])
            
        # Add pytest options
        cmd.extend([
            "--strict-markers",
            "--strict-config",
            "-ra",  # Show summary of all test outcomes
        ])
        
        # Run tests
        try:
            result = subprocess.run(cmd, cwd=self.root_dir)
            return result.returncode
        except FileNotFoundError:
            print("ERROR: pytest not found. Install with: pip install pytest")
            return 1
        except KeyboardInterrupt:
            print("\nTest run interrupted by user")
            return 130
            
    def run_unit_tests(self) -> int:
        """Run unit tests only"""
        print("Running UNIT tests...")
        return self.run_tests("tests/unit/", markers="unit")
        
    def run_integration_tests(self) -> int:
        """Run integration tests only"""
        print("Running INTEGRATION tests...")
        return self.run_tests("tests/integration/", markers="integration")
        
    def run_all_tests(self) -> int:
        """Run all tests"""
        print("Running ALL tests...")
        return self.run_tests("tests/")
        
    def validate_system(self) -> int:
        """
        Run complete system validation.
        
        Runs:
        1. Unit tests
        2. Integration tests
        3. Coverage report
        
        Returns:
            Exit code
        """
        print("=" * 70)
        print("SYSTEM VALIDATION")
        print("=" * 70)
        print()
        
        # Run unit tests
        print("\n" + "=" * 70)
        print("PHASE 1: UNIT TESTS")
        print("=" * 70)
        unit_result = self.run_unit_tests()
        
        if unit_result != 0:
            print("\n❌ Unit tests FAILED")
            return unit_result
            
        print("\n✅ Unit tests PASSED")
        
        # Run integration tests
        print("\n" + "=" * 70)
        print("PHASE 2: INTEGRATION TESTS")
        print("=" * 70)
        integration_result = self.run_integration_tests()
        
        if integration_result != 0:
            print("\n❌ Integration tests FAILED")
            return integration_result
            
        print("\n✅ Integration tests PASSED")
        
        # Summary
        print("\n" + "=" * 70)
        print("VALIDATION COMPLETE")
        print("=" * 70)
        print("✅ All tests passed")
        print("✅ System validated successfully")
        
        if self.coverage:
            print("\nCoverage report generated: htmlcov/index.html")
            
        return 0


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Thalos Prime Test Runner - Deterministic test execution"
    )
    
    parser.add_argument(
        "test_type",
        nargs="?",
        choices=["all", "unit", "integration", "validate"],
        default="all",
        help="Type of tests to run"
    )
    
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose output"
    )
    
    parser.add_argument(
        "-c", "--coverage",
        action="store_true",
        help="Enable coverage reporting"
    )
    
    parser.add_argument(
        "-p", "--path",
        type=str,
        help="Custom test path"
    )
    
    parser.add_argument(
        "-m", "--markers",
        type=str,
        help="Pytest markers to filter tests"
    )
    
    args = parser.parse_args()
    
    # Create runner
    runner = ThalosTestRunner(verbose=args.verbose, coverage=args.coverage)
    
    # Run tests based on type
    if args.path:
        exit_code = runner.run_tests(args.path, markers=args.markers)
    elif args.test_type == "unit":
        exit_code = runner.run_unit_tests()
    elif args.test_type == "integration":
        exit_code = runner.run_integration_tests()
    elif args.test_type == "validate":
        exit_code = runner.validate_system()
    else:  # all
        exit_code = runner.run_all_tests()
        
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
