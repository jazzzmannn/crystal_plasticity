"""
 Title:         Crystallographic Orienter
 Description:   For generating the crystallographic orientation of grains
 Author:        Janzen Choi

"""

# Libraries
import packages.symmetry as symmetry
import numpy as np, math

# Determines the coincidence site lattice value
def get_csl(euler_1, euler_2):
    om_1 = get_orientation_matrix(euler_1)
    om_2 = get_orientation_matrix(euler_2)
    om_2_i = get_inverted(om_2)
    product = get_matrix_product(om_1, om_2_i)
    uvw = [product[2][1] - product[1][2], product[0][2] - product[2][0], product[1][0] - product[0][1]]
    return uvw

# Determines the misorientation of two sets of euler angles (rads)
def get_misorientation_angle(euler_1, euler_2, type):
    return min(get_misorientation_angles(euler_1, euler_2, type))

# Determines the misorientations of two sets of euler angles (rads)
def get_misorientation_angles(euler_1, euler_2, type):
    om_1 = get_orientation_matrix(euler_1)
    om_2 = get_orientation_matrix(euler_2)
    angle_list = []
    for sym in symmetry.get_symmetry_matrices(type):
        matrix_1 = get_matrix_product(sym, om_1)
        matrix_2 = get_inverted(matrix_1)
        matrix_3 = get_matrix_product(matrix_2, om_2)
        angle = math.acos((matrix_3[0][0] + matrix_3[1][1] + matrix_3[2][2] - 1) / 2)
        angle_list.append(angle)
    return angle_list

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

# Determines the orientation matrix of a set of euler angles (rads)
def get_orientation_matrix(euler):
    om_11 = math.cos(euler[0])*math.cos(euler[2]) - math.sin(euler[0])*math.sin(euler[2])*math.cos(euler[1])
    om_12 = math.sin(euler[0])*math.cos(euler[2]) + math.cos(euler[0])*math.sin(euler[2])*math.cos(euler[1])
    om_13 = math.sin(euler[2])*math.sin(euler[1])
    om_21 = -math.cos(euler[0])*math.sin(euler[2]) - math.sin(euler[0])*math.cos(euler[2])*math.cos(euler[1])
    om_22 = -math.sin(euler[0])*math.sin(euler[2]) + math.cos(euler[0])*math.cos(euler[2])*math.cos(euler[1])
    om_23 = math.cos(euler[2])*math.sin(euler[1])
    om_31 = math.sin(euler[0])*math.sin(euler[1])
    om_32 = -math.cos(euler[0])*math.sin(euler[1])
    om_33 = math.cos(euler[1])
    om = [[om_11, om_12, om_13],
          [om_21, om_22, om_23],
          [om_31, om_32, om_33]]
    return om
