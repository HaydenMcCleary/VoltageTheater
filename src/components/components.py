
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout,
    QGraphicsView, QGraphicsScene, QGraphicsPixmapItem,
    QGraphicsEllipseItem, QGraphicsPathItem, QGraphicsItem, QLabel
)
from PyQt5.QtGui import QPixmap, QPainter, QPen, QColor, QPainterPath
from PyQt5.QtCore import Qt, QPointF, QRectF, QLineF

from src.gui.circuit import Terminal
        
class Component(QGraphicsPixmapItem):
    def __init__(self, image_path, terminals, target_size=(60, 60)):
        super().__init__()
        # load image of component 
        pixmap = QPixmap(image_path)
        if pixmap.isNull():
            raise FileNotFoundError(f"Could not load image: {image_path}")
        # resize component so each they can fit in the screen
        scaled_pixmap = pixmap.scaled(
            target_size[0], target_size[1],
            Qt.KeepAspectRatio, Qt.SmoothTransformation
        )
        self.setPixmap(scaled_pixmap)
        # actions the component can take 
        self.setFlags(
            QGraphicsItem.ItemIsMovable |
            QGraphicsItem.ItemIsSelectable |
            QGraphicsItem.ItemIsFocusable |
            QGraphicsItem.ItemSendsGeometryChanges
        )
        # get nodes 
        self.terminals = []
        for rel_x, rel_y in terminals:
            term = Terminal(rel_x, rel_y, parent=self)
            self.terminals.append(term)

    # call back to update the wire trace if the user moves or rotates it
    def itemChange(self, change, value):
        if change in (QGraphicsItem.ItemPositionChange, QGraphicsItem.ItemTransformChange):
            for term in self.terminals:
                for wire in term.connected_wires:
                    wire.update_position()
        return super().itemChange(change, value)