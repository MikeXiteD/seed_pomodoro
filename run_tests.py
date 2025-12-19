#!/usr/bin/env python3
"""Test runner with proper Python path setup."""
import sys
import os

# Change to project directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Add src directory to path
sys.path.insert(0, os.path.join(os.getcwd(), 'src'))

# Run pytest
import pytest

if __name__ == "__main__":
    args = [
        "tests/",
        "-v",
        "--tb=short"
    ]
    sys.exit(pytest.main(args))
