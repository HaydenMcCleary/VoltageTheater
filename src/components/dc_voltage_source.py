from components.components import Component

class dc_voltage_sorce(Component):
    def __init__(self):
        super().__init__("images/voltage.png", terminals=[(26, 0), (26, 60)])