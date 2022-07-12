"""
 Title:         Generator
 Description:   Generates all the files for creating a Neper tessellation and mesh
 Author:        Janzen Choi

"""

# Libraries
import random, os
import packages.progressor as progressor
import packages.lognormal as lognormal

# Filenames
RUN_FILE            = "run.sh"
RESULTS_DIR         = "./results/"
PARENT_EQ_DIAM      = RESULTS_DIR + "parent_eq_diam"
TWIN_WIDTH_PATH     = RESULTS_DIR + "twin_width"
TWIN_ORI_PATH       = RESULTS_DIR + "twin_ori"
CRYSTAL_ORI_PATH    = RESULTS_DIR + "crystal_ori"
OUTPUT_PATH         = RESULTS_DIR + "output"
IMAGE_PREFIX        = RESULTS_DIR + "img"

# Statistics (in microns)
TWIN_THICKNESS      = { "mu": 1.45213, "sigma": 0.87586, "mean": 6.28413, "variance": 46.0933 }
PARENT_EQ_RADIUS    = { "mu": 3.01160, "sigma": 1.20437, "mean": 42.3802, "variance": 6114.57 }
PARENT_SPHERICITY   = { "mu": -0.9614, "sigma": 0.13107, "mean": 0.38573, "variance": 0.00258 }

# The Generator Class
class Generator:

    # Constructor
    def __init__(self, volume_length, max_grains, max_twins):
        
        # For visualising the generation
        self.progressor = progressor.Progressor()
        self.progressor.start("Initialising the system")
        self.progressor.end()

        # Prepares the environment
        if not os.path.exists(RESULTS_DIR):
            os.mkdir(RESULTS_DIR)
        for file in os.listdir(RESULTS_DIR):
            os.remove(RESULTS_DIR + file)

        # For the shape of the volume
        self.volume_length = volume_length
        self.max_grains = max_grains
        self.max_twins = max_twins

    # For writing a file to the results directory
    def write_results(self, file_name, content):
        if not os.path.exists(RESULTS_DIR):
            os.mkdir(RESULTS_DIR)
        with open(file_name, "w+") as file:
            file.write(content)
    
    # Wrotes the parent grain equivalent diameters
    def generate_parent_eq_diam(self):
        self.progressor.start("Generating parent equivalent diameters")
        eq_diam_lognormal = lognormal.Lognormal(PARENT_EQ_RADIUS)
        eq_diam_list = [2 * eq_diam_lognormal.get_val() for _ in range(self.max_twins)]
        eq_diam_str = "\n".join([str(eq_diam) for eq_diam in eq_diam_list])
        self.write_results(PARENT_EQ_DIAM, eq_diam_str)
        self.progressor.end()

    # Writes the twin widths
    def generate_twin_widths(self):
        self.progressor.start("Generating twin widths")
        twin_lognormal = lognormal.Lognormal(TWIN_THICKNESS)
        gap_lognormal = lognormal.Lognormal(PARENT_EQ_RADIUS)
        width_string = ""
        for i in range(self.max_grains):
            lamellae_widths         = 2 * self.max_twins * [None]
            lamellae_widths[::2]    = [gap_lognormal.get_val() for _ in range(self.max_twins)]
            lamellae_widths[1::2]   = [twin_lognormal.get_val() for _ in range(self.max_twins)]
            width_string += "{} {}\n".format(i + 1, ":".join([str(lw) for lw in lamellae_widths]))
        self.write_results(TWIN_WIDTH_PATH, width_string)
        self.progressor.end()

    # Writes the twin orientations
    def generate_twin_ori(self):
        self.progressor.start("Generating twin orientations")
        ori_str = ""
        for i in range(self.max_grains):
            ori = " ".join([str(random.randrange(2)) for _ in range(3)])
            ori_str += "{} {}\n".format(i + 1, ori)
        self.write_results(TWIN_ORI_PATH, ori_str)
        self.progressor.end()

    # Writes the crystallographic orientations
    def generate_crystal_ori(self):
        self.progressor.start("Generating grain crystal orientations")
        main_crystal_ori = ""
        for i in range(self.max_grains):
            crystal_ori         = 2 * self.max_twins * [None]
            crystal_ori[::2]    = ["212.6 57.0 58.1" for _ in range(self.max_twins)]
            crystal_ori[1::2]   = ["104.5 15.2 32.9" for _ in range(self.max_twins)]
            crystal_ori_path    = "{}_{}".format(CRYSTAL_ORI_PATH, i)
            self.write_results(crystal_ori_path, "\n".join(crystal_ori))
            main_crystal_ori += "{} file({},des=euler-bunge)\n".format(i + 1, crystal_ori_path)
        self.write_results(CRYSTAL_ORI_PATH, main_crystal_ori)
        self.progressor.end()

    # Writes the bash file
    def generate_bash(self):
        self.progressor.start("Writing bash file")
        
        # Defines the morphology
        diameq      = "diameq:lognormal({},{})".format(2 * PARENT_EQ_RADIUS["mean"], 2 * PARENT_EQ_RADIUS["variance"]**0.5)
        sphericity  = "1-sphericity:lognormal({},{})".format(PARENT_SPHERICITY["mean"], round(PARENT_SPHERICITY["variance"]**(1/2), 5))
        lamellar    = "lamellar(w=file({}),v=crysdir(1,0,0))".format(TWIN_WIDTH_PATH)
        morpho      = "-morpho \"{},{}::{}\"".format(diameq, sphericity, lamellar)

        # Defines other options
        morphooptiini   = "-morphooptiini coo:packing,weight:radeq"
        domain          = "-domain \"cube({},{},{})\"".format(self.volume_length, self.volume_length, self.volume_length)
        crystal_ori     = "-ori \"random::msfile({})\"".format(CRYSTAL_ORI_PATH)

        # For creating the tessellation and mesh
        commands = "#!/bin/bash\n"
        commands += "neper -T -n from_morpho::from_morpho {} {} {} {} -o {}.tess &&".format(morpho, domain, morphooptiini, crystal_ori, OUTPUT_PATH)
        commands += "neper -V {}.tess -datacellcol ori -print {}_1 &&".format(OUTPUT_PATH, IMAGE_PREFIX)
        commands += "neper -M {}.tess &&".format(OUTPUT_PATH)
        commands += "neper -V {}.tess,{}.msh -datacellcol ori -print {}_2\n".format(OUTPUT_PATH, OUTPUT_PATH, IMAGE_PREFIX)

        # For removing the other files
        helper_files = [RUN_FILE, PARENT_EQ_DIAM, TWIN_WIDTH_PATH, TWIN_ORI_PATH, CRYSTAL_ORI_PATH]
        helper_files += ["{}_{}".format(CRYSTAL_ORI_PATH, i) for i in range(self.max_grains)]
        commands += "\n".join(["rm {}".format(file) for file in helper_files])

        # Write commands to a bash file
        self.write_results(RUN_FILE, commands)
        self.progressor.end()
