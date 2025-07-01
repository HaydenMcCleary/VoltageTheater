from src.components.components import Component

class dc_voltage_sorce(Component):
    def __init__(self, dc_voltage_symbol_path):
        super().__init__(dc_voltage_symbol_path, terminals=[(26, 0), (26, 60)])