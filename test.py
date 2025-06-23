import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel
)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt Right-Aligned Buttons")
        self.setGeometry(100, 100, 400, 300)

        # Main layout (horizontal: content left, buttons right)
        main_layout = QHBoxLayout()

        # Left side: placeholder content
        content_label = QLabel("Main Content Area")
        content_label.setStyleSheet("font-size: 18px;")
        main_layout.addWidget(content_label, 1)  # stretch factor 1

        # Right side: vertical button layout
        button_layout = QVBoxLayout()

        # Add some buttons
        button1 = QPushButton("Button 1")
        button2 = QPushButton("Button 2")
        button3 = QPushButton("Button 3")

        # Add buttons to the layout
        button_layout.addWidget(button1)
        button_layout.addWidget(button2)
        button_layout.addWidget(button3)
        button_layout.addStretch()  # pushes buttons to the top

        # Add the button layout to the main layout
        main_layout.addLayout(button_layout)

        # Set the layout on the main window
        self.setLayout(main_layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
