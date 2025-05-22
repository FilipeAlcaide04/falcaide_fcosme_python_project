""" Aqui vai ser executado um script que vai buscar os dados raw """

import os
import requests

# Folder onde os arquivos serão salvos
output_dir = "data/raw"
os.makedirs(output_dir, exist_ok=True) 

# urls dos ficheiros CSV 
files = {
    "distritos": "https://raw.githubusercontent.com/mapaslivres/divisoes-administrativas-pt/master/data/districts.csv",
    "municipios": "https://raw.githubusercontent.com/mapaslivres/divisoes-administrativas-pt/master/data/municipalities.csv",
    "freguesias": "https://raw.githubusercontent.com/mapaslivres/divisoes-administrativas-pt/master/data/freguesias.csv",
}

# Faz donwload dos csvs e se for preciso substitui os arquivos
for name, url in files.items():
    file_path = os.path.join(output_dir, f"{name}.csv")
    try:
        print(f"Downloading {name}...")
        response = requests.get(url)
        response.raise_for_status()

        # Guarda os arquivos
        with open(file_path, "wb") as f:
            f.write(response.content)

        print(f"Saved in: {file_path}")
    except requests.RequestException as e:
        print(f"Error while downloading {name}: {e}")
