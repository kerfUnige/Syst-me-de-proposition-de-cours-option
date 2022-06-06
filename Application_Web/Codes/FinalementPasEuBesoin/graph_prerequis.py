from Codes.FinalementPasEuBesoin.GraphPrerequis.noeud import Node
import mysql.connector
import queue


def createGraph(id_cours: str) -> dict:
    # On crée la racine
    racine = Node(id_cours)
    # On définit les noeuds déjà crée
    dejaCree = set()
    dejaCree.add(racine)
    # On définit les noeuds à explorer
    nonExplore = queue.Queue()
    nonExplore.put(racine)

    dicoPre = dict()

    # On explore les noeuds qui n'ont pas encore été explorés
    while nonExplore.qsize() != 0:
        # Parcours en profondeur
        noeudCourant = nonExplore.get()
        # La valeur du noeud courant est un ensemble vide qui sera rempli au fur à mesure qu'il existe des
        # prerequis pour ce cours.
        if noeudCourant.id_cours not in dicoPre:
            dicoPre[noeudCourant.id_cours] = set()
        # On récupère les predecesseurs du noeudCourant
        pred = noeudCourant.predecesseurs
        # On insère le noeud courant parmis ces prédecesseurs.
        pred.add(noeudCourant)
        # Connexion à la base de données pour récupérer les prerequis du noeud courant.
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            port=3306,
            database="pt1",
            password="..."
        )
        cursor = conn.cursor()
        # On récupère les prerequis.
        query = ""
        query = f"Select * from prerequis where id_cours= '{noeudCourant.id_cours}'"
        cursor.execute(query)
        descd = cursor.fetchall()
        # print(f"Prerequis de {noeudCourant.id_cours}-> {descd}")

        # On vérifie que le noeudCourant ait un descendant
        if len(descd) != 0:
            for d in descd:
                noeudSuivant = Node(d[-1])
                # Si le noeud a été crée il doit être dans l'ensemble des noeuds à explorer afin qu'on puisse l'explorer ou pas
                if noeudSuivant in dejaCree:
                    noeudCourant.descendants.add(noeudSuivant)
                    # les prédécesseurs du noeudCourant sont aussi les
                    # prédécesseurs du noeudSuivant.
                    for p in pred:
                        noeudSuivant.predecesseurs.add(p)
                    # On ajoute le noeudSuivant parmi les valeurs de la clé (noeudCourant)
                    dicoPre[noeudCourant.id_cours].add(noeudSuivant.id_cours)
                else:
                    dicoPre[noeudCourant.id_cours].add(noeudSuivant.id_cours)
                    # On ajoute le noeudSuivant dans l'ensemble des noeuds Crées
                    dejaCree.add(noeudSuivant)
                    # Et on l'ajoute dans l'ensemble des noeuds à explorer
                    nonExplore.put(noeudSuivant)
                    # On définit ces prédécesseurs
                    for p in pred:
                        noeudSuivant.predecesseurs.add(p)
        conn.close()

    # print(f"Dico prerequis\n{dicoPre}")
    return dicoPre
