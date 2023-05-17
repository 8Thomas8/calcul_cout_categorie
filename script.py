import csv
import os
import json
from tabulate import tabulate
from termcolor import colored

# Configuration
file_name = 'data.csv'

current_user_path = os.getcwd()

# Chemin du fichier CSV de sortie
output_csv_file = 'resultats.csv'

# Obtention du chemin absolu du fichier json dans le dossier courant
json_file_path = os.path.join(current_user_path, 'termes.json')

# Obtention du chemin absolu du fichier CSV dans le dossier courant
csv_file_path = os.path.join(current_user_path, file_name)

# Lecture du fichier JSON et stockage des termes de recherche dans specific_terms
with open(json_file_path, 'r') as json_file:
    categories_terms = json.load(json_file)

# Vérification de l'existence du fichier JSON
if not os.path.exists(json_file_path):
    print(colored(f"Erreur : Le fichier JSON 'termes.json' n'a pas été trouvé dans le dossier '{json_file_path}'.", "red"))
    exit(1)

# Vérification de l'existence du fichier CSV
if not os.path.exists(csv_file_path):
    print(colored(f"Erreur : Le fichier CSV '{file_name}' n'a pas été trouvé dans le dossier '{csv_file_path}'.", "red"))
    exit(1)

# Dictionnaire pour stocker les totaux par catégorie et par terme de recherche
category_term_totals = {}

# Dictionnaire pour stocker les totaux par catégorie
category_totals = {}

# Total pour la catégorie "divers"
divers_total = 0

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
            for category, terms in categories_terms.items():
                for word in terms:
                    if word.lower() in term.lower():
                        category_term_key = (category, word)
                        if category_term_key not in category_term_totals:
                            category_term_totals[category_term_key] = 0
                        category_term_totals[category_term_key] += cost
                        found_specific_term = True
                        break

                if found_specific_term:
                    if category not in category_totals:
                        category_totals[category] = 0
                    category_totals[category] += cost
                    break

            if not found_specific_term:
                category_term_key = ("divers", "")
                if category_term_key not in category_term_totals:
                    category_term_totals[category_term_key] = 0
                category_term_totals[category_term_key] += cost
                divers_total += cost

    # Préparation du tableau des totaux
    table = []

    # En-têtes du tableau
    table.append([colored("Catégorie", "cyan"), colored("Terme de recherche", "cyan"), colored("Coût Total (€)", "cyan")])

    for category, terms in categories_terms.items():
        category_total = 0  # Total pour la catégorie

        # Ligne de catégorie
        table.append([colored(category, "cyan"), '', ''])

        for term in terms:
            if (category, term) in category_term_totals:
                total_cost = round(category_term_totals[(category, term)], 2)
                table.append(['', term, f"{total_cost} €"])
                category_total += total_cost

        category_total = round(category_total, 2)
        table.append(['', colored("Total", "red"), colored(f"{category_total} €", "red")])

    # Ligne de la catégorie "divers"
    table.append([colored("divers", "cyan"), '', ''])
    table.append(['', colored("Divers", "cyan"), f"{round(divers_total, 2)} €"])

    # Ligne de total final
    total_cost_all_categories = sum(category_term_totals.values())
    table.append([colored("Total (toutes catégories)", "red"), '', colored(f"{total_cost_all_categories:.2f} €", "red")])

    # Calcul du total de la colonne "Coût"
    total_cost_csv = sum(category_term_totals.values())

    # Affichage du total de la colonne "Coût"
    table.append([colored("Total (colonne Coût)", "yellow"), '', colored(f"{total_cost_csv:.2f} €", "yellow")])

    # Affichage du tableau
    print(tabulate(table, tablefmt="fancy_grid"))

except FileNotFoundError:
    print(colored(f"Erreur : Le fichier CSV '{file_name}' n'a pas été trouvé.", "red"))
    exit(1)
except csv.Error as e:
    print(colored(f"Erreur lors de la lecture du fichier CSV : {e}", "red"))
    exit(1)

# Vérification de l'existence du fichier CSV de sortie
if os.path.exists(output_csv_file):
    os.remove(output_csv_file)
    print(f"Le fichier CSV existant '{output_csv_file}' a été supprimé.")
    
try:
    # Ouverture du fichier CSV de sortie en mode écriture
    with open(output_csv_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)

        # Écriture des en-têtes dans le fichier CSV
        writer.writerow(["Catégorie", "Terme de recherche", "Coût Total (€)"])

        # Écriture des lignes de données dans le fichier CSV
        for category, terms in categories_terms.items():
            category_total = 0

            # Ligne de catégorie
            writer.writerow([category])

            for term in terms:
                if (category, term) in category_term_totals:
                    total_cost = round(category_term_totals[(category, term)], 2)
                    writer.writerow(['', term, total_cost])
                    category_total += total_cost

            # Ligne de total pour la catégorie
            writer.writerow(['', 'Total', category_total])

        # Ligne de la catégorie "divers"
        writer.writerow(["divers", "Divers", divers_total])

        # Ligne de total final
        writer.writerow(['Total (toutes catégories)', '', total_cost_all_categories])

        # Ligne du total de la colonne "Coût"
        writer.writerow(['Total (colonne Coût)', '', total_cost_csv])

    print(f"Les résultats ont été exportés dans le fichier CSV : {output_csv_file}")

except IOError:
    print(f"Erreur lors de l'écriture dans le fichier CSV : {output_csv_file}")
