from PySide6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QCheckBox, QLabel, QTextEdit, QPushButton, 
    QDialog, QFormLayout, QLineEdit, QMessageBox, QListWidgetItem, QWidget, QButtonGroup, QRadioButton, QComboBox, QListWidget
)
from PySide6.QtCore import Qt
from Onglet import Onglet
import fetch

class Onglet_Config(Onglet):
    def __init__(self, name, visibility, parent_widget=None):
        super().__init__(name, visibility)
        self.parent_widget = parent_widget
        self.custom_fields = []
        
    
    def create_content(self):       
        self.widget.setLayout(self.init_ui())
        self.load_custom_fields_list()
    
    def init_ui(self):
        """Initialise l'interface utilisateur."""
        main_layout = QVBoxLayout()

        # Bouton pour ajouter un champ
        self.custom_field_button = QPushButton("Ajouter un champ")
        self.custom_field_button.setStyleSheet("""
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
        self.custom_field_button.clicked.connect(self.open_custom_field_dialog)
        main_layout.addWidget(self.custom_field_button)

        # Liste des champs personnalisés
        self.fields_list = QListWidget()
        self.fields_list.setStyleSheet("""
            QListWidget {
                background-color: #f7f7f7;
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 5px;
            }
            QListWidget::item {
                padding: 10px;
                border-radius: 5px;
                font-size: 14px;
                color: black;
            }
            QListWidget::item:hover {
                background-color: #98ab96;
            }
        """)
        main_layout.addWidget(self.fields_list)

        # Bouton pour supprimer un champ
        self.delete_field_button = QPushButton("Supprimer un champ")
        self.delete_field_button.setStyleSheet("""
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
        self.delete_field_button.clicked.connect(self.delete_custom_field)
        main_layout.addWidget(self.delete_field_button)

        return main_layout
    
    def load_custom_fields_list(self):
        self.fields_list.clear()
        self.custom_fields = fetch.fetch_custom_fields()  # Charger tous les champs personnalisés sans filtre
        if not self.custom_fields:
            return
        for field in self.custom_fields:
            field_name = field[1]
            field_type = field[2]
            item = QListWidgetItem(f"{field_name} ({field_type})")  # Affiche `field_name` et `field_type`
            item.setData(Qt.UserRole, field[0])  # Stocke l'ID du champ personnalisé
            self.fields_list.addItem(item)
    
    def open_custom_field_dialog(self):
        dialog = AddCustomFieldDialog(self)
        if dialog.exec():
            self.load_custom_fields_list()
    
    def delete_custom_field(self):
        """Supprime le champ personnalisé sélectionné."""
        selected_item = self.fields_list.currentItem()
        if selected_item:
            field_id = selected_item.data(Qt.UserRole)
            field_name = selected_item.text()

            # Demander confirmation
            reply = QMessageBox.question(
                self.widget,
                "Confirmation de suppression",
                f"Êtes-vous sûr de vouloir supprimer le champ '{field_name}' ?",
                QMessageBox.Yes | QMessageBox.No
            )
            if reply == QMessageBox.Yes:
                fetch.delete_custom_field(field_id)
                QMessageBox.information(self.widget, "Succès", "Champ personnalisé supprimé avec succès.")
                self.load_custom_fields_list()
        else:
            QMessageBox.warning(self.widget, "Erreur", "Veuillez sélectionner un champ à supprimer.")

class AddCustomFieldDialog(QDialog):
    def __init__(self, parent=None):
        # Si parent n'est pas un QWidget, le remplacer par None
        if not isinstance(parent, QWidget):
            parent = None
        super().__init__(parent)
        self.setWindowTitle("Ajouter un Champ Personnalisé")
        self.setMinimumSize(400, 300)

        layout = QFormLayout(self)

        self.entity_type_input = QComboBox()
        self.entity_type_input.addItems(["Commande", "Client", "Succursale", "Entrepôt"])  # À COMPLETER
        layout.addRow("Entité Associée:", self.entity_type_input)

        self.field_name_input = QLineEdit()
        layout.addRow("Nom du Champ:", self.field_name_input)

        self.field_type_input = QComboBox()
        self.field_type_input.addItems(["TEXT", "INTEGER", "FLOAT", "DATE"])
        layout.addRow("Type du Champ:", self.field_type_input)

        self.required_input = QCheckBox()
        layout.addRow("Champ Obligatoire:", self.required_input)

        save_button = QPushButton("Ajouter")
        save_button.clicked.connect(self.add_custom_field)
        layout.addWidget(save_button)

        self.setLayout(layout)

    def add_custom_field(self):
        entity_type = self.entity_type_input.currentText()
        field_name = self.field_name_input.text()
        field_type = self.field_type_input.currentText()
        is_required = self.required_input.isChecked()

        fetch.add_custom_field(entity_type, field_name, field_type, is_required)
        QMessageBox.information(self, "Succès", "Champ personnalisé ajouté avec succès.")
        self.accept()
