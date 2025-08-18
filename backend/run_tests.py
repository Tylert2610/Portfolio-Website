#!/usr/bin/env python3
"""
Test runner script for the Portfolio Blog API
"""
import os
import subprocess
import sys
from pathlib import Path


def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"Command: {' '.join(command)}")
    print("=" * 60)

    try:
        result = subprocess.run(command, check=True, capture_output=False)
        print(f"\n✅ {description} completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ {description} failed with exit code {e.returncode}")
        return False


def main():
    """Main test runner function"""
    # Get the backend directory
    backend_dir = Path(__file__).parent
    os.chdir(backend_dir)

    print("🚀 Portfolio Blog API Test Runner")
    print("=" * 60)

    # Check if we're in the right directory
    if not (backend_dir / "app").exists():
        print(
            "❌ Error: app directory not found. Make sure you're in the backend directory."
        )
        sys.exit(1)

    # Parse command line arguments
    if len(sys.argv) > 1:
        test_type = sys.argv[1].lower()
    else:
        test_type = "all"

    success = True

    if test_type in ["all", "unit"]:
        print("\n📋 Running unit tests...")
        success &= run_command(
            ["python", "-m", "pytest", "tests/", "-m", "unit", "-v"], "Unit Tests"
        )

    if test_type in ["all", "api"]:
        print("\n📋 Running API tests...")
        success &= run_command(
            ["python", "-m", "pytest", "tests/", "-m", "api", "-v"], "API Tests"
        )

    if test_type in ["all", "integration"]:
        print("\n📋 Running integration tests...")
        success &= run_command(
            ["python", "-m", "pytest", "tests/", "-m", "integration", "-v"],
            "Integration Tests",
        )

    if test_type in ["all", "auth"]:
        print("\n📋 Running authentication tests...")
        success &= run_command(
            ["python", "-m", "pytest", "tests/", "-m", "auth", "-v"],
            "Authentication Tests",
        )

    if test_type in ["all", "coverage"]:
        print("\n📋 Running tests with coverage...")
        success &= run_command(
            [
                "python",
                "-m",
                "pytest",
                "tests/",
                "--cov=app",
                "--cov-report=term-missing",
                "--cov-report=html:htmlcov",
                "-v",
            ],
            "Tests with Coverage",
        )

    if test_type == "fast":
        print("\n📋 Running fast tests (excluding slow tests)...")
        success &= run_command(
            ["python", "-m", "pytest", "tests/", "-m", "not slow", "-v"], "Fast Tests"
        )

    if test_type == "lint":
        print("\n📋 Running linting...")
        success &= run_command(
            ["python", "-m", "black", "--check", "app/", "tests/"],
            "Black Code Formatting Check",
        )
        success &= run_command(
            ["python", "-m", "isort", "--check-only", "app/", "tests/"],
            "Import Sorting Check",
        )
        success &= run_command(
            ["python", "-m", "flake8", "app/", "tests/"], "Flake8 Linting"
        )

    if test_type == "format":
        print("\n📋 Formatting code...")
        success &= run_command(
            ["python", "-m", "black", "app/", "tests/"], "Black Code Formatting"
        )
        success &= run_command(
            ["python", "-m", "isort", "app/", "tests/"], "Import Sorting"
        )

    # Summary
    print("\n" + "=" * 60)
    if success:
        print("🎉 All tests completed successfully!")
        sys.exit(0)
    else:
        print("❌ Some tests failed. Please check the output above.")
        sys.exit(1)


if __name__ == "__main__":
    main()
