import json
import urllib.request
from Codes.firstOccurence import *
import mysql.connector
from Codes.Exception.exception import *


def insertElements_salles():
    # déclaration des varaiables dont on a besoin
    # pour l'insertion des tuples dans la table horaires
    jourSemaine = ["LU", "MA", "ME", "JE", "VE"]
    dictCours = dict()
    dictBuilding = {"SM": "Section Mathématiques", "SCI ": "Sciences I", "SCI-": "Sciences I", "SCII ": "Sciences II", "SCII-": "Sciences II", "SCIII": "Sciences III", "Bat": "Battelle", "BAT": "Battelle", "DUF": "Dufour", "Physique": "École de Physique", "Ansermet": "Pavillon Ansermet", "ANSERMET": "Pavillon Ansermet", "Carl Vogt": "Carl Vogt", "MAIL": "Uni-Mail", "BAUD-BOVY": "Baud-Bovy"}
    dictKeyBuildingList = dictBuilding.keys()
    id_horaires = " "
    id_cours = " "
    periode = " "
    jour = " "
    heure_debut = 0
    heure_fin = 0
    building = ""
    room = ""
    multiple_rooms = []
    # dans horaires le premier élément de la liste correspond à l'heure de début
    # et le dernier à l'heure de fin.
    horaires = list()
    # la variable ci-dessous permet de récupérer le shortype du cours, séminaire, exos.
    # Ell est utilisé pour l'attribut séminaire.
    shorType = " "

    # On récupère l'id des cours qui n'ont pas jouer.
    # Nom de l'exception a gerer: mysql.connector.errors.IntegrityError
    cours_problemes = list()
    salles_cours = list()

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

                        for sched in coursSemaine:
                            if first_occurence("/", sched) and (
                                    not first_occurence("Bat", sched) or not first_occurence("BAT", sched)):
                                multiple_rooms = sched.split("/")
                            for batiment in dictKeyBuildingList:
                                if first_occurence(batiment, sched):
                                    building = dictBuilding.get(batiment)
                                    room = sched[1:]
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
                            if k == "building":
                                if dictCours.get(jour) is not None:
                                    if null(v):
                                        v = None
                                        dictCours[jour].append(v)
                                    else:
                                        dictCours[jour].append(v)
                            if k == "room":
                                if dictCours.get(jour) is not None:
                                    if null(v):
                                        v = None
                                        dictCours[jour].append(v)
                                    else:
                                        dictCours[jour].append(v)

                for date, hour in dictCours.items():
                    heure_debut = hour[0]
                    heure_fin = hour[1]
                    if len(hour) > 2:
                        building = hour[2]
                        room = hour[3]
                    if building is not None and room is not None:
                        if len(multiple_rooms) != 0:
                            for classe in multiple_rooms:
                                # creation de l'id_horaire
                                id_horaires = id_cours + str(heure_debut) + str(heure_fin) + shorType + date + periode[0]
                                # creation de l'id_salle
                                id_salle = id_horaires + "-" + classe
                                # print("Instance Salle: (" + id_salle + ", " + id_horaires + ", " + building + ", " + classe + ")")
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
                                        "INSERT INTO Salle (id_salle,id_horaires,batiment,num_salle) values (%s,%s,%s,%s)",
                                        (id_salle, id_horaires, building, classe))
                                    # On défait les opérations qui ont eu lieu dans la BD en cas d'exception.
                                    conn.rollback()
                                except mysql.connector.errors.IntegrityError as err:
                                    # On rajoute le cours qui a posé problème dans la BD.
                                    cours_problemes.append(id_cours)
                                    print("Error {}".format(err))
                                    print("ID cours {}".format(id_cours))
                                    continue
                                # S'il n'y pas eu d'exception alors on insère
                                else:
                                    cursor.execute(
                                        "INSERT INTO Salle (id_salle,id_horaires,batiment,num_salle) values (%s,%s,%s,%s)",
                                        (id_salle, id_horaires, building, classe))
                                    conn.commit()
                                    conn.close()
                        else:
                            # creation de l'id_horaire
                            id_horaires = id_cours + str(heure_debut) + str(heure_fin) + shorType + date + periode[0]
                            # creation de l'id_salle
                            id_salle = id_horaires + "-" + room
                            # print("Instance Salle: (" + id_salle + ", " + id_horaires + ", " + building + ", " + room + ")")
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
                                    "INSERT INTO Salle (id_salle,id_horaires,batiment,num_salle) values (%s,%s,%s,%s)",
                                    (id_salle, id_horaires, building, room))
                                # On défait les opérations qui ont eu lieu dans la BD en cas d'exception.
                                conn.rollback()
                            except mysql.connector.errors.IntegrityError as err:
                                # On rajoute le cours qui a posé problème dans la BD.
                                cours_problemes.append(id_cours)
                                print("Error {}".format(err))
                                print("ID cours {}".format(id_cours))
                                continue
                            # S'il n'y pas eu d'exception alors on insère
                            else:
                                cursor.execute(
                                    "INSERT INTO Salle (id_salle,id_horaires,batiment,num_salle) values (%s,%s,%s,%s)",
                                    (id_salle, id_horaires, building, room))
                                conn.commit()
                                conn.close()
                # On vide le dictionnaire et la liste de salles pour la prochaine itération.
                dictCours.clear()
                multiple_rooms.clear()

    print("Les cours qui posent problème" + str(cours_problemes))  # Le cours qui pose problème est: ID cours-> 7426AB
