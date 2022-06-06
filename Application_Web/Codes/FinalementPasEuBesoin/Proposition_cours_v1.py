import mysql.connector
from Codes.firstOccurence import *
from Codes.FinalementPasEuBesoin.GraphPrerequis.graph_prerequis import *


def option_obligatoire_accompli(cours_suivis, option_obligatoire):
    cours_proposees = []
    for x in option_obligatoire:
        for cours in cours_suivis:
            if wordDictionary(x[0], cours):
                return []
        cours_proposees.append(x)

    return cours_proposees


def interet_match_nom(cours, centre_interets, option_obligatoire_accompli):
    for interet in centre_interets:
        # on ne prend pas un cours à option obligatoire qui satisfait les intérêts de l'étudiant
        # si l'étudiant n'a pas encore validé au moins un cours à option obligatoire, sinon ça va créer des doublons
        # si un cours obligatoire rentre dans les intérêts, on ne le prend pas non plus en compte
        # on ne prend pas un cours qui a déjà été rajouté pour un intérêt antérieur
        if cours[5] == 0 or option_obligatoire_accompli:
            if wordDictionary(interet, cours[1]):
                return True
    return False


def interet_match_obj_des(cours, centre_interets, option_obligatoire_accompli):
    for interet in centre_interets:
        # on ne prend pas un cours à option obligatoire qui satisfait les intérêts de l'étudiant
        # si l'étudiant n'a pas encore validé au moins un cours à option obligatoire, sinon ça va créer des doublons
        # si un cours obligatoire rentre dans les intérêts, on ne le prend pas non plus en compte
        # on ne prend pas un cours qui a déjà été rajouté pour un intérêt antérieur
        if cours[5] == 0 or option_obligatoire_accompli:
            if wordDictionary(interet, str(cours[3])) or wordDictionary(interet, str(cours[4])):
                return True
    return False


def interets(centre_interets, cours_list, cours_suivis, cours_obligatoire, option_obligatoire_accompli):
    cours_proposees = []
    interets_par_nom = []
    for cours in cours_list:
        if cours[0] not in cours_obligatoire and cours[0] not in cours_suivis:
            if interet_match_nom(cours, centre_interets, option_obligatoire_accompli):
                interets_par_nom.append((cours[0], cours[1], cours[2], cours[3], cours[4], cours[6]))
            if interet_match_obj_des(cours, centre_interets, option_obligatoire_accompli):
                cours_proposees.append((cours[0], cours[1], cours[2], cours[3], cours[4], cours[6]))
    return interets_par_nom + cours_proposees


def no_collision(activity, obligatoire):
    for cours_obligatoire in obligatoire:
        if cours_obligatoire[4] == activity[4]:
            if (activity[5] <= cours_obligatoire[5] <= activity[6]) or (
                    activity[5] <= cours_obligatoire[6] <= activity[6]):
                return False
    return True


def noeuds_suivis(set, cours_suivis):
    for elm in set:
        if elm not in cours_suivis:
            return False
    return True


def contraintes(periode, planning_cours, obligatoire_courant):
    seminar_counter = 0
    possible_seminar_counter = 0
    # on considère qu'un cours ne rentre pas en collision lorsqu'au moins une séance de séminaire ne rentre pas
    # en revanche on exclu un cours où les séances de cours rentrent en collision avec les cours obligatoires
    for activity in planning_cours:
        if activity[2] == "CR" or activity[2] == "CS":
            if periode % 2 == 0:
                if activity[3] != "Printemps" or not no_collision(activity, obligatoire_courant):
                    return False
            else:
                if activity[3] != "Automne" or not no_collision(activity, obligatoire_courant):
                    return False
        elif activity[2] == "SE" or activity[2] == "EX":
            seminar_counter += 1
            if periode % 2 == 0:
                if activity[3] == "Printemps" and no_collision(activity, obligatoire_courant):
                    possible_seminar_counter += 1
            else:
                if activity[3] == "Automne" and no_collision(activity, obligatoire_courant):
                    possible_seminar_counter += 1
    if (seminar_counter == 0) or (seminar_counter > 0 and possible_seminar_counter > 0):
        return True
    else:
        return False


def prerequis(cours, prerequis_dict, cours_suivis):
    cours_a_prendre = []
    if len(prerequis_dict.get(cours)) == 0 or noeuds_suivis(prerequis_dict.get(cours), cours_suivis):
        cours_a_prendre.append(cours)
    else:
        for elm in prerequis_dict.get(cours):
            if elm not in cours_suivis:
                cours_valide = prerequis(elm, prerequis_dict, cours_suivis)
                if cours_valide not in cours_a_prendre:
                    for course in cours_valide:
                        cours_a_prendre.append(course)
    return cours_a_prendre


def cours_a_proposer(cours, cours_suivis, obligatoire, ajouts):
    connexion = mysql.connector.connect(
        host="localhost",
        user="root",
        port=3306,
        database="pt1",
        password="..."
    )
    cursor = connexion.cursor(buffered=True)
    cursor.execute(f"SELECT id_cours FROM prerequis WHERE correspCours= '{cours}'")
    cours_possibles = cursor.fetchall()
    if len(cours_possibles) == 0:
        return []
    else:
        for cours_prerequis in cours_possibles:
            if cours_prerequis[0] in cours_suivis:
                ajouts = cours_a_proposer(cours_prerequis[0], cours_suivis, obligatoire, ajouts)
            elif cours_prerequis[0] not in obligatoire:
                prerequis_dict = createGraph(cours_prerequis[0])
                if len(prerequis_dict.get(cours_prerequis[0])) != 0 and not noeuds_suivis(prerequis_dict.get(cours_prerequis[0]),
                                                                                          cours_suivis):
                    cours_possibles = prerequis(cours_prerequis[0], prerequis_dict, cours_suivis)

                    # on insère ensuite les cours dans la liste des cours à proposer
                    for course in cours_possibles:
                        cursor.execute(
                            f"SELECT id_cours, nom_cours, faculte, objectif, descriptif, nb_credits FROM cours WHERE id_cours= '{course}'")
                        cours_planning = cursor.fetchall()
                        ajouts.append(cours_planning[0])
        return ajouts


