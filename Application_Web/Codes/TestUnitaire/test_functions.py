import unittest
from Codes.firstOccurence import wordDictionary
from Codes.PropositionCours.Proposition_cours import *
from app import app



class Test_functions(unittest.TestCase):
    def test_wordDictionary(self):
        TargetString = "Mon chat! est beau sous le ciel bleu"
        StringTofind = "Ciel!"
        self.assertTrue(wordDictionary(StringTofind, TargetString))

    def test_noeuds_suivis(self):
        ensemble_prerequis = {"11MX001", "11MX002", "11MX003"}
        cours_suivis = ["11MX001", "11MX002", "11MX004"]
        self.assertFalse(noeuds_suivis(ensemble_prerequis, cours_suivis))

    def test_a_comme_prerequis(self):
        dictionnaire = {"c1": {"c2", "c3"}, "c6": {"c7", "c8", "c9", "c10"}, "c3": {"c7", "c8"}, "c7": {"c15"}}
        cours_suivis = ["c10", "c9", "c2"]
        self.result = list(a_comme_prerequis("c1", dictionnaire, cours_suivis))
        self.excepted = ["c8", "c15"]
        # L'instruction ci-dessous compare les éléments d'une liste indépendamment de l'ordre des éléments
        self.assertCountEqual(self.excepted, self.result)

    def test_est_prerequis_de(self):
        dict1 = {"X": {"a", "b", "c"}, "c": {"d", "e", "f"}, "e": {"f"}, "g": {"h"}, "h": {"i"}}
        dict2 = {"f": {"e", "c"}, "e": {"c"}, "d": {"c"}, "c": {"X"}, "b": {"X"}, "a": {"X"}, "i": {"h"}, "h": {"g"}}
        cours_suivis = ["a", "d", "f", "i"]
        ajout = a_comme_prerequis("X", dict1, cours_suivis)
        for course in cours_suivis:
            if course not in ajout:
                ajout += est_prerequis_de(course, dict1, dict2, cours_suivis)
        ajout = list(dict.fromkeys(ajout))
        expected = ["e", "h", "b"]
        self.assertCountEqual(expected, ajout)


class Flask_testRoutes(unittest.TestCase):
    def test_description(self):
        tester = app.test_client(self)
        response = tester.get('/description_cours?id_cours=11X008&no_immatriculation=10-300-30')
        self.assertEqual(response.status_code, 200)
    # On teste l'algo pour le calcul du nombre de crédits gagné apr l'étudiant
    def test_nbCreditsGagner(self):
        tester = app.test_client(self)
        expected = b'171.5'
        response = tester.get('/description_cours?id_cours=11X008&no_immatriculation=10-300-30')
        self.assertIn(expected, response.data)


if __name__ == "__main__":
    unittest.main()
