import numpy as np

file_data = np.loadtxt('task2.txt')

print("File Data:")
print(file_data)

estimating_values = np.where(file_data[-1, None, :],
                             (file_data[:-2, :] - np.min(file_data[:-2, :], axis=0)) /
                             (np.max(file_data[:-2, :], axis=0) - np.min(file_data[:-2, :], axis=0)),
                             (np.max(file_data[:-2, :], axis=0) - file_data[:-2, :]) /
                             (np.max(file_data[:-2, :], axis=0) - np.min(file_data[:-2, :], axis=0)))

print("\nEstimating Values:")
print(estimating_values)

results = np.dot(estimating_values, file_data[-2, :])
print("\nResults:")
print(results)

max_result_position = np.argmax(results) + 1
max_result = results[max_result_position - 1]
print(f'Max Result: {max_result} in alternative A{max_result_position}')
