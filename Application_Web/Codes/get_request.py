import requests
import json
import os
from firstOccurence import *

def parseJson():
    listOf_links = []
    pathCours = "./programmeCours.json"
    # On regarde si le fichier est vide avant d'insérer le json.
    if os.stat(pathCours).st_size == 0:
        with open(pathCours, "w") as json_file:
            api_data = requests.get(
                "https://wwwit.unige.ch/cursus/programme-des-cours/api/teachings/find?academicalYear=2021&page=0&size=5000").json()
            json.dump(api_data, json_file)

    with open(pathCours, "r") as js_files:
        niveau_etude = "Bachelor"
        data = json.load(js_files)
        for elmnt in data['_data']:
            if elmnt['studyLevel'] is not None:
                std_level = str(elmnt['studyLevel'])
                if first_occurence(niveau_etude, std_level):
                    currentLink = str(elmnt['_links']['self']['href'])
                    listOf_links.append(currentLink)

    # insertion des liens dans un fichier links.txt

    pathLinks = "./links.txt"
    if os.stat(pathLinks).st_size == 0:
        with open(pathLinks, "w") as link_file:
            for links in listOf_links:
                link_file.write(links+"\n")