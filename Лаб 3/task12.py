import numpy as np

# Сценарії будівництва заводів
# [Ціна будівництва, ймовірність попиту, дохід за рік]
A = [600000, [0.7, 0.3], [250000, -50000]]
B = [350000, [0.7, 0.3], [150000, 25000]]
C1 = [600000, [0.9 * 0.8, 0.1 * 0.8], [250000, -50000]]
C2 = [350000, [0.9 * 0.8, 0.1 * 0.8], [150000, 25000]]
C3 = [600000, [0.9 * 0.2, 0.1 * 0.2], [250000, -50000]]
C4 = [350000, [0.9 * 0.2, 0.1 * 0.2], [150000, 25000]]

tree = [A, B, C1, C2, C3, C4]


def calculate_expected_incomes(tree):
    result_incomes = []

    results = []
    for i in range(len(tree)):
        temp_results = []
        branch = tree[i]

        for j in range(2):
            price = branch[0]
            profit = branch[2][j]
            probability = branch[1][j]

            temp_results.append([
                branch[0],
                probability,
                profit,
                profit * 5 - price,
                probability * (profit * 5 - price),
            ])

        expected_income_full = np.sum(temp_results, axis=0)[4]
        result_incomes.append(expected_income_full)

        results.append(temp_results)

    return results, result_incomes


def display_results(results, result_incomes):
    for i in range(len(results)):
        print("\nВаріант №" + str(i + 1))
        print(f"Очікуваний чистий дохід за весь період {round(result_incomes[i], 2)}")

    print("\nВаріант №" + str(len(results) + 1))
    print("Не будувати завод")


results, result_incomes = calculate_expected_incomes(tree)

display_results(results, result_incomes)
