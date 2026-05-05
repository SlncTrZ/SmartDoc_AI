"""Backend: Setup Script — Install dependencies and prepare environment.

Run with: python setup.py

Wing: smartdoc_backend
Topic: environment_setup
Last Updated: 2026-05-05 09:30
"""

import subprocess
import sys
import os


def run_command(cmd, description):
    """Run command and display output."""
    print(f"\n{'='*60}")
    print(f"[Setup] {description}")
    print(f"{'='*60}")
    print(f"Running: {cmd}\n")

    try:
        result = subprocess.run(
            cmd,
            shell=True,
            check=True,
            capture_output=False,
            text=True
        )
        print(f"[OK] {description} completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] {description} failed!")
        print(f"Error: {e}")
        return False


def main():
    """Setup backend environment."""
    print("=" * 60)
    print("SMARTDOC AI - BACKEND SETUP")
    print("=" * 60)

    # Check Python version
    print("\n[Python] Version:")
    print(f"   {sys.version}")

    if sys.version_info < (3, 10):
        print("❌ Python 3.10+ required!")
        return False

    # Create virtual environment
    print("\n" + "=" * 60)
    print("[Setup] Creating Virtual Environment")
    print("=" * 60)

    venv_path = "venv"
    if os.path.exists(venv_path):
        print("[OK] Virtual environment already exists")
    else:
        if not run_command(f"{sys.executable} -m venv {venv_path}", "Virtual Environment Creation"):
            return False

    # Install dependencies
    print("\n" + "=" * 60)
    print("[Setup] Installing Dependencies")
    print("=" * 60)

    # Determine pip path
    if os.name == 'nt':  # Windows
        pip_path = os.path.join(venv_path, "Scripts", "pip")
        python_path = os.path.join(venv_path, "Scripts", "python")
    else:  # Unix
        pip_path = os.path.join(venv_path, "bin", "pip")
        python_path = os.path.join(venv_path, "bin", "python")

    if not run_command(f'"{pip_path}" install -r requirements.txt', "Dependency Installation"):
        print("\n[WARNING] Trying to install docling manually...")
        run_command(f'"{pip_path}" install docling', "Docling Installation")

    # Check Ollama
    print("\n" + "=" * 60)
    print("[Setup] Checking Ollama")
    print("=" * 60)

    try:
        result = subprocess.run(
            "ollama --version",
            shell=True,
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print(f"[OK] Ollama installed:")
            print(f"   {result.stdout.strip()}")
        else:
            print("[WARNING] Ollama not found in PATH")
            print("   Install from: https://ollama.ai")
    except Exception as e:
        print(f"⚠️  Could not check Ollama: {e}")

    # Summary
    print("\n" + "=" * 60)
    print("[Setup] COMPLETED!")
    print("=" * 60)
    print("\n[Next Steps]:")
    print(f"   1. Activate venv: venv\\Scripts\\activate (Windows)")
    print(f"   2. Run test: {python_path} quick_test.py")
    print(f"   3. Start server: {python_path} app.py")


if __name__ == '__main__':
    main()
