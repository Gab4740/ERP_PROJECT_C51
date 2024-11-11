from PySide6.QtWidgets import QVBoxLayout, QPushButton, QLabel, QComboBox, QLineEdit, QTextEdit
from Onglet import Onglet

class Onglet_magasin(Onglet):
    def __init__(self, name, visibility):
        super().__init__(name, visibility)

    def create_content(self):
        # Création du layout principal
        layout = QVBoxLayout()

        # Choisir le magasin (Chargement des fichiers dans le dossier)
        self.magasin_combo = QComboBox()
        self.load_magasin_list()  # Charge la liste des magasins depuis les fichiers
        layout.addWidget(QLabel("Choisir le magasin:"))
        layout.addWidget(self.magasin_combo)

        # Champ de recherche (optionnel, selon tes besoins)
        self.recherche_input = QLineEdit()
        self.recherche_input.setPlaceholderText("Entrez votre recherche")
        layout.addWidget(QLabel("Recherche:"))
        layout.addWidget(self.recherche_input)

        # Bouton de recherche
        self.recherche_button = QPushButton("Recherche")
        self.recherche_button.clicked.connect(self.on_recherche_clicked)  # Connexion au gestionnaire de clic
        layout.addWidget(self.recherche_button)

        # Affichage des résultats ou autre information
        self.resultats_display = QTextEdit()
        self.resultats_display.setReadOnly(True)
        layout.addWidget(QLabel("Résultats de la recherche:"))
        layout.addWidget(self.resultats_display)

        # Ajouter un nouveau magasin
        self.new_magasin_input = QLineEdit()
        self.new_magasin_input.setPlaceholderText("Nom du nouveau magasin")
        layout.addWidget(QLabel("Ajouter un nouveau magasin:"))
        layout.addWidget(self.new_magasin_input)

        # Bouton pour ajouter un magasin
        self.ajouter_button = QPushButton("Ajouter le magasin")
        self.ajouter_button.clicked.connect(self.on_ajouter_clicked)  # Connexion au gestionnaire d'ajout
        layout.addWidget(self.ajouter_button)

        # Bouton pour supprimer un magasin
        self.supprimer_button = QPushButton("Supprimer le magasin")
        self.supprimer_button.clicked.connect(self.on_supprimer_clicked)  # Connexion au gestionnaire de suppression
        layout.addWidget(self.supprimer_button)
        
        self.widget.setLayout(layout)

    def load_magasin_list(self):
        """Charge les magasins disponibles depuis les fichiers dans le répertoire."""
        # CHERCHER LES MAGASINS DANS LA BD

    def on_recherche_clicked(self):
        """Gestionnaire du clic sur le bouton 'Recherche'"""
        magasin = self.magasin_combo.currentText()  # Obtient le magasin sélectionné
        recherche = self.recherche_input.text()  # Obtient la recherche entrée par l'utilisateur

        # Simuler une recherche (ici un simple message affiché pour l'exemple)
        self.resultats_display.setText(f"Recherche '{recherche}' dans le magasin {magasin}...\nRésultats : ...")

    def on_ajouter_clicked(self):
        """Gestionnaire du clic sur le bouton 'Ajouter le magasin'"""
        new_magasin = self.new_magasin_input.text().strip()  # Récupère le texte saisi pour le nouveau magasin

        if new_magasin:
            # CRÉER NOUVEAU MAGASIN ICI
            pass
        else:
            self.resultats_display.setText("Veuillez entrer un nom de magasin valide.")

    def on_supprimer_clicked(self):
        """Gestionnaire du clic sur le bouton 'Supprimer le magasin'"""
        selected_magasin = self.magasin_combo.currentText()  # Récupère le magasin sélectionné

        if selected_magasin:
            # SUPPRIMER MAGASIN ICI
           pass
        else:
            self.resultats_display.setText("Veuillez sélectionner un magasin à supprimer.")
