#!/usr/bin/env python3
import os
import subprocess
import sys

# Change to seed_pomodoro directory
os.chdir('/workspace/seed_pomodoro')
print(f"Current directory: {os.getcwd()}")

# Check if src/app.py exists
if not os.path.exists('src/app.py'):
    print("❌ Error: src/app.py not found!")
    sys.exit(1)

# Check dependencies
print("Checking dependencies...")
try:
    import streamlit
    import pytest
    import dotenv
    print("✅ All dependencies are installed")
except ImportError as e:
    print(f"❌ Missing dependency: {e}")
    print("Installing requirements...")
    result = subprocess.run(
        [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        print(f"Failed to install: {result.stderr}")
        sys.exit(1)
    print("✅ Dependencies installed")

# Launch app
print("\n🚀 Launching SEED Pomodoro Timer...")
print("👉 The app will be available at http://localhost:8502")
print("👉 Press Ctrl+C to stop\n")

# Run streamlit
subprocess.run([
    sys.executable, "-m", "streamlit", "run",
    "src/app.py",
    "--server.port=8502",
    "--server.address=0.0.0.0",
    "--theme.base=dark"
])
