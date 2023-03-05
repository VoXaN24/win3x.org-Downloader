import requests
import os
import concurrent.futures
from tqdm import tqdm

def verifier_url(url):
    headers = {
        'Referer': 'http://www.win3x.org',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0'
    }
    response = requests.head(url, headers=headers, allow_redirects=True)
    if response.status_code == 200:
        return url
    else:
        return None

def tester_urls_existantes():
    urls = []
    for i in range(1, 10001):
        url = f'http://www.win3x.org/win3board/ext/win3x/download.php?id={i}'
        urls.append(url)

    valid_urls = []

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(verifier_url, url) for url in urls]

        for future in tqdm(concurrent.futures.as_completed(futures), total=len(futures), desc="Vérification des URLs"):
            result = future.result()
            if result is not None:
                valid_urls.append(result)

    with open("url.txt", "w") as f:
        for url in valid_urls:
            f.write(url + "\n")

if __name__ == '__main__':
    tester_urls_existantes()
  
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
tester_urls_existantes()
dl()
