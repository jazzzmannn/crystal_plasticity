"""
 Title:         Generator
 Description:   Outputs all the necessary files for Neper to generate the volume
 Author:        Janzen Choi

"""

# Libraries
import numpy as np
import random, time

# Filenames
RUN_FILE                = "run"
RESULTS_PATH            = "./results/"
TWIN_WIDTH_FILE         = RESULTS_PATH + "width.txt"
TWIN_ORIENTATION_FILE   = RESULTS_PATH + "orientation.txt"
OUTPUT_FILE             = RESULTS_PATH + "output"
IMAGE_PREFIX            = RESULTS_PATH + "img"

# Generation Parameters
VOLUME_LENGTH   = 200 # microns
MAX_GRAINS      = 3000
MAX_TWINS       = 50 # 1/2 of maximum lamellae

# Statistics (in microns)
TWIN_THICKNESS      = { "mu": 1.45213, "sigma": 0.87586, "mean": 6.28413, "variance": 46.0933 }
PARENT_EQ_RADIUS    = { "mu": 3.01160, "sigma": 1.20437, "mean": 42.3802, "variance": 6114.57 }
PARENT_SPHERICITY   = { "mu": -0.9614, "sigma": 0.13107, "mean": 0.38573, "variance": 0.00258 }

# Main function
def main():
    timer = Timer()
    write_twin_widths()
    print("1) Defined twin widths        ({})".format(timer.update_time()))
    write_twin_orientations()
    print("2) Defined twin orientations  ({})".format(timer.update_time()))
    write_bash_file()
    print("3) Wrote bash file            ({})".format(timer.update_time()))

# Writes the twin orientations
def write_twin_orientations():

    # Prepares the data
    orientation_string = ""
    for i in range(MAX_GRAINS):
        orientations = " ".join([str(random.randrange(2)) for _ in range(3)])
        orientation_string += "{} {}\n".format(i + 1, orientations)
    
    # Writes to twin orientation file
    with open(TWIN_ORIENTATION_FILE, "w") as file:
        file.write(orientation_string)

# Writes the twin widths
def write_twin_widths():

    # Defines the distributions for the twin widths and gaps
    twin_lognormal = Lognormal(TWIN_THICKNESS)
    gap_lognormal = Lognormal(PARENT_EQ_RADIUS)

    # Prepares the data
    width_string = ""
    for i in range(MAX_GRAINS):
        lamellae_widths         = 2 * MAX_TWINS * [None]
        lamellae_widths[::2]    = [gap_lognormal.get_val() for _ in range(MAX_TWINS)]
        lamellae_widths[1::2]   = [twin_lognormal.get_val() for _ in range(MAX_TWINS)]
        width_string += "{} {}\n".format(i + 1, ":".join([str(lw) for lw in lamellae_widths]))
    
    # Writes to twin width file
    with open(TWIN_WIDTH_FILE, "w") as file:
        file.write(width_string)

# Writes the bash file
def write_bash_file():
    
    # Defines the morphology
    diameq      = "diameq:lognormal({},{})".format(PARENT_EQ_RADIUS["mean"], PARENT_EQ_RADIUS["variance"]**(1/2))
    sphericity  = "1-sphericity:lognormal({},{})".format(PARENT_SPHERICITY["mean"], PARENT_SPHERICITY["variance"]**(1/2))
    lamellar    = "lamellar(w=file({}),v=file({}))".format(TWIN_WIDTH_FILE, TWIN_ORIENTATION_FILE)
    morpho      = "-morpho \"{},{}::{}\"".format(diameq, sphericity, lamellar)

    # Defines the domain (i.e., size)
    domain = "-domain \"cube({},{},{})\"".format(VOLUME_LENGTH, VOLUME_LENGTH, VOLUME_LENGTH)

    # Assembles the commands
    commands = "#!/bin/bash\n"
    commands += "rm ./{}.sh\n".format(RUN_FILE)
    commands += "neper -T -n from_morpho::from_morpho {} {} -o {}.tess\n".format(morpho, domain, OUTPUT_FILE)
    commands += "neper -V {}.tess -print {}_1\n".format(OUTPUT_FILE, IMAGE_PREFIX)
    commands += "neper -M {}.tess\n".format(OUTPUT_FILE)
    commands += "neper -V {}.tess,{}.msh -print {}_2\n".format(OUTPUT_FILE, OUTPUT_FILE, IMAGE_PREFIX)

    # Write commands to a bash file
    with open(RUN_FILE + ".sh", "w") as file:
        file.write(commands)

# Lognormal Class
class Lognormal:

    # Constructor
    def __init__(self, statistic):
        self.amount = 1000
        self.distribution = np.random.lognormal(statistic["mu"], statistic["sigma"], self.amount)

    # Gets a value from the lognormal distribution
    def get_val(self):
        return self.distribution[random.randrange(len(self.distribution))]

# Timer Class
class Timer:

    # Constructor
    def __init__(self):
        self.start_time = time.time()
        self.module_start_time = self.start_time

    # Updates and returns the time string
    def update_time(self):
        time_string = str(round((time.time() - self.module_start_time) * 1000)) + "ms"
        self.module_start_time = time.time()
        return time_string

# Calls the main function
if __name__ == "__main__":
    main()
