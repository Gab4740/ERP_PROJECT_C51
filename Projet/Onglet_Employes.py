from PySide6.QtWidgets import QMessageBox, QVBoxLayout, QHBoxLayout, QComboBox, QListWidget, QTextEdit, QLabel, QLineEdit, QPushButton, QDialog, QFormLayout, QListWidgetItem, QSpinBox, QDoubleSpinBox, QDateEdit, QWidget
from PySide6.QtCore import QDate
from Onglet import Onglet
import sqlite3
import fetch

class Onglet_Employes(Onglet):
    def __init__(self, name, visibility):
        super().__init__(name, visibility)
        
        self.selected_employee = None

    def create_content(self):
        self.shops = fetch.fetch_succursale()    
        
        # Initialize the UI
        self.widget.setLayout(self.init_ui())

    def init_ui(self):
        # Main layout - Horizontal layout to split the window
        main_layout = QHBoxLayout()

        # Left side: List of employees
        left_layout = QVBoxLayout()
        
        # Shop dropdown
        self.shop_combo = QComboBox()
        for s in self.shops:
            self.shop_combo.addItem(s[2])
        self.shop_combo.currentTextChanged.connect(self.on_shop_changed)
        left_layout.addWidget(self.shop_combo)
        
        self.refresh_button = QPushButton("refresh")
        self.refresh_button.clicked.connect(self.refresh_page)
        left_layout.addWidget(self.refresh_button)

        # List widget for employees
        self.employee_list = QListWidget()
        self.employee_list.itemClicked.connect(self.on_employee_clicked)
        left_layout.addWidget(self.employee_list)
        self.employee_list.setStyleSheet("""
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
        self.search_bar.textChanged.connect(self.filter_items)
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
        self.details_label = QLabel('Détails de l''employé:')
        self.details_label.setStyleSheet("font-weight: bold; font-size: 18px;")
        right_layout.addWidget(self.details_label)

        # Text edit to show selected employee details
        self.employee_details = QTextEdit()
        self.employee_details.setReadOnly(True)
        right_layout.addWidget(self.employee_details)
        self.employee_details.setStyleSheet("""
            QTextEdit {
                background-color: #f0f0f0;
                background-color: #f7f7f7;
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 5px;
            }
        """)
        
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
        
        self.supprimer_emp = QPushButton("Supprimer l'employe")
        self.supprimer_emp.setStyleSheet("""
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
        self.supprimer_emp.clicked.connect(self.supprimer_employer)
        right_layout.addWidget(self.supprimer_emp)

        main_layout.addLayout(right_layout)

        # Set the initial shop and employee list
        if self.shops:
            self.current_shop = self.shops[0][2]
            self.on_shop_changed(self.shops[0][2])
        
        return main_layout

    
    def supprimer_employer(self):
        if self.selected_employee:
            reply = QMessageBox.question(self.widget, 'Confirmation', 
                                     "Are you sure you want to delete this employee?", 
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, 
                                     QMessageBox.StandardButton.No)

        if reply == QMessageBox.Yes:
            fetch.delete_employee(self.selected_employee[0])

    def refresh_page(self):
        self.shop_combo.clear()
        
        shops = fetch.fetch_succursale()    
        for s in shops:
            self.shop_combo.addItem(s[2])
        
        current_shop = shops[0][2]
        self.update_employee_list(current_shop)
        
        self.selected_employee = None
    
    def on_shop_changed(self, shop_name):
        """Update the employee list when a new shop is selected."""
        self.current_shop = shop_name
        self.update_employee_list(shop_name)

    def update_employee_list(self, shop_name):
        shop_id = fetch.get_shop_id_by_name(shop_name)
        employees = fetch.get_employees_by_shop_id(shop_id)

        self.employee_list.clear()
        # Add employee names to the list widget
        for emp in employees:
            emp_info = fetch.get_employee_info_by_id(emp[0])
            item = QListWidgetItem(str(emp_info[2] + " " +  emp_info[3]))
            item.setData(1, emp[0])
            self.employee_list.addItem(item)
            
    def on_employee_clicked(self, item):
        """Display the selected employee's details in the right section."""
        emp_infos = fetch.get_employee_info_by_id(item.data(1))
        if emp_infos is not None:
            details = (
                f"Prenom: {emp_infos[2]}\n"
                f"Nom: {emp_infos[3]}\n"
                f"Date naissance: {emp_infos[4]}\n"
                f"Email: {emp_infos[5]}\n"
                f"Telephone: {emp_infos[6]}\n"
                f"Adresse: {emp_infos[7]}\n"
            )
            
            ###### AJOUTER CUSTOM FIELDS ##########################
            custom_fields = fetch.fetch_custom_field_values("Employee", emp_infos[0])
            for field_name, value in custom_fields:
                details += f"{field_name}: {value}\n"
            ##############################################################################
            
            self.employee_details.setText(details)
            self.selected_employee = emp_infos
            
    def filter_items(self):
        filter_text = self.search_bar.text().lower()

        for index in range(self.employee_list.count()):
            item = self.employee_list.item(index)
            item_text = item.text().lower()

            if filter_text in item_text:
                item.setHidden(False)
            else:
                item.setHidden(True) 
    
    def open_modify_dialog(self):
        """Open the modify dialog to edit the selected employee's details."""
        if self.selected_employee:
            dialog = ModifyEmployeeDialog(self.selected_employee)
            dialog.exec()

            self.refresh_page()

class ModifyEmployeeDialog(QDialog):
    def __init__(self, employee_data, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Modifier l'employée")
        self.setGeometry(150, 150, 400, 300)

        self.employee_data = employee_data
        self.employee_ID = employee_data[0]
        self.dynamic_fields = {}

        # Create form layout for the dialog
        layout = QFormLayout(self)
        
        self.nas_edit = QLineEdit(self)
        self.nas_edit.setText(self.employee_data[1])
        layout.addRow("NAS:", self.nas_edit)

        self.prenom_edit = QLineEdit(self)
        self.prenom_edit.setText(self.employee_data[2])
        layout.addRow("Prenom:", self.prenom_edit)
        
        self.nom_edit = QLineEdit(self)
        self.nom_edit.setText(self.employee_data[3])
        layout.addRow("Nom:", self.nom_edit)

        self.telephone_edit = QLineEdit(self)
        self.telephone_edit.setText(self.employee_data[6])
        layout.addRow("Telephone:", self.telephone_edit)

        self.adresse_edit = QLineEdit(self)
        self.adresse_edit.setText(self.employee_data[7])
        layout.addRow("Adresse:", self.adresse_edit)
        
        
        
        ###### AJOUTER CUSTOM FIELDS ##########################
        dynamic_fields = fetch.fetch_custom_fields("Employee")
        dynamic_values = fetch.fetch_custom_field_values("Employee", self.employee_ID, as_dict=True)
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
                date_value = dynamic_values.get(field_id)
                if date_value:
                    widget.setDate(QDate.fromString(date_value, "yyyy-MM-dd"))
            else:
                continue  
            
            self.dynamic_fields[field_id] = widget
            layout.addRow(field_name, widget)
        ##############################################################################

        # Save button
        save_button = QPushButton("Save", self)
        save_button.clicked.connect(self.save_changes)
        layout.addRow(save_button)

    def save_changes(self):
        fetch.update_employee_info(
            self.employee_ID,
            self.nas_edit.text(),  
            self.prenom_edit.text(), 
            self.nom_edit.text(), 
            self.telephone_edit.text(), 
            self.adresse_edit.text()
        )
        
        ###### AJOUTER CUSTOM FIELDS ##########################
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
        ##############################################################################
        
        #fetch.update_employee_info(self.employee_ID, self.prenom_edit.text(), self.nom_edit.text(), self.telephone_edit.text(), self.adresse_edit.text())
        fetch.update_custom_field_values("Employee", self.employee_ID, custom_field_values)
        self.accept()