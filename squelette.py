import sys
from datetime import datetime
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout,
    QPushButton, QLabel, QHBoxLayout, QMessageBox, QLineEdit, QDialog, QComboBox
)
from PyQt6.QtCore import QTimer, Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np

class Onglet:
    def __init__(self, name, role):
        self.name = name
        self.role = role
        self.last_login = datetime.now()

class Graphique:
    def __init__(self):
        pass

    def tracer_graphique(self, type_graphique, valeurs, categories=None):
        fig = Figure(figsize=(10, 5))
        canvas = FigureCanvas(fig)

        ax = fig.add_subplot(111)

        if type_graphique == 'ligne':
            x = np.arange(len(valeurs))
            ax.plot(x, valeurs, marker='o')
        elif type_graphique == 'barres':
            if categories is None:
                raise ValueError("Pour un graphique à barres, 'categories' doit être fourni.")
            ax.bar(categories, valeurs, color='skyblue')
        elif type_graphique == 'histogramme':
            ax.hist(valeurs, bins=10, color='lightgreen', edgecolor='black')
        else:
            raise ValueError("Type de graphique non reconnu.")

        ax.set_title('Graphique')
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.grid(True)

        return canvas

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Fenêtre avec Onglets Dynamiques")
        self.resize(600, 800)

        self.current_user_role = None
        self.onglets_existants = [
            Onglet("admin", "Admin"),
            Onglet("boss", "Boss"),
            Onglet("employe", "Employé"),
        ]

        self.tab_widget = QTabWidget()
        self.tab_widget.currentChanged.connect(self.update_last_index)

        self.quit_button = QPushButton("Quitter")
        self.quit_button.clicked.connect(self.close)

        self.back_button = QPushButton("Retour")
        self.back_button.clicked.connect(self.go_back)

        self.sign_out_button = QPushButton("Déconnexion")
        self.sign_out_button.clicked.connect(self.sign_out)

        self.connect_button = QPushButton("Connexion")
        self.connect_button.clicked.connect(self.show_login_dialog)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.back_button)
        button_layout.addWidget(self.quit_button)
        button_layout.addWidget(self.sign_out_button)
        button_layout.addWidget(self.connect_button)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.tab_widget)
        main_layout.addLayout(button_layout)

        self.time_label = QLabel()
        self.update_time()
        self.time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.time_label)

        self.user_info_label = QLabel()
        self.update_user_info("Invité", None)
        self.user_info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.user_info_label)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        self.last_index = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)

        self.update_button_visibility()

        # Création d'onglets
        self.create_tabs()

    def create_tabs(self):
        for onglet in self.onglets_existants:
            if self.user_role_can_access(onglet.role):
                self.add_tab(onglet.name, onglet.role)

    def add_tab(self, name, user_role):
        tab = QWidget()
        layout = QVBoxLayout()

        if user_role == "Boss":
            self.graphique_button = QPushButton("Afficher Graphique")
            self.graphique_button.clicked.connect(self.show_graphique_dialog)
            layout.addWidget(self.graphique_button)

        layout.addWidget(QLabel(f"Onglet créé par : {user_role}"))
        layout.addWidget(QLabel(f"Heure de dernière connexion : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"))
        tab.setLayout(layout)

        self.tab_widget.addTab(tab, name)
        self.tab_widget.setTabText(self.tab_widget.indexOf(tab), name)

    def show_graphique_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Créer un Graphique")

        layout = QVBoxLayout()

        type_graphique_label = QLabel("Type de Graphique:")
        self.type_graphique_combo = QComboBox()
        self.type_graphique_combo.addItems(['ligne', 'barres', 'histogramme'])

        titre_label = QLabel("Titre:")
        self.titre_input = QLineEdit()

        xlabel_label = QLabel("Nom de l'axe X:")
        self.xlabel_input = QLineEdit()

        ylabel_label = QLabel("Nom de l'axe Y:")
        self.ylabel_input = QLineEdit()

        valeurs_label = QLabel("Valeurs (séparées par des virgules):")
        self.valeurs_input = QLineEdit()

        categories_label = QLabel("Catégories (pour barres, séparées par des virgules):")
        self.categories_input = QLineEdit()

        create_button = QPushButton("Créer Graphique")
        create_button.clicked.connect(lambda: self.create_graphique(dialog))

        layout.addWidget(type_graphique_label)
        layout.addWidget(self.type_graphique_combo)
        layout.addWidget(titre_label)
        layout.addWidget(self.titre_input)
        layout.addWidget(xlabel_label)
        layout.addWidget(self.xlabel_input)
        layout.addWidget(ylabel_label)
        layout.addWidget(self.ylabel_input)
        layout.addWidget(valeurs_label)
        layout.addWidget(self.valeurs_input)
        layout.addWidget(categories_label)
        layout.addWidget(self.categories_input)
        layout.addWidget(create_button)

        dialog.setLayout(layout)
        dialog.exec()

    def create_graphique(self, dialog):
        type_graphique = self.type_graphique_combo.currentText()
        valeurs = list(map(float, self.valeurs_input.text().split(',')))
        categories = self.categories_input.text().split(',') if type_graphique == 'barres' else None

        boss_tab_index = self.tab_widget.indexOf(self.tab_widget.widget(1))  # Assumer que "Boss" est à l'index 1
        if boss_tab_index != -1:
            boss_tab = self.tab_widget.widget(boss_tab_index)

            if hasattr(self, 'graphique_canvas') and self.graphique_canvas is not None:
                self.graphique_canvas.deleteLater()

            graphique = Graphique()
            self.graphique_canvas = graphique.tracer_graphique(type_graphique, valeurs, categories)
            boss_tab.layout().addWidget(self.graphique_canvas)

        dialog.accept()

    def user_role_can_access(self, role):
        if self.current_user_role == "Boss":
            return True
        elif self.current_user_role == "Admin":
            return role in ["Admin", "Employé"]
        elif self.current_user_role == "Employé":
            return role == "Employé"
        return False

    def update_last_index(self, index):
        self.last_index = index

    def go_back(self):
        if self.last_index > 0:
            self.tab_widget.setCurrentIndex(self.last_index - 1)

    def update_time(self):
        current_time = datetime.now().strftime("%H:%M:%S")
        self.time_label.setText(f"Heure actuelle : {current_time}")

    def update_user_info(self, name, role):
        self.current_user_role = role
        self.user_info_label.setText(f"Connecté : {name} (Rôle : {role})" if role else "Connecté : Invité")
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
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
