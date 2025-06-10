"""Script para limpar e tratar os dados."""

import sys
from pathlib import Path

# Add parent directory to path to allow importing src
sys.path.insert(0, str(Path(__file__).parent.parent))

import src.file_handlers as data  # pylint: disable=wrong-import-position, import-error

# Isto está a funcionar não sei porque razão não encontrava o
# modulo src.file_handlers (Tentei de tudo, mas não consegui resolver)

def main():
    """Execute data cleaning operations."""
    data.main()
    data.sec_main('2019')
    data.sec_main('2024')

if __name__ == '__main__':
    main()
