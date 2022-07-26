"""
 Title:         Coincidence Site Lattice
 Description:   For generating euler angles that satisfy CSL criteria (only supports CSL3-11)
                More information can be found at http://pajarito.materials.cmu.edu/lectures/L14-CSL_Theory_GBE-17Mar16.pdf
 Author:        Janzen Choi

"""

# Libraries
import packages.orientation.angle as angle
import packages.orientation.matrix as matrix
import packages.orientation.orienter as orienter

# Constants
CSL3_OFFSET = [45, 70.53, 45]
CSL5_OFFSET = [0, 90, 36.86]
CSL7_OFFSET = [26.56, 73.4, 63.44]
CSL9_OFFSET = [26.56, 83.62, 26.56]
CSL11_OFFSET = [33.68, 79.53, 33.68]
CSL_DICT = {
    "3": CSL3_OFFSET,
    "5": CSL5_OFFSET,
    "7": CSL7_OFFSET,
    "9": CSL9_OFFSET,
    "11": CSL11_OFFSET,
}

# For generating two sets of euler angles that conform to CSL3
def get_csl_euler_angles(csl_sigma, euler_1 = []):

    # Generate a set of random euler angles if none specified
    euler_1 = euler_1 if euler_1 != [] else angle.random_euler()
    
    # Specify rotational offset
    euler_offset = angle.deg_to_rad(CSL_DICT[csl_sigma])

    # Determine second set of euler angles
    matrix_1 = orienter.euler_to_matrix(euler_1)
    matrix_offset = orienter.euler_to_matrix(euler_offset)
    matrix_2 = matrix.get_matrix_product(matrix_offset, matrix_1)
    euler_2 = orienter.matrix_to_euler(matrix_2)

    # Return
    return [euler_1, euler_2]