import requests
import os
from tqdm import tqdm

def verifier_urls():
    # Générer les URLs à vérifier pour les IDs de 1 à 10000
    urls = []
    for i in range(1, 10001):
        url = f"http://www.win3x.org/win3board/ext/win3x/download.php?id={i}"
        urls.append(url)

    # Vérifier l'existence de chaque URL avec une barre de progression
    urls_existantes = []
    headers = {'Referer': 'http://www.win3x.org', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0'}
    with tqdm(total=len(urls), desc='Vérification en cours', unit='URL') as pbar:
        for url in urls:
            response = requests.head(url, headers=headers)

            if response.status_code == 200:
                urls_existantes.append(url)

            pbar.update(1)

    # Enregistrer les URLs existantes dans un fichier urls_existantes.txt
    with open('urls_existantes.txt', 'w') as f:
        f.write('\n'.join(urls_existantes))

    tqdm.write(f"{len(urls_existantes)} URLs existantes ont été enregistrées dans le fichier urls_existantes.txt.")
    
def dl():
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
verifier_urls()
dl()
