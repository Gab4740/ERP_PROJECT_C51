import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton
)
from employe import EmployeWindow  # Assurez-vous que le fichier employe.py est dans le même répertoire

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Menu Principal")
        self.setGeometry(100, 100, 300, 200)

        # Créer un widget central
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Créer un layout vertical
        layout = QVBoxLayout(central_widget)

        # Bouton Employé
        self.employe_button = QPushButton("Employé", self)
        self.employe_button.clicked.connect(self.open_employe)
        layout.addWidget(self.employe_button)

        # Bouton Succursale
        self.succursale_button = QPushButton("Succursale", self)
        layout.addWidget(self.succursale_button)

        # Bouton Client
        self.client_button = QPushButton("Client", self)
        layout.addWidget(self.client_button)

        # Bouton Quitter
        self.quit_button = QPushButton("Quitter", self)
        self.quit_button.clicked.connect(self.close)
        layout.addWidget(self.quit_button)

    def open_employe(self):
        self.employe_window = EmployeWindow()  # Créer une instance de la fenêtre Employé
        self.employe_window.show()              # Afficher la fenêtre

if __name__ == "__main__":
    app = QApplication(sys.argv)  # Créer l'application ici
    window = MainWindow()         # Ensuite, créer la fenêtre principale
    window.show()                # Afficher la fenêtre
    sys.exit(app.exec())         # Lancer la boucle d'événements
