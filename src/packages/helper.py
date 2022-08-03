"""
 Title:         Helper
 Description:   General helper functions
 Author:        Janzen Choi

"""

# Libraries
import subprocess, os, csv
import numpy as np

# For safely making a directory
def safe_mkdir(dir_path):
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)

# Converts a list of dictionaries to a CSV format
def dict_list_to_csv(dictionary_list):
    headers = list(dictionary_list[0].keys())
    data = [[d[1] for d in dictionary.items()] for dictionary in dictionary_list]
    return headers, data

# For writing to CSV files
def write_to_csv(path, header, data):
    with open(path, "w+") as file:
        writer = csv.writer(file)
        writer.writerow(header)
        for row in data:
            writer.writerow(row)

# Runs a command using a single thread
def run(command, shell = True, check = True):
    subprocess.run(["OMP_NUM_THREADS=1 " + command], shell = shell, check = check)

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