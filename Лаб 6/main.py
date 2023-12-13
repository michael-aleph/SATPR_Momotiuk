import numpy as np
from scipy.optimize import linear_sum_assignment
import openpyxl


def get_matrix_from_sheet(sheet):
    matrix = [row for row in sheet.iter_rows(values_only=True)]
    return np.array(matrix)


def normalize_rows_and_columns(matrix):
    matrix -= np.min(matrix, axis=0)
    matrix -= np.min(matrix, axis=1)[:, np.newaxis]


def print_result(row_ids, col_ids, min_defect_percentage):
    print('Best combination:')
    for worker, workbench in zip(row_ids, col_ids):
        print(f'Worker {worker + 1}: workbench {workbench + 1}')

    print(f'\nMinimum percentage of defects: {min_defect_percentage:.1f}%')


file_path = 'lab6.xlsx'
matrix = get_matrix_from_sheet(openpyxl.load_workbook(file_path).worksheets[0])

row_ids, col_ids = linear_sum_assignment(matrix)
min_defect_percentage = matrix[row_ids, col_ids].sum()
print_result(row_ids, col_ids, min_defect_percentage)
