import mysql.connector

import requests


def insertElements_prerequis():
    # On récupère tous les cours qui sont disponibles dans la BD.
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        port=3306,
        database="pt1",
        password="..."
    )

    cursor = conn.cursor()
    query = "select * from Cours"
    cursor.execute(query)
    all_cours = cursor.fetchall()  # renvoit une liste ou chaque élément est un tuple.

    # On parcours tous les cours pour récupérer leurs prerequis s'il en existe.

    for cours in all_cours:
        datas = requests.get(
            "https://wwwit.unige.ch/cursus/programme-des-cours/api/teachings/{}".format(cours[0])).json()
        for k, v in datas['activities'][0].items():
            if k == "recommended" and v is not None:
                for elmnt in all_cours:
                    # S'il trouve le code du cours ou le nom alors on récupère l'id du cours.
                    if v.find(elmnt[0]) != -1 or v.find(elmnt[1]) != -1:
                        # Pour éviter de mettre dans les prerequis le code du cours dont cherche les prequis
                        if elmnt[0] != cours[0]:
                            # On crée l'id prerequis
                            # id_cours + id du cours qui est le prerequis
                            id_prerequis = cours[0] + elmnt[0]
                            cursor.execute(
                                "INSERT INTO prerequis(id_prerequis, id_cours, correspCours) values (%s,%s,%s)",
                                (id_prerequis, cours[0], elmnt[0])
                            )
                            conn.commit()
    conn.close()
