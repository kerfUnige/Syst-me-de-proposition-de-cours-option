import re
# Algo qui permet de trouver la première occurence d'une chaine de caractere dans une autre.
def first_occurence(strTo_find: str, targetString: str) -> bool:
    strLower = strTo_find.lower()
    targetLower = targetString.lower()
    for i in range(len(targetLower)):
        if (estAlaposition(strLower, i, targetLower)):
            return True
    return False


def wordDictionary(strTo_find: str, targetString: str) -> bool:
    strLower = strTo_find.lower()
    targetLower = targetString.lower()
    wordsList = re.split("[\'| ]", targetLower)
    interetsList = re.split("[\'| ]", strLower)
    unwanted_chars = ".,:!?"
    wordfreq = {}
    for raw_word in wordsList:
        word = raw_word.strip(unwanted_chars)
        if word not in wordfreq and len(word) > 1:
            wordfreq[word] = True
    for interet_mot in interetsList:
        interet_mot_clean = interet_mot.strip(unwanted_chars)
        if interet_mot_clean not in wordfreq:
            return False
    return True


def estAlaposition(strTo_find: str, i: int, targetString: str) -> bool:
    if (len(strTo_find) + i > len(targetString)):
        return False  # Aucune comparaison ne peut être faite.
    else:
        # On procède à la comparaison.
        for j in range(len(strTo_find)):
            if (strTo_find[j] != targetString[i + j]):
                return False
        return True


# Pour le schedule text
def occShecText(dateTo_find: str, schedule: str) -> int:
    date = dateTo_find.lower()
    sche = schedule.lower()
    for i in range(len(sche)):
        position = estAlapositionDate(date, i, sche)
        if position != 0:
            return position
    return 0


def estAlapositionDate(dateTo_find: str, i: int, schedule: str) -> int:
    if (len(dateTo_find) + i > len(schedule)):
        return 0  # Aucune comparaison ne peut être faite.
    else:
        # On procède à la comparaison.
        j = 0
        while j < len(dateTo_find):
            if dateTo_find[j] != schedule[i + j]:
                return 0
            j += 1
        # Pour récupérer l'heure directement.
        return (i + j - 1) + 2