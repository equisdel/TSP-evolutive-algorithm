import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QFileDialog, QLabel
from PyQt6.QtCore import Qt

class MatrixLoaderApp(QMainWindow):
    
    def __init__(self):
        
        super().__init__()
        self.setWindowTitle("Matrix Loader")
        self.setGeometry(100, 100, 400, 200)

        # Central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # Label to show the selected file
        self.file_label = QLabel("No file selected")
        self.file_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.file_label)

        # Button to open file dialog
        self.load_button = QPushButton("Select File")
        self.load_button.clicked.connect(self.open_file_dialog)
        layout.addWidget(self.load_button)

    def open_file_dialog(self):
        # Open a file dialog to select files with a specific extension (e.g., .txt)
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open File", "", "Text Files (*.txt);;All Files (*)"
        )

        if file_path:
            self.file_label.setText(f"Selected: {file_path}")
            matrix = self.load_matrix(file_path)
            print("Loaded Matrix:")
            for row in matrix:
                print(row)

    def load_matrix(self, file_path):
        # Reads the file and converts it into a matrix (list of lists)
        matrix = []
        try:
            with open(file_path, "r") as file:
                for line in file:
                    # Split the line into integers and add to the matrix
                    row = [int(num) for num in line.split()]
                    matrix.append(row)
        except Exception as e:
            print(f"Error reading file: {e}")
        return matrix


# Run the application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MatrixLoaderApp()
    window.show()
    sys.exit(app.exec_())
