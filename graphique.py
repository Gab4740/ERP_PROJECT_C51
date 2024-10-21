import matplotlib.pyplot as plt
import numpy as np

class Graphique:
    def __init__(self):
        pass

    def tracer_graphique(self, type_graphique, titre, xlabel, ylabel, valeurs, categories=None):
        plt.figure(figsize=(10, 5))

        if type_graphique == 'ligne':
            x = np.arange(len(valeurs))  # Utilisation des indices si aucune valeur X n'est fournie
            plt.plot(x, valeurs, marker='o')
        elif type_graphique == 'barres':
            if categories is None:
                raise ValueError("Pour un graphique à barres, 'categories' doit être fourni.")
            plt.bar(categories, valeurs, color='skyblue')
        elif type_graphique == 'histogramme':
            plt.hist(valeurs, bins=10, color='lightgreen', edgecolor='black')
        else:
            raise ValueError("Type de graphique non reconnu. Utilisez 'ligne', 'barres' ou 'histogramme'.")

        plt.title(titre)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.grid(True)
        plt.show()

# Exemple d'utilisation
if __name__ == '__main__':
    graphique = Graphique()

    # Graphique linéaire
    valeurs_ligne = np.sin(np.linspace(0, 10, 100))
    graphique.tracer_graphique(
        type_graphique='ligne',
        titre='Graphique de Sinus',
        xlabel='Index',
        ylabel='Valeur',
        valeurs=valeurs_ligne
    )

    # Graphique à barres
    categories = ['A', 'B', 'C', 'D']
    valeurs_barres = [10, 20, 15, 25]
    graphique.tracer_graphique(
        type_graphique='barres',
        titre='Graphique à Barres',
        xlabel='Catégories',
        ylabel='Valeurs',
        valeurs=valeurs_barres,
        categories=categories
    )

    # Histogramme
    donnees_histogramme = np.random.randn(1000)
    graphique.tracer_graphique(
        type_graphique='histogramme',
        titre='Histogramme des Données Aléatoires',
        xlabel='Valeurs',
        ylabel='Fréquence',
        valeurs=donnees_histogramme
    )
