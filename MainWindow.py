import sys
from datetime import datetime
import math as m
import locale

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout,
    QPushButton, QLabel, QHBoxLayout, QMessageBox, QLineEdit, QDialog, QComboBox
)
from PyQt6.QtCore import QTimer, Qt

class Onglet:
    def __init__(self, name, role):
        self.name = name
        self.role = role
        self.last_login = datetime.now()
        
    def get_role(self):
        return self.role
    
    def get_name(self):
        return self.role

class MainWindow(QMainWindow):
    def __init__(self, width, height):
        super().__init__()
        
        # PARAMETRE DE BASE
        self.percent = 0.85                                                         #Pourcentage de l'ecran pris par l'app au lancement
        self.setWindowTitle("Logiciel ERP")                                         #Titre de la topBar
        self.resize(m.floor(width * self.percent), m.floor(height * self.percent))  #Rezize de la fenetre
        self.current_user_role = None                                               #Current Visibility
        
        # ONGLETS EXISTANT
        self.onglets_existants = [  #EXEMPLES.....
            Onglet("General", "any"),
            Onglet("admin", "Admin"),
            Onglet("boss", "Boss"),
            Onglet("employe", "Employé"),
        ]
        # GESTION ONGLETS ACTIFS
        self.tab_widget = QTabWidget()
        self.tab_widget.currentChanged.connect(self.update_last_index)
        self.last_index = 0
        self.create_tabs()

        # BOUTTONS DU CONTROL BAR
        self.quit_button = QPushButton("Quitter")
        self.quit_button.clicked.connect(self.close)

        self.back_button = QPushButton("Retour")
        self.back_button.clicked.connect(self.go_back)

        self.sign_out_button = QPushButton("Déconnexion")
        self.sign_out_button.clicked.connect(self.sign_out)

        self.connect_button = QPushButton("Connexion")
        self.connect_button.clicked.connect(self.show_login_dialog)
        
        self.setting_button = QPushButton("Settings")
        #self.setting_button.clicked.connect(...)

        # CONTROL BAR
        # SETTING && BACK
        back_setting_sect = QVBoxLayout()
        vbox_container1 = QWidget()
        vbox_container1.setLayout(back_setting_sect)
        back_setting_sect.addWidget(self.back_button)
        back_setting_sect.addWidget(self.setting_button)
        
        # CONNECT && DISCONNECT && QUIT
        conn_discon_quit = QVBoxLayout()
        vbox_container2 = QWidget()
        vbox_container2.setLayout(conn_discon_quit)
        conn_discon_quit.addWidget(self.connect_button)
        conn_discon_quit.addWidget(self.sign_out_button)
        conn_discon_quit.addWidget(self.quit_button)

        # USER INFO    
        self.user_info_label = QLabel()
        self.user_info_label.setStyleSheet("font-size: 24px; color: black; font-weight: bold;")
        self.user_info_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.user_visibility = QLabel()
        self.user_visibility.setStyleSheet("font-size: 24px; color: black; font-weight: bold;")
        self.user_info_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.update_user_info("Invité", None)
        
        user_info = QVBoxLayout()
        vbox_container3 = QWidget()
        vbox_container3.setLayout(user_info)
        user_info.addWidget(self.user_info_label)
        user_info.addWidget(self.user_visibility)
        
        # TIME INFO
        self.time_label = QLabel()
        self.time_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.time_label.setStyleSheet("font-size: 24px; color: black; font-weight: bold;")
        self.date_label = QLabel()
        self.date_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.date_label.setStyleSheet("font-size: 24px; color: black; font-weight: bold;")
        self.update_time()
        
        time_info = QVBoxLayout()
        vbox_container4 = QWidget()
        vbox_container4.setLayout(time_info)
        time_info.addWidget(self.time_label)
        time_info.addWidget(self.date_label)
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)
        
        # MAIN WINDOW
        control_bar = QHBoxLayout()
        control_bar.addWidget(vbox_container3)
        control_bar.addWidget(vbox_container4)
        control_bar.addWidget(vbox_container1)
        control_bar.addWidget(vbox_container2)
        
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.tab_widget)
        main_layout.addLayout(control_bar)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)
        
        self.update_button_visibility()

    def create_tabs(self):
        for onglet in self.onglets_existants:
            if self.user_role_can_access(onglet.get_role()) or onglet.get_role() == "any":
                self.add_tab(onglet.name, onglet.get_role())

    def add_tab(self, name, user_role):
        tab = QWidget()
        layout = QVBoxLayout()

        layout.addWidget(QLabel(f"Onglet créé par : {user_role}"))
        layout.addWidget(QLabel(f"Heure de dernière connexion : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"))
        tab.setLayout(layout)

        self.tab_widget.addTab(tab, name)
        self.tab_widget.setTabText(self.tab_widget.indexOf(tab), name)

    # A MODIFIER
    def user_role_can_access(self, role):
        if self.current_user_role == "Boss":
            return True
        elif self.current_user_role == "Admin":
            return role in ["Admin", "Employé"]
        elif self.current_user_role == "Employé":
            return role == "Employé"
        return False

    # ON PEUX LE GARDER
    def update_last_index(self, index):
        self.last_index = index

    def go_back(self):
        if self.last_index > 0:
            self.tab_widget.setCurrentIndex(self.last_index - 1)

    def update_time(self):
        locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')
        
        current_time = datetime.now().strftime("%H:%M:%S")
        self.time_label.setText(f"Heure actuelle : {current_time}")
        
        date = datetime.now()
        day_of_month = date.day
        day_of_week = date.strftime("%A").capitalize()
        year = date.year
        
        self.date_label.setText(f"Date : {day_of_week} {day_of_month} {year}")

    def update_user_info(self, name, role):
        self.current_user_role = role
        self.user_info_label.setText(f"Utilisateur : {name}" if role else "Utilisateur : Invité")
        self.user_visibility.setText(f"Visibilité : {role}" if role else "Visibilité : Invité")
        self.tab_widget.clear()  # Vider les onglets existants
        self.create_tabs()  # Recréer les onglets en fonction du rôle
        self.update_button_visibility()

    def update_button_visibility(self):
        if self.current_user_role is None:
            self.sign_out_button.setVisible(False)
            self.connect_button.setVisible(True)
        else:
            self.sign_out_button.setVisible(True)
            self.connect_button.setVisible(False)

    def sign_out(self):
        QMessageBox.information(self, "Déconnexion", "Vous êtes déconnecté.")
        self.update_user_info("Invité", None)

    # A MODIFIER
    def show_login_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Connexion")

        layout = QVBoxLayout()
        username_label = QLabel("Identifiant:")
        self.username_input = QLineEdit()
        password_label = QLabel("Mot de passe:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        login_button = QPushButton("Se connecter")
        login_button.clicked.connect(lambda: self.login(dialog))

        layout.addWidget(username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(login_button)

        dialog.setLayout(layout)
        dialog.exec()

    # A MODIFIER
    def login(self, dialog):
        username = self.username_input.text()
        password = self.password_input.text()

        if username == "admin" and password == "admin":
            self.update_user_info(username, "Admin")
            dialog.accept()
        elif username == "boss" and password == "boss":
            self.update_user_info(username, "Boss")
            dialog.accept()
        elif username == "employe" and password == "employe":
            self.update_user_info(username, "Employé")
            dialog.accept()
        else:
            QMessageBox.warning(self, "Erreur de connexion", "Identifiant ou mot de passe incorrect.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # STYLE SHEET
    app.setStyleSheet("QPushButton{padding: 5px; font-size: 24px}")
    screen_info = app.primaryScreen().geometry()
    window = MainWindow(screen_info.width(), screen_info.height())
    
    window.show()
    sys.exit(app.exec())