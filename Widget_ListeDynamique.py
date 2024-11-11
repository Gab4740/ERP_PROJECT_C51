from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QScrollArea
from PySide6.QtCore import Qt

class EmployeeList(QWidget):
    def __init__(self, list_data, column_names, num_rows):
        super().__init__()

        self.setWindowTitle("Employee List")

        # Layout for the entire widget
        self.main_layout = QVBoxLayout(self)

        # Scroll Area to hold the list of employees
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)

        # Container widget for employee rows
        self.container_widget = QWidget()
        self.container_layout = QVBoxLayout(self.container_widget)

        # Add the container widget to the scroll area
        self.scroll_area.setWidget(self.container_widget)

        # Add the scroll area to the main layout
        self.main_layout.addWidget(self.scroll_area)

        # Set the main layout for the window
        self.setLayout(self.main_layout)

        # Store employee data, limit rows if necessary
        self.employee_data = list_data[:num_rows]  # Limit rows to the specified number
        self.column_names = column_names  # Store column names

        # Add the column headers
        self.add_column_headers()

        # Add employee rows to the layout
        self.add_employee_rows()

    def add_column_headers(self):
        """
        Add the column headers at the top of the list.
        """
        header_layout = QHBoxLayout()

        # Create a label for each column name and add it to the header layout
        for column_name in self.column_names:
            label = QLabel(column_name, self)
            label.setAlignment(Qt.AlignCenter)  # Center-align the text
            # Apply custom styling to column titles
            label.setStyleSheet("""
                background-color: #4CAF50;  /* Green background */
                color: white;               /* White text */
                font-size: 16px;            /* Font size */
                font-weight: bold;          /* Bold text */
                padding: 5px;               /* Padding inside labels */
            """)
            header_layout.addWidget(label)

        # Create a QWidget to hold the header layout
        header_widget = QWidget(self)
        header_widget.setLayout(header_layout)

        # Add the header widget to the container layout
        self.container_layout.addWidget(header_widget)

    def add_employee_rows(self):
        """
        Add a number of employee rows to the list based on the employee data.
        Each row is represented by a QLabel in a horizontal layout.
        """
        for employee in self.employee_data:
            row = self.create_employee_row(employee)
            self.container_layout.addWidget(row)

    def create_employee_row(self, employee):
        """
        Create a row (QWidget) to display employee data.
        Each employee is represented by a horizontal layout of labels.
        """
        row_layout = QHBoxLayout()

        # Create labels for each column of employee data
        for data in employee:
            label = QLabel(data, self)
            row_layout.addWidget(label)

        # Create a QWidget to hold the row layout
        row_widget = QWidget(self)
        row_widget.setLayout(row_layout)

        return row_widget


#  USAGE EXAMPLE
#  self.employee_data = [
#      ["John Doe", "Manager", "$5000"],
#      ["Jane Smith", "Engineer", "$4000"],
#      ["Bob Brown", "Designer", "$3500"],
#      ["Alice Green", "HR", "$3000"],
#      ["Charlie White", "Developer", "$4500"]
#  ]
#  self.column_names = ["Name", "Position", "Salary"]
#  
#  
#  self.employee_list_widget = EmployeeList(self.employee_data, self.column_names, len(self.employee_data))
