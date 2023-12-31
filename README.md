# À propos de système_project

système_project est un outil conçu pour la détection et l'analyse de variants génétiques communs entre différents fichiers au format VCF (Variant Call Format). Cet outil offre une solution efficace et personnalisable pour comparer les fichiers VCF  à travers une interface graphique interactif. Il facilite l'identification des variants génétiques partagés entre différents réplicats d'un même échantillon, permettant ainsi une meilleure compréhension des données génomiques.
Les variants sans séquences [&lt;DEL&gt;, &lt;DUP&gt;, &lt;INS&gt;...] sont dissociés des variants avec séquences. 

#### Fonctionnalités

- Détection de variants communs : compare efficacement les fichiers VCF pour identifier les variants communs entre réplicats d'un même échantillon.
- Personnalisation des paramètres de comparaison : possibilité de définir des critères spécifiques pour la comparaison des variants.

## Paramètres d'entrée

Le script prend en entrée trois paramètres :

- -p ou --path : Chemin du dossier contenant les fichiers VCF à analyser. Tous les dossiers et sous-dossiers seront explorés à partir de ce chemin. Ce paramètre est obligatoire.
- -d ou --distance : Distance nucléotidique minimale requise (valeur par défaut : 10) nécessaire pour considérer des variants comme communs. Doit être comprise entre 0 et 1 000 000.
- -id ou --id_sequence : Seuil d'identité de séquence minimale (valeur par défaut : 0.75) nécessaire pour considérer des variants comme communs. Doit être compris entre 0 et 1.
  
## Formatage des noms de fichiers VCF

Les fichiers VCF doivent suivre un formatage spécifique pour être traités correctement commençant par le nom de l'échantillon suivi par le nom du réplicat séparés par un tiret "-" et finissant par l'extension ".vcf" :

- Format correct :  ech1-rep1.vcf ; ech1-rep1.xx.vcf
- Format incorrect : ech1.vcf ; ech1_rep1.vcf

## Interface Graphique
Une interface graphique est créée en sortie pour une lecture graphique des résultats. L'utilisateur peut également refaire des analyses avec des paramètres différents directement depuis cette même interface.

![image](https://github.com/Hugo-Blvr/systeme_project/assets/152957598/974d375b-3a17-49b6-a093-1c12d8e10ddd)

1) Chaque échantillon est traité dans un onglet distinct
2) Permet d'inclure ou non les variants communs sans séquences dans le diagramme (3), par défaut les data_noseq sont inclus
3) Diagramme montrant le nombre de variants communs entre paire de réplicats
4) Permet de choisir la paire de réplicats utilisée pour le pie chart (6), affiche par défaut la paire avec le plus de variants communs
5) Affiche textuellement la répartition des types de variants communs de la paire de réplicats choisie (4)
6) Pie chart de la répartition des types de variants communs de la paire de réplicats choisie (4)
7) Permet de redéfinir le paramètre -d pour un recalcul (9)
8) Permet de redéfinir le paramètre -id pour un recalcul (9)
9) Permet de relancer une nouvelle analyse à partir des paramètres définis par (7) et (8)

## Dépendances (module)
Ce logiciel dépend des packages matplotlib et PyQt5. Si vous ne les avez jamais installés copiez ces lignes sur votre terminal pour les installer :

    $ sudo apt install python3-matplotlib
    $ sudo apt install python3-pyqt5

## TEST
Afin de tester le logiciel un dossier contenant des fichiers .vcf nommés correctement vous est proposé. Vous devriez obtenir les mêmes résultats que sur l'image de l'interface ci-dessus avec les paramètres par défaut : 
    
    $ ./main.sh -p votrePath/data
En remplacent 'votrePath' par le chemin d'accés au dossier data.

## Interprétation

### Interprétation de l'Histogramme
- **Réplicats de Mauvaise Qualité** : Si un réplicat, comme P15-2 dans l'exemple test, montre peu de variants communs avec les autres, cela peut indiquer une qualité inférieure, des erreurs de séquençage, ou des problèmes de manipulation de l'échantillon.
- **Impact sur l'Analyse Générale** : La faible qualité d'un réplicat peut fausser l'analyse globale, entraînant des conclusions erronées. Il est donc essentiel d'identifier et d'exclure ou de réexaminer de tels réplicas.
### Interprétation du Pieplot
- **Répartition des Types de Variants** : Le pieplot fournit une vue d'ensemble de la distribution des différents types de variants. Une répartition équilibrée ou une prédominance de certains types peut indiquer des caractéristiques spécifiques de l'échantillon ou de la condition étudiée.
- **Importance des Variants Séquencés** : Un pourcentage élevé de variants séquencés est préférable car il offre une meilleure compréhension des modifications génétiques. Cela est particulièrement important dans les études visant à identifier des mutations précises ou des marqueurs génétiques.

En somme, l'interprétation des résultats de système_project nécessite une analyse et une compréhension du contexte biologique. L'utilisateur doit prêter attention à la qualité des réplicats et à la répartition des types de variants pour tirer des conclusions précises et fiables.
