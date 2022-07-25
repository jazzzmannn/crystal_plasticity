"""
 Title:         The Main File
 Description:   Outputs all the necessary files for Neper to generate the volume
 Author:        Janzen Choi

"""

# Libraries
import packages.generator as generator

# Properties
DIMENSIONS      = 3
VOLUME_LENGTH   = 300 # microns
MISORIENTATION  = 60 # (degrees)
CRYSTAL_TYPE    = "cubic"

# Statistics
TWIN_THICKNESS      = { "mu": 1.43090, "sigma": 0.89090, "mean": 6.21960, "variance": 46.8620, "min": 0.42990, "max": 69.3133 }
PARENT_EQ_RADIUS    = { "mu": 2.95008, "sigma": 1.25695, "mean": 42.0996, "variance": 6831.80, "min": 1.63543, "max": 257.059 }
PARENT_SPHERICITY   = { "mu": -3.5689, "sigma": 1.17001, "mean": 0.05589, "variance": 0.00915, "min": 0.00373, "max": 0.57521 }

# Main function
if __name__ == "__main__":
    gen = generator.Generator(DIMENSIONS, VOLUME_LENGTH)
    gen.define_custom_3d_domain() # custom shape
    gen.tessellate_parents(PARENT_EQ_RADIUS, PARENT_SPHERICITY)
    gen.visualise_parents()
    gen.generate_twins(TWIN_THICKNESS)
    gen.generate_crystal_orientations(MISORIENTATION, CRYSTAL_TYPE)
    gen.tessellate_volume()
    gen.visualise_volume()
    gen.mesh_volume()
    gen.visualise_mesh()
    gen.end_generator()
