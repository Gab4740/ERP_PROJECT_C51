from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QComboBox, QLineEdit, QDateEdit, QGroupBox, QMessageBox, QWidget, QFormLayout
from Onglet import Onglet
import fetch
import re

class Onglet_usagers(Onglet):
    def __init__(self, name, visibility, parent_widget=None):
        super().__init__(name, visibility)
        self.parent_widget = parent_widget

    def create_content(self):
        # Layout principal
        layout = QVBoxLayout()
        
        # Informations personnelles
        personal_info_group = QGroupBox("Informations personnelles")
        personal_layout = QFormLayout()
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Nom")
        personal_layout.addRow(QLabel("Nom :"), self.name_input)

        self.surname_input = QLineEdit()
        self.surname_input.setPlaceholderText("Prénom")
        personal_layout.addRow(QLabel("Prénom :"), self.surname_input)

        self.nas_input = QLineEdit()
        self.nas_input.setPlaceholderText("Numéro d'assurance sociale")
        personal_layout.addRow(QLabel("N.A.S. :"), self.nas_input)

        self.birthday_input = QLineEdit()
        self.birthday_input.setPlaceholderText("Date de naissance")
        personal_layout.addRow(QLabel("Date de naissance :"), self.birthday_input)

        personal_info_group.setLayout(personal_layout)
        layout.addWidget(personal_info_group)

        # Informations de contact
        contact_info_group = QGroupBox("Contact")
        contact_layout = QFormLayout()
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email")
        contact_layout.addRow(QLabel("Email :"), self.email_input)

        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("Numéro de téléphone")
        contact_layout.addRow(QLabel("Numéro de téléphone :"), self.phone_input)

        self.adress_input = QLineEdit()
        self.adress_input.setPlaceholderText("Adresse")
        contact_layout.addRow(QLabel("Adresse :"), self.adress_input)

        contact_info_group.setLayout(contact_layout)
        layout.addWidget(contact_info_group)

        # Informations sur l'emploi
        job_info_group = QGroupBox("Informations sur l'emploi")
        job_layout = QFormLayout()
        self.job_title_input = QComboBox()
        self.job_title_input.addItem('Employé')
        self.job_title_input.addItem('Superviseur')
        self.job_title_input.addItem('Gérant')
        self.job_title_input.addItem('Modérateur')
        self.job_title_input.addItem('Administrateur')
        job_layout.addRow(QLabel("Poste :"), self.job_title_input)

        self.succursale_associe = QComboBox()
        succursale_fetched = fetch.fetch_succursale()
        for e in succursale_fetched:
            self.succursale_associe.addItem(e[2])
        job_layout.addRow(QLabel("Succursale :"), self.succursale_associe)

        self.salary_input = QLineEdit()
        self.salary_input.setPlaceholderText("Salaire")
        job_layout.addRow(QLabel("Salaire :"), self.salary_input)

        job_info_group.setLayout(job_layout)
        layout.addWidget(job_info_group)

        # Ajouter un bouton pour soumettre
        self.submit_button = QPushButton("Ajouter l'employé")
        layout.addWidget(self.submit_button)
        self.submit_button.clicked.connect(self.on_save_clicked)

        # Set the layout to the widget
        self.widget.setLayout(layout)
        
        self.widget.setStyleSheet("""
            /* Global styles */
            QWidget {
                background-color: #f7f7f7;
                font-family: Arial, sans-serif;
                font-size: 14px;
                padding: 20px;
            }

            QGroupBox {
                background-color: #ffffff;
                border: 2px solid #e0e0e0;
                border-radius: 10px;
                padding: 10px;
                margin-bottom: 20px;
            }

            QGroupBox:title {
                font-size: 16px;
                font-weight: bold;
                color: #4CAF50;
                padding: 0 10px;
            }

            QLineEdit, QComboBox, QDateEdit {
                background-color: #fff;
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 10px;
                font-size: 14px;
                margin: 10px 0;
            }

            QLineEdit:focus, QComboBox:focus, QDateEdit:focus {
                border-color: #4CAF50;
            }

            QLabel {
                font-size: 14px;
                color: #333;
                width: 150px; 
                min-width: 150px;
            }

            QPushButton {
                font-weight: bold;
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 15px;
                font-size: 16px;
                margin-top: 20px;
                cursor: pointer;
            }

            QPushButton:hover {
                background-color: #45a049;
            }

            QPushButton:pressed {
                background-color: #3e8e41;
            }

            /* Adjusting for small screens */
            @media (max-width: 600px) {
                QWidget {
                    padding: 10px;
                }

                QLineEdit, QComboBox, QDateEdit {
                    font-size: 12px;
                }

                QPushButton {
                    font-size: 14px;
                    padding: 12px;
                }
            }
        """)
       
    def on_save_clicked(self):
        # Gather form data
        name = self.name_input.text().strip()
        job_title = self.job_title_input.currentText()
        succursale = self.succursale_associe.currentText()
        email = self.email_input.text().strip()
        phone = self.phone_input.text().strip()
        salary = self.salary_input.text().strip()
        
        pattern = r"^\d{3}-\d{3}-\d{4}$"
        if not re.match(pattern, phone):
            QMessageBox.warning(self.widget, "Erreur", "Numéro de telephone mal entré")
            return

        if not name or not email or not phone:
            QMessageBox.warning(self.widget, "Erreur", "Nom, email et téléphone sont obligatoires.")
            return

        # Call the function to save the employee in the database
        #fetch.add_employee(
        #    name=name,
        #    job_title=job_title,
        #    email=email,
        #    phone=phone,
        #    start_date=start_date,
        #    salary=salary
        #)

        # Show success message
        QMessageBox.information(self.widget, "Succès", "L'employé a été enregistré avec succès.")
        self.reset_form()

    def on_reset_clicked(self):
        self.reset_form()

    def reset_form(self):
        # Reset the form fields
        self.name_input.clear()
        self.job_title_input.clear()
        self.email_input.clear()
        self.phone_input.clear()
        self.salary_input.clear()
        self.start_date_input.setDate(self.start_date_input.minimumDate())