import numpy as np
from sklearn.preprocessing import LabelBinarizer


def relative_majority(e, votes):
    return np.sum(e[0] * votes, axis=1)


def encoded(matrix, label_binarizer):
    encoded = label_binarizer.fit_transform(matrix.flatten())
    encoded = encoded.reshape(matrix.shape + (4,))
    encoded = encoded.transpose((0, 2, 1))
    return encoded


def relative(labels, e, votes):
    relative_majority_score = relative_majority(e, votes)
    relative_majority_result = labels[np.argmax(relative_majority_score)]
    return relative_majority_result


def absolute(labels, matrix, votes, encoded, label_binarizer):
    relative_majority_score = np.sum(encoded[0] * votes, axis=1)
    sorted_result = np.sort(relative_majority_score)[-2:]
    indices = np.where(np.isin(relative_majority_score, sorted_result))[0]
    second_indices = np.argmax(np.isin(matrix, labels[indices]), axis=0)
    top2_vector = label_binarizer.transform(
        matrix[second_indices, np.arange(matrix.shape[1])]).T * votes
    absolute_score = top2_vector.sum(axis=1)
    absolute_result = labels[np.argmax(absolute_score)]
    return absolute_result


def borda(encoded, votes, labels):
    mul_array = encoded * votes
    arr_score = mul_array * np.array([3, 2, 1, 0])[:, np.newaxis, np.newaxis]
    bord_score = arr_score.sum(axis=2).sum(axis=0)
    bord_result = labels[np.argmax(bord_score)]
    return bord_result


def condorcet(matrix, votes):
    unique_labels = np.unique(matrix)
    label_to_num = {label: i for i, label in enumerate(unique_labels)}

    num_matrix = np.vectorize(label_to_num.get)(matrix)
    matrix_cond = np.zeros((len(unique_labels), len(unique_labels)))

    for i, col in enumerate(num_matrix.T):
        for x in range(col.shape[0]):
            for y in range(x + 1, col.shape[0]):
                matrix_cond[col[x]][col[y]] += votes[i]

    return matrix_cond


def find_winner(matrix_cond, labels):
    for i, e1 in enumerate(labels):
        winner = all(matrix_cond[i][j] >= matrix_cond[j][i] for j in range(len(labels)) if i != j)
        if winner:
            return e1


def coplend(matrix, votes, labels):
    matrix_cond = condorcet(matrix, votes)
    cop_score = np.zeros(len(labels))
    for i, e1 in enumerate(labels):
        for j in range(len(labels)):
            if i != j:
                if matrix_cond[i][j] < matrix_cond[j][i]:
                    cop_score[i] -= 1
                elif matrix_cond[i][j] > matrix_cond[j][i]:
                    cop_score[i] += 1
    cop_result = labels[np.argmax(cop_score)]
    return cop_result


def simpson(matrix, votes, labels):
    matrix_cond = condorcet(matrix, votes)
    data_no_zeros = np.where(matrix_cond == 0, np.nan, matrix_cond)
    simpson_score = np.nanmin(data_no_zeros, axis=1)
    simpson_result = labels[np.argmax(simpson_score)]
    return simpson_result


def main():
    label_binarizer = LabelBinarizer()

    matrix = np.array([['A', 'B', 'C', 'C'],
                       ['C', 'C', 'A', 'A'],
                       ['B', 'A', 'B', 'D'],
                       ['D', 'D', 'D', 'B']])
    votes = np.array([6, 6, 3, 5])

    enc = encoded(matrix, label_binarizer)

    labels = np.array(['A', 'B', 'C', 'D'])

    rel = relative(labels, enc, votes)
    print("Relative Majority:", rel)
    absol = absolute(labels, matrix, votes, enc, label_binarizer)
    print("Absolute Majority:", absol)
    borda_res = borda(enc, votes, labels)
    print("Borda Winner:", borda_res)
    condorcet_res = find_winner(condorcet(matrix, votes), labels)
    print("Condorcet Winner:", condorcet_res)
    cop_res = coplend(matrix, votes, labels)
    print("Copeland Winner:", cop_res)
    simpson_res = simpson(matrix, votes, labels)
    print("Simpson Winner:", simpson_res)


if __name__ == '__main__':
    main()
