from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QTableWidget, QTableWidgetItem, QStackedWidget)
from PySide6.QtCore import Qt
from backend.TSPInstance import TSPInstance, TSPInstanceParser
from backend.EvolutiveAlgorithm import EvolutiveAlgorithm
from frontend.pages.StartPage import StartPage
from frontend.pages.InstancesPage import InstancesPage
from frontend.pages.EAPage import EAPage
from frontend.Header import Header
from DataHandler import DataHandler



class TSPApp(QWidget):

    def __init__(self):

        super().__init__()
    
        # database connection
        db = DataHandler()

        # window setup
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)
        self.header = Header(self.showMinimized, self.close)
        self.resize(800, 600)
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.header)

        # stacked widget: para transicionar entre páginas
        self.stacked_widget = QStackedWidget(self)
        self.layout.addWidget(self.stacked_widget)

        # page 1: start screen
        self.start_page = StartPage()
        self.stacked_widget.addWidget(self.start_page)      # add it to the stack for display
        self.start_page.start_button_pushed.connect(self.go_to_instances_page)

        # page 2: instances page
        self.instances_page = InstancesPage(db)
        self.stacked_widget.addWidget(self.instances_page)
        self.instances_page.footer.next_button.clicked.connect(self.go_to_ea_page)

        #self.matrix_page = InstancesPage(db.get_all_instances)
        #self.stacked_widget.addWidget(self.matrix_page)     # add it to the stack for display

        # page 3: simulation parameters (modifiable by the user)
        self.ea_page = EAPage()
        self.stacked_widget.addWidget(self.ea_page)

        # page 4: run simulation (time, number of generations so far, best solution so far, convergence conjuction (green or red ligts))

        # page 5: simulation results (when did we get the best solution, costo computacional y temporal, otras métricas). Guardado de los datos.

    def go_to_start_page(self):
        self.stacked_widget.setCurrentWidget(self.start_page)

    def go_to_instances_page(self):
        self.stacked_widget.setCurrentWidget(self.instances_page)

    def go_to_ea_page(self,file_path):
        self.instance = TSPInstanceParser.parse(file_path)
        self.stacked_widget.setCurrentWidget(self.ea_page)



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
