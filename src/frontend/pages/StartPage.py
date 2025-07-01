from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QGridLayout, QGraphicsOpacityEffect, QFileDialog, QTextEdit, QPlainTextEdit,  QComboBox, QLabel, QListWidget
from PySide6.QtCore import Qt
from PySide6.QtGui import QTextOption

class StartPage(QWidget):

    def __init__(self, on_start_button_click):

        super().__init__()
        
        # layout setup
        self.layout = QVBoxLayout(self)
        
        # start button
        self.start_button = QPushButton("START", self)
        self.layout.addWidget(self.start_button, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # connect the start button signal to the provided callback
        self.start_button.clicked.connect(on_start_button_click)