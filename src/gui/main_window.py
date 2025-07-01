import sys
import os

from src.gui.circuit import Terminal
from src.components.components import Component
from src.components.dc_voltage_source import dc_voltage_sorce
from src.components.resisitor import Resistor
from src.components.wire import Wire
from src.gui.circuit_builder import CircuitBuilder

from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout,
    QGraphicsView, QGraphicsScene, QGraphicsPixmapItem,
    QGraphicsEllipseItem, QGraphicsPathItem, QGraphicsItem, QLabel
)
from PyQt5.QtGui import QPixmap, QPainter, QPen, QColor, QPainterPath
from PyQt5.QtCore import Qt, QPointF



class MainWindow(QWidget):
    def __init__(self, cfg):
        super().__init__()

        self.cfg = cfg

        self.setWindowTitle("Circuit Builder")
        self.setGeometry(100, 100, 900, 600)

        main_layout = QVBoxLayout()
        self.status_label = QLabel("Circuit Status: Open")
        self.status_label.setStyleSheet("font-size: 16px; color: red;")
        main_layout.addWidget(self.status_label)

        content_layout = QHBoxLayout()

        self.scene = QGraphicsScene() 
        self.scene.setSceneRect(0, 0, 700, 600)

        self.view = CircuitBuilder(self.scene, self.status_label)
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
        resistor = Resistor(self.cfg["paths"]["symbols"]["resistor"])
        resistor.setPos(100, 150)
        self.scene.addItem(resistor)

    def add_voltage_source(self):
        vs = dc_voltage_sorce(self.cfg["paths"]["symbols"]["dc_volt_src"])
        vs.setPos(300, 150)
        self.scene.addItem(vs)
