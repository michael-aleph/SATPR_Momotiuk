file = open('task1.txt', 'r')

file_data = []

for row in file:
    file_data.append([int(num) for num in row.split() if num.isdigit()])

formatted_file_data = '\n'.join([' '.join(map(str, row)) for row in file_data])
print(formatted_file_data)

results = []

for i in range(len(file_data) - 1):
    sum_val = sum(file_data[i][j] * file_data[len(file_data) - 1][j] for j in range(len(file_data[0])))
    results.append(sum_val)

max_result = max(results)
max_result_position = results.index(max_result) + 1

print(results)
print(f'Max value {max_result} for alternative A{max_result_position}')
