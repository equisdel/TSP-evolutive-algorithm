import pyqtgraph as pg
from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QStackedWidget, QLabel, QPushButton
from PySide6.QtCore import Signal,Qt
from backend.Graph import Graph
pg.setConfigOption('foreground', 'k')  # white foreground (axes, labels, text)

class GraphWidget(pg.PlotWidget):
    

    def __init__(self):
        super().__init__()
        self.setBackground('k')
        self.addLegend()

        # Plot lines with color and marker similar to your matplotlib style
        self.curve_gen = self.plot(pen=pg.mkPen('b', width=2), name="Best: Generation",
                                   symbol='o', symbolSize=6, symbolBrush='b')
        self.curve_exe = self.plot(pen=pg.mkPen('y', width=2), name="Best: Execution")
        self.curve_abs = self.plot(pen=pg.mkPen('g', style=Qt.DotLine), name="Best: Absolute")

    def update_data(self, best_gen, best_exe, best_abs):
        print("update")
        x = list(range(len(best_gen)))
        self.curve_gen.setData(x, best_gen)
        self.curve_exe.setData(x, best_exe)
        self.curve_abs.setData(x, best_abs)

class EARunningPage(QWidget):
    
    next_button_pushed = Signal(str)     # emits when a file is selected
    back_button_pushed = Signal(str)

    def set_next_button_pushed(self):
        self.next_button_pushed.emit("xd")

    def set_back_button_pushed(self):
        self.back_button_pushed.emit("xd x2")

    def __init__(self,ea_created):

        super().__init__()

        self.layout = QVBoxLayout(self)

        self.plotWidget = GraphWidget()
        self.layout.addWidget(self.plotWidget) 
        #self.plotWidget.plot([1, 2, 3])

        self.stacked_widget = QStackedWidget()
        self.layout.addWidget(self.stacked_widget)

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

    def update_best(self, gen, exe, abs):
        self.ea_run_label.setText(str(gen[-1:])+":"+str(exe[-1:])+":"+str(abs[-1:]))
    
    def run_ea(self):
        self.ea.data_updated.connect(self.plotWidget.update_data)
        self.ea.data_updated.connect(self.update_best)
        self.ea.run(self.ea)
        ##pg.plot(self.ea.best_solutions_gen)
        self.graph = Graph(self.ea)
        self.graph.display("best_solutions_graph")
    
    def _on_ea_created(self,ea):
        self.ea = ea

