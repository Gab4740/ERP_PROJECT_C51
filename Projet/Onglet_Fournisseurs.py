from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QComboBox, QListWidget, QTextEdit, QLabel, QLineEdit, QListWidgetItem, QPushButton, QDialog, QFormLayout
from Onglet import Onglet
import sqlite3

class Onglet_Fournisseurs(Onglet):
    def __init__(self, name, visibility):
        super().__init__(name, visibility)

    def create_content(self):
        
        # SELECT FROM DATABASE
        self.fournisseurs = ['Fournisseurs Principaux', 'Fournisseur Secondaires', 'Fournisseur Tertiaires']
        self.entreprises = {
            'Fournisseurs Principaux': [
                {'name': 'Entreprise XYZ', 'address': '12345 Street X', 'email': 'xyz@fournisseur.com', 'phone': '123-456-7890'},
                {'name': 'Entreprise ABC', 'address': '98765 Street Y', 'email': 'abc@fournisseur.com', 'phone': '123-456-7891'}
            ],
            'Fournisseur Secondaires': [
                {'name': 'Entreprise QWERTY', 'address': '12345 Street X', 'email': 'qwerty@fournisseur.com', 'phone': '123-456-7890'},
                {'name': 'Entreprise AZERTY', 'address': '98765 Street Y', 'email': 'azerty@fournisseur.com', 'phone': '123-456-7891'}
            ],
            'Fournisseur Tertiaires': [
                {'name': 'Entreprise 000', 'address': '12345 Street X', 'email': '000@fournisseur.com', 'phone': '123-456-7890'},
                {'name': 'Entreprise 999', 'address': '98765 Street Y', 'email': '999@fournisseur.com', 'phone': '123-456-7891'}
            ]
        }

        self.current_entreprise = self.fournisseurs[0]
        self.selected_entreprise = None

        # Initialize the UI
        self.widget.setLayout(self.init_ui())

    def init_ui(self):
        # Main layout - Horizontal layout to split the window
        main_layout = QHBoxLayout()

        # Left side: List of employees
        left_layout = QVBoxLayout()
        
        # Shop dropdown
        self.shop_combo = QComboBox()
        self.shop_combo.addItems(self.fournisseurs)
        self.shop_combo.currentTextChanged.connect(self.on_fournisseur_changed)
        left_layout.addWidget(self.shop_combo)

        # List widget for employees
        self.entreprises_list = QListWidget()
        self.entreprises_list.itemClicked.connect(self.on_entreprise_clicked)
        left_layout.addWidget(self.entreprises_list)
        self.entreprises_list.setStyleSheet("""
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

        main_layout.addLayout(left_layout)

        # Right side: Employee details
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

        # Employee details title
        self.details_label = QLabel('Détails de l''entreprise:')
        self.details_label.setStyleSheet("font-weight: bold; font-size: 18px;")
        right_layout.addWidget(self.details_label)

        # Text edit to show selected employee details
        self.entreprise_details = QTextEdit()
        self.entreprise_details.setReadOnly(True)
        right_layout.addWidget(self.entreprise_details)
        self.entreprise_details.setStyleSheet("""
            QTextEdit {
                background-color: #f0f0f0;
                background-color: #f7f7f7;
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 5px;
            }
        """)

        # AJOUTER ENTREPRISE FOURNISSEUR
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
        # self.ajouter_button.clicked.connect()
        right_layout.addWidget(self.ajouter_button)
        
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
        # self.supprimer_button.clicked.connect()
        right_layout.addWidget(self.supprimer_button)

        main_layout.addLayout(right_layout)

        # Set the initial shop and employee list
        self.on_fournisseur_changed(self.fournisseurs[0])
        
        return main_layout

    def on_fournisseur_changed(self, shop_name):
        """Update the employee list when a new shop is selected."""
        self.current_entreprise = shop_name
        self.update_entreprises_list()

    def update_entreprises_list(self):
        """Update the employee list on the left side based on the current shop."""
        # Get employee data for the selected shop
        entreprises = self.entreprises.get(self.current_entreprise, [])

        # Sort the employee names alphabetically
        entreprises_sorted = sorted(entreprises, key=lambda x: x['name'].lower())

        # Clear the current list
        self.entreprises_list.clear()

        # Add employee names to the list widget
        for entreprise in entreprises_sorted:
            self.entreprises_list.addItem(entreprise['name'])

    def on_entreprise_clicked(self, item):
        """Display the selected employee's details in the right section."""
        entreprise_name = item.text()

        # Find the employee based on the selected name
        entreprises = self.entreprises.get(self.current_entreprise, [])
        for entreprise in entreprises:
            if entreprise['name'] == entreprise_name:
                self.selected_entreprise = entreprise
                self.display_entreprise_details()
                break

    def display_entreprise_details(self):
        """Display the detailed information of the selected employee."""
        if self.selected_entreprise:
            details = (
                f"Name: {self.selected_entreprise['name']}\n"
                f"Position: {self.selected_entreprise['address']}\n"
                f"Email: {self.selected_entreprise['email']}\n"
                f"Phone: {self.selected_entreprise['phone']}\n"
            )
            self.entreprise_details.setText(details)
            
    def filter_fournisseurs(self, text):
        """Filter the employees list based on the search input."""
        filter_text = text.lower()
        entreprises = self.entreprises.get(self.current_entreprise, [])
        filtered_entreprises = [ent for ent in entreprises if filter_text in ent['name'].lower()]

        # Clear existing rows and repopulate with filtered data
        self.entreprises_list.clear()
        for entreprise in filtered_entreprises:
            self.entreprises_list.addItem(entreprise['name'])
    
    def open_modify_dialog(self):
        """Open the modify dialog to edit the selected employee's details."""
        if self.selected_entreprise:
            dialog = ModifyEntrepriseDialog(self.selected_entreprise)
            dialog.exec()

            # After closing the dialog, update the employee list with any changes
            self.update_entreprises_list()
    
    
    
    ## A DEPLACER DANS LE DOCUEMNT fetch.py      
    def ajouter_nouvelle_entreprise(self, nom, adresse, email, telephone, type_entreprise):
        conn = sqlite3.connect('erp.db')
        cursor = conn.cursor()
        try:
            # Ajouter les informations de l'entité (INFO_CIE)
            cursor.execute("""
                INSERT INTO info.INFO_CIE (nom, adresse, telephone, email, type_entreprise)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (nom, adresse, telephone, email, type_entreprise))
            
            # Récupérer l'ID de l'entité insérée
            id_entite = cursor.lastrowid
            
            # Ajouter la succursale associée
            cursor.execute("""
                INSERT INTO rh.EMPLOYE (id_employe)
                VALUES (?)
            """, (id_entite,))
            
            conn.commit()
            print(f"Entreprise '{nom}' ajoutée avec succès.")
        except sqlite3.Error as e:
            print(f"Erreur SQL : {e}")
            raise e
        finally:
            conn.close()



class ModifyEntrepriseDialog(QDialog):
    def __init__(self, entreprise_data, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Modifier Entreprise")
        self.setGeometry(150, 150, 400, 300)

        self.entreprise_data = entreprise_data

        # Create form layout for the dialog
        layout = QFormLayout(self)

        self.name_edit = QLineEdit(self)
        self.name_edit.setText(self.entreprise_data['name'])
        layout.addRow("Name:", self.name_edit)

        self.adresse_edit = QLineEdit(self)
        self.adresse_edit.setText(self.entreprise_data['address'])
        layout.addRow("Adresse:", self.adresse_edit)

        self.email_edit = QLineEdit(self)
        self.email_edit.setText(self.entreprise_data['email'])
        layout.addRow("Email:", self.email_edit)

        self.phone_edit = QLineEdit(self)
        self.phone_edit.setText(self.entreprise_data['phone'])
        layout.addRow("Phone:", self.phone_edit)

        # Save button
        save_button = QPushButton("Save", self)
        save_button.clicked.connect(self.save_changes)
        layout.addRow(save_button)

    def save_changes(self):
        """Save the changes to the employee data."""
        self.entreprise_data['name'] = self.name_edit.text()
        self.entreprise_data['adresse'] = self.adresse_edit.text()
        self.entreprise_data['email'] = self.email_edit.text()
        self.entreprise_data['phone'] = self.phone_edit.text()

        self.accept()  # Close the dialog


