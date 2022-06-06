class Node:
    # Constructeur: méthode qui permet d'instancier un objet
    def __init__(self, id_cours: str):
        self.id_cours = id_cours
        self.descendants = set()
        self.predecesseurs = set()

