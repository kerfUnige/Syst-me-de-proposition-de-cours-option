import urllib.request
import json
import mysql.connector
from Codes.firstOccurence import *
from Codes.Exception.exception1 import *


# fonction qui permet d'insérer les tuples dans la table Cours

def insertElements_cours1():
    # On parcours le fichier conetenant la séquence des cours obligatoires
    semesters = ["1", "2", "3", "4", "5", "6"]
    path_pc = "../sequenceCours.json"
    dictCrs_semestre = dict()

    # Codage unicode: Utf-8 -> codage à taille variable (PFO, codage de texte). Il utilise 1, 2 ou 3 octets
    # pour représenter l'intégralité des points de code Unicode. Tandisque que le codage ASCII n'utilise qu'un seul octet
    # et ce limite uniquement au caractère anglais.
    with open(path_pc, "r", encoding='utf-8') as seq_file:
        seq_cours = json.load(seq_file)
        for semestre in semesters:
            for cours in seq_cours[semestre]:
                dictCrs_semestre[cours] = int(semestre)
    print(dictCrs_semestre)

    # Toutes les variables dont nous avons besoin pour
    # L'insertion des tuples
    id_cours: str = " "
    nom_cours: str = " "
    faculte: str = " "
    nb_credits: float = 0
    obligatoire: int = 0
    descriptif: str = " "
    objectif: str = " "
    option_obligatoire = False

    # Lecture du fichier links.txt
    path = "../links.txt"
    with open(path, "r") as link_file:
        for link in link_file:

            # On teste si la réponse fournit par le serveur n'est pas une erreur
            # cela permettra de savoir s'il faut procéder à l'extraction des données.
            try:
                urllib.request.urlopen(link)
            except urllib.error.HTTPError:
                continue

            resp = urllib.request.urlopen(link)
            if resp.code == 200:
                datas = json.load(resp)


                # Pour chacune des valeurs à récupérer on évite les exceptions
                id_cours = avoidException(id_cours, datas['code'])
                nom_cours = avoidException(nom_cours, datas['title'])
                faculte = avoidException(faculte, datas['facultyLabel'])
                nb_credits = avoidException(nb_credits, datas['credits'])

                # On parcours le fichier contenant la séquence des cours obligatoires
                # pour insérer les semestres correspondant à chaque cours.
                if first_occurence("Centre universitaire d'informatique", faculte):
                    for k in dictCrs_semestre.keys():
                        if nom_cours == k:
                            obligatoire = dictCrs_semestre.get(k)
                            print(f"{nom_cours} {obligatoire}")

                # On parse l'attribut activities pour récupérer le descriptif et l'objectif
                elements = datas['activities'][0]
                for k, v in elements.items():

                    if k == "objective":
                        objectif = avoidException(k,v)
                    if k == "description":
                        descriptif = avoidException(k,v)


                # On parcours le fichier des cours à option obligatoire afin de déterminer si le cours
                # est un cours à option obligatoire.
                path_optObligatoire = "../optionObligatoire.json"
                with open(path_optObligatoire, "r", encoding='utf-8') as opt_file:
                    optCours = json.load(opt_file)
                    for opt_crs in optCours['options_obligatoire']:
                        if nom_cours == opt_crs:
                            option_obligatoire = True

            # connexion à la base de données pour insérer les tuples dans la table cours
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                port=3306,
                database="pt1",
                password="...."
            )
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO Cours (id_cours,nom_cours,faculte,objectif,descriptif,obligatoire,option_obligatoire,nb_credits) values (%s,%s,%s,%s,%s,%s,%s,%s)",
                (id_cours, nom_cours, faculte, objectif, descriptif, obligatoire, option_obligatoire, nb_credits))
            conn.commit()
            conn.close()
            # On remet certaines variables à leur valeur par défaut pour la prochaine itération.
            obligatoire = 0
            option_obligatoire = False
