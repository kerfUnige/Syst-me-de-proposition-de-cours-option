import mysql.connector
from firstOccurence import *


def option_obligatoire_accompli(cours_suivis, option_obligatoire):
    cours_proposees = []
    for x in option_obligatoire:
        y = x + ("Ce cours est en option obligatoire. Il faut valider un des cours parmi l'option obligatoire.",)
        for cours in cours_suivis:
            if wordDictionary(y[0], cours):
                return []
        cours_proposees.append(y)

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
        # même procédure que pour les noms
        if cours[5] == 0 or option_obligatoire_accompli:
            if wordDictionary(interet, str(cours[3])) or wordDictionary(interet, str(cours[4])):
                return True
    return False


def interets(centre_interets, cours_list, cours_suivis, option_obligatoire_accompli):
    cours_proposees = []
    interets_par_nom = []
    for cours in cours_list:
        if cours[0] not in cours_suivis:
            if interet_match_nom(cours, centre_interets, option_obligatoire_accompli):
                interets_par_nom.append((cours[0], cours[1], cours[2], cours[3], cours[4], cours[6], ""))
            if interet_match_obj_des(cours, centre_interets, option_obligatoire_accompli):
                cours_proposees.append((cours[0], cours[1], cours[2], cours[3], cours[4], cours[6], ""))
    return interets_par_nom + cours_proposees


def no_collision(activity, obligatoire):
    for cours_obligatoire in obligatoire:
        if cours_obligatoire[4] == activity[4]:
            if ((activity[5] < cours_obligatoire[5] < activity[6]) or (
                    activity[5] < cours_obligatoire[6] < activity[6])) or (
                    activity[5] == cours_obligatoire[5] and activity[6] == cours_obligatoire[6]):
                return False
    return True


def noeuds_suivis(set, cours_suivis):
    for elm in set:
        if elm not in cours_suivis:
            return False
    return True


def contraintes(periode, planning_cours, obligatoire_courant):
    lecture_counter = 0
    seminar_counter = 0
    possible_seminar_counter = 0
    # on considère qu'un cours ne rentre pas en collision lorsque au moins une séance de séminaire ne rentre pas
    # en revanche on exclut un cours où les séances de cours rentrent en collision avec les cours obligatoires
    for activity in planning_cours:
        if activity[2] == "CR" or activity[2] == "CS":
            lecture_counter += 1
            if periode % 2 == 0:
                if activity[3] != "Printemps" or not no_collision(activity, obligatoire_courant):
                    return 0
            else:
                if activity[3] != "Automne" or not no_collision(activity, obligatoire_courant):
                    return 0
        elif activity[2] == "SE" or activity[2] == "EX" or activity[2] == "TP":
            seminar_counter += 1
            if periode % 2 == 0:
                if activity[3] == "Printemps" and no_collision(activity, obligatoire_courant):
                    possible_seminar_counter += 1
            else:
                if activity[3] == "Automne" and no_collision(activity, obligatoire_courant):
                    possible_seminar_counter += 1
    if (seminar_counter == 0) or (seminar_counter > 0 and possible_seminar_counter > 0):
        return 2
    elif lecture_counter > 0:
        return 1
    else:
        return 0


def a_comme_prerequis(cours, dictionnaire, cours_suivis):
    cours_ajout = []
    if noeuds_suivis(dictionnaire[cours], cours_suivis):
        cours_ajout.append(cours)
    elif cours in dictionnaire:
        for prerequis in dictionnaire[cours]:
            if prerequis not in cours_suivis:
                if prerequis in dictionnaire:
                    cours_ajout += a_comme_prerequis(prerequis, dictionnaire, cours_suivis)
                    if len(cours_ajout) == 0:
                        cours_ajout.append(prerequis)
                else:
                    cours_ajout.append(prerequis)

    return cours_ajout


def est_prerequis_de(cours, a_comme_prerequis_dict, est_prerequis_de_dict, cours_suivis):
    cours_ajout = []
    if cours in est_prerequis_de_dict:
        for prerequis in est_prerequis_de_dict[cours]:
            if prerequis in cours_suivis and prerequis in est_prerequis_de_dict:
                cours_ajout += est_prerequis_de(prerequis, a_comme_prerequis_dict, est_prerequis_de_dict, cours_suivis)
            else:
                cours_ajout += a_comme_prerequis(prerequis, a_comme_prerequis_dict, cours_suivis)
    return cours_ajout


