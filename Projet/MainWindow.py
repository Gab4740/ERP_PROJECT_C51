from datetime import datetime
import math as m
import locale
import Onglet_Horaire as horaire
import Onglet_Horaire_EMP as horaireEmp
import Onglet_Entrepot as entrepot
import Onglet_Magasin as magasin
import Onglet_Employes as employes
import Onglet_Client as clients
import Onglet_Usagers as usagers
import Onglet_Commande as commande
import Onglet_Fournisseurs as fournisseurs
import Onglet_config as config
import fetch

from PySide6.QtWidgets import QMainWindow, QTabWidget, QWidget, QVBoxLayout, QPushButton, QLabel, QHBoxLayout, QMessageBox, QLineEdit, QDialog
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QPixmap

class MainWindow(QMainWindow):
    def __init__(self, width, height, connexion):
        super().__init__()
        self.parent_connexion = connexion
        
        # PARAMETRE DE BASE
        self.percent = 0.85                                                         #Pourcentage de l'ecran pris par l'app au lancement
        self.setWindowTitle("Logiciel ERP")                                         #Titre de la topBar
        self.resize(m.floor(width * self.percent), m.floor(height * self.percent))  #Rezize de la fenetre
        self.current_user_role = 0                                                  #Current Visibility
        
        # ONGLETS EXISTANT
        self.onglets_existants = [
            horaire.Onglet_horaire("Modification Horaire", 3),
            horaireEmp.Onglet_horaire("Horaire", 0),
            magasin.Onglet_magasin("Magasins", 0, parent_widget=self),
            entrepot.Onglet_entrepot("Entrepôts", 3, parent_widget=self),
            clients.Onglet_Client("Clients", 3, parent_widget=self),
            commande.Onglet_Commande("Commandes", 4, parent_widget=self),
            employes.Onglet_Employes("Employés", 0),
            usagers.Onglet_usagers("Usagers", 0),
            fournisseurs.Onglet_Fournisseurs("Fournisseurs", 4),
            config.Onglet_Config("Configurations", 5, parent_widget=self)
        ]
        
        # VISIBILITÉ DICTIONNAIRE
        self.visi = {
            0 : "Invité",
            1 : "Employé",
            2 : "Superviseur",
            3 : "Gérant",
            4 : "Modérateur",
            5 : "Administrateur"
        }
        
        # GESTION ONGLETS ACTIFS
        self.tab_widget = QTabWidget()
        self.tab_widget.currentChanged.connect(self.update_last_index)
        self.last_index = 0
        self.create_tabs()

        self.add_logo_and_name()

        # BOUTTONS DU CONTROL BAR
        self.quit_button = QPushButton("Quitter")
        self.quit_button.setStyleSheet("QPushButton{padding: 2px; font-size: 24px}")
        self.quit_button.clicked.connect(self.close)

        self.back_button = QPushButton("Retour")
        self.back_button.setStyleSheet("QPushButton{padding: 2px; font-size: 24px}")
        self.back_button.clicked.connect(self.go_back)

        self.sign_out_button = QPushButton("Déconnexion")
        self.sign_out_button.setStyleSheet("QPushButton{padding: 2px; font-size: 24px}")
        self.sign_out_button.clicked.connect(self.sign_out)
        
        self.setting_button = QPushButton("Settings")
        self.setting_button.setStyleSheet("QPushButton{padding: 2px; font-size: 24px}")
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
        conn_discon_quit.addWidget(self.sign_out_button)
        conn_discon_quit.addWidget(self.quit_button)

        # USER INFO    
        self.user_info_label = QLabel()
        self.user_info_label.setStyleSheet("font-size: 24px; color: black; font-weight: bold;")
        self.user_info_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.user_visibility = QLabel()
        self.user_visibility.setStyleSheet("font-size: 24px; color: black; font-weight: bold;")
        self.user_info_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        
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

    def add_logo_and_name(self):
        top_right_widget = QWidget(self)
        top_right_layout = QVBoxLayout(top_right_widget)

        self.logo_label = QLabel(self)
        self.logo_pixmap = QPixmap('./logo.png') # file png
        self.logo_label.setPixmap(self.logo_pixmap.scaled(80, 80, Qt.AspectRatioMode.KeepAspectRatio))  # Resize the logo
        self.logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.enterprise_name_label = QLabel("ERP Development", self)  # enterprise name
        self.enterprise_name_label.setStyleSheet("font-size: 18px; color: black; font-weight: bold;")
        self.enterprise_name_label.setAlignment(Qt.AlignmentFlag.AlignRight)

        top_right_layout.addWidget(self.logo_label)
        top_right_layout.addWidget(self.enterprise_name_label)
        
        top_right_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        top_right_widget.setLayout(top_right_layout)

        self.layout().setMenuBar(top_right_widget)

    def create_tabs(self):
        for onglet in self.onglets_existants:
            if onglet.get_visibility() <= self.current_user_role or onglet.get_visibility() == 0:
                self.add_tab(onglet.name, onglet.get_widget())

    def add_tab(self, name, ongle_widget):
        self.tab_widget.addTab(ongle_widget, name)
        self.tab_widget.setTabText(self.tab_widget.indexOf(ongle_widget), name)

    # ON PEUX LE GARDER
    def update_last_index(self, index):
        self.last_index = index

    def go_back(self):
        if self.last_index > 0:
            self.tab_widget.setCurrentIndex(self.last_index - 1)

    def update_time(self):
        locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')
        
        current_time = datetime.now().strftime("%H:%M:%S")
        date = datetime.now()
        day_of_month = date.day
        day_of_week = date.strftime("%A").capitalize()
        
        year = date.year
        self.time_label.setText(f"Heure : {current_time}")
        self.date_label.setText(f"Date : {day_of_week} {day_of_month} {year}")

    def update_user_info(self, username, password, role = None):
        role = fetch.fetch_visibilite(username, password)
        self.current_user_role = role
        self.user_info_label.setText(f"Utilisateur : {username}" if role is not None else "Utilisateur : Invité")
        self.user_visibility.setText(f"Visibilité : {self.visi[role]}" if role is not None else "Visibilité : Invité")
        self.tab_widget.clear()  # Vider les onglets existants
        self.create_tabs()  # Recréer les onglets en fonction du rôle

    def sign_out(self):
        QMessageBox.information(self, "Déconnexion", "Vous êtes déconnecté.")
        self.parent_connexion.show()
        self.parent_connexion
        self.close()

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

        login_button = QPushButton("Se Deconnecter")
        login_button.clicked.connect(lambda: self.login(dialog))

        layout.addWidget(username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(login_button)

        dialog.setLayout(layout)
        dialog.exec()
