"""
 Title:         Main
 Description:   Outputs all the necessary files for Neper to generate the volume
 Author:        Janzen Choi

"""

# Libraries
import packages.generator as generator

# Constants
VOLUME_LENGTH   = 1500 # microns
MAX_GRAINS      = 300
MAX_TWINS       = 30 # 1/2 of maximum lamellae
DIMENSIONS      = 2

# Main function
def main():
    gen = generator.Generator(VOLUME_LENGTH, MAX_GRAINS, MAX_TWINS)
    # gen.generate_twin_ori()
    gen.generate_twin_widths()
    gen.generate_crystal_ori()
    gen.generate_bash(DIMENSIONS)

# Calls the main function
if __name__ == "__main__":
    main()
