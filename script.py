import csv
import os
import json
from tabulate import tabulate
from termcolor import colored

# Configuration
file_name = 'data.csv'

current_user_path = os.getcwd()

# Obtention du chemin absolu du fichier json dans le dossier courant
json_file_path = os.path.join(current_user_path, 'termes.json')

# Obtention du chemin absolu du fichier CSV dans le dossier courant
csv_file_path = os.path.join(current_user_path, file_name)

# Lecture du fichier JSON et stockage des termes de recherche dans specific_terms
with open(json_file_path, 'r') as json_file:
    specific_terms = json.load(json_file)

# Affichage des informations
print(colored("###################################################", "cyan"))
print(colored(f"Termes de recherches : {specific_terms}", "yellow"))
print(colored("###################################################", "cyan"))

# Vérification de l'existence du fichier CSV
if not os.path.exists(csv_file_path):
    print(colored(f"Erreur : Le fichier CSV '{file_name}' n'a pas été trouvé dans le dossier '{directory_path}'.", "red"))
    exit(1)

# Dictionnaire pour stocker les totaux
totals = {'divers': 0}
total_cost_column = 0

try:
    # Ouverture du fichier CSV
    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)

        # Vérification des en-têtes requis
        if 'Terme de recherche' not in header or 'Coût' not in header:
            print(colored("Erreur : Les en-têtes 'Terme de recherche' et 'Coût' sont requis dans le fichier CSV.", "red"))
            exit(1)

        # Récupération des index des colonnes
        term_index = header.index('Terme de recherche')
        cost_index = header.index('Coût')

        # Lecture du fichier CSV
        for row in reader:
            # Vérification du nombre de colonnes
            if len(row) != len(header):
                print(colored(f"Attention : La ligne {reader.line_num} ne contient pas le bon nombre de colonnes.", "yellow"))
                continue

            term = row[term_index]
            cost_str = row[cost_index].replace(',', '.')

            # Vérification de la validité du coût
            try:
                cost = float(cost_str)
            except ValueError:
                print(colored(f"Attention : La valeur du coût '{cost_str}' à la ligne {reader.line_num} n'est pas valide.", "yellow"))
                continue

            found_specific_term = False
            for word in specific_terms:
                if word.lower() in term.lower():
                    found_specific_term = True
                    if word not in totals:
                        totals[word] = 0
                    totals[word] += cost
                    break

            if not found_specific_term:
                totals['divers'] += cost

            total_cost_column += cost


    # Préparation du tableau des totaux
    table = []
    for category, total_cost in totals.items():
        total_cost = round(total_cost, 2)
        table.append([category, f"{total_cost} €"])

    # Ajoute une ligne de coût total dans le csv
    total_cost_column = round(total_cost_column, 2)
    table.append([colored("Total", "red"), colored(f"{total_cost_column} €", "red")])


    # Affichage du tableau
    print(tabulate(table, headers=[colored("Catégorie", "cyan"), colored("Coût Total (€)", "cyan")], tablefmt="fancy_grid"))

except FileNotFoundError:
    print(colored(f"Erreur : Le fichier CSV '{file_name}' n'a pas été trouvé.", "red"))
    exit(1)
except csv.Error as e:
    print(colored(f"Erreur lors de la lecture du fichier CSV : {e}", "red"))
    exit(1)
