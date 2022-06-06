from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
import mysql.connector
from Codes.PropositionCours.Proposition_cours import *

app = Flask(__name__)
Bootstrap(app)  # On spécifie que l'application utilise le templates Bootstrap.


@app.route('/')
def homepage():
    return render_template("home_page.html")


# Le formulaire pour la création du compte
@app.route("/formulaire_creer_compte")
def formulaire_creer_compte():
    return render_template("formulaire_creerCompte.html")


# Récupération des données du formulaire pour la création du compte.
@app.route("/creation_compte", methods=["POST"])
def creer_compte():
    # Récupération des champs du formulaire pour insérer les
    # éléments dans la tables étudiants
    nom = request.form.get("nom")
    prenom = request.form.get("prenom")
    num_immatriculation = request.form.get("num_immatriculation")
    semestre_etude = request.form.get("semestre_etude")
    centre_interets = request.form.get("centre_interets")
    # On laisse la possibilité aux étudiants de première année de ne pas avoir de cours suivis au paravant
    cours_suivis = request.form.get("cours_suivis")

    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="....",
        database="pt1",
        port=3306
    )

    # Minimisation des erreurs de l'utilisateur
    cursor = conn.cursor()
    cursor.execute(f"select * from etudiant where no_immatriculation='{num_immatriculation}'")
    resp_database = cursor.fetchall()
    tailleResp = 0

    if len(resp_database) != 0:
        # Alors l'étudiant existe déjà dans la base de données
        # Il n'a donc pas besoin de créer un compte.
        tailleResp = len(resp_database)
        return render_template("creer_compte.html", num_immatriculation=num_immatriculation,
                               tailleResp=tailleResp)

    else:
        # Donc l'étudiant n'existe pas dans la base de données
        # On va donc créer son compte
        cursor.execute(
            "INSERT INTO etudiant(no_immatriculation,nom,prenom,semestre_etude,centres_interets)values(%s,%s,%s,%s,%s)",
            (num_immatriculation, nom, prenom, int(semestre_etude), centre_interets))
        conn.commit()
        # On insère également les cours à option qu'il a suivit, il faut que ces cours
        # existe dans la base de données.

        if len(cours_suivis) != 0:

            cours_suivis_list = cours_suivis.split(",")

            for i in range(len(cours_suivis_list)):
                if i == 0:
                    print(cours_suivis_list[i])
                    cursor.execute("INSERT INTO coursetudiant(id_cours,no_immatriculation)values(%s,%s)",
                                   (cours_suivis_list[i], num_immatriculation))
                    conn.commit()
                else:
                    print(cours_suivis_list[i].replace(" ", ""))
                    cursor.execute("INSERT INTO coursetudiant(id_cours,no_immatriculation)values(%s,%s)",
                                   (cours_suivis_list[i].replace(" ", ""), num_immatriculation))
                    conn.commit()

        return render_template("creer_compte.html", num_immatriculation=num_immatriculation,
                               tailleResp=tailleResp)


# Le formulaire pour la modification du compte
@app.route("/formulaire_modifier_compte")
def formulaire_modifier_compte():
    return render_template("formulaire_modifierCompte.html")


