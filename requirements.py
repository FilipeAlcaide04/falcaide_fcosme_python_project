""" Run this before running the code ( Essencial para instalar todas as bibliotecas )"""
import subprocess
import sys

packages = [
    "xlrd",
    "flask",
    "pandas",
    "matplotlib",
    "openpyxl",
    "requests",
    "python-dotenv",
    "pylint",
    "pytest"
]


def install():
    """ Isto é para instalar os pacotes GIGANTES E COMPLEXOS """
    print("📦 Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
        subprocess.check_call([sys.executable, "-m", "pip", "install"] + packages)
        print("✅ All packages installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Installation failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    install()
