import json
import sympy as sp

def parse_resistance(value_str):
    value_str = value_str.lower().replace(" ", "")
    if value_str.endswith("k"):
        return float(value_str[:-1]) * 1e3
    elif value_str.endswith("m"):
        return float(value_str[:-1]) * 1e6
    else:
        return float(value_str)

def format_expr(expr):
    """Format sympy Eq expression to decimal strings with no scientific notation."""
    if isinstance(expr, sp.Equality):
        lhs = expr.lhs.evalf()
        rhs = expr.rhs.evalf()
    else:
        lhs = expr.evalf()
        rhs = 0.0

    def fmt(val):
        return f"{val:.8f}" if isinstance(val, (float, int, sp.Float)) else str(val)

    return f"{fmt(lhs)} = {fmt(rhs)}"

def generate_equations(circuit_name, data):
    print(f"\n=== {circuit_name.upper()} ===")

    # Symbolic voltage variables
    voltage_vars = {}
    for node, props in data["nodes"].items():
        if props["voltage_at_node"] == 0:
            voltage_vars[node] = 0  # Ground node
        else:
            voltage_vars[node] = sp.Symbol(f"V_{node}")

    # Gather all KCL terms per node (exclude ground)
    kcl = {node: 0 for node in voltage_vars if voltage_vars[node] != 0}
    kvl = []

    for comp in data["components"]:
        if comp["type"] == "resistor":
            n1, n2 = comp["from"], comp["to"]
            R = parse_resistance(comp["value"])
            I = (voltage_vars[n1] - voltage_vars[n2]) / R
            if n1 in kcl:
                kcl[n1] += I
            if n2 in kcl:
                kcl[n2] -= I

        elif comp["type"] == "dc_voltage_source":
            V = comp["voltage"]
            pos, neg = comp["positive"], comp["negative"]
            expr = voltage_vars[pos] - voltage_vars[neg] - V
            kvl.append(expr)

    # Print KVL equations
    print("\n--- KVL Equations (Voltage Sources) ---")
    for eq in kvl:
        print(format_expr(sp.Eq(eq, 0)))

    # Print KCL equations
    print("\n--- KCL Equations (Node Currents) ---")
    for node, expr in kcl.items():
        print(format_expr(sp.Eq(expr, 0)))

# --- Load and run ---
if __name__ == "__main__":
    test_circuits = {
        "test_1_loop": {
            "nodes": {
                "n0": { "voltage_at_node": 0 },
                "n1": { "voltage_at_node": "unknown" }
            },
            "components": [
                {
                    "type": "dc_voltage_source",
                    "voltage": 10,
                    "positive": "n1",
                    "negative": "n0"
                },
                {
                    "type": "resistor",
                    "value": "100k",
                    "from": "n1",
                    "to": "n0"
                }
            ],
            "expected_status": "closed"
        },

        "test_2_loop": {
            "nodes": {
                "n0": { "voltage_at_node": 0 },
                "n1": { "voltage_at_node": "unknown" },
                "n2": { "voltage_at_node": "unknown" },
                "n3": { "voltage_at_node": "unknown" }
            },
            "components": [
                {
                    "type": "dc_voltage_source",
                    "voltage": 10,
                    "positive": "n1",
                    "negative": "n0"
                },
                {
                    "type": "resistor",
                    "value": "100k",
                    "from": "n1",
                    "to": "n2"
                },
                {
                    "type": "resistor",
                    "value": "100k",
                    "from": "n2",
                    "to": "n0"
                },
                {
                    "type": "resistor",
                    "value": "100k",
                    "from": "n1",
                    "to": "n3"
                },
                {
                    "type": "resistor",
                    "value": "100k",
                    "from": "n3",
                    "to": "n0"
                }
            ],
            "expected_status": "closed"
        }
    }

    for name, circuit in test_circuits.items():
        generate_equations(name, circuit)
