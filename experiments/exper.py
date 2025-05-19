""" Python Script used to test some functions and other things :) """

import pandas as pd

df = pd.read_csv('data/raw/freguesias_portugal_raw.csv')

resultado = df[df['name'] == 'Aguada de Cima']

print(resultado)
