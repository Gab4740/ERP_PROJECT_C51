from datetime import datetime
from abc import ABC, abstractmethod
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout,
    QPushButton, QLabel, QHBoxLayout, QMessageBox, QLineEdit, QDialog, QComboBox
)

class Onglet(ABC):
    def __init__(self, name, visibility):
        self.name = name
        self.visibility = visibility
        self.last_login = datetime.now()
        self.widget = QWidget()
        
        self.create_content()
        
    def get_visibility(self):
        return self.visibility
    
    def get_name(self):
        return self.name
    
    def get_widget(self):
        return self.widget
    
    @abstractmethod
    def create_content(self):
        pass
        # A REDEFENIR DANS LES CLASSES ENFANTS   

      
# EXAMPLE GENERAL       
class Onglet_General(Onglet):
    def __init__(self, name, visibility):
        super().__init__(name, visibility)
    
    def create_content(self):
        label = QLabel()
        label.setText(self.visibility)
        layout = QHBoxLayout()
        layout.addWidget(label)
        self.widget.setLayout(layout)
  
     
# EXAMPLE ADMIN           
class Onglet_Admin(Onglet):
    def __init__(self, name, visibility):
        super().__init__(name, visibility)
    
    def create_content(self):
        label = QLabel()
        label.setText(self.visibility)
        label2 = QLabel()
        label2.setText(self.name)
        layout = QHBoxLayout()
        layout.addWidget(label)
        layout.addWidget(label2)
        self.widget.setLayout(layout)