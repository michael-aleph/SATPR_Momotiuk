import openpyxl
import numpy as np


def get_matrix_from_sheet(sheet):
    matrix = []

    for row in sheet.iter_rows(values_only=True):
        matrix.append(row)

    return np.array(matrix)


def find_alternative_values(workbook):
    awards_matrix = get_matrix_from_sheet(workbook.worksheets[0])
    chances_matrix = get_matrix_from_sheet(workbook.worksheets[1])

    num_rows = awards_matrix.shape[0]
    num_columns = awards_matrix.shape[1]

    alternative_values = np.zeros(num_rows)

    for row in range(num_rows):
        total_sum = 0

        for column in range(num_columns):
            total_sum += awards_matrix[row, column] * chances_matrix[0, column]

        alternative_values[row] = total_sum

    return alternative_values


file_path = 'lab3_5.xlsx'

try:
    workbook = openpyxl.load_workbook(file_path)
except FileNotFoundError:
    print(f"Файл '{file_path}' не знайдено.")
    exit()
alternative_values = find_alternative_values(workbook)
max_index = np.argmax(alternative_values)

print(alternative_values)
print(f'Очікуваний дохід за більший для альтернативи A{max_index + 1}: {alternative_values[max_index]}')

workbook.close()
