"""Aqui serão gerados dados ficticios relativamenta ás eleições legislativas de 2025"""

import json

# Tranformei o json com os partidos num dicionário com a Sigla e o Full Name
with open('data/raw/partidos.json', encoding='utf-8') as f:
    parties = json.load(f)

for sigla, nome in parties.items():
    print(f"{sigla}: {nome}")
