from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QGridLayout, QStackedWidget)
from PySide6.QtCore import Qt
import sys
import requests
import MainWindow
import client
import multiprocessing  
import server
import init_db

def lancer_serveur():
    server.app.run(debug=True, use_reloader=False)  


class Connexion(QMainWindow):
    def __init__(self, controleur, screen_info):
        super().__init__()
        self.controleur = controleur
        self.setWindowTitle("Application ERP")
        self.setGeometry(100, 100, 500, 300)
        
        # Mettre le widget centré dans l'écran
        screen_center_x = (screen_info.width() - self.width()) // 2
        screen_center_y = (screen_info.height() - self.height()) // 2 - 100
        self.move(screen_center_x, screen_center_y)

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.frame_connexion = self.creer_frame_connexion()
        self.frame_main_window = MainWindow.MainWindow(screen_info.width(), screen_info.height(), self)

        self.stacked_widget.addWidget(self.frame_connexion)

        # Affichage initial
        self.basculer_vers_connexion()

    def creer_frame_connexion(self):
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(50, 20, 50, 40)

        titre = QLabel("Connexion ERP")
        titre.setAlignment(Qt.AlignCenter)
        titre.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(titre)

        form_layout = QGridLayout()
        form_layout.setContentsMargins(50, 0, 50, 30)
        
        self.entry_username = QLineEdit()
        self.entry_password = QLineEdit()
        self.entry_password.setEchoMode(QLineEdit.Password)
        form_layout.addWidget(QLabel("Nom d'utilisateur"), 0, 0)
        form_layout.addWidget(self.entry_username, 0, 1)
        form_layout.addWidget(QLabel("Mot de passe"), 1, 0)
        form_layout.addWidget(self.entry_password, 1, 1)

        layout.addLayout(form_layout)

        self.button_login = QPushButton("Se connecter")
        self.button_login.clicked.connect(self.controleur.se_connecter)
        layout.addWidget(self.button_login)

        widget.setLayout(layout)
        return widget

    def afficher_message(self, titre, message):
        QMessageBox.information(self, titre, message)

    def basculer_vers_connexion(self):
        self.stacked_widget.setCurrentWidget(self.frame_connexion)
        
    def basculer_vers_main_window(self):
        self.frame_main_window.update_user_info(self.entry_username.text())
        self.entry_username.clear()
        self.entry_password.clear()
        self.frame_main_window.show()
        self.close()
        
    def obtenir_identifiants(self):
        return self.entry_username.text(), self.entry_password.text()
    
    def closeEvent(self, event):
        self.controleur.arreter_serveur()
        event.accept() 

class Controleur:
    def __init__(self, screen_info, app):
        self.screen_info = screen_info
        self.app = app
        
        init_db.initialize_db()
        
        self.process_serveur = multiprocessing.Process(target=lancer_serveur)
        self.process_serveur.start()
        
        self.modele = client.Modele()
        self.connexion = Connexion(self, self.screen_info)
        
        self.connexion.show()

    def se_connecter(self):
        username, password = self.connexion.obtenir_identifiants()
        if self.modele.verifier_identifiants(username, password) is not None:
            self.connexion.afficher_message("Succès", "Connexion réussie !")
            self.connexion.basculer_vers_main_window()
        else:
            self.connexion.afficher_message("Erreur", "Nom d'utilisateur ou mot de passe incorrect.")
    
    def arreter_serveur(self):
        if self.process_serveur.is_alive():
            self.process_serveur.terminate()
            self.process_serveur.join()

    def demarrer(self):
        self.connexion.show()
        sys.exit(self.app.exec())
        
    def __del__(self):
        if self.process_serveur.is_alive():
            self.process_serveur.terminate()
            self.process_serveur.join()
        else:
            self.arreter_serveur()

def main():
    app = QApplication(sys.argv)
    screen_info = app.primaryScreen().geometry()
    c = Controleur(screen_info, app)
    c.demarrer()
      
if __name__ == "__main__":
    main()
