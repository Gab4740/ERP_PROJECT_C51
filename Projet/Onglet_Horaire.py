from PySide6.QtWidgets import QVBoxLayout, QPushButton, QLabel, QHBoxLayout, QLineEdit, QComboBox, QTextEdit
from Onglet import Onglet
from PySide6.QtCore import QDate, Qt
import sqlite3
import fetch
from config import DB_PATH

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
        self.schedule_display.setStyleSheet("""
            QTextEdit {
                background-color: #f0f0f0;
                background-color: #f7f7f7;
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 5px;
            }
        """)

        # Boutons pour la mise à jour de l'horaire
        self.generate_button = QPushButton("Mise à jour de l'horaire")
        layout.addWidget(self.generate_button)
        self.generate_button.setStyleSheet("""
            QPushButton {
                background-color: #5a9fff;
                color: white;
                border: 1px solid #ccc;
                border-radius: 20px;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #4a8fd1;
            }
        """)

        self.prev_week_button = QPushButton("Semaine précédente")
        layout.addWidget(self.prev_week_button)
        self.prev_week_button.setStyleSheet("""
            QPushButton {
                background-color: #5a9fff;
                color: white;
                border: 1px solid #ccc;
                border-radius: 20px;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #4a8fd1;
            }
        """)

        self.next_week_button = QPushButton("Semaine suivante")
        layout.addWidget(self.next_week_button)
        self.next_week_button.setStyleSheet("""
            QPushButton {
                background-color: #5a9fff;
                color: white;
                border: 1px solid #ccc;
                border-radius: 20px;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #4a8fd1;
            }
        """)

        # Layout pour la modification de l'horaire ou du congé
        modify_layout = QHBoxLayout()

        # Liste des employés dans le combo box
        self.employee_combo = QComboBox()
        self.employee_combo.addItems(self.employees)
        titre_employe = QLabel("Employé:")
        modify_layout.addWidget(titre_employe)
        modify_layout.addWidget(self.employee_combo)
        titre_employe.setStyleSheet("font-weight: bold; font-size: 18px;")

        # Liste des jours dans le combo box
        self.day_combo = QComboBox()
        self.day_combo.addItems(["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"])
        titre_jour = QLabel("Jour:")
        modify_layout.addWidget(titre_jour)
        modify_layout.addWidget(self.day_combo)
        titre_jour.setStyleSheet("font-weight: bold; font-size: 18px;")

        # Champ de texte pour saisir l'horaire ou le congé
        self.hour_input = QLineEdit()
        self.hour_input.setPlaceholderText("Nouvel horaire (ex: 9h00 - 18h00)")
        titre_nouvel = QLabel("Nouvel horaire:")
        modify_layout.addWidget(titre_nouvel)
        modify_layout.addWidget(self.hour_input)
        titre_nouvel.setStyleSheet("font-weight: bold; font-size: 18px;")
        self.hour_input.setStyleSheet("""
            QLineEdit {
                background-color: #ffffff;
                border: 1px solid #ccc;
                border-radius: 20px;
                padding: 10px 20px;
                font-size: 14px;
                color: #333;
            }
            QLineEdit:focus {
                border-color: #5a9fff;
                background-color: #f3faff;
            }
            QLineEdit::placeholder {
                color: #aaa;
                font-style: italic;
            }
        """)

        # Bouton pour modifier l'horaire ou congé
        self.modify_button = QPushButton("Modifier l'horaire")
        modify_layout.addWidget(self.modify_button)
        self.modify_button.setStyleSheet("""
            QPushButton {
                background-color: #5a9fff;
                color: white;
                border: 1px solid #ccc;
                border-radius: 20px;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #4a8fd1;
            }
        """)

        layout.addLayout(modify_layout)

        # Bouton pour afficher les congés
        self.leave_button = QPushButton("Afficher les congés")
        layout.addWidget(self.leave_button)
        self.leave_button.setStyleSheet("""
            QPushButton {
                background-color: #5a9fff;
                color: white;
                border: 1px solid #ccc;
                border-radius: 20px;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #4a8fd1;
            }
        """)

        # Définir le layout principal sur le widget
        self.widget.setLayout(layout)

        # Connecter les boutons aux actions
        self.generate_button.clicked.connect(self.display_schedule)
        self.prev_week_button.clicked.connect(self.show_previous_week)
        self.next_week_button.clicked.connect(self.show_next_week)
        self.modify_button.clicked.connect(self.modify_schedule_or_leave)  # Logique de modification dynamique
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
        # Changer les éléments pour gérer les congés
        self.hour_input.setPlaceholderText("Nouvel congé (ex: Congé payé)")
        self.modify_button.setText("Modifier le congé")
        self.modify_button.clicked.disconnect()
        self.modify_button.clicked.connect(self.modify_leave)  # Lier au traitement des congés

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

    def modify_schedule_or_leave(self):
        """ Modifier l'horaire ou le congé d'un employé en fonction du mode (horaire ou congé) """
        if self.modify_button.text() == "Modifier l'horaire":
            self.modify_schedule()
        else:
            self.modify_leave()

    def modify_schedule(self):
        """ Modifier l'horaire d'un employé pour un jour donné """
        employee = self.employee_combo.currentText()
        day_index = self.day_combo.currentIndex()
        new_schedule = self.hour_input.text()

        day_date = self.start_date.addDays(day_index).toString(Qt.ISODate)

        if new_schedule:
            self.schedule[employee][day_date] = new_schedule
            self.hour_input.clear()
            self.display_schedule()

    def show_previous_week(self):
        """ Afficher l'horaire de la semaine précédente """
        self.start_date = self.start_date.addDays(-7)
        self.display_schedule()

    def show_next_week(self):
        """ Afficher l'horaire de la semaine suivante """
        self.start_date = self.start_date.addDays(7)
        self.display_schedule()


    #ajouter le fetch 
    
    def ajouter_conge(self):
        """ Ajouter un congé pour un employé à une date donnée dans la base de données """
        employee = self.employee_combo.currentText()  # Récupérer l'employé sélectionné
        day_index = self.day_combo.currentIndex()  # Récupérer le jour sélectionné
        new_leave = self.hour_input.text()  # Récupérer le type de congé saisi (ex : Congé payé)
        
        if new_leave:
            # Calculer la date à partir de start_date et du jour sélectionné
            day_date = self.start_date.addDays(day_index).toString(Qt.ISODate)

            # Connexion à la base de données
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()

            try:
                # Vérifier si l'employé existe dans la table info_PERSONNEL
                cursor.execute("SELECT id_individus FROM info_PERSONNEL WHERE nom = ?", (employee,))
                employee_id = cursor.fetchone()

                if employee_id:
                    employee_id = employee_id[0]  # Récupérer l'id de l'employé

                    # Insérer le congé dans la table congé pour l'employé
                    cursor.execute("""
                        INSERT INTO rh.CONGE (id_employe, date_conge, type_conge)
                        VALUES (?, ?, ?)
                    """, (employee_id, day_date, new_leave))
                    conn.commit()

                    # Rafraîchir l'affichage des congés
                    self.display_leaves()
                    self.hour_input.clear()  # Réinitialiser le champ de saisie
                    print(f"Congé ajouté pour {employee} le {day_date} : {new_leave}")
                else:
                    print("Employé non trouvé.")
            except sqlite3.Error as e:
                print(f"Erreur SQLite: {e}")
            finally:
                conn.close()

    
    def ajouter_horaire(self):
        """ Ajouter un horaire pour un employé spécifique à une date donnée dans la base de données """
        employee = self.employee_combo.currentText()  # Récupérer l'employé sélectionné
        day_index = self.day_combo.currentIndex()  # Récupérer le jour sélectionné
        new_schedule = self.hour_input.text()  # Récupérer l'horaire saisi
        
        if new_schedule:
            # Calculer la date à partir de start_date et du jour sélectionné
            day_date = self.start_date.addDays(day_index).toString(Qt.ISODate)

            # Connexion à la base de données
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()

            try:
                # Vérifier si l'employé existe dans la table info_PERSONNEL
                cursor.execute("SELECT id_individus FROM info_PERSONNEL WHERE nom = ?", (employee,))
                employee_id = cursor.fetchone()
                
                if employee_id:
                    employee_id = employee_id[0]  # Récupérer l'id de l'employé

                    # Insérer l'horaire dans la table horaire pour l'employé
                    cursor.execute("""
                        INSERT INTO rh.HORAIRE (id_employe, date_horaire, horaire)
                        VALUES (?, ?, ?)
                    """, (employee_id, day_date, new_schedule))
                    conn.commit()

                    # Rafraîchir l'affichage de l'horaire
                    self.display_schedule()
                    self.hour_input.clear()  # Réinitialiser le champ de saisie
                    print(f"Horaire ajouté pour {employee} le {day_date} : {new_schedule}")
                else:
                    print("Employé non trouvé.")
            except sqlite3.Error as e:
                print(f"Erreur SQLite: {e}")
            finally:
                conn.close()
