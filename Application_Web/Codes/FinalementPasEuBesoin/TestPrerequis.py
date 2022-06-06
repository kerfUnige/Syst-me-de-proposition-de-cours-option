from Codes.PropositionCours.Proposition_cours import *


def example():
    dict1 = {"X": {"a", "b", "c"}, "c": {"d", "e"}, "e": {"f"}, "g": {"h"}, "h": {"i"}}
    dict2 = {"f": {"e"}, "e": {"c"}, "d": {"c"}, "c": {"X"}, "b": {"X"}, "a": {"X"}, "i": {"h"}, "h": {"g"}}
    cours_suivis = ["a", "d", "f", "i"]
    ajout = a_comme_prerequis("X", dict1, cours_suivis)
    for course in cours_suivis:
        if course not in ajout:
            ajout += est_prerequis_de(course, dict1, dict2, cours_suivis)
    ajout = list(dict.fromkeys(ajout))
    print(str(ajout))
