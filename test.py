import sys
import os

from src.circuit import Terminal
from components.components import Component
from components.dc_voltage_source import dc_voltage_sorce
from components.resisitor import Resistor
from components.wire import Wire

from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout,
    QGraphicsView, QGraphicsScene, QGraphicsPixmapItem,
    QGraphicsEllipseItem, QGraphicsPathItem, QGraphicsItem, QLabel
)
from PyQt5.QtGui import QPixmap, QPainter, QPen, QColor, QPainterPath
from PyQt5.QtCore import Qt, QPointF

class CustomGraphicsView(QGraphicsView):
    # sets up the GUI 
    def __init__(self, scene, status_label):
        super().__init__(scene)
        self.setRenderHint(QPainter.Antialiasing)
        self.setStyleSheet("background-color: white;")
        self.status_label = status_label

    # takes input from user to perform action on circuit
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_W:
            self.connect_terminals()
        elif event.key() == Qt.Key_R:
            self.rotate_selected_components()
        else:
            super().keyPressEvent(event)

    # creates a wire between two selected nodes
    def connect_terminals(self):
        terminals = [item for item in self.scene().selectedItems() if isinstance(item, Terminal)]
        if len(terminals) != 2:
            print("Select exactly 2 terminals (Shift+Click).")
            return
        wire = Wire(terminals[0], terminals[1])
        self.scene().addItem(wire)
        wire.addedToScene()  # <- call after adding to scene
        self.update_circuit_status()

    # rotates component 90 degrees, redrawing wires 
    def rotate_selected_components(self):
        for item in self.scene().selectedItems():
            if isinstance(item, Component):
                item.setRotation(item.rotation() + 90)
                for term in item.terminals:
                    for wire in term.connected_wires:
                        wire.update_position()

    # check if there is an open circuit, using depth first search 
    def update_circuit_status(self):
        all_terminals = [item for item in self.scene().items() if isinstance(item, Terminal)]
        visited = set()

        def dfs(t):
            if t in visited:
                return
            visited.add(t)
            for wire in t.connected_wires:
                other = wire.terminal1 if wire.terminal2 == t else wire.terminal2
                dfs(other)

        if all_terminals:
            dfs(all_terminals[0])

        if len(visited) == len(all_terminals):
            self.status_label.setText("Circuit Status: Closed")
            self.status_label.setStyleSheet("color: green;")
        else:
            self.status_label.setText("Circuit Status: Open")
            self.status_label.setStyleSheet("color: red;")


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Circuit Builder")
        self.setGeometry(100, 100, 900, 600)

        main_layout = QVBoxLayout()
        self.status_label = QLabel("Circuit Status: Open")
        self.status_label.setStyleSheet("font-size: 16px; color: red;")
        main_layout.addWidget(self.status_label)

        content_layout = QHBoxLayout()

        self.scene = QGraphicsScene() 
        self.scene.setSceneRect(0, 0, 700, 600)

        self.view = CustomGraphicsView(self.scene, self.status_label)
        self.view.setDragMode(QGraphicsView.RubberBandDrag)
        content_layout.addWidget(self.view, 3)

        button_layout = QVBoxLayout()
        add_resistor_button = QPushButton("Add Resistor")
        add_voltage_button = QPushButton("Add Voltage Source")

        add_resistor_button.clicked.connect(self.add_resistor)
        add_voltage_button.clicked.connect(self.add_voltage_source)

        button_layout.addWidget(add_resistor_button)
        button_layout.addWidget(add_voltage_button)
        button_layout.addStretch()

        content_layout.addLayout(button_layout, 1)
        main_layout.addLayout(content_layout)
        self.setLayout(main_layout)

    def add_resistor(self):
        resistor = Resistor()
        resistor.setPos(100, 150)
        self.scene.addItem(resistor)

    def add_voltage_source(self):
        vs = dc_voltage_sorce()
        vs.setPos(300, 150)
        self.scene.addItem(vs)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
