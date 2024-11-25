from PySide6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QListWidget, QLabel, QTextEdit, QPushButton, 
    QDialog, QFormLayout, QLineEdit, QMessageBox, QListWidgetItem, QWidget, QButtonGroup, QRadioButton, QComboBox
)
from PySide6.QtCore import Qt
from Onglet import Onglet
import fetch

class Onglet_Commande(Onglet):
    def __init__(self, name, visibility, parent_widget=None):
        super().__init__(name, visibility)
        self.parent_widget = parent_widget

    def create_content(self):
        self.commandes = []
        self.widget.setLayout(self.init_ui())
        self.load_commandes_list()
        

    def init_ui(self):
        """Initialise l'interface utilisateur."""
        main_layout = QHBoxLayout()

        # Liste des commandes
        left_layout = QVBoxLayout()
        self.commandes_list = QListWidget()
        self.commandes_list.itemClicked.connect(self.on_commande_clicked)
        left_layout.addWidget(self.commandes_list)

        main_layout.addLayout(left_layout)

        # Détails de la commande
        right_layout = QVBoxLayout()
        self.details_label = QLabel("Détails de la commande:")
        right_layout.addWidget(self.details_label)

        self.commandes_details = QTextEdit()
        self.commandes_details.setReadOnly(True)
        right_layout.addWidget(self.commandes_details)

        # Boutons
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
        self.delete_button.clicked.connect(self.cancel_commande)
        right_layout.addWidget(self.delete_button)

        main_layout.addLayout(right_layout)
        return main_layout

    def load_commandes_list(self):
        """Charge la liste des commandes depuis la base de données."""
        self.commandes = fetch.fetch_commandes()
        self.commandes_list.clear()

        for commande in self.commandes:
            acheteur_nom = fetch.get_acheteur_nom(commande[4])
            item = QListWidgetItem(f"Commande #{commande[0]} - {acheteur_nom}")
            item.setData(Qt.UserRole, commande[0])
            self.commandes_list.addItem(item)

    def on_commande_clicked(self, item):
        """Affiche les détails de la commande sélectionnée."""
        id_commande = item.data(Qt.UserRole)
        commande = next((c for c in self.commandes if c[0] == id_commande), None)

        if commande:
            acheteur_nom = fetch.get_acheteur_nom(commande[4])
            details = (
                f"ID Commande: {commande[0]}\n"
                f"Date: {commande[1]}\n"
                f"Coût avant taxe: {commande[2]} €\n"
                f"Coût après taxe: {commande[3]} €\n"
                f"Acheteur: {acheteur_nom}\n"
                f"Statut: {commande[5]}"
            )
            self.commandes_details.setText(details)

    def open_add_dialog(self):
        """Ouvre une boîte de dialogue pour ajouter une commande."""
        dialog = AddCommandeDialog(self)
        if dialog.exec():
            self.load_commandes_list()

    def open_modify_dialog(self):
        """Ouvre une boîte de dialogue pour modifier une commande."""
        selected_item = self.commandes_list.currentItem()
        if selected_item:
            id_commande = selected_item.data(Qt.UserRole)
            commande = next((c for c in self.commandes if c[0] == id_commande), None)

            if commande:
                dialog = ModifyCommandeDialog(commande, self)
                if dialog.exec():
                    self.load_commandes_list()

    def cancel_commande(self):
        """Annule la commande sélectionnée."""
        selected_item = self.commandes_list.currentItem()
        if selected_item:
            id_commande = selected_item.data(Qt.UserRole)
            fetch.supprimer_commande(id_commande)
            QMessageBox.information(self.widget, "Succès", "Commande annulée avec succès.")
            self.load_commandes_list()
            self.commandes_details.clear()



