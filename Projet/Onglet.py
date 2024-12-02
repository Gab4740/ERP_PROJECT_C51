from datetime import datetime
from abc import ABC, abstractmethod
from PySide6.QtWidgets import QWidget

class Onglet(ABC):
    def __init__(self, name:str, visibility:int):
        self.name = name
        self.visibility = visibility
        self.last_view = datetime.now()
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