# Script de calcul des coûts par catégorie

Ce script permet de calculer le coût total pour chaque catégorie de termes de recherche dans un fichier CSV donné.

## Prérequis

Avant d'utiliser ce script, assurez-vous d'avoir les éléments suivants installés :

- Python (version 3.11)
- pip (outil de gestion des packages Python)

## Installation

1. Clonez ou téléchargez ce dépôt sur votre machine.

2. Ouvrez un terminal ou une invite de commandes et naviguez jusqu'au répertoire du script.

3. Installez les dépendances en exécutant la commande suivante :
   `pip install -r requirements.txt`

   Cela installera toutes les bibliothèques requises pour exécuter le script.

## Utilisation

1. Placez votre fichier CSV contenant les données dans le répertoire `Desktop/test` du projet et renommez-le en `data.csv`.

2. Renommez le fichier `termes.json.exemple` en `termes.json`.

3. Renseignez les termes de recherche en respectant la structure du fichier.

4. Exécutez le script en exécutant la commande suivante dans le terminal :
   `python script.py` ou `py script.py` ou autre, selon votre installation.

5. Les résultats seront affichés dans la console, présentant le coût total pour chaque catégorie de termes de recherche.

6. Les résultats seront également exportés dans un fichier CSV nommé `resultats.csv` dans le même répertoire que le script.

## Exemple de structure de fichier CSV

Assurez-vous que votre fichier CSV suit la structure suivante :


```
Terme de recherche,Coût
Recherche 1,10.50
Recherche 2,15.75
Recherche 3,5.25
...
```


- La première ligne du fichier CSV doit contenir les en-têtes des colonnes (Terme de recherche, Coût).
- Les termes de recherche et les coûts correspondants doivent être placés dans les colonnes appropriées.
- Le fichier peut contenir d'autres colonnes, qui seront ignorées.


