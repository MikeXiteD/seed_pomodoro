#!/usr/bin/env python3
"""
SEED Pomodoro Timer - Launch Script
"""

import subprocess
import sys
import os


def check_dependencies():
    """Check if required packages are installed."""
    required = ['streamlit', 'pytest']
    missing = []
    
    for package in required:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing.append(package)
    
    return missing


def install_dependencies():
    """Install missing dependencies."""
    print("Installing dependencies from requirements.txt...")
    result = subprocess.run(
        [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        print("✅ Dependencies installed successfully!")
        return True
    else:
        print("❌ Failed to install dependencies:")
        print(result.stderr)
        return False


def run_tests():
    """Run the test suite."""
    print("\n🧪 Running tests...")
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "tests/", "-v"],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        print("✅ All tests passed!")
    else:
        print("❌ Some tests failed:")
        print(result.stdout)
    
    return result.returncode == 0


def run_app():
    """Launch the Streamlit app."""
    print("\n🚀 Launching SEED Pomodoro Timer...")
    print("👉 Open your browser to http://localhost:8501")
    print("👉 Press Ctrl+C to stop the server\n")
    
    # Run streamlit
    subprocess.run([
        sys.executable, "-m", "streamlit", "run", 
        "src/app.py",
        "--server.port=8501",
        "--server.address=0.0.0.0",
        "--theme.base=dark"
    ])


def main():
    """Main entry point."""
    print("=" * 60)
    print("⏱️  SEED Pomodoro Timer")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not os.path.exists("src/app.py"):
        print("❌ Error: Please run this script from the seed_pomodoro directory")
        print("Current directory:", os.getcwd())
        return 1
    
    # Check dependencies
    missing = check_dependencies()
    if missing:
        print(f"⚠️  Missing dependencies: {', '.join(missing)}")
        if input("Install dependencies? (y/n): ").lower() == 'y':
            if not install_dependencies():
                return 1
        else:
            print("Cannot proceed without dependencies.")
            return 1
    
    # Ask what to do
    print("\nOptions:")
    print("1. 🚀 Run the app")
    print("2. 🧪 Run tests")
    print("3. 🧪 Run tests then launch app")
    print("4. ❌ Exit")
    
    choice = input("\nSelect option (1-4): ").strip()
    
    if choice == "1":
        run_app()
    elif choice == "2":
        run_tests()
    elif choice == "3":
        if run_tests():
            run_app()
        else:
            print("\n⚠️  Tests failed. Fix issues before running the app.")
    elif choice == "4":
        print("Goodbye! 👋")
        return 0
    else:
        print("Invalid choice.")
        return 1
    
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n👋 Session ended by user.")
        sys.exit(0)