# Récupération des données du formulaire pour la modification du compte.
@app.route("/modifier_compte", methods=["POST"])
def modifier_compte():
    # Les seuls éléments qui peuvent être modifié sont:
    # le semsetre d'étude, les centres d'intérêts, il peut ajouter des cours suivis
    num_immatriculation = request.form.get("num_immatriculation")
    semestre_etude = request.form.get("semestre_etude")
    centre_interets = request.form.get("centre_interets")
    cours_suivis = request.form.get("cours_suivis")
    # La variable ci-dessous permet de vérifier si l'étudiant souhaite écraser ces centres d'intérêts ou pas.
    ecraser_centres_interets = request.form.get("ecraser_centres_interets")

    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="....",
        database="pt1",
        port=3306
    )
    cursor = conn.cursor()

    cursor.execute(f"select * from etudiant where no_immatriculation='{num_immatriculation}'")
    # Verfication de l'existence de l'étudiant dans la base de données
    verif_etudiant = cursor.fetchall()
    existe = False

    if len(verif_etudiant) != 0:
        existe = True
        if semestre_etude is not None:
            cursor.execute(
                f"UPDATE etudiant SET semestre_etude='{semestre_etude}' WHERE no_immatriculation='{num_immatriculation}'"
            )
            conn.commit()

        if len(centre_interets) != 0:
            if ecraser_centres_interets == "OUI":
                cursor.execute(
                    f"UPDATE etudiant SET centres_interets='{centre_interets}' WHERE no_immatriculation='{num_immatriculation}'"
                )
                conn.commit()
            else:
                # On récupère les centres d'intérêts de l'étudiant
                cursor.execute(
                    f"Select centres_interets from etudiant where no_immatriculation='{num_immatriculation}'")
                centresInterest = cursor.fetchall()[0][0]
                centresInterest += f", {centre_interets}"
                cursor.execute(
                    f"UPDATE etudiant SET centres_interets='{centresInterest}' WHERE no_immatriculation='{num_immatriculation}'"
                )
                conn.commit()

        if len(cours_suivis) != 0:
            print("Ls liste de tuple cours-suivis est vide")
            cours_suivis_list = cours_suivis.split(",")
            for i in range(len(cours_suivis_list)):
                if i == 0:
                    print(cours_suivis_list[i])
                    cursor.execute("INSERT INTO coursetudiant(id_cours,no_immatriculation)values(%s,%s)",
                                   (cours_suivis_list[i], num_immatriculation))
                    conn.commit()
                else:
                    print(cours_suivis_list[i].replace(" ", ""))
                    cursor.execute("INSERT INTO coursetudiant(id_cours,no_immatriculation)values(%s,%s)",
                                   (cours_suivis_list[i].replace(" ", ""), num_immatriculation))
                    conn.commit()
    return render_template("modification_compte.html", existe=existe)


# Le formulaire pour la propoisition des cours à options
@app.route("/formulaire_proposition")
def formulaire_proposition():
    return render_template("formulaire_proposition_cours.html")


# Récupération des données du formualire pour la recommandation de cours.
@app.route("/proposition_cours", methods=["POST"])
def recom_cours():
    num_immatriculation = request.form.get("num_immatriculation")
    nom = " "
    prenom = " "
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="....",
        database="pt1",
        port=3306
    )
    cursor = conn.cursor()
    cursor.execute(f"select * from etudiant where no_immatriculation='{num_immatriculation}'")
    # Verfication de l'existence de l'étudiant dans la base de données
    verif_etudiant = cursor.fetchall()
    existe = False
    if len(verif_etudiant) != 0:
        # Donc on sait que l'étudiant existe dans la base de données
        existe = True
        # On effectue la requête select pour récupérer son nom et prénom.
        cursor.execute(f"select nom, prenom from etudiant where no_immatriculation='{num_immatriculation}'")
        response = cursor.fetchall()
        nom = response[0][0]
        prenom = response[0][1]
        cours_proposes, planning_coursObligatories, planning_coursProposes = proposition_cours_BD(num_immatriculation)

        return render_template("recom_cours.html", existe=existe, num_immatriculation=num_immatriculation, nom=nom,
                               prenom=prenom, cours_proposes=cours_proposes)

    else:
        return render_template("recom_cours.html", existe=existe, num_immatriculation=num_immatriculation)


