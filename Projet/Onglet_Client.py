from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QListWidget, QTextEdit, QLabel, QLineEdit, QListWidgetItem, QPushButton, QDialog, QFormLayout, QMessageBox, QWidget, QSpinBox, QDoubleSpinBox, QDateEdit
from Onglet import Onglet
from PySide6.QtCore import Qt, QDate
import fetch

class Onglet_Client(Onglet):
    def __init__(self, name, visibility, parent_widget=None):
        super().__init__(name, visibility)
        self.parent_widget = parent_widget

    def create_content(self):  
        # SELECT FROM DATABASE
        self.clients = []
        # Initialize the UI
        self.widget.setLayout(self.init_ui())
        
        self.load_clients_list()


        

    def init_ui(self):
        # Main layout - Horizontal layout to split the window
        main_layout = QHBoxLayout()

        # Left side: List of employees
        left_layout = QVBoxLayout()
        
        # Search Bar
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Recherche...")
        self.search_bar.textChanged.connect(self.filter_clients)
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

        # List widget for employees
        self.clients_list = QListWidget()
        self.clients_list.itemClicked.connect(self.on_client_clicked)
        left_layout.addWidget(self.clients_list)
        self.clients_list.setStyleSheet("""
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
        
        
        

        # Right side: clients details
        right_layout = QVBoxLayout()
    
        # clients details title
        self.details_label = QLabel('Détails du client:')
        self.details_label.setStyleSheet("font-weight: bold; font-size: 18px;")
        right_layout.addWidget(self.details_label)

        # Text edit to show selected clients details
        self.clients_details = QTextEdit()
        self.clients_details.setReadOnly(True)
        right_layout.addWidget(self.clients_details)
        self.clients_details.setStyleSheet("""
            QTextEdit {
                background-color: #f0f0f0;
                background-color: #f7f7f7;
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 5px;
            }
        """)
        
        
        self.add_button = QPushButton("Ajouter")
        self.add_button.setStyleSheet("""
            QPushButton {
                background-color: #70AD47;
                color: black;
                border: 1px solid #ccc;
                border-radius: 20px;
                padding: 10px 20px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #476D2D;
            }
        """)
        self.add_button.clicked.connect(self.open_add_dialog)
        right_layout.addWidget(self.add_button)
        
        
        
        self.modify_button = QPushButton("Modifier")
        self.modify_button.setStyleSheet("""
            QPushButton {
                background-color: #5a9fff;
                color: black;
                border: 1px solid #ccc;
                border-radius: 20px;
                padding: 10px 20px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #4a8fd1;
            }
        """)
        self.modify_button.clicked.connect(self.open_modify_dialog)
        right_layout.addWidget(self.modify_button)
        
        
        
        self.delete_button = QPushButton("Supprimer")
        self.delete_button.setStyleSheet("""
            QPushButton {
                background-color: #C00000;
                color: black;
                border: 1px solid #ccc;
                border-radius: 20px;
                padding: 10px 20px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #740000;
            }
        """)
        self.delete_button.clicked.connect(self.supprimer_client_selectionne)
        right_layout.addWidget(self.delete_button)
        

        main_layout.addLayout(right_layout)
        
        return main_layout



    def load_clients_list(self):
        self.clients = fetch.fetch_client() 
        self.clients_list.clear()

        for client in self.clients:
            id_client = client[0]
            nom = f"{client[4]} {client[5]}"  # Nom complet (nom + prénom)
            item = QListWidgetItem(nom)
            item.setData(Qt.UserRole, id_client)  # Associer l'ID du client aux données de l'item
            self.clients_list.addItem(item)



    def on_client_clicked(self, item):
        """Affiche les détails du client sélectionné."""
        id_client = item.data(Qt.UserRole)
        client = next((c for c in self.clients if c[0] == id_client), None)

        if client:
            details = (
                f"ID Client: {client[0]}\n"
                f"Nom: {client[4]} {client[5]}\n"
                f"Date de naissance: {client[6]}\n"
                f"Email: {client[7]}\n"
                f"Téléphone: {client[8]}\n"
                f"Adresse: {client[9]}\n"
                f"Type: {client[1]}\n"
            )
            
            ###### AJOUTER CUSTOM FIELDS ##########################
            custom_fields = fetch.fetch_custom_field_values("Client", id_client)
            for field_name, value in custom_fields:
                details += f"{field_name}: {value}\n"
            ####################################################
            
            self.clients_details.setText(details)
            
            

            
    def filter_clients(self, text):
        """Filtre la liste des clients en fonction de la recherche."""
        filter_text = text.lower()
        self.clients_list.clear()

        for client in self.clients:
            nom_complet = f"{client[4]} {client[5]}".lower()
            if filter_text in nom_complet:
                item = QListWidgetItem(f"{client[4]} {client[5]}")
                item.setData(Qt.UserRole, client[0])
                self.clients_list.addItem(item)
                
                
                
    def open_add_dialog(self):
        """Ouvre une boîte de dialogue pour ajouter un nouveau client."""
        dialog = AddClientDialog(self)
        if dialog.exec():
            self.load_clients_list()  # Recharger la liste des clients après ajout  
            
            
             
    
    def supprimer_client_selectionne(self):
        """Supprime le client sélectionné."""
        selected_item = self.clients_list.currentItem()
        if selected_item:
            id_client = selected_item.data(Qt.UserRole)

            reply = QMessageBox.question(
                self.widget,
                "Confirmation",
                f"Voulez-vous vraiment supprimer ce client ?",
                QMessageBox.Yes | QMessageBox.No
            )

            if reply == QMessageBox.Yes:
                fetch.supprimer_client(id_client)
                self.load_clients_list()  # Recharger la liste des clients
                self.clients_details.clear()  # Effacer les détails affichés
                QMessageBox.information(self.widget, "Succès", "Client supprimé avec succès.")
        else:
            QMessageBox.warning(self.widget, "Avertissement", "Veuillez sélectionner un client.")
            
    
    def open_modify_dialog(self):
        """
        Ouvre une boîte de dialogue pour modifier un client.
        """
        selected_item = self.clients_list.currentItem()
        if selected_item:
            id_client = selected_item.data(Qt.UserRole)
            client = next((c for c in self.clients if c[0] == id_client), None)

            if client:
                client_data = {
                    'id_client': client[0],
                    'type': client[1],
                    'nas': client[3],
                    'nom': client[4],
                    'prenom': client[5],
                    'date_naissance': client[6],
                    'email': client[7],
                    'telephone': client[8],
                    'adresse': client[9],         
                }

                dialog = ModifyClientDialog(client_data, self)
                if dialog.exec():
                    self.load_clients_list()  # Recharger la liste des clients après modification
            else:
                QMessageBox.warning(self, "Avertissement", "Client introuvable.")
        else:
            QMessageBox.warning(self, "Avertissement", "Veuillez sélectionner un client.")


    
  


class AddClientDialog(QDialog):
    def __init__(self, parent=None):
        # Si parent n'est pas un QWidget, le remplacer par None
        if not isinstance(parent, QWidget):
            parent = None
        super().__init__(parent)
        self.setWindowTitle("Ajouter un client")
        layout = QFormLayout(self)

        self.nas_input = QLineEdit()
        layout.addRow("NAS:", self.nas_input)

        self.nom_input = QLineEdit()
        layout.addRow("Nom:", self.nom_input)

        self.prenom_input = QLineEdit()
        layout.addRow("Prénom:", self.prenom_input)

        self.date_naissance_input = QLineEdit()
        layout.addRow("Date de naissance:", self.date_naissance_input)

        self.email_input = QLineEdit()
        layout.addRow("Email:", self.email_input)

        self.telephone_input = QLineEdit()
        layout.addRow("Téléphone:", self.telephone_input)

        self.adresse_input = QLineEdit()
        layout.addRow("Adresse:", self.adresse_input)

        self.type_input = QLineEdit()
        layout.addRow("Type:", self.type_input)
        
        
        ###### AJOUTER CUSTOM FIELDS ##########################
        self.dynamic_fields = {}
        dynamic_fields = fetch.fetch_custom_fields("Client")
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
        ####################################################
        

        self.save_button = QPushButton("Ajouter")
        self.save_button.clicked.connect(self.add_client)
        layout.addWidget(self.save_button)

    def add_client(self):
        """Ajoute un nouveau client dans la base de données."""
        client_id = fetch.ajouter_client(
            self.nas_input.text(),
            self.nom_input.text(),
            self.prenom_input.text(),
            self.date_naissance_input.text(),
            self.email_input.text(),
            self.telephone_input.text(),
            self.adresse_input.text(),
            self.type_input.text()
        )
        
        ###### AJOUTER CUSTOM FIELDS ##########################
        dynamic_field_values = []
        for field_id, widget in self.dynamic_fields.items():
            if isinstance(widget, QLineEdit):
                value = widget.text()
            elif isinstance(widget, QSpinBox):
                value = widget.value()
            elif isinstance(widget, QDoubleSpinBox):
                value = widget.value()
            elif isinstance(widget, QDateEdit):
                value = widget.date().toString("yyyy-MM-dd")
            dynamic_field_values.append((field_id, value))
        

        fetch.save_custom_field_values("Client", client_id, dynamic_field_values)
        ##############################################################################
        
        QMessageBox.information(self, "Succès", "Client ajouté avec succès.")
        self.accept()



class ModifyClientDialog(QDialog):
    def __init__(self, client_data, parent=None):
        # Si parent n'est pas un QWidget, le remplacer par None
        if not isinstance(parent, QWidget):
            parent = None
        super().__init__(parent)
        self.setWindowTitle("Modifier un client")
        self.setMinimumSize(400, 300)

        self.client_data = client_data  # Données actuelles du client à modifier
        self.dynamic_fields = {} # AJOUTER CUSTOM FIELDS - créer la liste

        layout = QFormLayout(self)

        self.nas_input = QLineEdit(self)
        self.nas_input.setText(client_data['nas'])
        layout.addRow("NAS:", self.nas_input)

        self.nom_input = QLineEdit(self)
        self.nom_input.setText(client_data['nom'])
        layout.addRow("Nom:", self.nom_input)

        self.prenom_input = QLineEdit(self)
        self.prenom_input.setText(client_data['prenom'])
        layout.addRow("Prénom:", self.prenom_input)

        self.date_naissance_input = QLineEdit(self)
        self.date_naissance_input.setText(client_data['date_naissance'])
        layout.addRow("Date de naissance:", self.date_naissance_input)

        self.email_input = QLineEdit(self)
        self.email_input.setText(client_data['email'])
        layout.addRow("Email:", self.email_input)

        self.telephone_input = QLineEdit(self)
        self.telephone_input.setText(client_data['telephone'])
        layout.addRow("Téléphone:", self.telephone_input)

        self.adresse_input = QLineEdit(self)
        self.adresse_input.setText(client_data['adresse'])
        layout.addRow("Adresse:", self.adresse_input)

        self.type_input = QLineEdit(self)
        self.type_input.setText(client_data['type'])
        layout.addRow("Type:", self.type_input)
        
        
        
        ###### AJOUTER CUSTOM FIELDS ##########################
        dynamic_fields = fetch.fetch_custom_fields("Client")
        dynamic_values = fetch.fetch_custom_field_values("Client", self.client_data['id_client'], as_dict=True)
        for field_id, field_name, field_type, is_required in dynamic_fields:
            if field_type == "TEXT":
                widget = QLineEdit(self)
                widget.setText(dynamic_values.get(field_id, ""))
            elif field_type == "INTEGER":
                widget = QSpinBox(self)
                widget.setValue(int(dynamic_values.get(field_id, 0)))
            elif field_type == "FLOAT":
                widget = QDoubleSpinBox(self)
                widget.setValue(float(dynamic_values.get(field_id, 0.0)))
            elif field_type == "DATE":
                widget = QDateEdit(self)
                widget.setCalendarPopup(True)
                widget.setDate(QDate.fromString(dynamic_values.get(field_id, ""), "yyyy-MM-dd"))
            self.dynamic_fields[field_id] = widget
            layout.addRow(field_name, widget)
        ########################################################################################################

        # Boutons
        save_button = QPushButton("Enregistrer")
        save_button.clicked.connect(self.save_changes)
        layout.addWidget(save_button)

    def save_changes(self):
        """Enregistre les modifications dans la base de données."""
        fetch.update_client(
            self.client_data['id_client'],
            self.nas_input.text(),
            self.nom_input.text(),
            self.prenom_input.text(),
            self.date_naissance_input.text(),
            self.email_input.text(),
            self.telephone_input.text(),
            self.adresse_input.text(),
            self.type_input.text()
        )
        
        ###### AJOUTER CUSTOM FIELDS ##########################
        dynamic_field_values = []
        for field_id, widget in self.dynamic_fields.items():
            if isinstance(widget, QLineEdit):
                value = widget.text()
            elif isinstance(widget, QSpinBox):
                value = widget.value()
            elif isinstance(widget, QDoubleSpinBox):
                value = widget.value()
            elif isinstance(widget, QDateEdit):
                value = widget.date().toString("yyyy-MM-dd")
            dynamic_field_values.append((field_id, value))

        fetch.update_custom_field_values("Client", self.client_data['id_client'], dynamic_field_values)
        ##############################################################################
        
        QMessageBox.information(self, "Succès", "Modifications enregistrées avec succès.")
        self.accept()  # Fermer la boîte de dialogue




