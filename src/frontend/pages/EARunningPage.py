from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QStackedWidget, QLabel, QPushButton
from PySide6.QtCore import Signal
from backend.Graph import Graph

class EARunningPage(QWidget):
    
    next_button_pushed = Signal(str)     # emits when a file is selected
    back_button_pushed = Signal(str)

    def set_next_button_pushed(self):
        self.next_button_pushed.emit("xd")

    def set_back_button_pushed(self):
        self.back_button_pushed.emit("xd x2")

    def __init__(self,ea_created):

        super().__init__()

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.stacked_widget = QStackedWidget(self)
        self.layout.addWidget(self.stacked_widget)

        # loading page
        self.loading = QWidget()
        self.loading_layout = QHBoxLayout(self.loading)
        self.loading_label = QLabel("LOADING")
        self.loading_layout.addWidget(self.loading_label)
        self.stacked_widget.addWidget(self.loading)

        # ea running page
        self.ea_running_page = QWidget()
        self.ea_run_layout = QHBoxLayout(self.ea_running_page)
        self.ea_run_label = QLabel("RUNNING")
        self.run_button = QPushButton("RUN")
        self.ea_run_layout.addWidget(self.ea_run_label)
        self.ea_run_layout.addWidget(self.run_button)
        self.stacked_widget.addWidget(self.ea_running_page)

        #self.stacked_widget.setCurrentWidget(self.loading)
        self.stacked_widget.setCurrentWidget(self.ea_running_page)

        self.run_button.clicked.connect(self.run_ea)
        ea_created.connect(self._on_ea_created)
    
    def run_ea(self):
        self.ea.run()
        self.graph = Graph(self.ea)
        self.graph.display("best_solutions_graph")
    
    def _on_ea_created(self,ea):
        print("luchi")
        self.ea = ea

