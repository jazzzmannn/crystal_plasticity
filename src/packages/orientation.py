"""
 Title:         Orientation
 Description:   For generating the orientation of grains
 Author:        Janzen Choi

"""

# Libraries
import numpy as np
import math, random

# Constants
SYMMETRY_MATRICES = [
    [[1,0,0], [0,1,0], [0,0,1]],
    [[0,0,-1], [0,-1,0], [-1,0,0]],
    [[0,0,-1], [0,1,0], [1,0,0]],
    [[-1,0,0], [0,1,0], [0,0,-1]],
    [[0,0,1], [0,1,0], [-1,0,0]],
    [[1,0,0], [0,0,-1], [0,1,0]],
    [[1,0,0], [0,-1,0], [0,0,-1]],
    [[1,0,0], [0,0,1], [0,-1,0]],
    [[0,-1,0], [1,0,0], [0,0,1]],
    [[-1,0,0], [0,-1,0], [0,0,1]],
    [[0,1,0], [-1,0,0], [0,0,1]],
    [[0,0,1], [1,0,0], [0,1,0]],
    [[0,1,0], [0,0,1], [1,0,0]],
    [[0,0,-1], [-1,0,0], [0,1,0]],
    [[0,-1,0], [0,0,1], [-1,0,0]],
    [[0,1,0], [0,0,-1], [-1,0,0]],
    [[0,0,-1], [1,0,0], [0,-1,0]],
    [[0,0,1], [-1,0,0], [0,-1,0]],
    [[0,-1,0], [0,0,-1], [1,0,0]],
    [[0,1,0], [1,0,0], [0,0,-1]],
    [[-1,0,0], [0,0,1], [0,1,0]],
    [[0,0,1], [0,-1,0], [1,0,0]],
    [[0,-1,0], [-1,0,0], [0,0,-1]],
    [[-1,0,0], [0,0,-1], [0,-1,0]]
]

# Generates a (uniformly) random quaternion
def random_quat():
    u = [random.uniform(0, 1) for _ in range(3)]
    x = math.sqrt(1 - u[0]) * math.sin(2 * math.pi * u[1])
    y = math.sqrt(1 - u[0]) * math.cos(2 * math.pi * u[1])
    z = math.sqrt(u[0]) * math.sin(2 * math.pi * u[2])
    w = math.sqrt(u[0]) * math.cos(2 * math.pi * u[2])
    return [x, y, z, w]

# Converts a set of euler angles (rads) into a quaternion (rads)
def euler_to_quat(roll, pitch, yaw):
    cy = math.cos(yaw * 0.5)
    sy = math.sin(yaw * 0.5)
    cp = math.cos(pitch * 0.5)
    sp = math.sin(pitch * 0.5)
    cr = math.cos(roll * 0.5)
    sr = math.sin(roll * 0.5)
    x = sr * cp * cy - cr * sp * sy
    y = cr * sp * cy + sr * cp * sy
    z = cr * cp * sy - sr * sp * cy
    w = cr * cp * cy + sr * sp * sy
    return [x, y, z, w]

# Converts a quaternion (rads) into a set of euler angles (rads)
def quat_to_euler(x, y, z, w):
    roll    = math.atan2(2 * (w * x + y * z), 1 - 2 * (x * x + y * y))
    pitch   = math.asin(max([min([2 * (w * y - z * x), 1]), -1]))
    yaw     = math.atan2(2 * (w * z + x * y), 1 - 2 * (y * y + z * z))
    return [2 * math.pi + q if q < 0 else q for q in [roll, pitch, yaw]]

# Determines the misorientation of two sets of euler numbers (rads)
def get_misorientation_angles(euler_1, euler_2):
    om_1 = get_orientation_matrix(euler_1)
    om_2 = get_orientation_matrix(euler_2)
    angle_list = []
    for sym in SYMMETRY_MATRICES:
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

# Determines the orientation matrix of a set of euler numbers (rads)
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
