from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QComboBox, QListWidget, QTextEdit, QLabel, QLineEdit, QListWidgetItem, QPushButton, QDialog, QFormLayout
from Onglet import Onglet
import sqlite3
import fetch

class Onglet_Employes(Onglet):
    def __init__(self, name, visibility):
        super().__init__(name, visibility)

    def create_content(self):
        self.shops = fetch.fetch_succursale()    
        print(self.shops)

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
        self.search_bar.textChanged.connect(self.filter_employees)
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

        main_layout.addLayout(right_layout)

        # Set the initial shop and employee list
        if self.shops:
            self.on_shop_changed(self.shops[0][2])
        
        return main_layout

    def on_shop_changed(self, shop_name):
        """Update the employee list when a new shop is selected."""
        self.current_shop = shop_name
        self.update_employee_list(shop_name)

    def update_employee_list(self, shop_name):
        print(shop_name)
        employee = fetch.get_employees_by_succursale(shop_name)
        print(employee, " lololol ")

        # Clear the current list
        self.employee_list.clear()

        # Add employee names to the list widget
        #for emp in employee:
        #    self.employee_list.addItem(employee['name'])

    def on_employee_clicked(self, item):
        """Display the selected employee's details in the right section."""
        employee_name = item.text()

        # Find the employee based on the selected name
        employees = self.employees.get(self.current_shop, [])
        for employee in employees:
            if employee['name'] == employee_name:
                self.selected_employee = employee
                self.display_employee_details()
                break

    def display_employee_details(self):
        """Display the detailed information of the selected employee."""
        if self.selected_employee:
            details = (
                f"Name: {self.selected_employee['name']}\n"
                f"Position: {self.selected_employee['position']}\n"
                f"Email: {self.selected_employee['email']}\n"
                f"Phone: {self.selected_employee['phone']}\n"
            )
            self.employee_details.setText(details)
            
    def filter_employees(self, text):
        """Filter the employees list based on the search input."""
        filter_text = text.lower()
        employees = self.employees.get(self.current_shop, [])
        filtered_employees = [emp for emp in employees if filter_text in emp['name'].lower()]

        # Clear existing rows and repopulate with filtered data
        self.employee_list.clear()
        for employee in filtered_employees:
            self.employee_list.addItem(employee['name'])
    
    def open_modify_dialog(self):
        """Open the modify dialog to edit the selected employee's details."""
        if self.selected_employee:
            dialog = ModifyEmployeeDialog(self.selected_employee)
            dialog.exec()

            # After closing the dialog, update the employee list with any changes
            self.update_employee_list()
    
    
    
    ## A DEPLACER DANS LE DOCUEMNT fetch.py      
    def ajouter_nouveau_employe(self, nas, nom ,prenom, date_naissance, email, telephone, adresse, id_succursale, id_poste):
        conn = sqlite3.connect('erp.db')
        cursor = conn.cursor()
        try:
            # Ajouter les informations de l'entité (INFO_CIE)
            cursor.execute("""
                INSERT INTO info.INFO_PERSONNEL (nas, nom, prenom, date_naissance, email, telephone, adresse)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (nas, nom, prenom, date_naissance, email, telephone, adresse))
            
            # Récupérer l'ID de l'entité insérée
            id_entite = cursor.lastrowid
            
            # Ajouter la succursale associée
            cursor.execute("""
                INSERT INTO rh.EMPLOYE (id_employe)
                VALUES (?)
            """, (id_entite,))
            
            cursor.execute("""
                INSERT INTO rh.EMPLOYE (id_succursale)
                VALUES (?)
            """, (id_succursale,))
            
            cursor.execute("""
                INSERT INTO rh.EMPLOYE (id_poste)
                VALUES (?)
            """, (id_poste,))
            
            conn.commit()
            print(f"Succursale '{nom}' ajoutée avec succès.")
        except sqlite3.Error as e:
            print(f"Erreur SQL : {e}")
            raise e
        finally:
            conn.close()



class ModifyEmployeeDialog(QDialog):
    def __init__(self, employee_data, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Modify Employee")
        self.setGeometry(150, 150, 400, 300)

        self.employee_data = employee_data

        # Create form layout for the dialog
        layout = QFormLayout(self)

        self.name_edit = QLineEdit(self)
        self.name_edit.setText(self.employee_data['name'])
        layout.addRow("Name:", self.name_edit)

        self.position_edit = QLineEdit(self)
        self.position_edit.setText(self.employee_data['position'])
        layout.addRow("Position:", self.position_edit)

        self.email_edit = QLineEdit(self)
        self.email_edit.setText(self.employee_data['email'])
        layout.addRow("Email:", self.email_edit)

        self.phone_edit = QLineEdit(self)
        self.phone_edit.setText(self.employee_data['phone'])
        layout.addRow("Phone:", self.phone_edit)

        # Save button
        save_button = QPushButton("Save", self)
        save_button.clicked.connect(self.save_changes)
        layout.addRow(save_button)

    def save_changes(self):
        """Save the changes to the employee data."""
        self.employee_data['name'] = self.name_edit.text()
        self.employee_data['position'] = self.position_edit.text()
        self.employee_data['email'] = self.email_edit.text()
        self.employee_data['phone'] = self.phone_edit.text()

        self.accept()  # Close the dialog


