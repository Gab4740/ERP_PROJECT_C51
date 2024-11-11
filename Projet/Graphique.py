from PySide6.QtWidgets import (QVBoxLayout, QPushButton, QLabel, QLineEdit, QDialog, QComboBox)
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np

class Graphique:
    def __init__(self):
        pass

    def tracer_graphique(self, type_graphique, valeurs, categories=None):
        fig = Figure(figsize=(10, 5))
        canvas = FigureCanvas(fig)

        ax = fig.add_subplot(111)

        if type_graphique == 'ligne':
            x = np.arange(len(valeurs))
            ax.plot(x, valeurs, marker='o')
        elif type_graphique == 'barres':
            if categories is None:
                raise ValueError("Pour un graphique à barres, 'categories' doit être fourni.")
            ax.bar(categories, valeurs, color='skyblue')
        elif type_graphique == 'histogramme':
            ax.hist(valeurs, bins=10, color='lightgreen', edgecolor='black')
        else:
            raise ValueError("Type de graphique non reconnu.")

        ax.set_title('Graphique')
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.grid(True)

        return canvas
    
    def show_graphique_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Créer un Graphique")

        layout = QVBoxLayout()

        type_graphique_label = QLabel("Type de Graphique:")
        self.type_graphique_combo = QComboBox()
        self.type_graphique_combo.addItems(['ligne', 'barres', 'histogramme'])

        titre_label = QLabel("Titre:")
        self.titre_input = QLineEdit()

        xlabel_label = QLabel("Nom de l'axe X:")
        self.xlabel_input = QLineEdit()

        ylabel_label = QLabel("Nom de l'axe Y:")
        self.ylabel_input = QLineEdit()

        valeurs_label = QLabel("Valeurs (séparées par des virgules):")
        self.valeurs_input = QLineEdit()

        categories_label = QLabel("Catégories (pour barres, séparées par des virgules):")
        self.categories_input = QLineEdit()

        create_button = QPushButton("Créer Graphique")
        create_button.clicked.connect(lambda: self.create_graphique(dialog))

        layout.addWidget(type_graphique_label)
        layout.addWidget(self.type_graphique_combo)
        layout.addWidget(titre_label)
        layout.addWidget(self.titre_input)
        layout.addWidget(xlabel_label)
        layout.addWidget(self.xlabel_input)
        layout.addWidget(ylabel_label)
        layout.addWidget(self.ylabel_input)
        layout.addWidget(valeurs_label)
        layout.addWidget(self.valeurs_input)
        layout.addWidget(categories_label)
        layout.addWidget(self.categories_input)
        layout.addWidget(create_button)

        dialog.setLayout(layout)
        dialog.exec()
        
    def create_graphique(self, dialog):
        type_graphique = self.type_graphique_combo.currentText()
        valeurs = list(map(float, self.valeurs_input.text().split(',')))
        categories = self.categories_input.text().split(',') if type_graphique == 'barres' else None

        boss_tab_index = self.tab_widget.indexOf(self.tab_widget.widget(1))  # Assumer que "Boss" est à l'index 1
        if boss_tab_index != -1:
            boss_tab = self.tab_widget.widget(boss_tab_index)

            if hasattr(self, 'graphique_canvas') and self.graphique_canvas is not None:
                self.graphique_canvas.deleteLater()

            graphique = Graphique()
            self.graphique_canvas = graphique.tracer_graphique(type_graphique, valeurs, categories)
            boss_tab.layout().addWidget(self.graphique_canvas)

        dialog.accept()
        
    def create_graphique_auto(self):
        pass