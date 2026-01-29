"""
Pytest configuration and fixtures

This file configures pytest to properly import the app module by adding
the project root directory to the Python path. This solves ModuleNotFoundError
when running tests in CI/CD environments.
"""
import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))