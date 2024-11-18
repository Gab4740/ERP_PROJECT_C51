from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QComboBox, QLineEdit, QDateEdit, QDialog, QMessageBox, QWidget
from Onglet import Onglet
import fetch

class Onglet_usagers(Onglet):
    def __init__(self, name, visibility, parent_widget=None):
        super().__init__(name, visibility)
        self.parent_widget = parent_widget

    def create_content(self):
        # Layout principal
        layout = QVBoxLayout()

        # Full Name
        self.name_input = QLineEdit(self.widget)
        self.name_input.setPlaceholderText("Nom complet")
        layout.addWidget(QLabel("Nom complet:"))
        layout.addWidget(self.name_input)

        # Job Title
        self.job_title_input = QLineEdit(self.widget)
        self.job_title_input.setPlaceholderText("Poste")
        layout.addWidget(QLabel("Poste:"))
        layout.addWidget(self.job_title_input)

        # Email
        self.email_input = QLineEdit(self.widget)
        self.email_input.setPlaceholderText("Email")
        layout.addWidget(QLabel("Email:"))
        layout.addWidget(self.email_input)

        # Phone Number
        self.phone_input = QLineEdit(self.widget)
        self.phone_input.setPlaceholderText("Numéro de téléphone")
        layout.addWidget(QLabel("Numéro de téléphone:"))
        layout.addWidget(self.phone_input)

        # Start Date
        self.start_date_input = QDateEdit(self.widget)
        self.start_date_input.setCalendarPopup(True)
        layout.addWidget(QLabel("Date d'embauche:"))
        layout.addWidget(self.start_date_input)

        # Salary (Optional)
        self.salary_input = QLineEdit(self.widget)
        self.salary_input.setPlaceholderText("Salaire")
        layout.addWidget(QLabel("Salaire:"))
        layout.addWidget(self.salary_input)

        # Buttons to register or reset
        buttons_layout = QHBoxLayout()
        self.save_button = QPushButton("Enregistrer")
        self.reset_button = QPushButton("Réinitialiser")
        
        self.save_button.clicked.connect(self.on_save_clicked)
        self.reset_button.clicked.connect(self.on_reset_clicked)

        buttons_layout.addWidget(self.save_button)
        buttons_layout.addWidget(self.reset_button)

        layout.addLayout(buttons_layout)

        # Set the layout to the widget
        self.widget.setLayout(layout)

    def on_save_clicked(self):
        # Gather form data
        name = self.name_input.text().strip()
        job_title = self.job_title_input.text().strip()
        email = self.email_input.text().strip()
        phone = self.phone_input.text().strip()
        start_date = self.start_date_input.date().toString("yyyy-MM-dd")
        salary = self.salary_input.text().strip()

        if not name or not email or not phone:
            QMessageBox.warning(self.widget, "Erreur", "Nom, email et téléphone sont obligatoires.")
            return

        # Call the function to save the employee in the database
        fetch.add_employee(
            name=name,
            job_title=job_title,
            email=email,
            phone=phone,
            start_date=start_date,
            salary=salary
        )

        # Show success message
        QMessageBox.information(self.widget, "Succès", "L'employé a été enregistré avec succès.")
        self.reset_form()

    def on_reset_clicked(self):
        self.reset_form()

    def reset_form(self):
        # Reset the form fields
        self.name_input.clear()
        self.job_title_input.clear()
        self.email_input.clear()
        self.phone_input.clear()
        self.salary_input.clear()
        self.start_date_input.setDate(self.start_date_input.minimumDate())

