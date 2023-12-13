import numpy as np
from pulp import *

def northwest_corner_rule(supply_arr, demand_arr):
    rows = len(supply_arr)
    cols = len(demand_arr)
    result = np.zeros((rows, cols))

    i, j = 0, 0

    while i < rows and j < cols:
        quantity = min(supply_arr[i], demand_arr[j])
        result[i, j] = quantity
        supply_arr[i] -= quantity
        demand_arr[j] -= quantity

        if supply_arr[i] == 0:
            i += 1

        if demand_arr[j] == 0:
            j += 1

    return result

def solve_transportation_problem(supply, demand, costs):
    supply_count, demand_count = len(supply), len(demand)

    initial_allocation = northwest_corner_rule(supply.copy(), demand.copy())

    costs_dict = makeDict([range(supply_count), range(demand_count)], costs, 0)

    prob = LpProblem("Transportation_Problem", LpMinimize)

    routes = [(i, j) for i in range(supply_count) for j in range(demand_count)]
    route_vars = LpVariable.dicts("Route", (range(supply_count), range(demand_count)), 0, None, LpInteger)

    prob += lpSum([route_vars[supplier][consumer] * costs_dict[supplier][consumer] for (supplier, consumer) in routes]), "Minimize_Transportation_Cost"

    for supplier_index in range(supply_count):
        prob += lpSum([route_vars[supplier_index][consumer] for consumer in range(demand_count)]) <= supply[supplier_index], f"Supply_Constraint_{supplier_index}"

    for consumer_index in range(demand_count):
        prob += lpSum([route_vars[supplier][consumer_index] for supplier in range(supply_count)]) >= demand[consumer_index], f"Demand_Constraint_{consumer_index}"

    prob.solve()

    results = np.array([v.varValue for v in prob.variables()]).reshape(supply_count, demand_count)

    return results, value(prob.objective)

supply = [200, 300, 250]
demand = [210, 150, 120, 135, 135]
costs = [
    [20, 10, 13, 13, 18],
    [27, 19, 20, 16, 22],
    [26, 17, 19, 21, 23]
]

nw_result, total_cost = solve_transportation_problem(supply, demand, costs)

print("Фінальний розподіл запасів (за правилом північно-західного кута):")
print(nw_result)
print("\nСуммарна ціна плану (оптимальне рішення):", total_cost)
