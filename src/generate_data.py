"""Aqui serão gerados dados ficticios relativamenta ás eleições legislativas de 2025"""

import json
import pandas as pd
import os
import sys
import random as r
import argparse

partidos_19 = 'data/raw/partidos_19.json'
partidos_24 = 'data/raw/partidos_25.json'
dados_regionais = "data/processed/dados_regionais_processed.csv"

# Tranformei o json com os partidos num dicionário com a Sigla e o Full Name
with open(partidos_19, encoding='utf-8') as f:
    parties = json.load(f)


