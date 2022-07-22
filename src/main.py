"""
 Title:         The Main File
 Description:   Outputs all the necessary files for Neper to generate the volume
 Author:        Janzen Choi

"""

# Libraries
import packages.generator as generator

# Properties
DIMENSIONS      = 2
VOLUME_LENGTH   = 200 # microns
MISORIENTATION  = 60 # (degrees)
CRYSTAL_TYPE    = "cubic"

# Statistics
TWIN_THICKNESS      = { "mu": 1.43090, "sigma": 0.89090, "mean": 6.21960, "variance": 46.8620, "min": 0.42990, "max": 69.3133 }
PARENT_EQ_RADIUS    = { "mu": 2.950077, "sigma": 1.256951, "mean": 42.099649, "variance": 6831.803092, "min": 1.635426, "max": 257.058914 }
PARENT_EQ_RADIUS_1  = { "mu": 1.908533, "sigma": 0.843008, "mean": 9.620190, "variance": 95.818480, "min": 1.635426, "max": 24.744041 }
PARENT_EQ_RADIUS_2  = { "mu": 3.985832, "sigma": 0.527962, "mean": 61.880403, "variance": 1230.961962, "min": 24.870175, "max": 215.109386 }
PARENT_SPHERICITY   = { "mu": -3.568930, "sigma": 1.170012, "mean": 0.055885, "variance": 0.009154, "min": 0.003727, "max": 0.575208 }

# Main function
if __name__ == "__main__":
    gen = generator.Generator(DIMENSIONS, VOLUME_LENGTH)
    gen.tessellate_parents([PARENT_EQ_RADIUS_1, PARENT_EQ_RADIUS_2], PARENT_SPHERICITY)
    gen.visualise_parents()
    gen.generate_twins(TWIN_THICKNESS)
    gen.generate_crystal_orientations(MISORIENTATION, CRYSTAL_TYPE)
    gen.tessellate_volume()
    gen.visualise_volume()
    gen.mesh_volume()
    gen.visualise_mesh()
    gen.end_generator()
