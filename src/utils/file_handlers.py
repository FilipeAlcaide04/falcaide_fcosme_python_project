""" Módulo usado para ordernar e processar os ficheiros raw"""
import pandas as pd

# Dar load ao CSVS
distritos = pd.read_csv('data/raw/distritos.csv')
municipios = pd.read_csv('data/raw/municipios.csv')
freguesias = pd.read_csv('data/raw/freguesias.csv')

#Garantir que todos os códigos tem os digitos corrertos (2,4,6)
distritos['ine_id'] = distritos['ine_id'].astype(str).str.zfill(2)
municipios['ine_id'] = municipios['ine_id'].astype(str).str.zfill(4)
freguesias['ine_id'] = freguesias['ine_id'].astype(str).str.zfill(6)

# Renomear colunas para evitar conflitos
distritos = distritos.rename(columns={'name': 'distrito'})
municipios = municipios.rename(columns={'name': 'municipio'})
freguesias = freguesias.rename(columns={'name': 'freguesia'})

#Junta o distrito e o municipio
freguesias['distrito_id'] = freguesias['ine_id'].str[:2]
freguesias['municipio_id'] = freguesias['ine_id'].str[:4]



#Juntar os dados todos num data frame
# Primeiro, juntar freguesias com municípios
df = pd.merge(
    freguesias,
    municipios[['ine_id', 'municipio']],
    left_on='municipio_id',
    right_on='ine_id',
    how='left'
).drop(columns=['ine_id_y']).rename(columns={'ine_id_x': 'ine_id'})

# Depois, juntar com distritos
df = pd.merge(
    df,
    distritos[['ine_id', 'distrito']],
    left_on='distrito_id',
    right_on='ine_id',
    how='left'
).drop(columns=['ine_id_y']).rename(columns={'ine_id_x': 'ine_id'})

# Ordenar colunas
df = df[['ine_id', 'distrito', 'municipio', 'freguesia']]

#Guardar em csv com os dados já limpos
#df.to_csv('data/processed/portugal_administrative_divisions.csv', index=False)
