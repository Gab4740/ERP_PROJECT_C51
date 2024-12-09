from PySide6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QListWidget, QLabel, QTextEdit, QPushButton, 
    QDialog, QFormLayout, QLineEdit, QMessageBox, QListWidgetItem, QWidget, QButtonGroup, QRadioButton, QComboBox, QSpinBox, QDoubleSpinBox, QDateEdit
)
from Onglet import Onglet
from PySide6.QtCore import Qt, QDate
import sqlite3
import fetch
from config import DB_PATH

class Onglet_Fournisseurs(Onglet):
    def __init__(self, name, visibility):
        super().__init__(name, visibility)
        self.selected_fournisseur = None

    def create_content(self):
        self.widget.setLayout(self.init_ui())
        self.update_fournisseurs_list()
        
        # # SELECT FROM DATABASE
        # self.fournisseurs = ['Fournisseurs Principaux', 'Fournisseur Secondaires', 'Fournisseur Tertiaires']
        # self.entreprises = {
        #     'Fournisseurs Principaux': [
        #         {'name': 'Entreprise XYZ', 'address': '12345 Street X', 'email': 'xyz@fournisseur.com', 'phone': '123-456-7890'},
        #         {'name': 'Entreprise ABC', 'address': '98765 Street Y', 'email': 'abc@fournisseur.com', 'phone': '123-456-7891'}
        #     ],
        #     'Fournisseur Secondaires': [
        #         {'name': 'Entreprise QWERTY', 'address': '12345 Street X', 'email': 'qwerty@fournisseur.com', 'phone': '123-456-7890'},
        #         {'name': 'Entreprise AZERTY', 'address': '98765 Street Y', 'email': 'azerty@fournisseur.com', 'phone': '123-456-7891'}
        #     ],
        #     'Fournisseur Tertiaires': [
        #         {'name': 'Entreprise 000', 'address': '12345 Street X', 'email': '000@fournisseur.com', 'phone': '123-456-7890'},
        #         {'name': 'Entreprise 999', 'address': '98765 Street Y', 'email': '999@fournisseur.com', 'phone': '123-456-7891'}
        #     ]
        # }

        # self.current_entreprise = self.fournisseurs[0]
        # self.selected_entreprise = None

        # Initialize the UI
        # self.widget.setLayout(self.init_ui())

    def init_ui(self):
        # Main layout - Horizontal layout to split the window
        main_layout = QHBoxLayout()

        # Left side: List of employees
        left_layout = QVBoxLayout()
        
        # List widget for suppliers
        self.fournisseurs_list = QListWidget()
        self.fournisseurs_list.setStyleSheet("""
            QListWidget {
                background-color: #f7f7f7;
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 5px;
            }
            QListWidget::item {
                padding: 10px;
                border-radius: 5px;
                font-size: 30px;
                color: black;
            }
            QListWidget::item:hover {
                background-color: #98ab96;
            }
        """)
        self.fournisseurs_list.itemClicked.connect(self.on_fournisseur_clicked)
        left_layout.addWidget(self.fournisseurs_list)
        
        main_layout.addLayout(left_layout)
        
        # Right side: Supplier details
        right_layout = QVBoxLayout()
        
        # Search Bar
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Recherche...")
        self.search_bar.textChanged.connect(self.filter_fournisseurs)
        left_layout.addWidget(self.search_bar)
        self.search_bar.setStyleSheet("""
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

        # Supplier details title
        self.details_label = QLabel('Détails du fournisseur:')
        self.details_label.setStyleSheet("font-weight: bold; font-size: 18px;")
        right_layout.addWidget(self.details_label)

        # Text edit to show selected supplier details
        self.fournisseur_details = QTextEdit()
        self.fournisseur_details.setReadOnly(True)
        right_layout.addWidget(self.fournisseur_details)
        self.fournisseur_details.setStyleSheet("""
            QTextEdit {
                background-color: #f0f0f0;
                background-color: #f7f7f7;
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 5px;
            }
        """)

        # Add Supplier Button
        self.ajouter_button = QPushButton("Ajouter")
        self.ajouter_button.setStyleSheet("""
            QPushButton {
                background-color: #91AB00;
                color: white;
                border: 1px solid #ccc;
                border-radius: 20px;
                padding: 10px 20px;
                font-size: 14px;
                font-weight:bold;
            }
            QPushButton:hover {
                background-color: #687A00;
            }
        """)
        self.ajouter_button.clicked.connect(self.open_add_dialog)
        right_layout.addWidget(self.ajouter_button)

        # Modify Supplier Button
        self.modify_button = QPushButton("Modifier")
        self.modify_button.setStyleSheet("""
            QPushButton {
                background-color: #5a9fff;
                color: white;
                border: 1px solid #ccc;
                border-radius: 20px;
                padding: 10px 20px;
                font-size: 14px;
                font-weight:bold;
            }
            QPushButton:hover {
                background-color: #4a8fd1;
            }
        """)
        self.modify_button.clicked.connect(self.open_modify_dialog)
        right_layout.addWidget(self.modify_button)
        
        # SUPPRIMER ENTREPRISE FOURNISSEUR
        self.supprimer_button = QPushButton("Supprimer")
        self.supprimer_button.setStyleSheet("""
            QPushButton {
                background-color: #D22B2B;
                color: white;
                border: 1px solid #ccc;
                border-radius: 20px;
                padding: 10px 20px;
                font-size: 14px;
                font-weight:bold;
            }
            QPushButton:hover {
                background-color: #A52A2A;
            }
        """)
        self.supprimer_button.clicked.connect(self.delete_fournisseur)
        right_layout.addWidget(self.supprimer_button)

        main_layout.addLayout(right_layout)

        return main_layout



    def delete_fournisseur(self):
        selected_item = self.fournisseurs_list.currentItem()
        if selected_item:
            id_fournisseur = selected_item.data(Qt.UserRole)
            fetch.delete_fournisseur(id_fournisseur)
            QMessageBox.information(self.widget, "Succès", "Fournisseur supprimé avec succès.")
            self.update_fournisseurs_list()
            self.fournisseurs_list.clear()
            
            
            

    def filter_fournisseurs(self, text):
        """Filter the list of suppliers based on the search input."""
        filter_text = text.lower()  # Convert search text to lowercase for case-insensitive filtering
        fournisseurs = fetch.fetch_fournisseurs()  # Fetch all suppliers from the database

        self.fournisseurs_list.clear()  # Clear the current list

        # Loop through the suppliers and add only the matching ones to the list
        for fournisseur in fournisseurs:
            name = fournisseur[1].lower()  # Assuming `fournisseur[1]` is the supplier's name
            address = fournisseur[2].lower() if fournisseur[2] else ""  # Assuming `fournisseur[2]` is the address
            email = fournisseur[4].lower() if fournisseur[4] else ""  # Assuming `fournisseur[4]` is the email

            # Check if the search text matches the name, address, or email
            if filter_text in name or filter_text in address or filter_text in email:
                item = QListWidgetItem(fournisseur[1])  # Display the supplier's name
                item.setData(Qt.UserRole, fournisseur[0])  # Store the supplier ID
                self.fournisseurs_list.addItem(item)

    
    
    def update_fournisseurs_list(self):
        """Update the list of suppliers."""
        fournisseurs = fetch.fetch_fournisseurs()
        self.fournisseurs_list.clear()

        for fournisseur in fournisseurs:
            item = QListWidgetItem(fournisseur[1])  # Assuming `fournisseur[1]` is the name
            item.setData(Qt.UserRole, fournisseur[0])  # Store the supplier ID
            self.fournisseurs_list.addItem(item)
    
    
    def on_fournisseur_clicked(self, item):
        """Display details of the selected supplier."""
        fournisseur_id = item.data(Qt.UserRole)
        fournisseur_details = fetch.fetch_fournisseur_details(fournisseur_id)
        custom_fields = fetch.fetch_custom_field_values("Fournisseur", fournisseur_id)

        if fournisseur_details:
            details = (
                f"Nom: {fournisseur_details['name']}\n"
                f"Adresse: {fournisseur_details['address']}\n"
                f"Téléphone: {fournisseur_details['phone']}\n"
                f"Email: {fournisseur_details['email']}\n"
                f"Type: {fournisseur_details['type']}\n"
            )
            # Add custom field details
            for field_name, value in custom_fields:
                details += f"{field_name}: {value}\n"

            self.fournisseur_details.setText(details)
            self.selected_fournisseur = fournisseur_details

    def open_add_dialog(self):
        dialog = AddFournisseurDialog(self)
        if dialog.exec():
            self.update_fournisseurs_list()

    def open_modify_dialog(self):
        if self.selected_fournisseur:
            dialog = ModifyFournisseurDialog(self.selected_fournisseur)
            if dialog.exec():
                self.update_fournisseurs_list()


class AddFournisseurDialog(QDialog):
    def __init__(self, parent=None):
        # Si parent n'est pas un QWidget, le remplacer par None
        if not isinstance(parent, QWidget):
            parent = None
        super().__init__(parent)
        self.setWindowTitle("Ajouter un Fournisseur")
        self.dynamic_fields = {}

        layout = QFormLayout(self)

        self.name_input = QLineEdit()
        layout.addRow("Nom:", self.name_input)

        self.address_input = QLineEdit()
        layout.addRow("Adresse:", self.address_input)

        self.phone_input = QLineEdit()
        layout.addRow("Téléphone:", self.phone_input)

        self.email_input = QLineEdit()
        layout.addRow("Email:", self.email_input)
        
        self.type_input = QLineEdit()
        layout.addRow("Type:", self.type_input)

        # Add custom fields dynamically
        dynamic_fields = fetch.fetch_custom_fields("Fournisseur")
        for field_id, field_name, field_type, is_required in dynamic_fields:
            if field_type == "TEXT":
                widget = QLineEdit()
            elif field_type == "INTEGER":
                widget = QSpinBox()
            elif field_type == "FLOAT":
                widget = QDoubleSpinBox()
            elif field_type == "DATE":
                widget = QDateEdit()
                widget.setCalendarPopup(True)
            else:
                continue

            self.dynamic_fields[field_id] = widget
            layout.addRow(field_name, widget)

        save_button = QPushButton("Ajouter")
        save_button.clicked.connect(self.save_fournisseur)
        layout.addWidget(save_button)

        self.setLayout(layout)

    def save_fournisseur(self):
        name = self.name_input.text()
        address = self.address_input.text()
        phone = self.phone_input.text()
        email = self.email_input.text()
        type = self.type_input.text()

        if not name or not email:
            QMessageBox.warning(self, "Erreur", "Les champs Nom et Email sont obligatoires.")
            return

        fournisseur_id = fetch.add_fournisseur(name, address, phone, email, type)

        # Save custom fields
        custom_field_values = []
        for field_id, widget in self.dynamic_fields.items():
            if isinstance(widget, QLineEdit):
                value = widget.text()
            elif isinstance(widget, QSpinBox):
                value = widget.value()
            elif isinstance(widget, QDoubleSpinBox):
                value = widget.value()
            elif isinstance(widget, QDateEdit):
                value = widget.date().toString("yyyy-MM-dd")
            custom_field_values.append((field_id, value))

        fetch.save_custom_field_values("Fournisseur", fournisseur_id, custom_field_values)
        QMessageBox.information(self, "Succès", "Fournisseur ajouté avec succès.")
        self.accept()


class ModifyFournisseurDialog(QDialog):
    def __init__(self, fournisseur_data, parent=None):
        # Si parent n'est pas un QWidget, le remplacer par None
        if not isinstance(parent, QWidget):
            parent = None
        super().__init__(parent)
        self.setWindowTitle("Modifier Fournisseur")
        self.fournisseur_data = fournisseur_data
        self.dynamic_fields = {}

        layout = QFormLayout(self)

        self.name_input = QLineEdit()
        self.name_input.setText(fournisseur_data['name'])
        layout.addRow("Nom:", self.name_input)

        self.address_input = QLineEdit()
        self.address_input.setText(fournisseur_data['address'])
        layout.addRow("Adresse:", self.address_input)

        self.phone_input = QLineEdit()
        self.phone_input.setText(fournisseur_data['phone'])
        layout.addRow("Téléphone:", self.phone_input)

        self.email_input = QLineEdit()
        self.email_input.setText(fournisseur_data['email'])
        layout.addRow("Email:", self.email_input)
        
        self.type_input = QLineEdit()
        self.type_input.setText(fournisseur_data['type'])
        layout.addRow("Type:", self.type_input)

        # Load and update custom fields dynamically
        dynamic_fields = fetch.fetch_custom_fields("Fournisseur")
        custom_values = fetch.fetch_custom_field_values("Fournisseur", fournisseur_data['id'], as_dict=True)
        for field_id, field_name, field_type, is_required in dynamic_fields:
            if field_type == "TEXT":
                widget = QLineEdit()
                widget.setText(custom_values.get(field_id, ""))
            elif field_type == "INTEGER":
                widget = QSpinBox()
                widget.setValue(int(custom_values.get(field_id, 0)))
            elif field_type == "FLOAT":
                widget = QDoubleSpinBox()
                widget.setValue(float(custom_values.get(field_id, 0.0)))
            elif field_type == "DATE":
                widget = QDateEdit()
                widget.setCalendarPopup(True)
                widget.setDate(QDate.fromString(custom_values.get(field_id, ""), "yyyy-MM-dd"))
            else:
                continue

            self.dynamic_fields[field_id] = widget
            layout.addRow(field_name, widget)

        save_button = QPushButton("Enregistrer")
        save_button.clicked.connect(self.save_changes)
        layout.addWidget(save_button)

        self.setLayout(layout)

    def save_changes(self):
        name = self.name_input.text()
        address = self.address_input.text()
        phone = self.phone_input.text()
        email = self.email_input.text()
        type = self.type_input.text()

        fetch.update_fournisseur(self.fournisseur_data['id'], name, address, phone, email, type)

        # Update custom fields
        custom_field_values = []
        for field_id, widget in self.dynamic_fields.items():
            if isinstance(widget, QLineEdit):
                value = widget.text()
            elif isinstance(widget, QSpinBox):
                value = widget.value()
            elif isinstance(widget, QDoubleSpinBox):
                value = widget.value()
            elif isinstance(widget, QDateEdit):
                value = widget.date().toString("yyyy-MM-dd")
            custom_field_values.append((field_id, value))

        fetch.update_custom_field_values("Fournisseur", self.fournisseur_data['id'], custom_field_values)
        QMessageBox.information(self, "Succès", "Fournisseur modifié avec succès.")
        self.accept()
