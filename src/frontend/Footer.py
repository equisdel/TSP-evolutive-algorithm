from PySide6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QApplication
from PySide6.QtCore import Qt, Signal
import sys

class Footer(QWidget):

    def __init__(self,initial_state_next_button=False):
        
        super().__init__()
        self.layout = QHBoxLayout()

        self.setFixedHeight(48)

        self.back_button = QPushButton("BACK")
        self.next_button = QPushButton("NEXT")

        self.back_button.setFixedSize(80, 32)
        self.next_button.setFixedSize(80, 32)

        self.layout.addWidget(self.back_button, alignment=Qt.AlignLeft)
        self.layout.addStretch(1)
        self.layout.addWidget(self.next_button, alignment=Qt.AlignRight)

        self.next_button.setEnabled(initial_state_next_button)

        self.setLayout(self.layout)

    def enable_next(self):
        self.next_button.setEnabled(True)

if __name__ == "__main__":
    app = QApplication(sys.argv)  # Create the application
    f = Footer(print, print)
    f.show()                      # Show the widget
    sys.exit(app.exec())  
