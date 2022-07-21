"""
 Title:         Crystallographic Orienter
 Description:   For generating the crystallographic orientation of grains
 Author:        Janzen Choi

"""

# Libraries
import packages.angle as angle
import numpy as np
import packages.orientation as orientation
from scipy.optimize import minimize

# Generates a pair of euler angles based on a misorientation (rads)
def generate_euler_pair(misorientation, type):
    euler = angle.random_euler()
    pairer = Pairer(euler, misorientation, type)
    pairing_euler = pairer.get_pairing_euler()
    # print(angle.rad_to_deg(get_misorientation_angle(euler, pairing_euler, type)))
    return [euler, pairing_euler]

# The Pairer Class
class Pairer:

    # Constructor
    def __init__(self, euler, misorientation, type):
        self.euler = euler
        self.misorientation = misorientation
        self.type = type

    # Determines a pairing set of euler angles from a misorientation angle (rads)
    def get_pairing_euler(self):
        x0 = np.array([1, 1, 1])
        res = minimize(self.pairing_euler_obj, x0, method="nelder-mead", options={"disp": False})
        return list(res.x)

    # Objective function for determining a pairing set of euler angles (rads)
    def pairing_euler_obj(self, euler):
        misorientation = orientation.get_misorientation_angle(self.euler, euler, self.type)
        return (self.misorientation - misorientation) ** 2