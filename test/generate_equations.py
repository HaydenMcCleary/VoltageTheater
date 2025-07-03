import json
import sympy as sp
from collections import defaultdict
from itertools import count

# ---------------------
# Utility Functions
# ---------------------
def format_expr(expr):
    def fmt(val):
        return f"{val:.8f}" if isinstance(val, (float, int, sp.Float)) else str(val)
    if isinstance(expr, sp.Equality):
        return f"{fmt(expr.lhs)} = {fmt(expr.rhs)}"
    else:
        return str(expr)

# ---------------------
# Core Equation Generator
# ---------------------
def generate_equations(name, circuit):
    if not circuit or "nodes" not in circuit or "components" not in circuit:
        print(f"\n=== {name.upper()} ===")
        print("Invalid or empty circuit data. Skipping.\n")
        return

    print(f"\n=== {name.upper()} ===")

    current_gen = count(1)
    current_vars = {}
    node_voltages = {n: sp.Symbol(f"V_{n}") for n in circuit["nodes"]}
    zero_ref_node = next((n for n, data in circuit["nodes"].items() if data.get("voltage_at_node") == 0), None)
    if zero_ref_node is not None:
        node_voltages[zero_ref_node] = 0

    components = circuit["components"]

    # Build a graph of nodes and assign currents
    graph = defaultdict(list)
    branch_labels = {}

    for comp in components:
        if not comp or not isinstance(comp, dict):
            continue
        comp_type = comp.get("type")
        n1 = comp.get("from") or comp.get("positive")
        n2 = comp.get("to") or comp.get("negative")
        if n1 is None or n2 is None:
            continue
        key = tuple(sorted((n1, n2)))
        if comp_type in ("resistor", "dc_voltage_source"):
            if key not in current_vars:
                current_vars[key] = sp.Symbol(f"I_{next(current_gen)}")
            branch_labels[(n1, n2)] = comp
            graph[n1].append(n2)
            graph[n2].append(n1)

    # Generate KVL by detecting unique loops using DFS
    def find_loops():
        loops = []
        visited_paths = set()

        def dfs(path, visited_edges):
            current = path[-1]
            for neighbor in graph[current]:
                edge = tuple(sorted((current, neighbor)))
                if edge in visited_edges:
                    continue
                if neighbor in path:
                    loop_start = path.index(neighbor)
                    loop = path[loop_start:] + [neighbor]
                    loop_key = tuple(sorted(set(zip(loop, loop[1:]))))
                    if loop_key not in visited_paths:
                        visited_paths.add(loop_key)
                        loops.append(loop)
                    continue
                dfs(path + [neighbor], visited_edges | {edge})

        for node in graph:
            dfs([node], set())

        return loops

    print("\nKVL:")
    any_kvl_printed = False
    for loop in find_loops():
        expr = 0
        for i in range(len(loop) - 1):
            n1 = loop[i]
            n2 = loop[i + 1]
            comp = branch_labels.get((n1, n2)) or branch_labels.get((n2, n1))
            if not comp or not isinstance(comp, dict):
                continue
            direction = 1 if (n1, n2) in branch_labels else -1
            key = tuple(sorted((n1, n2)))
            if comp.get("type") == "resistor":
                R = float(str(comp.get("value", "0")).replace("k", "e3"))
                expr += direction * R * current_vars.get(key, 0)
            elif comp.get("type") == "dc_voltage_source":
                V = comp.get("voltage", 0)
                expr -= direction * V
        if expr != 0:
            any_kvl_printed = True
            print(format_expr(sp.Eq(expr, 0)))
    if not any_kvl_printed:
        print("(none)")

    print("\nKCL:")
    for node in circuit["nodes"]:
        expr = 0
        for (n1, n2), I in current_vars.items():
            if node == n1:
                expr -= I  # current leaving
            elif node == n2:
                expr += I  # current entering
        print(format_expr(sp.Eq(expr, 0)))

# ---------------------
# Load and Run Tests
# ---------------------

with open("test_circuits.json") as f:
    test_data = json.load(f)

for name, circuit in test_data.items():
    generate_equations(name, circuit)
