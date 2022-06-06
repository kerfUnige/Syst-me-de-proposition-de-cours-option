import json
import urllib.request
from Codes.firstOccurence import *
import mysql.connector
from Codes.Exception.exception import *


def insertElements_horaires():
    # déclaration des varaiables dont on a besoin
    # pour l'insertion des tuples dans la table horaires
    jourSemaine = ["LU", "MA", "ME", "JE", "VE"]
    dictCours = dict()
    id_horaires = " "
    id_cours = " "
    periode = " "
    jour = " "
    heure_debut = 0
    heure_fin = 0
    # dans horaires le premier élément de la liste correspond à l'heure de début
    # et le dernier à l'heure de fin.
    horaires = list()
    # la variable ci-dessous permet de récupérer le shortype du cours, séminaire, exos.
    # Ell est utilisé pour l'attribut séminaire.
    shorType = " "

    # On récupère l'id des cours qui n'ont pas jouer.
    # Nom de l'exception a gerer: mysql.connector.errors.IntegrityError
    cours_problemes = list()

    path_link = "./links.txt"
    with open(path_link, "r") as link_file:
        for link in link_file:
            try:
                urllib.request.urlopen(link)
            except urllib.error.HTTPError:
                # on passe à la prochaine itération
                continue
            resp = urllib.request.urlopen(link)
            datas = json.load(resp)
            # On récupère l'id du cours
            id_cours = datas['code']
            # On récupère les autres attributs

            for i in range(len(datas['activities'])):
                for att, val in datas['activities'][i].items():
                    if att == "shortType":
                        shorType = val
                    if att == "periodicity":
                        periode = val

                    if att == "scheduleText" and val != None:
                        coursSemaine = val.split(",")
                        for day in jourSemaine:
                            for sched in coursSemaine:
                                position = occShecText(day, sched)
                                if position != 0 and first_occurence("h-", sched):
                                    # la chaine représentant l'horaire
                                    # ne peut pas faire plus de 8 caractères
                                    if len(sched[position:]) < 8:
                                        dictCours[day.upper()] = sched[position:].upper()

                        for k, v in dictCours.items():
                            v += "-"
                            dictCours[k] = v

                        for k, v in dictCours.items():
                            horaires = v.split("H-")
                            dictCours[k] = horaires[:-1]

                        for date, hor in dictCours.items():
                            heure_debut = int(hor[0])
                            heure_fin = None
                            if len(hor) > 1:
                                heure_fin = int(hor[1])
                            dictCours[date] = [heure_debut, heure_fin]

                    if att == "courses" and len(val) != 0:
                        for k, v in val[0].items():
                            if k == "shortDay":
                                # Si le jour n'est pas spécifié alors on passe
                                # à la prochaine itération.
                                if null(v):
                                    continue
                                jour = v.upper()
                                dictCours[jour] = list()
                            if k == "startHour":
                                if dictCours.get(jour) is not None:
                                    if null(v):
                                        v = None
                                        dictCours[jour].append(v)
                                    else:
                                        dictCours[jour].append(int(v))
                                    # heure_debut = v
                            if k == "endHour":
                                if dictCours.get(jour) is not None:
                                    if null(v):
                                        v = None
                                        dictCours[jour].append(v)
                                    else:
                                        dictCours[jour].append(int(v))

                for date, hour in dictCours.items():
                    heure_debut = hour[0]
                    heure_fin = hour[1]
                    # creation de l'id_horaire
                    id_horaires = id_cours + str(heure_debut) + str(heure_fin) + shorType + date + periode[0]
                    conn = mysql.connector.connect(
                        host="localhost",
                        user="root",
                        port=3306,
                        database="pt1",
                        password="..."
                    )
                    cursor = conn.cursor()
                    try:
                        cursor.execute(
                            "INSERT INTO Horaires (id_horaires,id_cours,periode,jour,heure_debut,heure_fin,seminaire) values (%s,%s,%s,%s,%s,%s,%s)",
                            (id_horaires, id_cours, periode, date, heure_debut, heure_fin, shorType))
                        # On défait les opérations qui ont eu lieu dans la BD en cas d'exception.
                        conn.rollback()
                    except mysql.connector.errors.IntegrityError as err:
                        # On rajoute le cours qui a posé probleme dans la BD.
                        cours_problemes.append(id_cours)
                        print("Error {}".format(err))
                        print("ID cours {}".format(id_cours))
                        continue
                    # S'il n'y pas eu d'exception alors on insère
                    else:
                        cursor.execute(
                            "INSERT INTO Horaires (id_horaires,id_cours,periode,jour,heure_debut,heure_fin,seminaire) values (%s,%s,%s,%s,%s,%s,%s)",
                            (id_horaires, id_cours, periode, date, heure_debut, heure_fin, shorType))
                        conn.commit()
                        conn.close()
                # On vide le dictionnaire pour la prochaine itération.
                dictCours.clear()

    print(cours_problemes) # Le cours qui pose problème est: ID cours-> 7426AB

