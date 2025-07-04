from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QGridLayout, QGraphicsOpacityEffect, QFileDialog, QTextEdit, QPlainTextEdit,  QComboBox, QLabel, QListWidget
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QTextOption


class StartPage(QWidget):

    start_button_pushed = Signal(str)       # button signal

    def __init__(self):

        super().__init__()
        
        # layout setup
        self.layout = QVBoxLayout(self)
        
        # start button
        self.start_button = QPushButton("START", self)
        self.start_button.clicked.connect(self.emit_start_button_pushed)
        self.layout.addWidget(self.start_button, alignment=Qt.AlignmentFlag.AlignCenter)

    def emit_start_button_pushed(self):     # button signal emission (happens when clicked)
        self.start_button_pushed.emit(":)")