import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, 
    QTextEdit, QLineEdit, QLabel, QComboBox, QHBoxLayout
)
from PySide6.QtCore import QDate, Qt

class ScheduleApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Horaire des Employés")
        self.setGeometry(100, 100, 800, 600)

        self.start_date = QDate.currentDate().addDays(-QDate.currentDate().dayOfWeek() + 1)
        self.employees = ["Alice", "Bob", "Charlie", "David", "Eva"]
        
        self.schedule = {employee: {} for employee in self.employees}
        self.leaves = {employee: [] for employee in self.employees}

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        self.schedule_display = QTextEdit(self)
        self.schedule_display.setReadOnly(True)
        self.schedule_display.setFixedHeight(400)
        layout.addWidget(self.schedule_display)

        self.generate_button = QPushButton("Mise à jour de l'horaire", self)
        self.generate_button.clicked.connect(self.display_schedule)
        layout.addWidget(self.generate_button)

        self.prev_week_button = QPushButton("Semaine précédente", self)
        self.prev_week_button.clicked.connect(self.prev_week)
        layout.addWidget(self.prev_week_button)

        self.next_week_button = QPushButton("Semaine suivante", self)
        self.next_week_button.clicked.connect(self.next_week)
        layout.addWidget(self.next_week_button)

        modify_layout = QHBoxLayout()
        self.employee_combo = QComboBox(self)
        self.employee_combo.addItems(self.employees)
        modify_layout.addWidget(QLabel("Employé:"))
        modify_layout.addWidget(self.employee_combo)

        self.day_combo = QComboBox(self)
        self.day_combo.addItems(["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"])
        modify_layout.addWidget(QLabel("Jour:"))
        modify_layout.addWidget(self.day_combo)

        self.hour_input = QLineEdit(self)
        self.hour_input.setPlaceholderText("Nouvel horaire (ex: 9h00 - 18h00)")
        modify_layout.addWidget(QLabel("Nouvel horaire:"))
        modify_layout.addWidget(self.hour_input)

        self.modify_button = QPushButton("Modifier l'horaire", self)
        self.modify_button.clicked.connect(self.modify_schedule)
        modify_layout.addWidget(self.modify_button)

        layout.addLayout(modify_layout)

        self.leave_button = QPushButton("Afficher les congés", self)
        self.leave_button.clicked.connect(self.show_leave_window)
        layout.addWidget(self.leave_button)

        self.quit_button = QPushButton("Quitter", self)
        self.quit_button.clicked.connect(self.close)
        layout.addWidget(self.quit_button)

        for button in [self.generate_button, self.prev_week_button, self.next_week_button, self.modify_button, self.leave_button, self.quit_button]:
            button.setFixedHeight(30)

        self.display_schedule()

    def display_schedule(self):
        header = "Employé  | " + " | ".join(
            [f"{day} - {self.start_date.addDays(i).toString('dd/MM/yyyy')}" for i, day in enumerate(["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"])]
        ) + "\n"
        header += "-" * (len(header) - 1) + "\n"
        
        schedule_text = header
        
        for employee in self.employees:
            schedule_text += f"{employee:<8} | "  
            for i in range(7):  
                day_date = self.start_date.addDays(i).toString(Qt.ISODate)
                hour = self.schedule[employee].get(day_date, "8h00 - 17h00")
                if day_date in self.leaves[employee]:
                    hour = "Congé"  # Mark leave
                schedule_text += f"{hour:<15} | "  
            schedule_text += "\n\n"  

        self.schedule_display.setPlainText(schedule_text)

    def modify_schedule(self):
        employee = self.employee_combo.currentText()
        day_index = self.day_combo.currentIndex()
        new_schedule = self.hour_input.text()

        day_date = self.start_date.addDays(day_index).toString(Qt.ISODate)

        if new_schedule:
            total_hours = self.calculate_total_hours(employee)
            new_hours = self.parse_hours(new_schedule)

            if total_hours + new_hours > 40:
                print(f"Erreur: Total des heures dépassé pour {employee}.")
                return

            self.schedule[employee][day_date] = new_schedule
            self.hour_input.clear()
            self.display_schedule()

    def calculate_total_hours(self, employee):
        total_hours = 0
        for day, hours in self.schedule[employee].items():
            total_hours += self.parse_hours(hours)
        return total_hours

    def parse_hours(self, hour_str):
        if hour_str == "Congé":
            return 0
        try:
            start, end = hour_str.split(" - ")
            start_hour, start_minute = map(int, start[:-1].split('h'))
            end_hour, end_minute = map(int, end[:-1].split('h'))
            return (end_hour + end_minute / 60) - (start_hour + start_minute / 60)
        except ValueError:
            print(f"Erreur de format d'heure: {hour_str}")
            return 0  # Retourne 0 en cas d'erreur

    def next_week(self):
        self.start_date = self.start_date.addDays(7)
        self.display_schedule()

    def prev_week(self):
        self.start_date = self.start_date.addDays(-7)
        self.display_schedule()

    def show_leave_window(self):
        self.leave_window = LeaveWindow(self.employees, self.leaves, self.schedule, self.start_date)
        self.leave_window.show()

