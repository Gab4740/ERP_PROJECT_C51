from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QComboBox, QLineEdit, QTextEdit, QDialog, QMessageBox, QWidget, QSpinBox, QDoubleSpinBox, QDateEdit
from Onglet import Onglet
import fetch

class Onglet_entrepot(Onglet):
    def __init__(self, name, visibility, parent_widget=None):
        super().__init__(name, visibility)
        self.parent_widget = parent_widget

    def create_content(self):
        # Création du layout principal
        layout = QVBoxLayout()

        # Choisir l'entrepôt
        self.entrepot_combo = QComboBox()
        self.load_entrepot_list()
        #self.entrepot_combo.addItems(["Entrepôt A", "Entrepôt B", "Entrepôt C", "Entrepôt D"])
        layout.addWidget(QLabel("Choisir l'entrepôt:"))
        layout.addWidget(self.entrepot_combo)

        # Champ de recherche (optionnel, selon tes besoins)
        # self.recherche_input = QLineEdit()
        # self.recherche_input.setPlaceholderText("Entrez votre recherche")
        # layout.addWidget(QLabel("Recherche:"))
        # layout.addWidget(self.recherche_input)

        # Bouton de recherche
        self.recherche_button = QPushButton("Recherche")
        self.recherche_button.clicked.connect(self.on_recherche_clicked)  # Connexion au gestionnaire de clic
        layout.addWidget(self.recherche_button)

        # Affichage des résultats ou autre information
        self.resultats_display = QTextEdit()
        self.resultats_display.setReadOnly(True)
        layout.addWidget(QLabel("Résultats de la recherche:"))
        layout.addWidget(self.resultats_display)

        # Ajouter un nouvel entrepôt
        # self.new_entrepot_input = QLineEdit()
        # self.new_entrepot_input.setPlaceholderText("Nom du nouvel entrepôt")
        # layout.addWidget(QLabel("Ajouter un nouvel entrepôt:"))
        # layout.addWidget(self.new_entrepot_input)

        # Bouton pour ajouter un entrepôt
        self.ajouter_button = QPushButton("Ajouter l'entrepôt")
        self.ajouter_button.clicked.connect(self.on_ajouter_clicked)  # Connexion au gestionnaire d'ajout
        layout.addWidget(self.ajouter_button)

        # Bouton pour supprimer un entrepôt
        self.supprimer_button = QPushButton("Supprimer l'entrepôt")
        self.supprimer_button.clicked.connect(self.on_supprimer_clicked)  # Connexion au gestionnaire de suppression
        layout.addWidget(self.supprimer_button)
        
        self.widget.setLayout(layout)
    
    def load_entrepot_list(self):
        entrepots = fetch.fetch_entrepot()  # Récupère une liste de tuples (id_entrepot, nom)
        self.entrepot_combo.clear()  # Vide la combo box actuelle

        for entrepot in entrepots:
            id_entrepot = entrepot[0]  # La première colonne est id_entrepot
            nom = entrepot[2]  # La troisième colonne est le nom de l'entrepot dans info_INFO_CIE
            self.entrepot_combo.addItem(nom, userData=id_entrepot)
    
    def get_info_by_nom(self, nom):
        entrepots = fetch.fetch_entrepot()  
        for row in entrepots:
            if row[2] == nom:
                return {
                    "id_entrepot": row[0],
                    "nom": row[2],
                    "adresse": row[3],
                    "telephone": row[4],
                    "email": row[5],
                    "type": row[6]
                }
        return None

    def on_recherche_clicked(self):
        entrepot = self.entrepot_combo.currentText()  # Obtient l'entrepot sélectionné
        #recherche = self.recherche_input.text()  # Obtient la recherche entrée par l'utilisateur
        
        # Récupérer les infos de l'entrepot
        infos_entrepot = self.get_info_by_nom(entrepot)

        if infos_entrepot:
            # Construire le texte à afficher
            details = (
                f"ID Entrepot : {infos_entrepot['id_entrepot']}\n"
                f"Nom : {infos_entrepot['nom']}\n"
                f"Adresse : {infos_entrepot['adresse']}\n"
                f"Téléphone : {infos_entrepot['telephone']}\n"
                f"Email : {infos_entrepot['email']}\n"
                f"Type : {infos_entrepot['type']}\n"
            )
            
            ###### AJOUTER CUSTOM FIELDS ##########################
            custom_fields = fetch.fetch_custom_field_values("Entrepôt", infos_entrepot["id_entrepot"])
            for field_name, value in custom_fields:
                details += f"{field_name}: {value}\n"
            ##############################################################################
            
            self.resultats_display.setText(details)
        else:
            # Si aucune info trouvée
            self.resultats_display.setText("Aucune information trouvée pour cet entrepôt.")

    def on_ajouter_clicked(self):
        dialog = AjouterEntrepotDialog(self.parent_widget if isinstance(self.parent_widget, QWidget) else None)
        if dialog.exec():
            data = dialog.confirmer()
            if data:
                entrepot_id = fetch.ajouter_entrepot(
                    nom=data["nom"],
                    adresse=data["adresse"],
                    telephone=data["telephone"],
                    email=data["email"],
                    type_cie=data["type_cie"],
                )

                # Enregistrer les champs personnalisés
                fetch.save_custom_field_values("Entrepôt", entrepot_id, data["custom_fields"])

                QMessageBox.information(
                    self.parent_widget if isinstance(self.parent_widget, QWidget) else None,
                    "Succès",
                    "Entrepôt ajouté avec succès."
                )
                self.load_entrepot_list()
        else:
            QMessageBox.information(
                self.parent_widget if isinstance(self.parent_widget, QWidget) else None,
                "Annulé",
                "Ajout annulé."
            )

    def on_supprimer_clicked(self):
        selected_entrepot = self.entrepot_combo.currentText()  

        if selected_entrepot:
            # Demander confirmation à l'utilisateur
            reply = QMessageBox.question(
                self.parent_widget if isinstance(self.parent_widget, QWidget) else None,
                "Confirmation",
                f"Voulez-vous vraiment supprimer l'entrepôt '{selected_entrepot}' ?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )

            if reply == QMessageBox.StandardButton.Yes:
                fetch.supprimer_entrepot(selected_entrepot)

                # Afficher un message de succès
                QMessageBox.information(self.parent_widget if isinstance(self.parent_widget, QWidget) else None, "Succès", f"L'entrepôt '{selected_entrepot}' a été supprimée.")

                # Mettre à jour l'interface
                self.load_entrepot_list()  
                self.resultats_display.clear()  

        else:
            self.resultats_display.setText("Veuillez sélectionner un entrepôt à supprimer.")


class AjouterEntrepotDialog(QDialog):
    def __init__(self, parent=None):
        # Si parent n'est pas un QWidget, le remplacer par None
        if not isinstance(parent, QWidget):
            parent = None
        super().__init__(parent)
        self.setWindowTitle("Ajouter un nouveau entrepôt")
        self.setMinimumSize(400, 300)

        # Champs de saisie
        self.nom_input = QLineEdit(self)
        self.adresse_input = QLineEdit(self)
        self.telephone_input = QLineEdit(self)
        self.email_input = QLineEdit(self)
        self.type_input = QLineEdit(self)

        # Mise en page
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Nom de l'entrepôt:"))
        layout.addWidget(self.nom_input)
        layout.addWidget(QLabel("Adresse:"))
        layout.addWidget(self.adresse_input)
        layout.addWidget(QLabel("Téléphone:"))
        layout.addWidget(self.telephone_input)
        layout.addWidget(QLabel("Email:"))
        layout.addWidget(self.email_input)
        layout.addWidget(QLabel("Type:"))
        layout.addWidget(self.type_input)
        
        ###### AJOUTER CUSTOM FIELDS ##########################
        self.dynamic_fields = {}
        dynamic_fields = fetch.fetch_custom_fields("Entrepôt")
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
            layout.addWidget(QLabel(field_name))
            layout.addWidget(widget)
        ##############################################################################
        

        # Boutons
        buttons_layout = QHBoxLayout()
        self.confirmer_button = QPushButton("Confirmer")
        self.annuler_button = QPushButton("Annuler")

        buttons_layout.addWidget(self.confirmer_button)
        buttons_layout.addWidget(self.annuler_button)
        layout.addLayout(buttons_layout)

        self.setLayout(layout)

        # Connecter les boutons
        self.confirmer_button.clicked.connect(self.confirmer)
        self.annuler_button.clicked.connect(self.reject)

    def confirmer(self):
        nom = self.nom_input.text().strip()
        adresse = self.adresse_input.text().strip()
        telephone = self.telephone_input.text().strip()
        email = self.email_input.text().strip()
        type_cie = self.type_input.text().strip()

        if not nom:
            QMessageBox.warning(self, "Erreur", "Le nom de l'entrepôt est obligatoire.")
            return
        if len(telephone) > 15:
            QMessageBox.warning(self, "Erreur", "Le numéro de téléphone ne doit pas dépasser 15 caractères.")
            return
        if not email or "@" not in email:
            QMessageBox.warning(self, "Erreur", "Veuillez entrer une adresse email valide.")
            return

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

        self.accept()
        return {
            "nom": nom,
            "adresse": adresse,
            "telephone": telephone,
            "email": email,
            "type_cie": type_cie,
            "custom_fields": custom_field_values
        }
