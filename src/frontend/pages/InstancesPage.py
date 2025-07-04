from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QGridLayout, QGraphicsOpacityEffect, QFileDialog, QTextEdit, QPlainTextEdit,  QComboBox, QLabel, QListWidget, QMessageBox
from PySide6.QtGui import QTextOption 
from PySide6.QtCore import Signal  # ✅ Works with the rest of your imports
from frontend.Footer import Footer
from backend.TSPInstance import TSPInstanceParser

class InstancesPage(QWidget):

    file_was_selected = Signal(str)     # emits when a file is selected
    next_button_pushed = Signal(str)     # emits when a file is selected
    
    def __init__(self,db):
        
        super().__init__()

        self.db = db
        full_layout = QVBoxLayout()
        full_layout.setSpacing(10)
        # Create a grid layout
        layout = QGridLayout()
        layout.setSpacing(10)  # Optional: spacing between sections

        # Create four sections with different background colors
        left_top = self.create_colored_widget("red")
        left_bottom = self.create_colored_widget("blue")
        right_top = self.create_colored_widget("green")
        right_bottom = self.create_colored_widget("yellow")

        # left_top
        layout_left_top = QVBoxLayout(left_top)
        title = QTextEdit()
        title.setReadOnly(True)
        title.setPlainText("Choose a valid TSP instance file!")
        title.setStyleSheet("""
            background-color: rgba(0,0,0,0);
            font-size: 30px;
            font-weight: bold;
            font-family: Arial, sans-serif;
        """)

        requirements_label = QLabel()
        #requirements_label.setTextInteractionFlags(requirements_label.textInteractionFlags() | Qt.TextInteractionFlag.TextSelectableByMouse)
        requirements_label.setText("""
        <h3> Requirements for a Valid <code>.atsp</code> File:</h3>
        <ul>
            <li><b>Header Section</b>: Must start with a <code>NAME</code> field specifying the instance name (e.g., <code>NAME: atsp_example</code>).</li>
            <li><b>Problem Type</b>: Must specify <code>TYPE: ATSP</code>.</li>
            <li><b>Dimension Definition</b>: Must include the <code>DIMENSION</code> field (e.g., <code>DIMENSION: 5</code>).</li>
            <li><b>Edge Weight Type</b>: Must specify <code>EDGE_WEIGHT_TYPE: EXPLICIT</code>.</li>
            <li><b>Edge Weight Format</b>: Must define the format using <code>EDGE_WEIGHT_FORMAT</code> (e.g., <code>FULL_MATRIX</code>).</li>
            <li><b>Edge Weight Section</b>: Provide a matrix of weights in the <code>EDGE_WEIGHT_SECTION</code>, with costs between nodes.</li>
            <li><b>Asymmetry</b>: Costs from node <i>i</i> to <i>j</i> can differ from <i>j</i> to <i>i</i>.</li>
            <li><b>Non-Negativity</b>: Weights must be non-negative integers (e.g., self-loops have weight 0).</li>
            <li><b>File Termination</b>: The file must end with <code>EOF</code>.</li>
        </ul>
        """)
        requirements_label.setStyleSheet("""
            color: rgba(50,50,50,255);
            padding: 10px;
            background-color: rgba(0,0,0,0);
            font-size: 10px;
            font-style: normal;
            font-family: Arial, sans-serif;
        """)
        requirements_label.setWordWrap(False)  # Allow text wrapping

        layout_left_top.addWidget(title,stretch=1)
        layout_left_top.addWidget(requirements_label,stretch=10)

        # left_bottom
        layout_left_bottom = QVBoxLayout(left_bottom)

        self.load_button = QPushButton("Upload instance file")
        self.load_button.setStyleSheet("font-size: 12px;")
        self.load_button.clicked.connect(self.load_file)
        
        self.selection_layout = QHBoxLayout(left_bottom)
        self.label = QLabel("Select an item:")
        self.label.setStyleSheet("background-color: rgba(0,0,0,0);")
        self.selection_layout.addWidget(self.label)
        self.selection_layout.addWidget(self.load_button)
        layout_left_bottom.addLayout(self.selection_layout)
        self.list_widget = QListWidget()
        self.populate_list()
        self.list_widget.itemClicked.connect(self.on_item_selected)
        layout_left_bottom.addWidget(self.list_widget)
        #self.setLayout(layout)

        # right_top

        # right_bottom
        layout_right_bottom = QVBoxLayout(right_bottom)
        self.text_viewer = QPlainTextEdit()
        self.text_viewer.setWordWrapMode(QTextOption.NoWrap)
        self.text_viewer.setReadOnly(True)
        layout_right_bottom.addWidget(self.text_viewer)


        # Add widgets to the grid layout
        layout.addWidget(left_top, 0, 0)    # Top-left
        layout.addWidget(left_bottom, 1, 0) # Bottom-left
        layout.addWidget(right_top, 0, 1)   # Top-right
        layout.addWidget(right_bottom, 1, 1) # Bottom-right

        # Set column and row stretch to define proportions
        layout.setColumnStretch(0, 5)  # Left sections take 2/3 of the width
        layout.setColumnStretch(1, 3)  # Right sections take 1/3 of the width
        layout.setRowStretch(0, 3)     # Top sections take equal height
        layout.setRowStretch(1, 5)     # Bottom sections take equal height

        # Set the layout for the widget
    
        full_layout.addLayout(layout, stretch=1)
        self.footer = Footer(print,print)
        self.file_was_selected.connect(self.footer.enable_next)
        full_layout.addWidget(self.footer, stretch=0)
        self.setLayout(full_layout)


    def get_instance(self):
        return self.instance


    def create_colored_widget(self, color):
        # Create a widget with a specific background color
        widget = QWidget()
        #color = "rgba(25, 25, 25, 128)"
        color = "rgba(25, 25, 25, 25)"
        widget.setStyleSheet(f"""
            background-color: {color};
            border-radius: 5px;  /* Adjust the radius to change roundness */
            border: 0.1px solid white;  /* Optional: Add a border for emphasis */
        """)
        return widget

    def populate_list(self):
    
        self.list_widget.clear()
        self.list_widget.addItems(self.db.get_all_instances())

    def on_item_selected(self, item):
        # Get the selected item's text
        selected_item = item.text()
        self.label.setText(f"Selected: {selected_item}")
        self.set_instance_file_path("./data/instances/"+selected_item)
        self.display_file("./data/instances/"+selected_item)

    def set_instance_file_path(self, file_path):
        self.file_path = file_path
        if file_path is not None:
            self.file_was_selected.emit(file_path)

    def load_file(self):
        import os
        import shutil
        
        self.file_path, _ = QFileDialog.getOpenFileName(self, "Abrir Archivo de Texto", "", "Archivos de Texto (*.atsp)")
        if self.file_path:
            # Define the target directory
            target_directory = "./data/instances"
            os.makedirs(target_directory, exist_ok=True)  # Ensure the directory exists
            
            # Define the target file path
            target_file_path = os.path.join(target_directory, os.path.basename(self.file_path))
            
            # If the file doesn't exist in the target directory, copy it there
            if not os.path.exists(target_file_path):
                shutil.copy(self.file_path, target_file_path)
                QMessageBox.information(self, "Archivo Copiado", f"El archivo ha sido copiado a: {target_file_path}")
            else:
                QMessageBox.warning(self, "Archivo Existente", "El archivo ya existe en la carpeta de destino.")
            self.populate_list()
            self.display_file("./data/instances/"+self.file_path)
        else:
            print("error")
    
    def display_file(self, file_path):
        try:
            # Cargar contenido del archivo
            print(file_path)
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
                self.text_viewer.setPlainText(content)
        except Exception as e:
            self.text_viewer.setPlainText(f"Error al cargar el archivo: {e}")


        






