"""
 Title:         Main
 Description:   Outputs all the necessary files for Neper to generate the volume
 Author:        Janzen Choi

"""

# Libraries
import packages.generator as generator

# Properties
DIMENSIONS      = 2
VOLUME_LENGTH   = 1000 # microns
MAX_GRAINS      = 100
MAX_TWINS       = 40 # 1/2 of maximum lamellae
MISORIENTATION  = 60 # (degrees)
CRYSTAL_TYPE    = "cubic"
STATISTICS      = {
    "twin_thickness":       { "mu": 1.45213, "sigma": 0.87586, "mean": 6.28413, "variance": 46.0933, "min": 0.6042, "max": 59.8839 },
    "parent_eq_radius":     { "mu": 3.01160, "sigma": 1.20437, "mean": 42.3802, "variance": 6114.57, "min": 2.0349, "max": 221.314 },
    "parent_sphericity":    { "mu": -0.9614, "sigma": 0.13107, "mean": 0.38573, "variance": 0.00258 },
}

# Main function
if __name__ == "__main__":
    gen = generator.Generator(VOLUME_LENGTH, MAX_GRAINS, MAX_TWINS, MISORIENTATION, CRYSTAL_TYPE, STATISTICS)
    gen.generate_twin_widths()
    gen.generate_crystal_ori()
    gen.generate_bash(DIMENSIONS)