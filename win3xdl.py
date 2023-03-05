import requests
import os
from tqdm import tqdm

def tester_urls_existantes():
    # URL de base avec l'ID comme paramètre
    base_url = "http://www.win3x.org/win3board/ext/win3x/download.php?id="

    # Liste pour stocker les URLs existantes
    urls_existantes = []

    # Tester l'existence des pages pour les ID de 1 à 10000
    for i in range(1, 10001):
        url = base_url + str(i)
        headers = {'Referer': 'http://www.win3x.org', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0'}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            urls_existantes.append(url)

    # Écrire les URLs existantes dans un fichier
    with open('urls_existantes.txt', 'w') as f:
        for url in urls_existantes:
            f.write(url + '\n')

    print(f"{len(urls_existantes)} URLs existantes ont été écrites dans urls_existantes.txt.")
    
def telecharger_urls_existantes():
    # Créer le dossier de téléchargement s'il n'existe pas déjà
    if not os.path.exists('dl'):
        os.mkdir('dl')

    # Charger les URLs existantes depuis le fichier urls_existantes.txt
    with open('urls_existantes.txt', 'r') as f:
        urls = f.read().splitlines()

    # Télécharger les fichiers à partir des URLs existantes avec une barre de progression
    for url in tqdm(urls, desc='Téléchargement en cours', unit='fichier'):
        filename = url.split('/')[-1]
        headers = {'Referer': 'http://www.win3x.org', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0'}
        response = requests.get(url, headers=headers, stream=True)

        if response.status_code == 200:
            with open(os.path.join('dl', filename), 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)

            tqdm.write(f"{filename} a été téléchargé avec succès dans le dossier dl.")

    tqdm.write(f"Tous les fichiers ont été téléchargés avec succès dans le dossier dl.")
