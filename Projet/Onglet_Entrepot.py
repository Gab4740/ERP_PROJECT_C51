from PySide6.QtWidgets import QVBoxLayout, QPushButton, QLabel, QComboBox, QLineEdit, QTextEdit
from Onglet import Onglet

class Onglet_entrepot(Onglet):
    def __init__(self, name, visibility):
        super().__init__(name, visibility)

    def create_content(self):
        # Création du layout principal
        layout = QVBoxLayout()

        # Choisir l'entrepôt
        self.entrepot_combo = QComboBox()
        self.entrepot_combo.addItems(["Entrepôt A", "Entrepôt B", "Entrepôt C", "Entrepôt D"])
        layout.addWidget(QLabel("Choisir l'entrepôt:"))
        layout.addWidget(self.entrepot_combo)

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

        # Ajouter un nouvel entrepôt
        self.new_entrepot_input = QLineEdit()
        self.new_entrepot_input.setPlaceholderText("Nom du nouvel entrepôt")
        layout.addWidget(QLabel("Ajouter un nouvel entrepôt:"))
        layout.addWidget(self.new_entrepot_input)

        # Bouton pour ajouter un entrepôt
        self.ajouter_button = QPushButton("Ajouter l'entrepôt")
        self.ajouter_button.clicked.connect(self.on_ajouter_clicked)  # Connexion au gestionnaire d'ajout
        layout.addWidget(self.ajouter_button)

        # Bouton pour supprimer un entrepôt
        self.supprimer_button = QPushButton("Supprimer l'entrepôt")
        self.supprimer_button.clicked.connect(self.on_supprimer_clicked)  # Connexion au gestionnaire de suppression
        layout.addWidget(self.supprimer_button)
        
        self.widget.setLayout(layout)

    def on_recherche_clicked(self):
        """Gestionnaire du clic sur le bouton 'Recherche'"""
        entrepot = self.entrepot_combo.currentText()  # Obtient l'entrepôt sélectionné
        recherche = self.recherche_input.text()  # Obtient la recherche entrée par l'utilisateur

        # Simuler une recherche (ici un simple message affiché pour l'exemple)
        self.resultats_display.setText(f"Recherche '{recherche}' dans {entrepot}...\nRésultats : ...")

    def on_ajouter_clicked(self):
        """Gestionnaire du clic sur le bouton 'Ajouter l'entrepôt'"""
        new_entrepot = self.new_entrepot_input.text().strip()  # Récupère le texte saisi pour le nouvel entrepôt

        if new_entrepot:
            # Ajout du nouvel entrepôt dans la liste déroulante
            self.entrepot_combo.addItem(new_entrepot)
            self.new_entrepot_input.clear()  # Effacer le champ de texte après l'ajout
            self.resultats_display.setText(f"Entrepôt '{new_entrepot}' ajouté avec succès!")
        else:
            # Si le champ est vide, on affiche un message d'erreur
            self.resultats_display.setText("Veuillez entrer un nom d'entrepôt valide.")

    def on_supprimer_clicked(self):
        """Gestionnaire du clic sur le bouton 'Supprimer l'entrepôt'"""
        selected_entrepot = self.entrepot_combo.currentText()  # Récupère l'entrepôt sélectionné

        if selected_entrepot:
           pass
           # SUPPRIMER L'ENTREPOT ICI
        else:
            # Si aucun entrepôt n'est sélectionné
            self.resultats_display.setText("Veuillez sélectionner un entrepôt à supprimer.")