def proposition_cours_no_BD(periode, cours_suivis, centre_interets):
    connexion = mysql.connector.connect(
        host="localhost",
        user="root",
        port=3306,
        database="pt1",
        password="..."
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

    # recherche des cours qui rentrent dans le centre d'intérêt de l'étudiant dans le tableau de cours
    cursor.execute(
        "SELECT id_cours, nom_cours, faculte, objectif, descriptif, option_obligatoire, nb_credits FROM cours WHERE obligatoire = 0 ")
    cours_list = cursor.fetchall()
    # on prend en compte si l'étudiant a validé un cours à option obligatoire
    cours_proposees += interets(centre_interets_list, cours_list, cours_suivis_list, len(cours_proposees) == 0)

    # on construit deux dictionnaires de prérequis
    a_comme_prerequis_dict = dict()
    est_prerequis_de_dict = dict()
    cursor.execute("SELECT * FROM prerequis")
    prerequis = cursor.fetchall()
    for tuple in prerequis:
        if tuple[1] not in a_comme_prerequis_dict:
            a_comme_prerequis_dict[tuple[1]] = {tuple[2]}
        else:
            a_comme_prerequis_dict[tuple[1]].add(tuple[2])
        if tuple[2] not in est_prerequis_de_dict:
            est_prerequis_de_dict[tuple[2]] = {tuple[1]}
        else:
            est_prerequis_de_dict[tuple[2]].add(tuple[1])

    # on vérifie d'abord si les cours déjà proposées ont des cours prérequis que l'étudiant n'a pas déjà validé
    # si c'est le cas, on enlève ce cours et on insère les cours prérequis à valider
    for cours in cours_proposees:
        if cours[0] in a_comme_prerequis_dict and not noeuds_suivis(a_comme_prerequis_dict[cours[0]],
                                                                    cours_suivis_list):
            cours_proposees.remove(cours)
            cours_ajout = a_comme_prerequis(cours[0], a_comme_prerequis_dict, cours_suivis_list)
            for course in cours_ajout:
                cursor.execute(
                    f"SELECT id_cours, nom_cours, faculte, objectif, descriptif, nb_credits FROM cours WHERE id_cours =  '{course}'")
                new_cours = cursor.fetchone()
                x = ()
                if new_cours in option_obligatoire:
                    x = new_cours + (
                    "Ce cours est en option obligatoire. Il faut valider un des cours parmi l'option obligatoire.",)
                else:
                    x = new_cours + ("",)
                if x not in cours_proposees and x[0] not in cours_obligatoire:
                    cours_proposees.append(x)

    # on cherche ensuite les cours qui ont comme prérequis les cours que l'étudiant a déjà validé pour les proposer
    for cours in cours_suivis_list:
        if cours in est_prerequis_de_dict and not noeuds_suivis(est_prerequis_de_dict[cours], cours_suivis_list):
            cours_ajout = est_prerequis_de(cours, a_comme_prerequis_dict, est_prerequis_de_dict, cours_suivis_list)
            for course in cours_ajout:
                cursor.execute(
                    f"SELECT id_cours, nom_cours, faculte, objectif, descriptif, nb_credits FROM cours WHERE id_cours =  '{course}'")
                new_cours = cursor.fetchone()
                x = ()
                if new_cours in option_obligatoire:
                    x = new_cours + (
                    "Ce cours est en option obligatoire. Il faut valider un des cours parmi l'option obligatoire.",)
                else:
                    x = new_cours + ("",)
                if x not in cours_proposees and x[0] not in cours_obligatoire:
                    cours_proposees.append(x)

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
        if len(planning_cours) == 0:  # si le cours n'a pas d'horaires et de salles, alors on l'exclus de la liste de propositions
            cours_proposees = [x for x in cours_proposees if x != cours]
        elif contraintes(periode, planning_cours, obligatoire_courant) == 2:
            x = cours + ("",)
            cours_proposees_possibles.append(x)
            for planning in planning_cours:
                if no_collision(planning, obligatoire_courant):
                    planning_cours_proposees.append(planning)
        elif contraintes(periode, planning_cours, obligatoire_courant) == 1:
            x = cours + (
                "Les séances de séminaires de ce cours rentrent en collision avec les cours obligatoires du semestre.",)
            cours_proposees_possibles.append(x)
            for planning in planning_cours:
                if no_collision(planning, obligatoire_courant):
                    planning_cours_proposees.append(planning)
    cours_proposees_possibles = list(dict.fromkeys(cours_proposees_possibles))
    planning_cours_proposees = list(dict.fromkeys(planning_cours_proposees))

    connexion.close()

    return cours_proposees_possibles, obligatoire_courant, planning_cours_proposees
