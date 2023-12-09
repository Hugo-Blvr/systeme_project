import os
import sys

def find_fichiers_vcf(dossier):
    fichiers_vcf = []
    for racine, dossiers, fichiers in os.walk(dossier):
        for fichier in fichiers:
            if fichier.endswith('.vcf'):
                chemin_complet = os.path.join(racine, fichier)
                fichiers_vcf.append(chemin_complet)
    return fichiers_vcf


def definir_echantillon(dossier):
    fichiers_vcf = find_fichiers_vcf(dossier)
    dico_fichier = {}
    for fichier_vcf in fichiers_vcf:
        id_echantillon = fichier_vcf.split('/')[-1].split('-')[0]
        if id_echantillon not in dico_fichier:
            dico_fichier[id_echantillon] = []
        dico_fichier[id_echantillon].append(fichier_vcf)

    liste_fichiers = dico_fichier
    return liste_fichiers
