from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QComboBox, QLineEdit, QTextEdit, QDialog, QMessageBox, QWidget, QSpinBox, QDoubleSpinBox, QDateEdit
from Onglet import Onglet
import fetch

class Onglet_magasin(Onglet):
    def __init__(self, name, visibility, parent_widget=None):
        super().__init__(name, visibility)
        self.parent_widget = parent_widget

    def create_content(self):
        # Création du layout principal
        layout = QVBoxLayout()

        # Choisir le magasin (Chargement des fichiers dans le dossier)
        self.magasin_combo = QComboBox()
        self.load_magasin_list()  # Charge la liste des magasins depuis les fichiers
        self.title = QLabel("Choisir le magasin:")
        self.title.setStyleSheet("font-weight: bold; font-size: 18px;")
        layout.addWidget(self.title)
        layout.addWidget(self.magasin_combo)

        # Champ de recherche (optionnel, selon tes besoins)
        # self.recherche_input = QLineEdit()
        # self.recherche_input.setPlaceholderText("Entrez votre recherche")
        # layout.addWidget(QLabel("Recherche:"))
        # layout.addWidget(self.recherche_input)

        # Bouton de recherche
        self.recherche_button = QPushButton("Recherche")
        self.recherche_button.clicked.connect(self.on_recherche_clicked)  # Connexion au gestionnaire de clic
        layout.addWidget(self.recherche_button)
        self.recherche_button.setStyleSheet("""
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

        # Affichage des résultats ou autre information
        self.resultats_display = QTextEdit()
        self.resultats_display.setReadOnly(True)
        self.title = QLabel("Résultats de la recherche:")
        self.title.setStyleSheet("font-weight: bold; font-size: 18px;")
        layout.addWidget(self.title)
        layout.addWidget(self.resultats_display)
        self.resultats_display.setStyleSheet("""
            QTextEdit {
                background-color: #f0f0f0;
                background-color: #f7f7f7;
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 5px;
            }
        """)

        # Ajouter un nouveau magasin
        # self.new_magasin_input = QLineEdit()
        # self.new_magasin_input.setPlaceholderText("Nom du nouveau magasin")
        # layout.addWidget(QLabel("Ajouter un nouveau magasin:"))
        # layout.addWidget(self.new_magasin_input)

        # Bouton pour ajouter un magasin
        self.ajouter_button = QPushButton("Ajouter le magasin")
        self.ajouter_button.clicked.connect(self.on_ajouter_clicked)  # Connexion au gestionnaire d'ajout
        layout.addWidget(self.ajouter_button)
        self.ajouter_button.setStyleSheet("""
            QPushButton {
                background-color: #91AB00;
                color: white;
                border: 1px solid #ccc;
                border-radius: 20px;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #687A00;
            }
        """)

        # Bouton pour supprimer un magasin
        self.supprimer_button = QPushButton("Supprimer le magasin")
        self.supprimer_button.clicked.connect(self.on_supprimer_clicked)  # Connexion au gestionnaire de suppression
        layout.addWidget(self.supprimer_button)
        self.supprimer_button.setStyleSheet("""
            QPushButton {
                background-color: #D22B2B;
                color: white;
                border: 1px solid #ccc;
                border-radius: 20px;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #A52A2A;
            }
        """)
        
        self.widget.setLayout(layout)

    def load_magasin_list(self):
        # CHERCHER LES MAGASINS DANS LA BD
        magasins = fetch.fetch_succursale()  # Récupère une liste de tuples (id_succursale, nom)
        self.magasin_combo.clear()  # Vide la combo box actuelle

        for magasin in magasins:
            id_succursale = magasin[0]  # La première colonne est id_succursale
            nom = magasin[2]  # La troisième colonne est le nom de la succursale dans info_INFO_CIE
            self.magasin_combo.addItem(nom, userData=id_succursale)


    def get_info_by_nom(self, nom):
        succursales = fetch.fetch_succursale()  # Liste de tuples (id_succursale, nom, adresse, téléphone, email, type, ...)
        for row in succursales:
            # row[1] est le nom car la requête sélectionne id_succursale, puis toutes les colonnes de info_CIE
            if row[2] == nom:  # row[2] correspond au nom de la succursale
                return {
                    "id_succursale": row[0],
                    "nom": row[2],
                    "adresse": row[3],
                    "telephone": row[4],
                    "email": row[5],
                    "type": row[6]
                }
        
        return None
    



    def on_recherche_clicked(self):
        magasin = self.magasin_combo.currentText()  # Obtient le magasin sélectionné
        #recherche = self.recherche_input.text()  # Obtient la recherche entrée par l'utilisateur
        
        # Récupérer les infos de la succursale
        infos_magasin = self.get_info_by_nom(magasin)

        if infos_magasin:
            # Construire le texte à afficher
            details = (
                f"ID Succursale : {infos_magasin['id_succursale']}\n"
                f"Nom : {infos_magasin['nom']}\n"
                f"Adresse : {infos_magasin['adresse']}\n"
                f"Téléphone : {infos_magasin['telephone']}\n"
                f"Email : {infos_magasin['email']}\n"
                f"Type : {infos_magasin['type']}\n"
            )
            
            ###### AJOUTER CUSTOM FIELDS ##########################
            custom_fields = fetch.fetch_custom_field_values("Succursale", infos_magasin["id_succursale"])
            for field_name, value in custom_fields:
                details += f"{field_name}: {value}\n"
            ####################################################
            
            self.resultats_display.setText(details)
        else:
            # Si aucune info trouvée
            self.resultats_display.setText("Aucune information trouvée pour ce magasin.")
        
        

    def on_ajouter_clicked(self):
        dialog = AjouterMagasinDialog(self.parent_widget if isinstance(self.parent_widget, QWidget) else None)
        if dialog.exec():  # Si l'utilisateur valide le dialogue
            data = dialog.confirmer()  # Récupérer les données confirmées
            if data:  # S'assurer que les données sont retournées
                magasin_id = fetch.ajouter_succursale(
                    nom=data["nom"],
                    adresse=data["adresse"],
                    telephone=data["telephone"],
                    email=data["email"],
                    type_cie=data["type_cie"],
                )

                # Enregistrer les valeurs des champs personnalisés
                fetch.save_custom_field_values("Succursale", magasin_id, data["custom_fields"])

                QMessageBox.information(
                    self.parent_widget if isinstance(self.parent_widget, QWidget) else None,
                    "Succès",
                    "Magasin ajouté avec succès."
                )
                self.load_magasin_list()
        else:
            QMessageBox.information(
                self.parent_widget if isinstance(self.parent_widget, QWidget) else None,
                "Annulé",
                "Ajout annulé."
            )



    def on_supprimer_clicked(self):
        selected_magasin = self.magasin_combo.currentText()  # Récupère le magasin sélectionné

        if selected_magasin:
            # Demander confirmation à l'utilisateur
            reply = QMessageBox.question(
                self.parent_widget if isinstance(self.parent_widget, QWidget) else None,
                "Confirmation",
                f"Voulez-vous vraiment supprimer la succursale '{selected_magasin}' ?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )

            if reply == QMessageBox.StandardButton.Yes:
                # Supprimer le magasin via la fonction dans fetch.py
                fetch.supprimer_succursale(selected_magasin)

                # Afficher un message de succès
                QMessageBox.information(self.parent_widget if isinstance(self.parent_widget, QWidget) else None, "Succès", f"La succursale '{selected_magasin}' a été supprimée.")

                # Mettre à jour l'interface
                self.load_magasin_list()  # Recharger la liste des magasins
                self.resultats_display.clear()  # Effacer l'affichage des résultats

        else:
            # Si aucun magasin sélectionné
            self.resultats_display.setText("Veuillez sélectionner un magasin à supprimer.")

class AjouterMagasinDialog(QDialog):
    def __init__(self, parent=None):
        # Si parent n'est pas un QWidget, le remplacer par None
        if not isinstance(parent, QWidget):
            parent = None
        super().__init__(parent)
        self.setWindowTitle("Ajouter un nouveau magasin")
        self.setMinimumSize(400, 300)

        # Champs de saisie
        self.nom_input = QLineEdit(self)
        self.adresse_input = QLineEdit(self)
        self.telephone_input = QLineEdit(self)
        self.email_input = QLineEdit(self)
        self.type_input = QLineEdit(self)

        # Mise en page
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Nom du magasin:"))
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
        dynamic_fields = fetch.fetch_custom_fields("Succursale")  # Charger les custom fields pour "Succursale"
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
                continue  # Ignorer les types inconnus

            self.dynamic_fields[field_id] = widget
            layout.addWidget(QLabel(field_name))
            layout.addWidget(widget)
        ####################################################
        
        
        
        

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
            QMessageBox.warning(self, "Erreur", "Le nom du magasin est obligatoire.")
            return
        if len(telephone) > 15:
            QMessageBox.warning(self, "Erreur", "Le numéro de téléphone ne doit pas dépasser 15 caractères.")
            return
        if not email or "@" not in email:
            QMessageBox.warning(self, "Erreur", "Veuillez entrer une adresse email valide.")
            return
        
        ###### RÉCUPÉRER CUSTOM FIELDS ##########################
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
        ####################################################

        # Données validées
        self.accept()
        return {
            "nom": nom,
            "adresse": adresse,
            "telephone": telephone,
            "email": email,
            "type_cie": type_cie,
            "custom_fields": custom_field_values
        }
