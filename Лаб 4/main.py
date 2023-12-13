import openpyxl
import numpy as np


def get_matrix_out_of_sheet(sheet):
    matrix = []

    for row in sheet.iter_rows(values_only=True):
        matrix.append(row)

    return np.array(matrix)


def gurviz(workbook):
    pay_matrix = get_matrix_out_of_sheet(workbook.worksheets[0])
    l = get_matrix_out_of_sheet(workbook.worksheets[2])[0][0]

    number_of_rows = pay_matrix.shape[0]
    number_of_columns = pay_matrix.shape[1]

    result = 0
    index = 0

    for row in range(number_of_rows):
        min_value = 100000
        max_value = -100000

        for column in range(number_of_columns):
            if pay_matrix[row, column] < min_value:
                min_value = pay_matrix[row, column]

            if pay_matrix[row, column] > max_value:
                max_value = pay_matrix[row, column]

        total_sum = max_value * l + min_value * (1 - l)

        if total_sum > result:
            result = total_sum
            index = row

    print(f'A{index + 1}: {result}')


def laplace(workbook):
    pay_matrix = get_matrix_out_of_sheet(workbook.worksheets[0])

    number_of_rows = pay_matrix.shape[0]
    number_of_columns = pay_matrix.shape[1]

    result = 0
    index = 0

    for row in range(number_of_rows):
        total_sum = 0

        for column in range(number_of_columns):
            total_sum += pay_matrix[row, column]

        total_sum /= number_of_columns

        if total_sum > result:
            result = total_sum
            index = row

    print(f'A{index + 1}: {result}')


def bayes_laplace(workbook):
    pay_matrix = get_matrix_out_of_sheet(workbook.worksheets[0])
    ps = get_matrix_out_of_sheet(workbook.worksheets[1])
    l = get_matrix_out_of_sheet(workbook.worksheets[2])[0][0]

    number_of_rows = pay_matrix.shape[0]
    number_of_columns = pay_matrix.shape[1]

    result = 0
    index = 0

    for row in range(number_of_rows):
        total_sum = 0

        for column in range(number_of_columns):
            total_sum += pay_matrix[row, column] * ps[0, column] * l

        if total_sum > result:
            result = total_sum
            index = row

    print(f'A{index + 1}: {result}')


def hodge_leman(workbook):
    pay_matrix = get_matrix_out_of_sheet(workbook.worksheets[0])
    ps = get_matrix_out_of_sheet(workbook.worksheets[1])
    l = get_matrix_out_of_sheet(workbook.worksheets[2])[0][0]

    number_of_rows = pay_matrix.shape[0]
    number_of_columns = pay_matrix.shape[1]

    result = 0
    index = 0

    for row in range(number_of_rows):
        total_sum = 0
        min_value = 100000

        for column in range(number_of_columns):
            total_sum += pay_matrix[row, column] * ps[0, column] * l

            if pay_matrix[row, column] < min_value:
                min_value = pay_matrix[row, column]

        total_sum += min_value * l

        if total_sum > result:
            result = total_sum
            index = row

    print(f'A{index + 1}: {result}')


def vald(workbook):
    pay_matrix = get_matrix_out_of_sheet(workbook.worksheets[0])

    number_of_rows = pay_matrix.shape[0]
    number_of_columns = pay_matrix.shape[1]

    result = 0
    index = 0

    for row in range(number_of_rows):
        min_value = 100000

        for column in range(number_of_columns):
            if pay_matrix[row, column] < min_value:
                min_value = pay_matrix[row, column]

        if min_value > result:
            result = min_value
            index = row

    print(f'A{index + 1}: {result}')


def savage(workbook):
    pay_matrix = get_matrix_out_of_sheet(workbook.worksheets[0])

    number_of_rows = pay_matrix.shape[0]
    number_of_columns = pay_matrix.shape[1]

    matrix = np.zeros((number_of_rows, number_of_columns))
    values = np.zeros(number_of_rows)
    indexes = np.zeros(number_of_rows)

    result = 0

    for row in range(number_of_rows):
        max_value = -100000

        for column in range(number_of_columns):
            if max_value < pay_matrix[row, column]:
                max_value = pay_matrix[row, column]

        values[row] = max_value
        indexes[row] = np.argmax(pay_matrix[row])

    for column in range(number_of_columns):
        for row in range(number_of_rows):
            index = np.where(indexes == column)[0]

            if index.size != 0:
                index = index[0]
                matrix[row, column] = values[index] - pay_matrix[row, column]
            else:
                matrix[row, column] = pay_matrix[row, column]

    values = np.zeros(number_of_rows)

    for row in range(number_of_rows):
        max_value = -100000

        for column in range(number_of_columns):
            if max_value < matrix[row, column]:
                max_value = matrix[row, column]

        values[row] = max_value

    index = np.argmin(values)

    result = values[index]

    print(f'A{index + 1}: {result}')


file_path = 'lab4_2.xlsx'

workbook = openpyxl.load_workbook(file_path)

print('Gurviz:')
gurviz(workbook)

print('\nLaplace:')
laplace(workbook)

print('\nBayesLaplace:')
bayes_laplace(workbook)

print('\nHodgeLeman:')
hodge_leman(workbook)

print('\nVald:')
vald(workbook)

print('\nSavage:')
savage(workbook)

workbook.close()
