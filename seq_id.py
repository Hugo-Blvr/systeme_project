#  PERMET D'OBTENIR L'ID DE SÉQUENCES AVEC DÉCALAGE POUR TESTER CHAQUE ALIGNEMENT ENTRE LES 2 SÉQUENCES
def calcul_id(seq1, seq2,id_seq):
    # Identifie la séquence la plus longue et la plus courte
    longue, courte = seq1, seq2
    if len(seq1) < len(seq2):
        longue, courte = seq2, seq1

    #  GLISSEMENT DE LA SEQUENCE LA PLUS COURTE SUR LA PLUS LONGUE + CALCUL DU MAX DE SIMILARITE
    max_similarite = 0
    for i in range(len(longue)):
        similarite = sum(c1 == c2 for c1, c2 in zip(courte, longue[i: i+len(courte)]))
        #  ↑ calcule la similarité entre la courte le long de la longue avec un décalage de 1 par itération
        similarite /= len(longue)  # Normalisation par la longueur de la séquence courte

        # Met à jour la similarité max
        if similarite >= id_seq:  # Return car condition atteinte
            return similarite
        if similarite > max_similarite:
            max_similarite = similarite

    return max_similarite


#  PERMET D'OBTENIR UN BOOLEAN QUI COMPARE L'ID ENTRE LES VARIANTS ET LE PARAMETRE D'ID MINIMUM CHOISIS PAR L'UTILISATEUR
def decision(varsA, varsB, id_seq):
    for varA in varsA:  # Chaque variant d'une position dans un replicat A
        for varB in varsB:  # Comparer à tous les variant de cette même position dans le réplicat B
            if calcul_id(varA, varB, id_seq) >= id_seq:
                return True
    return False

def decisionNoseq(varsA, varsB):
    # Créer un ensemble pour les éléments communs
    common_elements = set(varsA) & set(varsB)
    # Initialiser le compteur et l'élément le plus commun
    max_count = 0
    most_common = False
    # Parcourir les éléments communs et compter leurs occurrences dans les deux listes
    for element in common_elements:
        count = varsA.count(element) + varsB.count(element)
        if count > max_count:
            max_count = count
            most_common = element

    # Retourner l'élément le plus commun
    return most_common

    


# ------------------ TEST ----------------------
if __name__ == "__main__":
    a = ['CGT', 'ACTA', 'RRR']
    b = ["AACG", 'CGTC', 'AAAA']

    for i in a:
        for j in b:
            print(f"id_seq entre {i} et {j} : {calcul_id(i,j, id_seq=0.75)}")

    print(decision(a, b, id_seq=0.75))

    a = ['<DUP>']
    b = ['<DUP>']

    print(decisionNoseq(a, b))

# ------------------ AMELIO ----------------------
"""Cree un cache pour eviter de calculer deux fois le score pour les meme sequence ?"""