class AddCommandeDialog(QDialog):
    def __init__(self, parent=None):
        # Si parent n'est pas un QWidget, le remplacer par None
        if not isinstance(parent, QWidget):
            parent = None
        super().__init__(parent)
        self.setWindowTitle("Ajouter une commande")
        layout = QFormLayout(self)

        # Champ de date
        self.date_input = QLineEdit()
        layout.addRow("Date (YYYY-MM-DD):", self.date_input)

        # Champ coût avant taxe
        self.cout_avant_input = QLineEdit()
        layout.addRow("Coût avant taxe:", self.cout_avant_input)
        self.cout_apres_label = QLineEdit()
        self.cout_apres_label.setReadOnly(True)
        layout.addRow("Coût après taxe (calculé):", self.cout_apres_label)

        # Connecter le coût avant taxe pour recalculer le coût après taxe
        self.cout_avant_input.textChanged.connect(self.calculate_cout_apres_taxe)

        
        # Sélection de l'acheteur
        self.buyer_group = QButtonGroup(self)
        self.client_radio = QRadioButton("Client")
        self.succursale_radio = QRadioButton("Succursale")
        self.entrepot_radio = QRadioButton("Entrepôt")
        self.buyer_group.addButton(self.client_radio)
        self.buyer_group.addButton(self.succursale_radio)
        self.buyer_group.addButton(self.entrepot_radio)
        self.buyer_group.buttonClicked.connect(self.load_acheteur_options)
        
        layout.addRow("Type d'acheteur:", self.client_radio)
        layout.addRow("", self.succursale_radio)
        layout.addRow("", self.entrepot_radio)
        
        self.acheteur_combo = QComboBox()
        layout.addRow("Acheteur:", self.acheteur_combo)

        # Statut
        self.statut_input = QLineEdit()
        layout.addRow("Statut:", self.statut_input)

        self.save_button = QPushButton("Ajouter")
        self.save_button.clicked.connect(self.add_commande)
        layout.addWidget(self.save_button)
        
    def calculate_cout_apres_taxe(self):
        """Calcule automatiquement le coût après taxe."""
        cout_avant = float(self.cout_avant_input.text())
        taxes = fetch.fetch_taxes()  # Récupère TPS et TVQ
        if taxes:
            tps, tvq = taxes
            cout_apres = cout_avant * (1 + tps + tvq)
            self.cout_apres_label.setText(f"{cout_apres:.2f}")
    
    def load_acheteur_options(self):
        """Charge les options pour le type d'acheteur sélectionné."""
        self.acheteur_combo.clear()
        if self.client_radio.isChecked():
            acheteurs = fetch.fetch_client()
            acheteurs = [{'id': client[0], 'nom': f"{client[4]} {client[5]}"} for client in acheteurs]
        elif self.succursale_radio.isChecked():
            acheteurs = fetch.fetch_succursale()
            acheteurs = [{'id': succursale[0], 'nom': succursale[2]} for succursale in acheteurs]
        elif self.entrepot_radio.isChecked():
            acheteurs = fetch.fetch_entrepot()
            acheteurs = [{'id': entrepot[0], 'nom': entrepot[2]} for entrepot in acheteurs]
        else:
            acheteurs = []
            
        for acheteur in acheteurs:
            self.acheteur_combo.addItem(acheteur['nom'], acheteur['id'])




    def add_commande(self):
        fetch.ajouter_commande(
            self.date_input.text(),
            float(self.cout_avant_input.text()),
            float(self.cout_apres_label.text()),
            self.acheteur_combo.currentData(),
            self.statut_input.text()
        )
        QMessageBox.information(self, "Succès", "Commande ajoutée avec succès.")
        self.accept()





class ModifyCommandeDialog(QDialog):
    def __init__(self, commande_data, parent=None):
        # Si parent n'est pas un QWidget, le remplacer par None
        if not isinstance(parent, QWidget):
            parent = None
        super().__init__(parent)
        self.setWindowTitle("Modifier une commande")
        self.setMinimumSize(400, 300)

        self.commande_data = commande_data  

        layout = QFormLayout(self)

        # Champ de date
        self.date_input = QLineEdit(self)
        self.date_input.setText(commande_data[1])  # Index 1 pour `date_commande`
        layout.addRow("Date (YYYY-MM-DD):", self.date_input)

        # Champ coût avant taxe
        self.cout_avant_input = QLineEdit(self)
        self.cout_avant_input.setText(str(commande_data[2]))  # Index 2 pour `cout_avant_taxe`
        self.cout_avant_input.textChanged.connect(self.calculate_cout_apres_taxe)
        layout.addRow("Coût avant taxe:", self.cout_avant_input)

        # Champ coût après taxe (calculé)
        self.cout_apres_label = QLineEdit(self)
        self.cout_apres_label.setReadOnly(True)
        layout.addRow("Coût après taxe (calculé):", self.cout_apres_label)
        
        # Calcul initial
        self.calculate_cout_apres_taxe()


        # Champ statut
        self.statut_input = QLineEdit(self)
        self.statut_input.setText(commande_data[5])  # Index 5 pour `statut`
        layout.addRow("Statut:", self.statut_input)


        # Boutons
        save_button = QPushButton("Enregistrer")
        save_button.clicked.connect(self.save_changes)
        layout.addWidget(save_button)
    
    def calculate_cout_apres_taxe(self):
        """Calcule automatiquement le coût après taxe."""
        cout_avant = float(self.cout_avant_input.text())
        taxes = fetch.fetch_taxes()
        if taxes:
            tps, tvq = taxes
            cout_apres = cout_avant * (1 + tps + tvq)
            self.cout_apres_label.setText(f"{cout_apres:.2f}")

    def save_changes(self):
        """Enregistre les modifications dans la base de données."""
        fetch.modifier_commande(
            self.commande_data[0],  # Index 0 pour `id_commande`
            self.date_input.text(),
            float(self.cout_avant_input.text()),
            self.statut_input.text()
        )
        QMessageBox.information(self, "Succès", "Modifications enregistrées avec succès.")
        self.accept()  # Fermer la boîte de dialogue
