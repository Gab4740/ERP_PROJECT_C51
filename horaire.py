# horaire.py
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout,
    QPushButton, QLabel, QHBoxLayout, QMessageBox, QLineEdit, QDialog, QComboBox,QTextEdit
)
from Onglet import Onglet

class Onglet_horaire(Onglet):
    def __init__(self, name, visibility):
        super().__init__(name, visibility)

    def create_content(self):
        layout = QVBoxLayout()  # Ne pas passer self.widget ici

        # Affichage de l'horaire
        self.schedule_display = QTextEdit()
        self.schedule_display.setReadOnly(True)
        layout.addWidget(self.schedule_display)

        # Boutons pour la mise à jour de l'horaire
        self.generate_button = QPushButton("Mise à jour de l'horaire")
        layout.addWidget(self.generate_button)

        self.prev_week_button = QPushButton("Semaine précédente")
        layout.addWidget(self.prev_week_button)

        self.next_week_button = QPushButton("Semaine suivante")
        layout.addWidget(self.next_week_button)

        # Layout pour la modification de l'horaire
        modify_layout = QHBoxLayout()
        self.employee_combo = QComboBox()
        self.employee_combo.addItems(["Alice", "Bob", "Charlie", "David", "Eva"])
        modify_layout.addWidget(QLabel("Employé:"))
        modify_layout.addWidget(self.employee_combo)

        self.day_combo = QComboBox()
        self.day_combo.addItems(["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"])
        modify_layout.addWidget(QLabel("Jour:"))
        modify_layout.addWidget(self.day_combo)

        self.hour_input = QLineEdit()
        self.hour_input.setPlaceholderText("Nouvel horaire (ex: 9h00 - 18h00)")
        modify_layout.addWidget(QLabel("Nouvel horaire:"))
        modify_layout.addWidget(self.hour_input)

        self.modify_button = QPushButton("Modifier l'horaire")
        modify_layout.addWidget(self.modify_button)

        layout.addLayout(modify_layout)

        self.leave_button = QPushButton("Afficher les congés")
        layout.addWidget(self.leave_button)
            
        self.widget.setLayout(layout)