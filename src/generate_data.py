"""Aqui serão gerados dados ficticios relativamenta ás eleições legislativas de 2025"""

import json
import pandas as pd
import os
import sys
import random as r
import argparse

dd = 'data/raw/partidos.json' #usar argparse
rr = "data/processed/dados_regionais_processed.csv"

# Tranformei o json com os partidos num dicionário com a Sigla e o Full Name
with open(dd, encoding='utf-8') as f:
    parties = json.load(f)

"""for sigla, nome in parties.items():
    print(f"{sigla}: {nome}")"""

# Pegar nos dados regionais já processados

freguesias = pd.read_csv(rr)

print(freguesias)