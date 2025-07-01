import sys
import os

from src.gui.circuit import Terminal
from src.components.components import Component
from src.components.dc_voltage_source import dc_voltage_sorce
from src.components.resisitor import Resistor
from src.components.wire import Wire

from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout,
    QGraphicsView, QGraphicsScene, QGraphicsPixmapItem,
    QGraphicsEllipseItem, QGraphicsPathItem, QGraphicsItem, QLabel
)
from PyQt5.QtGui import QPixmap, QPainter, QPen, QColor, QPainterPath
from PyQt5.QtCore import Qt, QPointF

class CircuitBuilder(QGraphicsView):
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

    # rotates component 90 degrees, redrawing wires 
    def rotate_selected_components(self):
        for item in self.scene().selectedItems():
            if isinstance(item, Component):
                item.setRotation(item.rotation() + 90)
                for term in item.terminals:
                    for wire in term.connected_wires:
                        wire.update_position()

