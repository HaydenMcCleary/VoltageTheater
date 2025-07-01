from src.components.components import Component

class Resistor(Component):
    def __init__(self, resisotr_path):
        super().__init__(resisotr_path, terminals=[(12, 10), (48, 10)])