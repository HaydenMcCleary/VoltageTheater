from components.components import Component

class Resistor(Component):
    def __init__(self):
        super().__init__("images/resistor.png", terminals=[(12, 10), (48, 10)])
