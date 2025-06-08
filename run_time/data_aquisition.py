
""" Aqui vai ser executado um script que vai buscar os dados raw """

import requests
import zipfile
import io
import os
from pathlib import Path


def main():
    # Folder onde os arquivos serão salvos
    output_dir = "data/raw"
    os.makedirs(output_dir, exist_ok=True) 

    # urls dos ficheiros CSV 
    files = {
        "distritos": "https://raw.githubusercontent.com/mapaslivres/divisoes-administrativas-pt/master/data/districts.csv",
        "municipios": "https://raw.githubusercontent.com/mapaslivres/divisoes-administrativas-pt/master/data/municipalities.csv",
        "freguesias": "https://raw.githubusercontent.com/mapaslivres/divisoes-administrativas-pt/master/data/freguesias.csv",
    }

    # Faz download dos csvs e se for preciso substitui os arquivos
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

    ###############################################################################################################################

    """ Aqui será feito o download dos dados relativos as elições de 2019 e 2024 """

    output_dir = Path("data/raw/elections")
    os.makedirs(output_dir, exist_ok=True)

    # Election files configuration
    elections = {
        "leg_19": {
            "url": "https://www.cne.pt/sites/default/files/dl/ar2019-quadro-resultados.zip",
        },
        "leg_24": {
            "url": "https://www.cne.pt/sites/default/files/dl/eleicoes/2024_ar/docs_geral/2024_ar_quadro_resultados.zip",
        }
    }

    def download_and_extract_zip(url, output_path):
        """Downloads and extracts a zip file to the specified path"""
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
            print(f"The downloaded file is not a valid ZIP archive")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        
        return False

    # Process each election
    for election_id, config in elections.items():
        print(f"\n{'='*50}")
        print(f"Processing {election_id} election data")
        
        # Download and extract directly to output_dir
        success = download_and_extract_zip(config["url"], output_dir)
        
        if success:
            print(f"✔ {election_id} completed successfully")
        else:
            print(f"✖ Failed to process {election_id}")

    print("\n" + "="*50)
    print("All election data processing complete!")
    print(f"Files saved in: {output_dir.absolute()}")
    print("Extracted files:")
    for f in os.listdir(output_dir):
        print(f"- {f}")

    # Isto aqui é só para apagar as ods, porque não vão ser necessárias e deixa a pasta mais limpa
    # Lista de arquivos a serem removidos

    files_to_remove = [
        os.path.join("data", "raw", "elections", "2024_ar_quadro_resultados.ods"),
        os.path.join("data", "raw", "elections", "ar2019-quadro-resultados.ods")
    ]

    for file_path in files_to_remove:
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"Removed: {file_path}")
        else:
            print(f"File not found: {file_path}")
        
if __name__ == "__main__":
    main()