"""
class InstancesPage(QWidget):

    def __init__(self,all_instances):

        super().__init__()
        
        # Layout setup
        self.matrix_layout = QVBoxLayout(self)  # vertical layout
        self.matrix_table = QTableWidget(self)
        self.matrix_layout.addWidget(self)
        

        # Connect the start button signal to the provided callback
        #self.start_button.clicked.connect(on_start_button_click)


    def load_tsp_instances(self):
        # fetches from the database
        file_name, _ = QFileDialog.getOpenFileName(
            self, 
            "Open TSP Instance File",
            "C:/Users/Delfina/Downloads/Evolutiva/Material/Instancias TSP",
            "Text Files (*.atsp);;All Files (*)"
        )

        if file_name:
            print(f"Selected file: {file_name}")
            instance = TSPInstanceParser.parse(file_name)
            if instance:
                print(instance.matrix)
                self.display_matrix(instance)
                self.stacked_widget.setCurrentWidget(self.matrix_page)  # Switch to the Matrix page
            else:
                print("Failed to parse TSP instance.")
        else:
            print("No file selected.")

    def display_matrix(self, instance: TSPInstance):
        # Display the matrix in a QTableWidget
        matrix = instance.matrix
        dimension = instance.dimension

        self.matrix_table.setRowCount(dimension)
        self.matrix_table.setColumnCount(dimension)

        for i in range(dimension):
            for j in range(dimension):
                self.matrix_table.setItem(i, j, QTableWidgetItem(str(matrix[i][j])))
    """