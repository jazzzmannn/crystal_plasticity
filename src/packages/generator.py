"""
 Title:         File Generator
 Description:   Generates all the files for creating a Neper tessellation and mesh
 Author:        Janzen Choi

"""

# Libraries
import os
import packages.progressor as progressor
import packages.lognormal as lognormal
import packages.orientation as orientation
import packages.angle as angle

# Filenames
RUN_FILE            = "run.sh"
RESULTS_DIR         = "results/"
TWIN_WIDTH_PATH     = RESULTS_DIR + "twin_width"
CRYSTAL_ORI_PATH    = RESULTS_DIR + "crystal_ori"
OUTPUT_PATH         = RESULTS_DIR + "output"
IMAGE_PREFIX        = RESULTS_DIR + "img"

# The Generator Class
class Generator:

    # Constructor
    def __init__(self, volume_length, max_grains, max_twins, misorientation, crystal_type, statistics):
        
        # Properties of the volume
        self.progressor = progressor.Progressor()
        self.progressor.start("Initialising the system")
        self.volume_length      = volume_length
        self.max_grains         = max_grains
        self.max_twins          = max_twins
        self.misorientation     = misorientation
        self.crystal_type       = crystal_type
        self.twin_thickness     = statistics["twin_thickness"]
        self.parent_eq_radius   = statistics["parent_eq_radius"]
        self.parent_sphericity  = statistics["parent_sphericity"]
        self.progressor.end()

        # Prepares the environment
        self.progressor.start("Resetting the results directory")
        if not os.path.exists(RESULTS_DIR):
            os.mkdir(RESULTS_DIR)
        for file in os.listdir(RESULTS_DIR):
            os.remove(RESULTS_DIR + file)
        self.progressor.end()

    # For writing a file to the results directory
    def write_results(self, file_name, content):
        if not os.path.exists(RESULTS_DIR):
            os.mkdir(RESULTS_DIR)
        with open(file_name, "w+") as file:
            file.write(content)

    # Writes the twin widths
    def generate_twin_widths(self):
        self.progressor.start("Generating twin widths")
        twin_lognormal = lognormal.Lognormal(self.twin_thickness["mu"], self.twin_thickness["sigma"], self.twin_thickness["min"], self.twin_thickness["max"])
        gap_lognormal = lognormal.Lognormal(self.parent_eq_radius["mu"], self.parent_eq_radius["sigma"], self.parent_eq_radius["min"], self.parent_eq_radius["max"])
        width_string = ""
        for i in range(self.max_grains):
            lamellae_widths       = 2 * self.max_twins * [None]
            lamellae_widths[::2]  = [gap_lognormal.get_val() for _ in range(self.max_twins)]
            lamellae_widths[1::2] = [twin_lognormal.get_val() for _ in range(self.max_twins)]
            width_string += "{} {}\n".format(i + 1, ":".join([str(lw) for lw in lamellae_widths]))
        self.write_results(TWIN_WIDTH_PATH, width_string)
        self.progressor.end()

    # Writes the crystallographic orientations
    def generate_crystal_ori(self):

        # Initialise
        self.progressor.start("Generating crystal orientations")
        main_crystal_ori = ""
        misorientation = angle.deg_to_rad(self.misorientation)

        # Iterate through grains
        for i in range(self.max_grains):

            # Generate a pair of euler angles with a misorientation of 60 degs
            euler_pair = orientation.generate_euler_pair(misorientation, self.crystal_type)
            euler_pair = [" ".join([str(e) for e in euler]) for euler in euler_pair]

            # Create alternating string of euler angles
            crystal_ori       = 2 * self.max_twins * [None]
            crystal_ori[::2]  = [euler_pair[0] for _ in range(self.max_twins)]
            crystal_ori[1::2] = [euler_pair[1] for _ in range(self.max_twins)]
            
            # Write euler angle pairs for parent and twin grains
            crystal_ori_path    = "{}_{}".format(CRYSTAL_ORI_PATH, i)
            self.write_results(crystal_ori_path, "\n".join(crystal_ori))
            main_crystal_ori += "{} file({},des=euler-bunge)\n".format(i + 1, crystal_ori_path)
        
        # Write index of euler angle files
        self.write_results(CRYSTAL_ORI_PATH, main_crystal_ori)
        self.progressor.end()

    # Writes the bash file (dim = 2 or 3)
    def generate_bash(self, dim = 3):
        self.progressor.start("Writing bash file")
        
        # Defines the morphology
        diameq      = "diameq:lognormal({},{})".format(2 * self.parent_eq_radius["mean"], 2 * self.parent_eq_radius["variance"]**0.5)
        sphericity  = "1-sphericity:lognormal({},{})".format(self.parent_sphericity["mean"], round(self.parent_sphericity["variance"]**(1/2), 5))
        lamellar    = "lamellar(w=file({}),v=crysdir(1,0,0))".format(TWIN_WIDTH_PATH)
        morpho      = "-morpho \"{},{}::{}\"".format(diameq, sphericity, lamellar)

        # Defines shape of volume
        dimensions  = "-dim {}".format(dim)
        domain_3d   = "-domain \"cube({},{},{})\"".format(self.volume_length, self.volume_length, self.volume_length)
        domain_2d   = "-domain \"square({},{})\"".format(self.volume_length, self.volume_length)
        domain      = domain_3d if dim == 3 else domain_2d
        shape       = "{} {}".format(dimensions, domain)

        # Defines other options
        morphooptiini   = "-morphooptiini coo:packing,weight:radeq"
        crystal_ori     = "-ori \"random::msfile({},des=euler-bunge)\"".format(CRYSTAL_ORI_PATH)
        output_format   = "-format tess,tesr -oridescriptor euler-bunge -tesrsize {} -tesrformat ascii".format(self.volume_length // 2)
        tess_options    = "{} {} {} {} {}".format(morpho, shape, morphooptiini, crystal_ori, output_format)
        vis_options     = "-datacellcol ori -datacellcolscheme 'ipf(y)' -cameraangle 14.5 -imagesize 800:800"

        # For creating the tessellation and mesh
        commands = "#!/bin/bash\n"
        commands += "neper -T -n from_morpho::from_morpho {} -o {} &&".format(tess_options, OUTPUT_PATH)
        commands += "neper -V {}.tess {} -print {}_1 &&".format(OUTPUT_PATH, vis_options, IMAGE_PREFIX)
        commands += "neper -V {}.tesr {} -print {}_2 &&".format(OUTPUT_PATH, vis_options, IMAGE_PREFIX)
        commands += "neper -M {}.tess &&".format(OUTPUT_PATH)
        commands += "neper -V {}.tess,{}.msh {} -print {}_3\n".format(OUTPUT_PATH, OUTPUT_PATH, vis_options, IMAGE_PREFIX)

        # For removing the other files
        helper_files = [RUN_FILE, TWIN_WIDTH_PATH, CRYSTAL_ORI_PATH]
        helper_files += ["{}_{}".format(CRYSTAL_ORI_PATH, i) for i in range(self.max_grains)]
        commands += "\n".join(["rm {}".format(file) for file in helper_files])

        # Write commands to a bash file
        self.write_results(RUN_FILE, commands)
        self.progressor.end()
