""" Aqui vai ser executado o script para limpar e tratar os dados """

from pathlib import Path
import sys

# Adiciona o diretório pai ao PATH do Python
sys.path.append(str(Path(__file__).parent.parent))

import src.file_handlers as data

data.main()

data.sec_main('2019')

data.sec_main('2024')