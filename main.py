import requests
from bs4 import BeautifulSoup as Bs
import yaml
import os
import msvcrt
from settings import *

URL = input("Veuillez coller l'URL à scrapper : ")
largest_file = ""
largest_number = -1
folder_path = os.path.join(os.getcwd(), "images")
nom_dossier = URL.strip("/").split("/")[-1]
nom_complet = str(folder_path)+"/"+str(nom_dossier)

if not os.path.exists(nom_complet):
    os.mkdir(f'{folder_path}/{nom_dossier}')
    print(f"Le dossier '{nom_dossier}' a été créé avec succès.")
else:
    print(f"Le dossier '{nom_dossier}' existe déjà.")

for filename in os.listdir(nom_complet):
    if filename.endswith(".jpg") or filename.endswith(".jpeg"):  # Filtrer les fichiers d'extension .jpg ou .jpeg
        file_path = os.path.join(nom_complet, filename)
        # Extraire le numéro de fichier du nom
        file_number = int(filename.replace("image_", "").replace(".jpg", "").replace(".jpeg", ""))
        if file_number > largest_number:
            largest_number = file_number
            largest_file = filename
if largest_file == "":
    indicefile = 1
else:
    indicefile = largest_file.split("_")[1]
    indicefile = indicefile.split(".")[0]
    indicefile = int(indicefile)

for i in range(indicefile,int(indicefile)+NBFILES):
    with open("headers.yml") as f_headers:
        browser_headers = yaml.safe_load(f_headers)
    url = f"{URL}/{i}"
    headers = browser_headers["Chrome"]
    response = requests.get(url, headers=headers)
    html = response.text
    soup = Bs(html,'html.parser')
    images_url = soup.find_all('img')
    alt_img =''
    imagebool = False
    index = IMAGE_INDEX
    while not imagebool and index >= 0:
        try:
            alt_img = images_url[index]['src']
            img_data = requests.get(alt_img).content
            image_size = len(img_data)
            size = 10000
            if image_size >= size:
                imagebool = True
            else:
                print(f"L'image n°{i} est inférieure à {size/1000}")
                index -= 1
        except:
            break
    if imagebool == True:
        img_data = requests.get(alt_img).content
        filename = f'{nom_complet}/image_{i}.jpg'
        with open(filename, 'wb') as file:
            file.write(img_data)
        print(f"L'image n°{i} a été téléchargée avec succès.")
    else:
        print(f"L'image n'a pas été téléchargée, image suivante n°{i+1}")

