from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt

class Header(QWidget):

    def __init__(self,minimize_app,close_app):

        super().__init__()

        self.setStyleSheet("background-color: rgba(0,0,0,0);")
        self.setFixedHeight(20)
        
        # Layout for title bar
        title_bar_layout = QHBoxLayout(self)
        title_bar_layout.setContentsMargins(1, 0, 1, 0)

        # Add logo or title
        self.logo_label = QLabel("TSP: An Evolutive Approach")
        self.logo_label.setStyleSheet("color: white; font-size: 12px; font-weight: 10px;")
        title_bar_layout.addWidget(self.logo_label)

        # Add buttons
        self.minimize_button = QPushButton("")
        self.minimize_button.setFixedSize(15, 15)
        self.minimize_button.setStyleSheet("background-color: #444; color: white; border: none; border-radius: 7px;")
        self.minimize_button.clicked.connect(minimize_app)
        title_bar_layout.addWidget(self.minimize_button)

        self.close_button = QPushButton("")
        self.close_button.setFixedSize(15, 15)
        self.close_button.setStyleSheet("background-color: #900; color: white; border: none; border-radius: 7px;")
        self.close_button.clicked.connect(close_app)
        title_bar_layout.addWidget(self.close_button)