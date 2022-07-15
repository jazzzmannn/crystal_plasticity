"""
 Title:         Angle Operations
 Description:   Dealing with angle related operations
 Author:        Janzen Choi

"""

# Libraries
import math, random

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

# Generates a set of (uniformly) random euler-bunge angles 
def random_euler():
    quat = random_quat()
    euler = quat_to_euler(*quat) 
    return euler

# Converts a set of euler-bunge angles into a quaternion (rads)
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

# Converts a quaternion into a set of euler-bunge angles (rads)
def quat_to_euler(x, y, z, w):
    roll    = math.atan2(2 * (w * x + y * z), 1 - 2 * (x * x + y * y))
    pitch   = math.asin(max([min([2 * (w * y - z * x), 1]), -1]))
    yaw     = math.atan2(2 * (w * z + x * y), 1 - 2 * (y * y + z * z))
    return [roll, pitch, yaw]