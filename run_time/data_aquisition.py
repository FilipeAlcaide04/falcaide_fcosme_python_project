#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para descarregar e extrair dados administrativos e eleitorais.
"""

import io
import os
import zipfile
from pathlib import Path

import requests


def download_and_extract_zip(url, output_path):
    """
    Faz o download e extrai um ficheiro ZIP para o caminho indicado.

    Args:
        url (str): URL do ficheiro ZIP.
        output_path (str or Path): Caminho onde os ficheiros serão extraídos.

    Returns:
        bool: True se a extração for bem-sucedida, False caso contrário.
    """
    try:
        print(f"Downloading from {url}...")
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        print(f"Extracting files to {output_path}...")
        with zipfile.ZipFile(io.BytesIO(response.content)) as zip_ref:
            zip_ref.extractall(output_path)

        print(f"Successfully extracted files to {output_path}")
        return True

    except requests.exceptions.RequestException as e:
        print(f"Download failed: {e}")
    except zipfile.BadZipFile:
        print("The downloaded file is not a valid ZIP archive")

    return False


def main():
    """
    Função principal que descarrega dados administrativos e eleitorais,
    extrai ficheiros ZIP e remove ficheiros ODS desnecessários.
    """
    # Diretório onde os arquivos serão salvos
    output_dir = "data/raw"
    os.makedirs(output_dir, exist_ok=True)

    # URLs dos ficheiros CSV
    files = {
        "distritos": "https://raw.githubusercontent.com/mapaslivres/"\
            "divisoes-administrativas-pt/master/data/districts.csv",
        "municipios": "https://raw.githubusercontent.com/mapaslivres/"\
            "divisoes-administrativas-pt/master/data/municipalities.csv",
        "freguesias": "https://raw.githubusercontent.com/mapaslivres/"\
            "divisoes-administrativas-pt/master/data/freguesias.csv",
    }

    # Faz download dos CSVs
    for name, url in files.items():
        file_path = os.path.join(output_dir, f"{name}.csv")
        try:
            print(f"Downloading {name}...")
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            with open(file_path, "wb") as file:
                file.write(response.content)

            print(f"Saved in: {file_path}")
        except requests.RequestException as e:
            print(f"Error while downloading {name}: {e}")

    # Diretório para os dados eleitorais
    election_dir = Path("data/raw/elections")
    os.makedirs(election_dir, exist_ok=True)

    elections = {
        "leg_19": {
            "url": "https://www.cne.pt/sites/default/files/dl/ar2019-quadro-resultados.zip",
        },
        "leg_24": {
            "url": "https://www.cne.pt/sites/default/files/dl/"\
                "eleicoes/2024_ar/docs_geral/2024_ar_quadro_resultados.zip",
        }
    }

    for election_id, config in elections.items():
        print("\n" + "=" * 50)
        print(f"Processing {election_id} election data")

        success = download_and_extract_zip(config["url"], election_dir)

        if success:
            print(f"✔ {election_id} completed successfully")
        else:
            print(f"✖ Failed to process {election_id}")

    print("\n" + "=" * 50)
    print("All election data processing complete!")
    print(f"Files saved in: {election_dir.absolute()}")
    print("Extracted files:")
    for file in os.listdir(election_dir):
        print(f"- {file}")

    # Remover ficheiros .ods desnecessários
    files_to_remove = [
        os.path.join(election_dir, "2024_ar_quadro_resultados.ods"),
        os.path.join(election_dir, "ar2019-quadro-resultados.ods"),
    ]

    for file_path in files_to_remove:
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"Removed: {file_path}")
        else:
            print(f"File not found: {file_path}")


if __name__ == "__main__":
    main()