def proposition_cours(cours_suivis, periode, centre_interets):
    connexion = mysql.connector.connect(
        host="localhost",
        user="root",
        port=3306,
        database="pt1",
        password="...."
    )
    cursor = connexion.cursor(buffered=True)
    cours_suivis_list = []
    centre_interets_list = []
    if cours_suivis != "":
        cours_suivis_list = cours_suivis.split(", ")
    if centre_interets != "":
        centre_interets_list = centre_interets.split(", ")
    cursor.execute("SELECT id_cours FROM cours WHERE obligatoire <> 0 AND obligatoire < " + str(periode))
    cours_obligatoire_suivis = cursor.fetchall()
    for x in cours_obligatoire_suivis:
        cours_suivis_list.append(x[0])
    cours_obligatoire = []
    cursor.execute("SELECT id_cours FROM cours WHERE obligatoire <> 0")
    for elm in cursor:
        cours_obligatoire.append(elm[0])
    cursor.execute(
        "SELECT id_cours, nom_cours, faculte, objectif, descriptif, nb_credits FROM cours WHERE option_obligatoire = 1")
    option_obligatoire = cursor.fetchall()
    # on vérifie que l'étudiant ait validé un cours à option obligatoire ou non
    cours_proposees = option_obligatoire_accompli(cours_suivis_list, option_obligatoire)

    # recherche des cours qui rentrent dans le centre d'intérêt de l'étudiant dans la table avec tous les cours
    cursor.execute(
        "SELECT id_cours, nom_cours, faculte, objectif, descriptif, option_obligatoire, nb_credits FROM cours")
    cours_list = cursor.fetchall()
    if len(cours_proposees) == 0:  # si l'étudiant a validé un cours à option obligatoire
        cours_proposees += interets(centre_interets_list, cours_list, cours_suivis_list, cours_obligatoire, True)
    else:
        cours_proposees += interets(centre_interets_list, cours_list, cours_suivis_list, cours_obligatoire, False)

    # on vérifie si les cours déjà proposées ont des cours prérequis que l'étudiant n'a pas déjà validé
    # si c'est le cas, on enlève ce cours et on insère les cours prérequis à valider
    for cours in cours_proposees:
        prerequis_dict = createGraph(cours[0])
        if len(prerequis_dict.get(cours[0])) != 0 and not noeuds_suivis(prerequis_dict.get(cours[0]),
                                                                        cours_suivis_list):
            cours_proposees = [x for x in cours_proposees if x != cours]
            cours_possibles = prerequis(cours[0], prerequis_dict, cours_suivis_list)

            # on insère ensuite les cours dans la liste des cours à proposer
            for course in cours_possibles:
                cursor.execute(
                    f"SELECT id_cours, nom_cours, faculte, objectif, descriptif, nb_credits FROM cours WHERE id_cours= '{course}'")
                cours_planning = cursor.fetchall()
                cours_proposees.append(cours_planning[0])
    cours_proposees = list(dict.fromkeys(cours_proposees))

    # on cherche les cours qui ont comme prérequis les cours que l'étudiant a déjà validé pour les proposer
    for cours in cours_suivis_list:
        cours_ajoutes = []
        cours_ajoutes = cours_a_proposer(cours, cours_suivis_list, cours_obligatoire, cours_ajoutes)
        for ajout in cours_ajoutes:
            cours_proposees.append(ajout)
    cours_proposees = list(dict.fromkeys(cours_proposees))

    planning_cours_proposees = []
    cours_proposees_possibles = []
    # on récupère les cours obligatoires du semestre actuel
    cursor.execute(
        "SELECT cours.id_cours, nom_cours, type, periode, jour, heure_debut, heure_fin, batiment, num_salle FROM cours, horaires, salle WHERE cours.id_cours = horaires.id_cours AND horaires.id_horaires = salle.id_horaires AND obligatoire = " + str(
            periode))
    obligatoire_courant = cursor.fetchall()

    # on filtre la liste des cours proposées pour n'avoir que des cours dans la bonne période
    # et qui ne rentrent pas en collision avec les cours obligatoires du semestre actuel de l'étudiant
    for cours in cours_proposees:
        cursor.execute(
            "SELECT cours.id_cours, nom_cours, type, periode, jour, heure_debut, heure_fin, batiment, num_salle FROM cours, horaires, salle WHERE cours.id_cours = horaires.id_cours AND horaires.id_horaires = salle.id_horaires AND cours.id_cours = \"" +
            cours[0] + "\"")
        planning_cours = cursor.fetchall()

        if contraintes(periode, planning_cours, obligatoire_courant):
            cours_proposees_possibles.append(cours)
            for planning in planning_cours:
                if no_collision(planning, obligatoire_courant):
                    planning_cours_proposees.append(planning)

    print("\nCours proposées:")
    for cours in cours_proposees_possibles:
        print(cours[0] + " " + cours[1] + " (" + cours[2] + ") - ECTS: " + str(cours[5]))  # + "\nObjectif: " + str(
        # cours[3]) + "\nDescriptif:" + str(cours[4]) + "\n")
    print("\nPlanning:\nCours obligatoires:")
    for cours in obligatoire_courant:
        print(cours)
    print("\nCours à options:")
    for plan in planning_cours_proposees:
        print(plan)
    print("\n\n")

    connexion.close()
