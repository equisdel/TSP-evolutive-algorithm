from PySide6.QtWidgets import (
    QApplication, QMainWindow, QSplitter, QVBoxLayout, QHBoxLayout,
    QFrame, QScrollArea, QGroupBox, QPushButton, QLabel, QLineEdit,
    QComboBox, QSpinBox, QCheckBox, QSlider, QWidget
)
from PySide6.QtCore import Qt
from frontend.Footer import Footer
from backend.Configuration import Configuration
from frontend.pages.InstancesPage import InstancesPage

class EAPage(QMainWindow):
    
    def __init__(self):
   
        super().__init__()

    def showEvent(self, event):
        config = Configuration(self.instance.get_dimension())    
        json_config = config.get_json_config()    # this is what should load by default
        
        self.layout = QVBoxLayout()
        self.setGeometry(200, 200, 1000, 700)
        main_splitter = QSplitter(Qt.Horizontal)
        self.right_panel = self.create_right_panel()
        # method to load default_config into the section on the right
        main_splitter.addWidget(self.right_panel)
        main_splitter.setStretchFactor(0, 1)  # 1/3 of the width



        self.left_panel = self.create_vertical_tabs(json_config)
        main_splitter.addWidget(self.left_panel)
        main_splitter.setStretchFactor(1, 2)  # 2/3 of the width

        self.layout.addWidget(main_splitter)
        self.layout.addWidget(Footer(print, print))  # sin stretch

        central_widget = QWidget()
        central_widget.setLayout(self.layout)
        self.setCentralWidget(central_widget)
        return super().showEvent(event)

    def create_vertical_tabs(self, json_config):

        left_frame = QFrame()
        left_layout = QVBoxLayout()

        # Scroll Area for Tabs
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        # Content for Scroll Area
        tab_content = QWidget()
        tab_layout = QVBoxLayout()

        # Add Sections as Expandable Tabs
        for section_name in list(json_config.keys()):
            
            print(section_name)
            group_box = QGroupBox()

            group_layout = QVBoxLayout()
            label = QLabel(f"{section_name.upper()}")
            label.setStyleSheet("font-weight: 800;")
            group_layout.addWidget(label)
            for parameter in (json_config[section_name]):
                # parameter should tell its type and valid range (come with QtValidator?)
                group_layout.addWidget(QLineEdit(parameter))
            group_box.setLayout(group_layout)

            tab_layout.addWidget(group_box)

        tab_content.setLayout(tab_layout)
        scroll_area.setWidget(tab_content)

        # Add Scroll Area to Left Layout
        left_layout.addWidget(scroll_area)
        left_frame.setLayout(left_layout)
        return left_frame

    def create_right_panel(self):
        right_frame = QFrame()
        right_layout = QVBoxLayout()

        # Database Access Section
        db_label = QLabel("Load Previous Configurations:")
        db_combo = QComboBox()
        db_combo.addItems(["Config 1", "Config 2", "Config 3"])  # Example options
        load_button = QPushButton("Load Configuration")
        db_layout = QHBoxLayout()
        db_layout.addWidget(db_combo)
        db_layout.addWidget(load_button)

        # Action Buttons
        button_layout = QHBoxLayout()
        reset_button = QPushButton("Reset to Default")
        save_button = QPushButton("Save Configuration")
        button_layout.addWidget(reset_button)
        button_layout.addWidget(save_button)

        # Add to Right Layout
        right_layout.addWidget(db_label)
        right_layout.addLayout(db_layout)
        right_layout.addStretch()  # Spacer for layout alignment
        right_layout.addLayout(button_layout)
        right_frame.setLayout(right_layout)

        return right_frame

    def load_configuration(self):
        
        instance = self.instancePage.get_instance()
        print("I am in EAPage and the following should be instance: ",instance)

if __name__ == "__main__":
    app = QApplication([])
    window = EAPage()
    window.show()
    app.exec()
