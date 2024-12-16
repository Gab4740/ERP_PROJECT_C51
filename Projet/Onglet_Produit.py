from PySide6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QListWidget, QListWidgetItem, QLabel, QTextEdit, QPushButton,
    QDialog, QFormLayout, QLineEdit, QMessageBox, QComboBox, QSpinBox, QDoubleSpinBox, QWidget, QButtonGroup, QRadioButton
)
from PySide6.QtCore import Qt
from Onglet import Onglet
import fetch


class Onglet_Produits(Onglet):
    def __init__(self, name, visibility, parent_widget=None):
        super().__init__(name, visibility)
        self.parent_widget = parent_widget
        self.selected_product = None

    def create_content(self):
        self.widget.setLayout(self.init_ui())
        self.update_product_list()

    def init_ui(self):
        # Main layout - Horizontal layout to split the window
        main_layout = QHBoxLayout()

        # Left: Product list
        left_layout = QVBoxLayout()

        self.product_list = QListWidget()
        self.product_list.setStyleSheet("""
            QListWidget {
                background-color: #f7f7f7;
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 5px;
            }
            QListWidget::item {
                padding: 10px;
                border-radius: 5px;
                font-size: 16px;
                color: black;
            }
            QListWidget::item:hover {
                background-color: #98ab96;
            }
        """)
        self.product_list.itemClicked.connect(self.on_product_clicked)
        left_layout.addWidget(self.product_list)

        main_layout.addLayout(left_layout)

        # Right: Product details and actions
        right_layout = QVBoxLayout()

        # Product details section
        self.details_label = QLabel('Détails du produit:')
        self.details_label.setStyleSheet("font-weight: bold; font-size: 18px;")
        right_layout.addWidget(self.details_label)

        self.product_details = QTextEdit()
        self.product_details.setReadOnly(True)
        right_layout.addWidget(self.product_details)
        self.product_details.setStyleSheet("""
            QTextEdit {
                background-color: #f0f0f0;
                background-color: #f7f7f7;
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 5px;
            }
        """)

        # Add product button
        self.add_button = QPushButton("Ajouter un produit")
        self.add_button.setStyleSheet("""
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
        self.add_button.clicked.connect(self.open_add_dialog)
        right_layout.addWidget(self.add_button)

        # Transfer product button
        self.transfer_button = QPushButton("Transférer un produit")
        self.transfer_button.setStyleSheet("""
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
        self.transfer_button.clicked.connect(self.open_transfer_dialog)
        right_layout.addWidget(self.transfer_button)

        # Order low stock products button
        self.order_button = QPushButton("Commander des produits")
        self.order_button.setStyleSheet("""
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
        self.order_button.clicked.connect(self.open_order_dialog)
        right_layout.addWidget(self.order_button)

        main_layout.addLayout(right_layout)

        return main_layout

    def update_product_list(self):
        """Fetch and display the product list."""
        products = fetch.fetch_products()
        self.product_list.clear()

        for product in products:
            item = QListWidgetItem(f"{product['name']} - Stock: {product['stock']}")
            item.setData(Qt.UserRole, product['id'])
            self.product_list.addItem(item)

    def on_product_clicked(self, item):
        """Display details of the selected product."""
        product_id = item.data(Qt.UserRole)
        product_details = fetch.fetch_product_details(product_id)

        if product_details:
            details = (
                f"Nom: {product_details['name']}\n"
                f"Description: {product_details['description']}\n"
                f"Catégorie: {product_details['category']}\n"
                f"Prix unitaire: {product_details['price']} €\n"
                f"Stock disponible: {product_details['stock']}\n"
                # f"Emplacement: {product_details['location']}\n"
            )
            self.product_details.setText(details)
            self.selected_product = product_details

    def open_add_dialog(self):
        """Open the dialog to add a new product."""
        dialog = AddProductDialog(self.parent_widget if isinstance(self.parent_widget, QWidget) else None)
        if dialog.exec():
            self.update_product_list()

    def open_transfer_dialog(self):
        """Open the dialog to transfer a product."""
        if self.selected_product:
            dialog = TransferProductDialog(self.selected_product, self.parent_widget if isinstance(self.parent_widget, QWidget) else None)
            if dialog.exec():
                self.update_product_list()

    def open_order_dialog(self):
        """Open the dialog to order low stock products."""
        dialog = OrderProductDialog(self.parent_widget if isinstance(self.parent_widget, QWidget) else None)
        if dialog.exec():
            self.update_product_list()


class AddProductDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Ajouter un produit")
        layout = QFormLayout(self)

        self.name_input = QLineEdit()
        layout.addRow("Nom:", self.name_input)

        self.description_input = QLineEdit()
        layout.addRow("Description:", self.description_input)

        self.category_input = QLineEdit()
        layout.addRow("Catégorie:", self.category_input)

        self.price_input = QDoubleSpinBox()
        self.price_input.setPrefix("€ ")
        layout.addRow("Prix unitaire:", self.price_input)

        self.stock_input = QSpinBox()
        layout.addRow("Stock initial:", self.stock_input)

        self.location_group = QButtonGroup(self)
        self.department_radio = QRadioButton("Département")
        self.warehouse_radio = QRadioButton("Entrepôt")
        self.branch_radio = QRadioButton("Succursale")
        
        self.location_group.addButton(self.department_radio)
        self.location_group.addButton(self.warehouse_radio)
        self.location_group.addButton(self.branch_radio)
        self.department_radio.setChecked(True)
        
        location_type_layout = QHBoxLayout()
        location_type_layout.addWidget(self.department_radio)
        location_type_layout.addWidget(self.warehouse_radio)
        location_type_layout.addWidget(self.branch_radio)
        layout.addRow("Type d'emplacement:", location_type_layout)
        
        self.location_combo = QComboBox()
        layout.addRow("Emplacement:", self.location_combo)
        
        self.department_radio.toggled.connect(self.update_location_options)
        self.warehouse_radio.toggled.connect(self.update_location_options)
        self.branch_radio.toggled.connect(self.update_location_options)
        
        self.update_location_options()

        save_button = QPushButton("Ajouter")
        save_button.clicked.connect(self.add_product)
        layout.addWidget(save_button)

        self.setLayout(layout)
        
    def update_location_options(self):
        """Met à jour les options dans le ComboBox en fonction du type d'emplacement sélectionné."""
        self.location_combo.clear()

        if self.department_radio.isChecked():
            locations = fetch.fetch_succursale()
            locations = [{'id': succursale[0], 'nom': succursale[2]} for succursale in locations]
        elif self.warehouse_radio.isChecked():
            locations = fetch.fetch_entrepot()
            locations = [{'id': entrepot[0], 'nom': entrepot[2]} for entrepot in locations]
        elif self.branch_radio.isChecked():
            locations = fetch.fetch_succursale()
            locations = [{'id': succursale[0], 'nom': succursale[2]} for succursale in locations]
        else:
            locations = []
        
        for location in locations:
            self.location_combo.addItem(location['nom'], location['id'])


    def add_product(self):
        name = self.name_input.text()
        description = self.description_input.text()
        category = self.category_input.text()
        price = self.price_input.value()
        stock = self.stock_input.value()
        location_id = self.location_combo.currentData()
        
        inventory_type = None
        if self.department_radio.isChecked():
            inventory_type = "Department"
        elif self.warehouse_radio.isChecked():
            inventory_type = "Entrepot"
        elif self.branch_radio.isChecked():
            inventory_type = "Succursale"

        if not name or not category or location_id is None:
            QMessageBox.warning(self, "Erreur", "Tous les champs obligatoires doivent être remplis.")
            return

        fetch.add_product(
            name=name,
            description=description,
            category=category,
            price=price,
            stock=stock,
            inventory_id=location_id,  # The selected location ID
            supplier_id=None,          # Optional, can be updated later
            department_id=location_id if inventory_type == "Department" else None,
            private_label=False
        )

        QMessageBox.information(self, "Succès", "Produit ajouté avec succès.")
        self.accept()


class TransferProductDialog(QDialog):
    def __init__(self, product, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Transférer un produit")
        self.product = product

        layout = QFormLayout(self)

        self.source_inventory = QComboBox()
        self.source_inventory.addItems(fetch.fetch_inventories())
        layout.addRow("Inventaire source:", self.source_inventory)

        self.target_inventory = QComboBox()
        self.target_inventory.addItems(fetch.fetch_inventories())
        layout.addRow("Inventaire cible:", self.target_inventory)

        self.quantity_input = QSpinBox()
        self.quantity_input.setMaximum(self.product['stock'])
        layout.addRow("Quantité à transférer:", self.quantity_input)

        transfer_button = QPushButton("Transférer")
        transfer_button.clicked.connect(self.transfer_product)
        layout.addWidget(transfer_button)

        self.setLayout(layout)

    def transfer_product(self):
        source = self.source_inventory.currentText()
        target = self.target_inventory.currentText()
        quantity = self.quantity_input.value()

        if source == target:
            QMessageBox.warning(self.parentWidget(), "Erreur", "Les inventaires source et cible doivent être différents.")
            return

        if quantity <= 0 or quantity > self.product['stock']:
            QMessageBox.warning(self.parentWidget(), "Erreur", "Quantité invalide.")
            return

        fetch.transfer_product(self.product['id'], source, target, quantity)
        QMessageBox.information(self.parentWidget(), "Succès", "Produit transféré avec succès.")
        self.accept()


class OrderProductDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Commander des produits")
        layout = QVBoxLayout(self)

        self.low_stock_list = QListWidget()
        low_stock_products = fetch.fetch_low_stock_products()

        for product in low_stock_products:
            item = QListWidgetItem(f"{product['name']} - Stock: {product['stock']}")
            item.setData(Qt.UserRole, product['id'])
            self.low_stock_list.addItem(item)

        layout.addWidget(self.low_stock_list)

        order_button = QPushButton("Commander")
        order_button.clicked.connect(self.order_products)
        layout.addWidget(order_button)

        self.setLayout(layout)

    def order_products(self):
        selected_items = self.low_stock_list.selectedItems()
        product_ids = [item.data(Qt.UserRole) for item in selected_items]

        if not product_ids:
            QMessageBox.warning(self.parentWidget(), "Erreur", "Aucun produit sélectionné.")
            return

        fetch.order_products(product_ids)
        QMessageBox.information(self.parentWidget(), "Succès", "Commande effectuée avec succès.")
        self.accept()
