import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton
)
from horaire import ScheduleApp  # Assurez-vous que le fichier horaire.py est dans le même répertoire

class EmployeWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fenêtre Employé")
        self.setGeometry(100, 100, 300, 200)

        # Créer un widget central
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Créer un layout vertical
        layout = QVBoxLayout(central_widget)

        # Bouton Horaire
        self.horaire_button = QPushButton("Horaire", self)
        self.horaire_button.clicked.connect(self.open_horaire)
        layout.addWidget(self.horaire_button)

        # Bouton Fiche de Paie (pour l'instant, juste un exemple)
        self.paye_button = QPushButton("Fiche de Paie", self)
        layout.addWidget(self.paye_button)

        # Bouton Quitter
        self.quit_button = QPushButton("Retour", self)
        self.quit_button.clicked.connect(self.close)  # Connecter au slot de fermeture
        layout.addWidget(self.quit_button)

    def open_horaire(self):
        self.schedule_window = ScheduleApp()  # Créer une instance de la fenêtre d'horaire
        self.schedule_window.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)  # Créer l'application ici
    window = EmployeWindow()       # Ensuite, créer la fenêtre
    window.show()                  # Afficher la fenêtre
    sys.exit(app.exec())          # Lancer la boucle d'événements
