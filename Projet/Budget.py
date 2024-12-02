import csv
from datetime import datetime, timedelta
from collections import defaultdict

# Base de données fictive des paiements (initialement vide)
paiements = []

# Calcul du salaire brut, net, des impôts et des taxes
def salaire_brut(salaire_net, taux_impot=0.2, taux_taxe=0.15):
    salaire_brut = salaire_net / (1 - (taux_impot + taux_taxe))
    return salaire_brut

def salaire_net(salaire_brut, taux_impot=0.2, taux_taxe=0.15):
    salaire_net = salaire_brut * (1 - (taux_impot + taux_taxe))
    return salaire_net

def calcul_impots(salaire_brut, taux_impot=0.2):
    impots = salaire_brut * taux_impot
    return impots

def calcul_taxes(salaire_brut, taux_taxe=0.15):
    taxes = salaire_brut * taux_taxe
    return taxes

# Fonction pour enregistrer un paiement
def enregistrer_paiement(salaire_brut, taux_impot=0.2, taux_taxe=0.15):
    impots = calcul_impots(salaire_brut, taux_impot)
    taxes = calcul_taxes(salaire_brut, taux_taxe)
    salaire_net = salaire_net(salaire_brut, taux_impot, taux_taxe)
    
    paiement = {
        'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'salaire_brut': salaire_brut,
        'impots': impots,
        'taxes': taxes,
        'salaire_net': salaire_net
    }
    paiements.append(paiement)

# Fonction pour générer un rapport des paiements
def rapport_paiements():
    # Affichage du rapport complet dans le terminal
    print("Rapport des paiements:")
    for paiement in paiements:
        print(f"Date: {paiement['date']}")
        print(f"Salaire brut: {paiement['salaire_brut']} €")
        print(f"Impôts: {paiement['impots']} €")
        print(f"Taxes: {paiement['taxes']} €")
        print(f"Salaire net: {paiement['salaire_net']} €")
        print("******************************")

# Fonction pour générer un rapport des paiements pour une période donnée (hebdo, mensuel, annuel)
def rapport_periode(période="mensuel"):
    """
    Génère un rapport des paiements pour une période donnée :
    - 'hebdo' pour la semaine,
    - 'mensuel' pour le mois,
    - 'annuel' pour l'année.
    """
    # Date actuelle
    date_aujourdhui = datetime.now()
    
    # Dictionnaire pour organiser les paiements par période
    rapport = defaultdict(list)

    # Filtrer les paiements selon la période
    for paiement in paiements:
        date_paiement = datetime.strptime(paiement['date'], "%Y-%m-%d %H:%M:%S")

        # Selon la période, on filtre les paiements
        if période == "hebdo":
            # Ajouter les paiements faits dans la semaine courante
            if date_aujourdhui - timedelta(days=7) <= date_paiement <= date_aujourdhui:
                rapport['Hebdomadaire'].append(paiement)

        elif période == "mensuel":
            # Ajouter les paiements faits dans le mois courant
            if date_aujourdhui.month == date_paiement.month and date_aujourdhui.year == date_paiement.year:
                rapport['Mensuel'].append(paiement)

        elif période == "annuel":
            # Ajouter les paiements faits cette année
            if date_aujourdhui.year == date_paiement.year:
                rapport['Annuel'].append(paiement)

    # Afficher le rapport
    print(f"Rapport des paiements pour la période : {période.capitalize()}")
    for periode, paiements_periode in rapport.items():
        print(f"\n{periode}:")
        for paiement in paiements_periode:
            print(f"Date: {paiement['date']}")
            print(f"Salaire brut: {paiement['salaire_brut']} $")
            print(f"Impôts: {paiement['impots']} $")
            print(f"Taxes: {paiement['taxes']} $")
            print(f"Salaire net: {paiement['salaire_net']} $")
            print("******************************")

# Fonction pour générer un rapport CSV des paiements
def generer_rapport_csv(filename="rapport_paiements.csv"):
    """
    Génère un fichier CSV contenant tous les paiements enregistrés.
    """
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        # Écrire l'en-tête du fichier CSV
        writer.writerow(["Date", "Salaire brut", "Impôts", "Taxes", "Salaire net"])

        # Écrire les données des paiements
        for paiement in paiements:
            writer.writerow([paiement['date'], paiement['salaire_brut'], paiement['impots'], paiement['taxes'], paiement['salaire_net']])

    print(f"Le rapport a été généré et sauvegardé dans '{filename}'.")


# Affichage du rapport complet
rapport_paiements()

# Rapport par période (hebdomadaire, mensuel, annuel)
rapport_periode("hebdo")
rapport_periode("mensuel")
rapport_periode("annuel")

# Génération d'un fichier CSV de rapport des paiements
generer_rapport_csv("rapport_paiements.csv")
