from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QTableWidget, QTableWidgetItem, QStackedWidget)
from PySide6.QtCore import Qt
from TSPInstance import TSPInstance, TSPInstanceParser

class TSPApp(QWidget):

    def __init__(self):

        super().__init__()

        # window setup
        self.setWindowTitle("TSP: An Evolutive Approach")
        self.resize(800, 600)
        self.layout = QVBoxLayout(self)

        # stacked widget: para transicionar entre páginas
        self.stacked_widget = QStackedWidget(self)
        self.layout.addWidget(self.stacked_widget)

        # page 1: start screen
        self.start_page = QWidget()
        #self.start_page.setStyleSheet("background-image: url('path_to_background_image.jpg'); background-size: cover;")
        self.start_layout = QVBoxLayout(self.start_page)    # vertical layout

        self.start_button = QPushButton("START", self.start_page)
        self.start_button.setStyleSheet("font-size: 20px; padding: 10px;")
        self.start_layout.addWidget(self.start_button, alignment=Qt.AlignmentFlag.AlignCenter)

        self.start_button.clicked.connect(self.load_tsp_instance)

        self.stacked_widget.addWidget(self.start_page)      # add it to the stack for display

        # page 2: instance info display

        # number of cities
        # overview of the matrix
        # best solution so far (known solution and found solution, takes it from the output)
        # 
        self.matrix_page = QWidget()
        self.matrix_layout = QVBoxLayout(self.matrix_page)  # vertical layout

        self.matrix_table = QTableWidget(self.matrix_page)
        self.matrix_layout.addWidget(self.matrix_table)

        self.stacked_widget.addWidget(self.matrix_page)     # add it to the stack for display

        # page 3: simulation parameters (modifiable by the user)

        # page 4: run simulation (time, number of generations so far, best solution so far, convergence conjuction (green or red ligts))

        # page 5: simulation results (when did we get the best solution, costo computacional y temporal, otras métricas). Guardado de los datos.

    def load_tsp_instance(self):

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

    def display_matrix(self, instance: TSPInstance):
        # Display the matrix in a QTableWidget
        matrix = instance.matrix
        dimension = instance.dimension

        self.matrix_table.setRowCount(dimension)
        self.matrix_table.setColumnCount(dimension)

        for i in range(dimension):
            for j in range(dimension):
                self.matrix_table.setItem(i, j, QTableWidgetItem(str(matrix[i][j])))


if __name__ == "__main__":
    
    app = QApplication([])

    window = TSPApp()
    window.show() 

    app.exec()
