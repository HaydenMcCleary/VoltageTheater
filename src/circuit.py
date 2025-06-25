# nodes for parent component 



from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout,
    QGraphicsView, QGraphicsScene, QGraphicsPixmapItem,
    QGraphicsEllipseItem, QGraphicsPathItem, QGraphicsItem, QLabel
)
from PyQt5.QtGui import QPixmap, QPainter, QPen, QColor, QPainterPath
from PyQt5.QtCore import Qt, QPointF, QRectF, QLineF


class Terminal(QGraphicsEllipseItem):
    def __init__(self, x, y, parent=None):
        super().__init__(-4, -4, 8, 8)
        self.setBrush(QColor("red"))
        self.setZValue(1)
        self.setParentItem(parent)
        self.setPos(x, y)
        self.setFlags(QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemIsFocusable)
        self.connected_wires = []

    def sceneTerminalPos(self):
        return self.mapToScene(QPointF(0, 0))
    
    # selection criteria for wiring 
    def mousePressEvent(self, event):
        modifiers = QApplication.keyboardModifiers()
        if modifiers == Qt.ShiftModifier:
            self.setSelected(not self.isSelected())
        else:
            self.scene().clearSelection()
