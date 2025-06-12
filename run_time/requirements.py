""" Run this before running the code ( Essencial para instalar todas as bibliotecas )"""
import subprocess
import sys

packages = [
    "xlrd==2.0.1",
    "flask==2.3.3",
    "pandas==2.2.2",
    "openpyxl==3.1.2",
    "requests==2.31.0",
    "python-dotenv==1.0.1",
    "pylint==3.1.0",
    "pytest==8.2.1",
    "platformdirs==4.2.1"
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