# Affichage des informations concernant les cours proposés.
@app.route("/description_cours", methods=["GET"])
def description_cours():
    # Récupération de l'id_cours
    id_cours = request.args['id_cours']
    num_immatriculation = request.args['no_immatriculation']
    message_important = False

    cours_proposes, planning_coursObligatories, planning_coursProposes = proposition_cours_BD(num_immatriculation)
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="....",
        database="pt1",
        port=3306
    )

    cursor = conn.cursor()

    # On récupère le nombre de crédits qu'il a gagné avec les cours à option déjà suivis
    cursor.execute(
        f"select sum(nb_credits) as credit_gagner from coursetudiant, cours where coursetudiant.no_immatriculation ='{num_immatriculation}' and cours.id_cours = coursetudiant.id_cours")

    total_credits = cursor.fetchall()[0][0]

    cursor.execute(
        f"CREATE OR REPLACE VIEW nbrGagne_obg as select sum(nb_credits) as nb_gagne_ob from cours, etudiant where no_immatriculation='{num_immatriculation}' and obligatoire between 1 and semestre_etude")
    cursor.execute("select * from nbrGagne_obg")
    # On récupère le nombre de crédits qu'il a gagné avec les cours obligatoires jusqu'à maintenant
    nbr_creditsOb = cursor.fetchall()[0][0]
    cours = list(filter(lambda cours: cours[0] == id_cours, cours_proposes))[0]

    # calcul pour le nombre de crédits total obtenus par l'étudiant en fonction des cours déjà suivis
    # et les cours obligatoires.
    if cours[5] is not None and total_credits is not None:
        total_credits += cours[5]
        total_credits += nbr_creditsOb
    elif cours[5] is None and total_credits is None:
        total_credits = nbr_creditsOb
    elif cours[5] is None and total_credits is not None:
        total_credits += nbr_creditsOb
    elif cours[5] is not None and total_credits is None:
        total_credits = cours[5] + nbr_creditsOb

    if cours[-1] != '' or cours[-2] != '':
        message_important = True

    return render_template("info_cours.html", id_cours=id_cours, num_immatriculation=num_immatriculation,
                           cours=cours
                           , message_important=message_important, total_credits=total_credits)


@app.route("/calendrier")
def calendrier():
    num_immatriculation = request.args['no_immatriculation']
    id_cours = request.args['id_cours']

    cours_ob = " "

    cours_proposes, planning_coursObligatories, planning_coursProposes = proposition_cours_BD(num_immatriculation)
    # On prend uniquement les cours qui ont l'id cours[0]
    cours_choisi = list(filter(lambda cours: cours[0] == id_cours, planning_coursProposes))

    indice = 0
    for cours in cours_choisi:
        collisions = list(map(lambda cs: (cs[7], cs[8]), filter(lambda c: c[5] == cours[5], cours_choisi)))
        if len(collisions) > 1:
            cours = list(cours)
            cours[7] = list(map(lambda t: t[0], collisions))
            cours[8] = list(map(lambda t: t[1], collisions))
            cours_choisi[indice] = tuple(cours)
        indice += 1

    # liste_cours = planning_coursObligatories

    # Pour l'ajout des propriétés css
    liste_cours = []
    for crs_ob in planning_coursObligatories:
        cours_ob = "cours_ob"
        tuple_cours = list(crs_ob)
        tuple_cours.append(cours_ob)
        corresponding_cours = tuple(tuple_cours)
        liste_cours.append(corresponding_cours)

    h = -1
    for cours in cours_choisi:
        if cours[5] != h:
            cours_ob = "cours_nonOb"
            tuple_cours = list(cours)
            tuple_cours.append(cours_ob)
            corresponding_cours = tuple(tuple_cours)
            liste_cours.append(corresponding_cours)
        h = cours[5]

    # Création du calendrier
    jours = [None, None, None, None, None]
    planning = []
    for i in range(13):
        planning.append(jours.copy())

    jour_indice = {'LU': 0, 'MA': 1, 'ME': 2, 'JE': 3, 'VE': 4}
    for cours in liste_cours:
        indice_jour = jour_indice[cours[4]]
        indice_debut = cours[5] - 8
        indice_fin = cours[6] - 8
        temps = indice_fin - indice_debut
        obligatoire = cours[-1]

        if type(cours[7]) is not list:
            infos_cours = cours[1] + "\n" + cours[2] + " " + cours[7] + " : " + cours[8]
        else:
            infos_cours = cours[1] + "\n" + cours[2]
            for i in range(len(cours[7])):
                infos_cours += " " + cours[7][i] + " : " + cours[8][i]

        planning[indice_debut][indice_jour] = (infos_cours, temps, obligatoire)
        for i in range(indice_debut + 1, indice_fin):
            planning[i][indice_jour] = (infos_cours, -1)

    print(planning)

    return render_template("calendrier_cours.html", planning=planning)


if __name__ == '__main__':
    app.run(debug=True)
