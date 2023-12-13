import openpyxl
import numpy as np

def get_matrix_out_of_sheet(sheet):
    return np.array(list(sheet.iter_rows(values_only=True)))

def find_strategy(workbook):
    pay_matrix = get_matrix_out_of_sheet(workbook.worksheets[0])

    min_values = [min(row) for row in pay_matrix]
    max_values = [max(col) for col in pay_matrix.T]

    minmax = max(min_values)
    maxmin = min(max_values)

    print(f'min A: {min_values}')
    print(f'max B: {max_values}\n')
    print(f'Максимальне серед мінімальних: {maxmin}')
    print(f'Мінімальне серед максимальних: {minmax}\n')

    if maxmin != minmax:
        print("Сідлової точки не існує, отже рівноваги в чистих стратегіях немає")
    else:
        print(f'Сідлова точка: {minmax}')

filePath = 'lab5_1.xlsx'
workbook = openpyxl.load_workbook(filePath)

find_strategy(workbook)
workbook.close()
