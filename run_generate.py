#!/usr/bin/env python3
"""
Run script for generating synthetic data.
Execute this from the project root directory.

Usage:
    python run_generate.py
"""

import subprocess
import sys

def main():
    # Install dependencies
    print("📦 Installing dependencies...")
    subprocess.run([sys.executable, "-m", "pip", "install", "pandas", "numpy", "scipy", "faker", "-q"])
    
    # Run the generator
    print("\n🚀 Running data generator...")
    from src import data_generator
    data_generator.main()
    
    # Run validation
    print("\n🔍 Running validation...")
    from src import validators
    validator = validators.DataValidator()
    validator.run_all_checks()

if __name__ == "__main__":
    main()
