"""
 Title:         Matrix related operations
 Description:   Contains matrix related operations
 Author:        Janzen Choi

"""

# Libraries
import numpy as np

# Performs a 3x3 matrix multiplication
def get_matrix_product(matrix_1, matrix_2):
    result = [[0,0,0], [0,0,0], [0,0,0]]
    for i in range(3):
        for j in range(3):
            for k in range(3):
                result[i][j] += matrix_1[i][k] * matrix_2[k][j]
    return result

# Inverts a matrix
def get_inverted(matrix):
    matrix = np.array(matrix)
    inverted = [list(i) for i in np.linalg.inv(matrix)]
    return inverted