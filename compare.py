import seq_id as id


def compare(input_files, distance_pos=10, seq_id=0.75):
    dico_communVar = {}  # Création d'un dictionnaire pour le nb de variant commun entre paire de réplicats
    dico_communNoSeq = {}  

    for id_echantillon in input_files:  # Boucle sur les tuples contenant les vcf d'un échantillon
        dico_communVar[id_echantillon] = {}  # Création d'un dictionnaire par échantillon dans le dico dico_communVar
        dico_communNoSeq[id_echantillon] = {}
        dico_replicats = {}  # Création d'un dictionnaire pour les variants avec séquence(s)
        dico_no_seq = {}  # Création d'un dictionnaire pour les variants sans séquence 

        # AJOUT DE CHAQUE SEQUENCE DE VARIANT EN FONCTION DE SON REPLICAT ET DE SON ID (CHROM + POS) DANS DICO ADEQUATE
        for vcf_replicat in input_files[id_echantillon]:  # Boucle sur les fichiers vcf de l'échantillon
            id_rep = vcf_replicat.split('/')[-1].split('.')[0]  # Définis l'id du réplicat
            dico_replicats[id_rep] = {}  # Création d'un dictionnaire par replicat dans le dico dico_replicats
            dico_no_seq[id_rep] = {}  

            with open(vcf_replicat, 'r') as vcf:  # Ouverture du vcf (fermeture auto avec 'with open')
                for ligne in vcf:  # Boucle sur les lignes du fichier vcf
                    if not ligne.startswith('#'):  # Non prise en compte des infos commenter
                        infos = ligne.strip().split("\t")  # Split des infos par colonnes
                        pos_variant = f"{infos[1]}"  # Définis la position du variant
                        seq_variant = infos[4]  # Définis la séquence du variant

                        # Classification des variants selon qu'ils ont une séquence ou non
                        if seq_variant.startswith("<"):
                            if pos_variant not in dico_no_seq[id_rep]:
                                dico_no_seq[id_rep][pos_variant] = [seq_variant]
                            else:
                                dico_no_seq[id_rep][pos_variant].append(seq_variant)
                        else:
                            if pos_variant not in dico_replicats[id_rep]:
                                dico_replicats[id_rep][pos_variant] = [seq_variant]
                            else:
                                dico_replicats[id_rep][pos_variant].append(seq_variant)


        #  DÉNOMBREMENT DES VARIANT COMMUN (EN FONCTION DES PARAMÈTRES) DES REPLICATS, DEUX A DEUX (A,B)
        for id_repA in dico_replicats:  # Boucle sur les id_rep contenu dans dico_replicats
            vars_repA = sorted(dico_replicats[id_repA].items(), key=lambda items: int(items[0]))
            #  ↑ Liste triée par position du dico (id_variant,[séquence(s)]) du réplicat A pour pouvoir optimiser la comparaison
            for id_repB in dico_replicats:  # Boucle de nouveau sur id_rep pr comparaison
                if id_repA == id_repB:  # Empêche comparaison intra_replicats
                    continue
                
                id_reps = sorted((id_repA, id_repB))  # Liste triée des id des réplicats comparés
                id_comp = f"{id_reps[0]}_{id_reps[1]}"  # Définis l'id de la comparaison
                if id_comp not in dico_communVar[id_echantillon]:  # Création d'un dico par comparaison dans le dico dico_communVar
                    dico_communVar[id_echantillon][id_comp] = 0
                else:  # Empêche les comparaisons doubles (car id de comparaison triés)
                    continue

                vars_repB = sorted(dico_replicats[id_repB].items(), key=lambda items: int(items[0]))
                #  ↑ Liste triée par position du dico (id_variant : séquence(s)) du réplicat B

                ligne_repA, ligne_repB = 0, 0
                # Initialisation des compteurs pour parcourir les listes de variants de deux réplicats différents
                while ligne_repA < len(vars_repA) and len(vars_repB) != 0:
                    # Boucle pour parcourir tous les variants du réplicat A tant qu'il y a des variants dans le réplicat B à comparer

                    id_varA = vars_repA[ligne_repA][0]
                    pos_varA, seq_varA = int(id_varA), dico_replicats[id_repA][id_varA]
                    # Extraction de l'identifiant, de la position et des la séquence(s) du variant actuel du réplicat A

                    id_varB = vars_repB[ligne_repB][0]
                    pos_varB, seq_varB = int(id_varB), dico_replicats[id_repB][id_varB]
                    # Extraction de l'identifiant, de la position et de la séquence(s) du variant actuel du réplicat B

                    condition_pos = pos_varB - distance_pos <= pos_varA <= pos_varB + distance_pos
                    # Vérification si la position du variant de A est dans la plage de tolérance spécifiée autour du variant de B

                    # Comparaison des variants en fonction de la position et de la similarité des séquences
                    if condition_pos:
                        if id.decision(seq_varA, seq_varB, seq_id):
                            dico_communVar[id_echantillon][id_comp] += 1
                            del vars_repB[ligne_repB]
                            ligne_repA += 1
                            ligne_repB = 0
                            # Si les séquences sont suffisamment similaires selon la fonction de décision, le variant est compté comme commun, et on passe au variant suivant dans A et réinitialise le compteur pour B
                        else: ligne_repB += 1
                        # Si les séquences ne sont pas suffisamment similaires, on passe au variant suivant dans B
                         
                    else:
                        if pos_varA > pos_varB + distance_pos: del vars_repB[ligne_repB]
                        # Si la position du variant A est au-delà de la plage de tolérance du variant B, le variant B est supprimé de la liste pour optimisation
                        else:
                            ligne_repA += 1
                            ligne_repB = 0
                            # Si le variant A est avant la plage de tolérance de B, on passe au variant suivant dans A et réinitialise le compteur pour B

                    if len(vars_repB) == ligne_repB:
                        ligne_repA += 1
                        ligne_repB = 0
                        # Si tous les variants de B ont été parcourus pour un variant spécifique de A, passer au prochain variant dans A et réinitialiser le compteur pour B
                        # Utile pour les conditions de position superieure a la position max du repB

        
        for id_repA in dico_no_seq:  # Boucle sur les id_rep contenu dans dico_replicats
            vars_repA = sorted(dico_no_seq[id_repA].items(), key=lambda items: int(items[0]))
            for id_repB in dico_no_seq:
                if id_repA == id_repB:
                    continue
                id_reps = sorted((id_repA, id_repB))
                id_comp = f"{id_reps[0]}_{id_reps[1]}"
                if id_comp not in dico_communNoSeq[id_echantillon]: dico_communNoSeq[id_echantillon][id_comp] = {}
                else: continue
                vars_repB = sorted(dico_no_seq[id_repB].items(), key=lambda items: int(items[0]))
                ligne_repA, ligne_repB = 0, 0
                while ligne_repA < len(vars_repA) and len(vars_repB) != 0:
                    id_varA = vars_repA[ligne_repA][0]
                    pos_varA, seq_varA = int(id_varA), dico_no_seq[id_repA][id_varA]
                    id_varB = vars_repB[ligne_repB][0]
                    pos_varB, seq_varB = int(id_varB), dico_no_seq[id_repB][id_varB]
                    seq_varB = dico_no_seq[id_repB][id_varB]
                    condition_pos = pos_varB - distance_pos <= pos_varA <= pos_varB + distance_pos
                    if condition_pos and id.decisionNoseq(seq_varA, seq_varB):
                        if id.decisionNoseq(seq_varA, seq_varB) not in dico_communNoSeq[id_echantillon][id_comp]:
                            dico_communNoSeq[id_echantillon][id_comp][id.decisionNoseq(seq_varA, seq_varB)] = 1
                        else:
                            dico_communNoSeq[id_echantillon][id_comp][id.decisionNoseq(seq_varA, seq_varB)] += 1

                        del vars_repB[ligne_repB]
                        ligne_repA += 1
                        ligne_repB = 0
                    else:
                        if pos_varA > pos_varB + distance_pos:
                            del vars_repB[ligne_repB]
                        else:
                            ligne_repA += 1
                            ligne_repB = 0
                    if len(vars_repB) == ligne_repB:
                        ligne_repA += 1
                        ligne_repB = 0
    return dico_communVar,dico_communNoSeq


# ------------------ TEST ----------------------
if __name__ == "__main__":
    input_files = {
        "P15":["../Data/P15/P15-1.trimed1000.sv_sniffles.vcf",
        "../Data/P15/P15-2.trimed1000.sv_sniffles.vcf",
        "../Data/P15/P15-3.trimed1000.sv_sniffles.vcf"],
       "P30":["../Data/P30/P30-1.trimed1000.sv_sniffles.vcf",
        "../Data/P30/P30-3.trimed1000.sv_sniffles.vcf",
        "../Data/P30/P30-2.trimed1000.sv_sniffles.vcf"]}

    a, b = compare(input_files, 1, 1)
    for echSEQ, echNOSEQ in zip(a, b):
        print("")
        print(f"--------------{echSEQ}--------------")
        for comp, nb, compnoseq, nbnoseq in zip(a[echSEQ].keys(), a[echSEQ].values(), b[echNOSEQ].keys(), b[echNOSEQ].values()):
            print(f"{comp} : {nb}, {sum(nbnoseq.values())} : {', '.join(f'{i}:{nb_occurence}' for i, nb_occurence in nbnoseq.items())}")

