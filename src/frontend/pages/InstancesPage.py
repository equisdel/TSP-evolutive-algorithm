from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTableWidget
from PySide6.QtCore import Qt

class InstancesPage(QWidget):

    def __init__(self,all_instances):

        super().__init__()
        
        # Layout setup
        self.matrix_layout = QVBoxLayout(self)  # vertical layout
        self.matrix_table = QTableWidget(self)
        self.matrix_layout.addWidget(self)
        

        # Connect the start button signal to the provided callback
        #self.start_button.clicked.connect(on_start_button_click)


    def load_tsp_instances(self):
        # fetches from the database
        file_name, _ = QFileDialog.getOpenFileName(
            self, 
            "Open TSP Instance File",
            "C:/Users/Delfina/Downloads/Evolutiva/Material/Instancias TSP",
            "Text Files (*.atsp);;All Files (*)"
        )

        if file_name:
            print(f"Selected file: {file_name}")
            instance = TSPInstanceParser.parse(file_name)
            if instance:
                print(instance.matrix)
                self.display_matrix(instance)
                self.stacked_widget.setCurrentWidget(self.matrix_page)  # Switch to the Matrix page
            else:
                print("Failed to parse TSP instance.")
        else:
            print("No file selected.")

    """
    def display_matrix(self, instance: TSPInstance):
        # Display the matrix in a QTableWidget
        matrix = instance.matrix
        dimension = instance.dimension

        self.matrix_table.setRowCount(dimension)
        self.matrix_table.setColumnCount(dimension)

        for i in range(dimension):
            for j in range(dimension):
                self.matrix_table.setItem(i, j, QTableWidgetItem(str(matrix[i][j])))
    """