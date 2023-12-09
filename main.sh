#!/bin/bash

# Valeurs par défaut pour distance et id_sequence
distance_default=10
id_sequence_default=0.75

# Fonction pour afficher l'aide
show_help() {
    echo "Usage: $0 [path] [distance] [id_sequence]"
    echo ""
    echo "Options:"
    echo "  -h, --help           Affiche ce message d'aide"
    echo "  -p, --path [path]    *Obligatoire; Spécifie le chemin du dossier à parcourir"
    echo "  -d, --distance [distance] Distance nucléotidique minimale requise pour considérer des variants communs entre eux (default: $distance_default)"
    echo "      doit être supérieure ou égale à 0"
    echo "  -id, --id_sequence [id_sequence] Identité de séquence minimale requise pour considérer des variants communs entre eux (default: $id_sequence_default)"
    echo "      doit être inclus entre 0 et 1 compris"
    echo ""
}

# Initialiser les variables avec les valeurs par défaut
distance=$distance_default
id_sequence=$id_sequence_default

# Parcourir les arguments ($0 : 'main.sh' $1 -parametre $2 valeur)
while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            show_help
            exit 0
            ;;
        -p|--path)
            path="$2"
            shift # passer l'argument
            ;;
        -d|--distance)
            distance="$2"
            shift # passer l'argument
            ;;
        -id|--id_sequence)
            id_sequence="$2"
            shift # passer l'argument
            ;;
        *)
            echo "Option invalide: $1" 
            show_help
            exit 1
            ;;
    esac
    shift # passer l'option
done

# Vérifier si le chemin a été fourni
if [ -z "$path" ]; then
    echo "Indiquer un chemin d'entrée"
    show_help
    exit 1
fi

# Vérifier les bornes pour -d (distance)
if ! [[ "$distance" =~ ^[0-9]+$ ]] || [ "$distance" -lt 0 ]; then
    echo "La distance doit être un nombre entier supérieur ou égal à 0"
    show_help
    exit 1
fi

# Vérifier les bornes pour -id (identité de séquence)
if ! [[ "$id_sequence" =~ ^[0-9]+(\.[0-9]+)?$ ]] || (( $(echo "$id_sequence < 0 || $id_sequence > 1" | bc -l) )); then
    echo "L'identité de séquence doit être compris entre 0 et 1"
    show_help
    exit 1
fi

# Exécute communVar.py avec les valeurs fournies
python3 interface.py "$path" "$distance" "$id_sequence"
