import packages.orientation as orientation
import numpy as np

euler_1 = [0.3404, 1.3610, 3.8399]
euler_2 = [1.2423, 2.9281, 3.4985]

misorientation = orientation.get_misorientation_angles(euler_1, euler_2)
misorientation = [m * 180 / 3.1415 for m in misorientation]
print(misorientation)