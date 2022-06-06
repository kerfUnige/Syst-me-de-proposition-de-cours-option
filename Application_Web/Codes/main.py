from Codes.PropositionCours.Proposition_cours import *
from Codes.connLocal import *

if __name__ == '__main__':
    connexion = mysql.connector.connect(
        host="localhost",
        user="root",
        port=3306,
        database="pt1",
        password="...."
    )
    cursor = connexion.cursor(buffered=True)
    cursor.execute(f"SELECT * FROM etudiant ORDER BY nom")
    etudiants = cursor.fetchall()
    for etudiant in etudiants:
        cursor.execute(
            f"SELECT nom_cours FROM cours, coursetudiant WHERE cours.id_cours = coursetudiant.id_cours AND no_immatriculation = '{etudiant[0]}'")
        cours_suivis_tuple = cursor.fetchall()
        cours_suivis = []
        for i in cours_suivis_tuple:
            cours_suivis.append(i[0])
        print("\nnuméro d'immatriculation: " + etudiant[0] +
              "\nnom: " + etudiant[1] +
              "\nprénom: " + etudiant[2] +
              "\nsemestre d'étude: " + str(etudiant[3]) +
              "\ncentres d'intérêts: " + etudiant[4] +
              "\ncours suivis: " + ", ".join(cours_suivis) +
              "\n"
              )

        x1, x2, x3 = proposition_cours_BD(etudiant[0])

        print("Cours proposées:")  # Il contient le message.
        for x in x1:
            print(str(x))
            if x[-1] != '' or x[-2] != '':
                print("Il y a un message important")

        print("\nPlanning des cours obligatoires:")
        for x in x2:
            print(str(x))

        print("\nPlanning des cours proposées:")
        for x in x3:
            print(str(x))

    connexion.close()
