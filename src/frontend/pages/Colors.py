from PyQt6.QtWidgets import QWidget, QGridLayout
from PyQt6.QtCore import Qt

class GridPage(QWidget):
    def __init__(self):
        super().__init__()

        # Create a grid layout
        layout = QGridLayout()
        layout.setSpacing(5)  # Optional: spacing between sections

        # Create four sections with different background colors
        left_top = self.create_colored_widget("red")
        left_bottom = self.create_colored_widget("blue")
        right_top = self.create_colored_widget("green")
        right_bottom = self.create_colored_widget("yellow")

        # Add widgets to the grid layout
        layout.addWidget(left_top, 0, 0)    # Top-left
        layout.addWidget(left_bottom, 1, 0) # Bottom-left
        layout.addWidget(right_top, 0, 1)   # Top-right
        layout.addWidget(right_bottom, 1, 1) # Bottom-right

        # Set column and row stretch to define proportions
        layout.setColumnStretch(0, 2)  # Left sections take 2/3 of the width
        layout.setColumnStretch(1, 1)  # Right sections take 1/3 of the width
        layout.setRowStretch(0, 1)     # Top sections take equal height
        layout.setRowStretch(1, 1)     # Bottom sections take equal height

        # Set the layout for the widget
        self.setLayout(layout)

    def create_colored_widget(self, color):
        # Create a widget with a specific background color
        widget = QWidget()
        widget.setStyleSheet(f"background-color: {color};")
        return widget
