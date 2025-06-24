from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QTableWidget, QTableWidgetItem, QStackedWidget)
from PySide6.QtCore import Qt
from backend.TSPInstance import TSPInstance, TSPInstanceParser
from frontend.pages.StartPage import StartPage
from frontend.pages.InstancesPage import InstancesPage
from frontend.pages.Colors import GridPage

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

        # database connection
        #self.client = MongoClient("mongodb://localhost:27017/")
        #self.db = self.client.my_database
        #self.collection = self.db.my_collection

        # page 1: start screen
        self.start_page = StartPage(self.load_tsp_instances)
        self.stacked_widget.addWidget(self.start_page)      # add it to the stack for display

        # page 2: instances page display
        self.matrix_page = InstancesPage()
        self.stacked_widget.addWidget(self.matrix_page)     # add it to the stack for display

        # page 3: simulation parameters (modifiable by the user)

        # page 4: run simulation (time, number of generations so far, best solution so far, convergence conjuction (green or red ligts))

        # page 5: simulation results (when did we get the best solution, costo computacional y temporal, otras métricas). Guardado de los datos.

    def load_tsp_instances(self):
        # fetches from the database
        data = self.collection.find_all({})  # Example query
        if data:
            self.data_label.setText(f"Name: {data['name']}, Age: {data['age']}")
        else:
            self.data_label.setText("No data found.")
        return instances

    def display_matrix(self, instance: TSPInstance):
        # Display the matrix in a QTableWidget
        matrix = instance.matrix
        dimension = instance.dimension

        self.matrix_table.setRowCount(dimension)
        self.matrix_table.setColumnCount(dimension)

        for i in range(dimension):
            for j in range(dimension):
                self.matrix_table.setItem(i, j, QTableWidgetItem(str(matrix[i][j])))

def apply_stylesheet(app, qss_file):
    with open(qss_file, "r") as file:
        app.setStyleSheet(file.read())

if __name__ == "__main__":
    
    app = QApplication([]) #

    window = TSPApp()
    apply_stylesheet(app, "./src/frontend/darkstyle.qss")
    window.show()

    app.exec()
