import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel,
    QPushButton, QComboBox, QTextEdit
)
from PySide6.QtCore import Qt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class InventoryApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Application d'Inventaire")
        self.setGeometry(100, 100, 800, 600)

        # Données des produits
        self.products_data = {
            "Produit A": [100, 120, 140, 160, 180, 200],
            "Produit B": [80, 90, 100, 110, 120, 130],
            "Produit C": [150, 160, 170, 180, 190, 200],
        }
        self.product_prices = {
            "Produit A": 10,
            "Produit B": 15,
            "Produit C": 20,
        }
        self.months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]

        # Créer un widget central
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Liste déroulante pour sélectionner un produit
        self.product_combo = QComboBox(self)
        self.product_combo.addItems(self.products_data.keys())
        layout.addWidget(QLabel("Sélectionnez un produit:"))
        layout.addWidget(self.product_combo)

        # Bouton pour afficher le graphique
        self.plot_button = QPushButton("Afficher les Ventes", self)
        self.plot_button.clicked.connect(self.plot_sales)
        layout.addWidget(self.plot_button)

        # Affichage des revenus
        self.revenue_display = QTextEdit(self)
        self.revenue_display.setReadOnly(True)
        layout.addWidget(self.revenue_display)

        # Bouton pour calculer le revenu
        self.calculate_button = QPushButton("Calculer le Revenu", self)
        self.calculate_button.clicked.connect(self.calculate_revenue)
        layout.addWidget(self.calculate_button)

        # Créer un canvas pour le graphique
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

    def plot_sales(self):
        product = self.product_combo.currentText()
        sales = self.products_data[product]

        # Effacer l'ancienne figure
        self.figure.clear()

        # Créer un nouvel axe
        ax = self.figure.add_subplot(111)
        ax.bar(self.months, sales, color='blue')
        ax.set_title(f'Ventes de {product} par Mois')
        ax.set_xlabel('Mois')
        ax.set_ylabel('Nombre de Produits Vendus')
        ax.grid(axis='y')

        # Actualiser le canvas
        self.canvas.draw()

    def calculate_revenue(self):
        product = self.product_combo.currentText()
        sales = self.products_data[product]
        total_revenue = sum(sale * self.product_prices[product] for sale in sales)
        self.revenue_display.setPlainText(f"Revenu total pour {product}: ${total_revenue}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = InventoryApp()
    window.show()
    sys.exit(app.exec())
