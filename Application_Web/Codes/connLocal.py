import mysql.connector

def connBD():
    connexion = mysql.connector.connect(
        host="localhost",
        user="root",
        port=3306,
        database="pt1",
        password="....."
    )

    cursor = connexion.cursor()
    #cursor.execute("INSERT INTO users VALUES (%s,%s)", ("Ibrahim", 32))
    # Pour enregistrer les modifications faite à la BD.
    #connexion.commit()
    cursor.execute(f"Select centres_interets from etudiant where no_immatriculation='10-513-512'")
    centresInterest = cursor.fetchall()[0][0]
    print(centresInterest)
    chaine_ajoute = "sport, géographie"


    """
    centres = centresInterest[0][0]
    centres += f", {chaine_ajoute}"
    print(centres)
    """




    # la méthode fetchall parcorus les différents lignes du résulats et les retourne sous-forme de tuple.
    #print(cursor.fetchall())

    connexion.close()