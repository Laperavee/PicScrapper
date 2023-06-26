import requests
from bs4 import BeautifulSoup as Bs
import yaml
import os
from settings import *
for i in range(1,100):
    URL = "Votre URL ici"
    largest_file = ""
    largest_number = -1
    folder_path = os.path.join(os.getcwd(), "images")
    response = requests.get(url=URL)
    html = response.text
    soup = Bs(html, 'html.parser')
    images_url = soup.find_all('picture')
    for image in images_url:
        image_source = image.find("img")
        image_dict = {
            'alt': image_source.get('alt'),
            'src': image_source.get('src'),
        }
        try:
            img_data = requests.get(image_dict['src']).content
            filename = f'{folder_path}/{image_dict["alt"]}.jpg'
            with open(filename, 'wb') as file:
                file.write(img_data)
            print(f"L'image {image_dict['alt']} a été téléchargée avec succès.")
        except:
            print(f"L'image {image_dict['alt']} n'a pas été téléchargée ")

