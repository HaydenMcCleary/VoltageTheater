
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout,
    QGraphicsView, QGraphicsScene, QGraphicsPixmapItem,
    QGraphicsEllipseItem, QGraphicsPathItem, QGraphicsItem, QLabel
)
from PyQt5.QtGui import QPixmap, QPainter, QPen, QColor, QPainterPath
from PyQt5.QtCore import Qt, QPointF, QRectF, QLineF


# nodes for parent component 
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
            

# draws path between two nodes 
class CustomWire(QGraphicsPathItem):
    def __init__(self, terminal1, terminal2):
        super().__init__()
        self.terminal1 = terminal1
        self.terminal2 = terminal2
        self.setZValue(-1)
        self.setPen(QPen(QColor("red"), 2))

        # Add self to terminal's connected wires
        terminal1.connected_wires.append(self)
        terminal2.connected_wires.append(self)

    def addedToScene(self):
        # This is manually called after being added to the scene
        self.update_position()

    def update_position(self):
        p1 = self.terminal1.sceneTerminalPos()
        p2 = self.terminal2.sceneTerminalPos()

        scene = self.scene()
        if scene is None:
            return

        # Bounding boxes for all components except the ones being connected
        def padded_rect(item, pad=10):
            rect = item.mapToScene(item.boundingRect()).boundingRect()
            return QRectF(rect.x() - pad, rect.y() - pad, rect.width() + 2*pad, rect.height() + 2*pad)

        obstacles = [
            padded_rect(item)
            for item in scene.items()
            if isinstance(item, Component) and item not in (self.terminal1.parentItem(), self.terminal2.parentItem())
        ]

        def intersects_any(rects, line):
            return any(rect.intersects(QRectF(line.p1(), line.p2())) for rect in rects)

        path = QPainterPath()
        path.moveTo(p1)

        # Try L-paths and Z-paths in priority order
        options = [
            [p1, QPointF(p2.x(), p1.y()), p2],  # horizontal → vertical
            [p1, QPointF(p1.x(), p2.y()), p2],  # vertical → horizontal
            [p1, QPointF((p1.x()+p2.x())/2, p1.y()), QPointF((p1.x()+p2.x())/2, p2.y()), p2],  # Z path
        ]

        for points in options:
            lines = [QLineF(points[i], points[i+1]) for i in range(len(points)-1)]
            if not any(intersects_any(obstacles, line) for line in lines):
                for pt in points[1:]:
                    path.lineTo(pt)
                self.setPath(path)
                return

        # Fallback: single bend if no clear path
        path.lineTo(p2)
        self.setPath(path)


        
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


class Resistor(Component):
    def __init__(self):
        super().__init__("images/resistor.png", terminals=[(12, 10), (48, 10)])


class VoltageSource(Component):
    def __init__(self):
        super().__init__("images/voltage.png", terminals=[(26, 0), (26, 60)])