class LeaveWindow(QMainWindow):
    def __init__(self, employees, leaves, schedule, start_date):
        super().__init__()
        self.setWindowTitle("Congés des Employés")
        self.setGeometry(100, 100, 800, 600)
        
        self.start_date = start_date
        self.employees = employees
        self.leaves = leaves
        self.schedule = schedule
        
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        
        self.layout = QVBoxLayout(self.central_widget)

        self.leave_display = QTextEdit(self)
        self.leave_display.setReadOnly(True)
        self.leave_display.setFixedHeight(400)
        self.layout.addWidget(self.leave_display)

        self.prev_week_button = QPushButton("Semaine précédente", self)
        self.prev_week_button.clicked.connect(self.prev_week)
        self.layout.addWidget(self.prev_week_button)

        self.next_week_button = QPushButton("Semaine suivante", self)
        self.next_week_button.clicked.connect(self.next_week)
        self.layout.addWidget(self.next_week_button)

        modify_layout = QHBoxLayout()
        self.leave_employee_combo = QComboBox(self)
        self.leave_employee_combo.addItems(self.employees)
        modify_layout.addWidget(QLabel("Employé:"))
        modify_layout.addWidget(self.leave_employee_combo)

        self.leave_day_combo = QComboBox(self)
        self.leave_day_combo.addItems(["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"])
        modify_layout.addWidget(QLabel("Jour:"))
        modify_layout.addWidget(self.leave_day_combo)

        self.add_leave_button = QPushButton("Ajouter Congé", self)
        self.add_leave_button.clicked.connect(self.add_leave)
        modify_layout.addWidget(self.add_leave_button)

        self.remove_leave_button = QPushButton("Retirer Congé", self)
        self.remove_leave_button.clicked.connect(self.remove_leave)
        modify_layout.addWidget(self.remove_leave_button)

        self.layout.addLayout(modify_layout)

        self.close_button = QPushButton("Retour", self)
        self.close_button.clicked.connect(self.close)
        self.layout.addWidget(self.close_button)

        self.display_leaves()

    def display_leaves(self):
        header = "Employé  | " + " | ".join(
            [f"{day} - {self.start_date.addDays(i).toString('dd/MM/yyyy')}" for i, day in enumerate(["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"])]
        ) + "\n"
        header += "-" * (len(header) - 1) + "\n"
        
        leave_text = header
        
        for employee in self.employees:
            leave_text += f"{employee:<8} | "  
            for i in range(7):  
                day_date = self.start_date.addDays(i).toString(Qt.ISODate)
                if day_date in self.leaves[employee]:
                    leave_text += "Congé         | "  
                else:
                    leave_text += "              | "  
            leave_text += "\n\n"  

        self.leave_display.setPlainText(leave_text)

    def add_leave(self):
        employee = self.leave_employee_combo.currentText()
        day_index = self.leave_day_combo.currentIndex()
        day_date = self.start_date.addDays(day_index).toString(Qt.ISODate)

        if day_date not in self.leaves[employee]:
            self.leaves[employee].append(day_date)
            self.display_leaves()
            self.update_schedule_with_leave(employee, day_date)

    def remove_leave(self):
        employee = self.leave_employee_combo.currentText()
        day_index = self.leave_day_combo.currentIndex()
        day_date = self.start_date.addDays(day_index).toString(Qt.ISODate)

        if day_date in self.leaves[employee]:
            self.leaves[employee].remove(day_date)
            self.display_leaves()
            self.update_schedule_with_leave(employee, day_date, remove=True)

    def update_schedule_with_leave(self, employee, day_date, remove=False):
        if remove:
            if day_date in self.schedule[employee]:
                del self.schedule[employee][day_date]  # Remove leave from schedule
        else:
            self.schedule[employee][day_date] = "Congé"  # Mark as leave

    def next_week(self):
        self.start_date = self.start_date.addDays(7)
        self.display_leaves()

    def prev_week(self):
        self.start_date = self.start_date.addDays(-7)
        self.display_leaves()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ScheduleApp()
    window.show()
    sys.exit(app.exec())
