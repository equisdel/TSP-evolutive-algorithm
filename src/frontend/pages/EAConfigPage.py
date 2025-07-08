from PySide6.QtWidgets import (
    QApplication, QMainWindow, QSplitter, QVBoxLayout, QHBoxLayout,
    QFrame, QScrollArea, QGroupBox, QPushButton, QLabel, QLineEdit,
    QComboBox, QSpinBox, QCheckBox, QSlider, QWidget
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QIntValidator, QDoubleValidator
from frontend.Footer import Footer
from backend.Configuration import Configuration
from frontend.pages.InstancesPage import InstancesPage

class EAConfigPage(QMainWindow):
    
    next_button_pushed = Signal(str)     # emits when a file is selected
    back_button_pushed = Signal(str)

    def set_next_button_pushed(self):
        self.collect_inputs()
        print()
        print(self.config.display_json_config())
        self.next_button_pushed.emit("")

    def set_back_button_pushed(self):
        self.back_button_pushed.emit("")

    def __init__(self,main):
        self.main = main
        main.instance_created.connect(self.create_configuration)
        super().__init__()

    def create_configuration(self, instance):
        self.config = Configuration(instance.get_dimension())    
        self.json_config = self.config.get_json_config()    # this is what should load by default

    def showEvent(self, event):

        self.layout = QVBoxLayout()
        self.setGeometry(200, 200, 1000, 700)
        main_splitter = QSplitter(Qt.Horizontal)
        self.right_panel = self.create_right_panel()
        # method to load default_config into the section on the right
        main_splitter.addWidget(self.right_panel)
        main_splitter.setStretchFactor(0, 1)  # 1/3 of the width

        self.left_panel = self.create_vertical_tabs(self.json_config)
        main_splitter.addWidget(self.left_panel)
        main_splitter.setStretchFactor(1, 2)  # 2/3 of the width

        self.layout.addWidget(main_splitter)


        self.footer = Footer(True)
        #self.file_was_selected.connect(self.footer.enable_next)
        self.footer.next_button.clicked.connect(self.set_next_button_pushed)
        self.footer.back_button.clicked.connect(self.set_back_button_pushed)
        self.layout.addWidget(self.footer, stretch=0)
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
        for section_name in json_config:
            
            print(section_name)
            group_box = QGroupBox()

            group_layout = QVBoxLayout()
            label = QLabel(f"{section_name.upper()}")
            label.setStyleSheet("font-weight: 800;")
            group_layout.addWidget(label)
            internal_dict = json_config[section_name]
            for parameter in internal_dict:
                print(parameter)
                row_layout = QHBoxLayout()
                label = QLabel(parameter)
                row_layout.addWidget(label)
                param = internal_dict[parameter]
                input = self.get_qt_input(param)
                input.setObjectName(section_name+" : "+parameter)
                row_layout.addWidget(input)
                group_layout.addLayout(row_layout)
            group_box.setLayout(group_layout)

            tab_layout.addWidget(group_box)

        tab_content.setLayout(tab_layout)
        scroll_area.setWidget(tab_content)

        # Add Scroll Area to Left Layout
        left_layout.addWidget(scroll_area)
        left_frame.setLayout(left_layout)
        return left_frame

    def get_qt_input(self,parameter):
        p_type = parameter.get_type()
        p_range = parameter.get_range()
        if (p_type == "int" or p_type == "float" or p_type == "prob"):
            input = QLineEdit()
            input.setFixedWidth(300)               # Set width of the text box
            input.setAlignment(Qt.AlignmentFlag.AlignLeft) 
            input.setText(str(parameter.get_value()))
            if p_type == "int":
                input.setValidator(QIntValidator(p_range[0],p_range[1]))
            elif p_type == "float" or p_type == "prob":
                input.setValidator(QDoubleValidator(float(p_range[0]),float(p_range[1]),10)) 
        elif (p_type == "bool"):
            input = QCheckBox()
        elif (p_type == "array"):
            input = QComboBox()
            input.setFixedWidth(300)
            input.setFixedHeight(24)               # Set width of the text box
            input.setStyleSheet("background-color: rgba(80,80,80,80);")
            input.addItems(p_range)
            input.setCurrentIndex(parameter.get_index())
        return input
        
    def collect_inputs(self):
        inputs = {}

        for line in self.findChildren(QLineEdit):
            if line.isModified():
                name = line.objectName()
                print(name.split(" : "))
                section_name, param_name = name.split(" : ")
                self.config.update_parameter(section_name,param_name,line.text())
                inputs[line.objectName()] = line.text()

        # Get QCheckBox values
        for checkbox in self.findChildren(QCheckBox):
            name = checkbox.objectName()
            print(name.split(" : "))
            section_name, param_name = name.split(" : ")
            self.config.update_parameter(section_name,param_name,checkbox.isChecked())
            inputs[checkbox.objectName()] = checkbox.isChecked()

        # Get QComboBox values
        for combo in self.findChildren(QComboBox):
            if (len(combo.objectName().split())>1):
                print(len(combo.objectName().split())>1)
                name = combo.objectName()
                print(name.split(" : "))
                section_name, param_name = name.split(" : ")
                print("xxxx",combo.currentIndex())
                self.config.update_parameter(section_name,param_name,combo.currentIndex())
                #inputs[combo.objectName()] = combo.currentText()

        print("Collected inputs:", inputs)


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


if __name__ == "__main__":
    app = QApplication([])
    window = EAConfigPage()
    window.show()
    app.exec()
