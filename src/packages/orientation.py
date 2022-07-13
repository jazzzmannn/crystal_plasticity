"""
 Title:         Orientation
 Description:   For generating the orientation of grains
 Author:        Janzen Choi

"""

# Libraries
import numpy as np
import math, random
from scipy.optimize import minimize

# Generates a pair of euler angles based on a misorientation
def generate_euler_pair(misorientation):
    
    # Generate random euler pair
    euler = random_euler()
    pairer = Pairer(euler, misorientation)
    pairing_euler = pairer.get_pairing_euler()
    
    # Convert to positive degree
    euler = [360 + d if d < 0 else d for d in rad_to_deg(euler)]
    pairing_euler = [360 + d if d < 0 else d for d in rad_to_deg(pairing_euler)]
    return [euler, pairing_euler]

# The Pairer Class
class Pairer:

    # Constructor
    def __init__(self, euler, misorientation):
        self.euler = euler
        self.misorientation = misorientation

    # Determines a pairing set of euler angles from a misorientation angle (rads)
    def get_pairing_euler(self):
        x0 = np.array([1, 1, 1])
        res = minimize(self.pairing_euler_obj, x0, method="nelder-mead", options={"disp": False})
        return list(res.x)

    # Objective function for determining a pairing set of euler angles (rads)
    def pairing_euler_obj(self, euler):
        misorientation = get_misorientation_angle(self.euler, euler)
        return (self.misorientation - misorientation) ** 2

# Converts radians to degrees
def rad_to_deg(radians):
    if isinstance(radians, list):
        return [rad_to_deg(r) for r in radians]
    return radians * 180 / math.pi

# Converts degrees to radians
def deg_to_rad(degrees):
    if isinstance(degrees, list):
        return [deg_to_rad(d) for d in degrees]
    return degrees * math.pi / 180

# Generates a (uniformly) random quaternion
def random_quat():
    u = [random.uniform(0, 1) for _ in range(3)]
    x = math.sqrt(1 - u[0]) * math.sin(2 * math.pi * u[1])
    y = math.sqrt(1 - u[0]) * math.cos(2 * math.pi * u[1])
    z = math.sqrt(u[0]) * math.sin(2 * math.pi * u[2])
    w = math.sqrt(u[0]) * math.cos(2 * math.pi * u[2])
    return [x, y, z, w]

# Generates a set of (uniformly) random euler angles
def random_euler():
    quat = random_quat()
    euler = quat_to_euler(*quat) 
    return euler

# Converts a set of euler angles into a quaternion (rads)
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

# Converts a quaternion into a set of euler angles (rads)
def quat_to_euler(x, y, z, w):
    roll    = math.atan2(2 * (w * x + y * z), 1 - 2 * (x * x + y * y))
    pitch   = math.asin(max([min([2 * (w * y - z * x), 1]), -1]))
    yaw     = math.atan2(2 * (w * z + x * y), 1 - 2 * (y * y + z * z))
    return [roll, pitch, yaw]

# Determines the misorientation of two sets of euler numbers (rads) 
def get_misorientation_angle(euler_1, euler_2):
    om_1 = euler_to_orientation_matrix(euler_1)
    om_2 = euler_to_orientation_matrix(euler_2)
    om_2 = get_inverted(om_2)
    mm = get_matrix_product(om_1, om_2)
    angle = math.acos((mm[0][0] + mm[1][1] + mm[2][2] - 1) / 2)
    return angle

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
def euler_to_orientation_matrix(euler):
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

# Determines a set of euler angles from an orientation matrix (rads)
def orientation_matrix_to_euler(om):
    Phi = math.acos(om[2][2])
    phi_1 = math.acos(-om[2][1] / math.sin(Phi))
    phi_2 = math.acos(om[1][2] / math.sin(Phi))
    return [phi_1, Phi, phi_2]
