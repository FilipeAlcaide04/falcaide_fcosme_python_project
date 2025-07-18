""" Run this before running the code ( Essencial para instalar todas as bibliotecas )"""
import subprocess
import sys

packages = [
    "astroid           == 3.1.0",
    "blinker           == 1.9.0",
    "certifi           == 2025.4.26",
    "charset-normalizer == 3.4.2",
    "click             == 8.2.1",
    "dill              == 0.4.0",
    "et_xmlfile        == 2.0.0",
    "Flask             == 2.3.3",
    "idna              == 3.10",
    "iniconfig         == 2.1.0",
    "isort             == 5.13.2",
    "itsdangerous      == 2.2.0",
    "Jinja2            == 3.1.6",
    "MarkupSafe        == 3.0.2",
    "mccabe            == 0.7.0",
    "numpy             == 2.3.0",
    "openpyxl          == 3.1.2",
    "packaging         == 25.0",
    "pandas            == 2.2.2",
    "pip               == 24.3.1",
    "platformdirs      == 4.2.1",
    "pluggy            == 1.6.0",
    "pylint            == 3.1.0",
    "pytest            == 8.2.1",
    "python-dateutil   == 2.9.0.post0",
    "python-dotenv     == 1.0.1",
    "pytz              == 2025.2",
    "requests          == 2.31.0",
    "six               == 1.17.0",
    "tomlkit           == 0.13.3",
    "tzdata            == 2025.2",
    "urllib3           == 2.4.0",
    "Werkzeug          == 3.1.3",
    "xlrd              == 2.0.1"
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
