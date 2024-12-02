from PySide6.QtWidgets import QVBoxLayout, QPushButton, QLabel, QHBoxLayout, QLineEdit, QComboBox, QTextEdit
from Onglet import Onglet
from PySide6.QtCore import QDate, Qt
import sqlite3
import fetch

class Onglet_horaire(Onglet):
    def __init__(self, name, visibility):
        super().__init__(name, visibility)

    def create_content(self):
        # Définition des variables nécessaires
        self.start_date = QDate.currentDate().addDays(-QDate.currentDate().dayOfWeek() + 1)
        self.employees = ["Alice", "Bob", "Charlie", "David", "Eva"]
        self.schedule = {employee: {} for employee in self.employees}
        self.leaves = {employee: {} for employee in self.employees}  # Nouveau dictionnaire pour les congés

        layout = QVBoxLayout()  # Layout principal

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

        # Layout pour la modification de l'horaire ou du congé
        modify_layout = QHBoxLayout()

        # Liste des employés dans le combo box
        self.employee_combo = QComboBox()
        self.employee_combo.addItems(self.employees)
        modify_layout.addWidget(QLabel("Employé:"))
        modify_layout.addWidget(self.employee_combo)

        # Liste des jours dans le combo box
        self.day_combo = QComboBox()
        self.day_combo.addItems(["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"])
        modify_layout.addWidget(QLabel("Jour:"))
        modify_layout.addWidget(self.day_combo)
        
        # Bouton pour afficher les congés
        self.leave_button = QPushButton("Afficher les congés")
        layout.addWidget(self.leave_button)

        # Définir le layout principal sur le widget
        self.widget.setLayout(layout)

        # Connecter les boutons aux actions
        self.generate_button.clicked.connect(self.display_schedule)
        self.prev_week_button.clicked.connect(self.show_previous_week)
        self.next_week_button.clicked.connect(self.show_next_week)
        self.leave_button.clicked.connect(self.display_leaves)  # Afficher les congés

    def display_schedule(self):
        """ Afficher l'horaire des employés de la semaine actuelle """
        header = "Employé  | " + " | ".join(
            [f"{day} - {self.start_date.addDays(i).toString('dd/MM/yyyy')}" for i, day in enumerate(["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"])]
        ) + "\n"
        header += "-" * (len(header) - 1) + "\n"
        
        schedule_text = header
        
        for employee in self.employees:
            schedule_text += f"{employee:<8} | "  
            for i in range(7):  
                day_date = self.start_date.addDays(i).toString(Qt.ISODate)
                
                # Si l'employé a un congé ce jour-là, afficher "C/D"
                if day_date in self.leaves[employee]:
                    schedule_text += f"C/D | "
                else:
                    hour = self.schedule[employee].get(day_date, "8h00 - 17h00")
                    schedule_text += f"{hour:<15} | "  
            schedule_text += "\n\n"  

        self.schedule_display.setPlainText(schedule_text)

    def display_leaves(self):
        """ Afficher les congés des employés de la semaine actuelle """
        header = "Employé  | " + " | ".join(
            [f"{day} - {self.start_date.addDays(i).toString('dd/MM/yyyy')}" for i, day in enumerate(["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"])]
        ) + "\n"
        header += "-" * (len(header) - 1) + "\n"
        
        leave_text = header
        
        for employee in self.employees:
            leave_text += f"{employee:<8} | "
            for i in range(7):  
                day_date = self.start_date.addDays(i).toString(Qt.ISODate)
                leave = self.leaves[employee].get(day_date, "Aucun congé")
                leave_text += f"{leave:<15} | "  
            leave_text += "\n\n"  

        self.schedule_display.setPlainText(leave_text)

    def modify_leave(self):
        """ Modifier le congé d'un employé pour un jour donné """
        employee = self.employee_combo.currentText()
        day_index = self.day_combo.currentIndex()
        new_leave = self.hour_input.text()  # "hour_input" sert pour les congés aussi

        day_date = self.start_date.addDays(day_index).toString(Qt.ISODate)

        if new_leave:
            self.leaves[employee][day_date] = new_leave  # Ajoute un congé au jour sélectionné
            self.hour_input.clear()
            self.display_leaves()  # Rafraîchir l'affichage des congés

    def show_previous_week(self):
        """ Afficher l'horaire de la semaine précédente """
        self.start_date = self.start_date.addDays(-7)
        self.display_schedule()

    def show_next_week(self):
        """ Afficher l'horaire de la semaine suivante """
        self.start_date = self.start_date.addDays(7)
        self.display_schedule()