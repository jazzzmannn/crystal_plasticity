"""
 Title:         Generator
 Description:   Generates the RVE using Neper
 Author:        Janzen Choi

"""

# Libraries
import os, random
import packages.progressor as progressor
import packages.lognormal as lognormal
import packages.pairer as pairer
import packages.angle as angle
import packages.commander as commander

# Output files
RESULTS_DIR         = "results/"
OUTPUT_PATH         = RESULTS_DIR + "output"
IMAGE_PREFIX        = RESULTS_DIR + "img"

# Auxiliary files
AUXILIARY_DIR       = RESULTS_DIR + "auxiliary/"
PARENT_DIAM_PATH    = AUXILIARY_DIR + "parent"
TWIN_WIDTH_PATH     = AUXILIARY_DIR + "twin_width"
CRYSTAL_ORI_PATH    = AUXILIARY_DIR + "crystal_ori"

# Other constants
MAX_EXPECTED_TWINS  = 10

# The Generator Class
class Generator:

    # Constructor
    def __init__(self, dimensions, volume_length):
        self.progressor = progressor.Progressor()
        self.progressor.start("Initialising the system")
        
        # Initialise
        self.volume_length = volume_length
        dim         = "-dim {}".format(dimensions)
        domain_3d   = "-domain \"cube({},{},{})\"".format(self.volume_length, self.volume_length, self.volume_length)
        domain_2d   = "-domain \"square({},{})\"".format(self.volume_length, self.volume_length)
        domain      = domain_3d if dimensions == 3 else domain_2d
        self.shape  = "{} {}".format(dim, domain)

        # Prepares the environment
        create_empty_directory(RESULTS_DIR)
        create_empty_directory(AUXILIARY_DIR)
        remove_mesh_files()
        self.auxiliary_files = []
        self.progressor.end()
    
    # For writing a file to the helper directory
    def write_auxiliary(self, file_name, content):
        if not os.path.exists(AUXILIARY_DIR):
            os.mkdir(AUXILIARY_DIR)
        with open(file_name, "w+") as file:
            file.write(content)
        self.auxiliary_files.append(file_name)

    # Finishes generating the RVE
    def end_generator(self):
        self.progressor.start("Cleaning up the system")
        # for file in self.auxiliary_files:
        #     os.remove(file)
        # os.rmdir(AUXILIARY_DIR)
        self.progressor.end()
        self.progressor.end_all()

    # Generates the tessellation of the parent grains
    def tessellate_parents(self, parent_eq_radius_list, parent_sphericity):
        self.progressor.start("Tessellating the parent grains")
        
        # Define the morphology
        diameq      = "diameq:" + "+".join(["lognormal({},{})".format(2 * stat["mean"], 2 * stat["variance"]**0.5) for stat in parent_eq_radius_list])
        sphericity  = "1-sphericity:lognormal({},{})".format(parent_sphericity["mean"], parent_sphericity["variance"]**0.5)
        morpho      = "-morpho \"{},{}\"".format(diameq, sphericity)
        optiini     = "-morphooptiini coo:packing,weight:radeq"

        # Assemble and run the command
        command = "neper -T -n from_morpho {} {} -statcell diameq,sphericity -o {}".format(morpho, self.shape, PARENT_DIAM_PATH)
        commander.run(command)
        self.auxiliary_files.append(PARENT_DIAM_PATH + ".stcell")
        self.auxiliary_files.append(PARENT_DIAM_PATH + ".tess")
        self.progressor.end()

    # Visualises the parent grains
    def visualise_parents(self):
        self.progressor.start("Visualising the parent grains")
        options = "-datacellcol ori -datacellcolscheme 'ipf(y)' -cameraangle 14.5 -imagesize 800:800"
        command = "neper -V {}.tess {} -print {}_1".format(PARENT_DIAM_PATH, options, IMAGE_PREFIX)
        commander.run(command)
        self.progressor.end()

    # Generates the twins
    def generate_twins(self, twin_thickness):
        self.progressor.start("Generating the twin widths")
        
        # Read parent diametres and sphericities
        file = open(PARENT_DIAM_PATH + ".stcell", "r")
        parent_diametre_list, parent_sphericity_list = [], []
        for line in file.readlines():
            values = line.replace("\n", "").split(" ")
            parent_diametre_list.append(float(values[0]))
            parent_sphericity_list.append(float(values[1]))
        self.num_grains = len(parent_diametre_list)
        file.close()

        # Generate twin width distributions
        twin_lognormal = lognormal.Lognormal(twin_thickness["mu"], twin_thickness["sigma"], twin_thickness["min"], twin_thickness["max"])
        
        # Generate twin widths and gaps
        width_string = "{} {}\n".format(1, self.volume_length)
        for i in range(1, self.num_grains):
            num_expected_twins = random.randrange(MAX_EXPECTED_TWINS + 1)
            if num_expected_twins == 0:
                width_string += "{} {}\n".format(i + 1, self.volume_length)
                continue
            factor = parent_diametre_list[i] / parent_sphericity_list[i]
            lamellae_widths       = 2 * num_expected_twins * [None]
            lamellae_widths[::2]  = twin_lognormal.get_norm_vals(num_expected_twins, factor)
            lamellae_widths[1::2] = twin_lognormal.get_vals(num_expected_twins)
            width_string += "{} {}\n".format(i + 1, ":".join([str(lw) for lw in lamellae_widths]))

        # Write generated data
        self.write_auxiliary(TWIN_WIDTH_PATH, width_string)
        self.progressor.end()

    # Writes the crystallographic orientations
    def generate_crystal_orientations(self, misorientation, crystal_type):
        self.progressor.start("Generating the crystal orientations")

        # Initialise
        main_crystal_ori = ""
        misorientation = angle.deg_to_rad(misorientation)

        # Iterate through grains
        for i in range(self.num_grains):

            # Generate a pair of euler angles with a misorientation of 60 degs
            euler_pair = pairer.generate_euler_pair(misorientation, crystal_type)
            euler_pair = angle.rad_to_deg(euler_pair)
            euler_pair = [" ".join([str(e) for e in euler]) for euler in euler_pair]

            # Write alternating string of euler angles
            crystal_ori = (euler_pair[0] + "\n" + euler_pair[1] + "\n") * MAX_EXPECTED_TWINS
            crystal_ori_path = "{}_{}".format(CRYSTAL_ORI_PATH, i)
            self.write_auxiliary(crystal_ori_path, crystal_ori)
            main_crystal_ori += "{} file({},des=euler-bunge)\n".format(i + 1, crystal_ori_path)
        
        # Write index of euler angle files
        self.write_auxiliary(CRYSTAL_ORI_PATH, main_crystal_ori)
        self.progressor.end()

    # Generates the tessellation with parents and twins
    def tessellate_volume(self):
        self.progressor.start("Tessellating the multi-scale volume")

        # Define the morphology and crystal orientation
        morpho          = "-morpho \"voronoi::lamellar(w=file({}),v=crysdir(1,0,0))\"".format(TWIN_WIDTH_PATH)
        optiini         = "-morphooptiini \"file({})\"".format(PARENT_DIAM_PATH + ".tess")
        crystal_ori     = "-ori \"random::msfile({},des=euler-bunge)\"".format(CRYSTAL_ORI_PATH)
        output_format   = "-oridescriptor euler-bunge -format tess,tesr -tesrsize {} -tesrformat ascii".format(self.volume_length // 2)

        # Assemble and run command
        options = "{} {} {} {} {}".format(morpho, optiini, crystal_ori, output_format, self.shape)
        command = "neper -T -n {}::from_morpho {} -o {}".format(self.num_grains, options, OUTPUT_PATH)
        commander.run(command)
        self.progressor.end()
    
    # Visualises the tessellation
    def visualise_volume(self):
        self.progressor.start("Visualising multi-scale tessellation")
        options = "-datacellcol ori -datacellcolscheme 'ipf(y)' -cameraangle 14.5 -imagesize 800:800"
        command = "neper -V {}.tess {} -print {}_2".format(OUTPUT_PATH, options, IMAGE_PREFIX)
        commander.run(command)
        self.progressor.end()

    # Mesh the volume
    def mesh_volume(self):
        self.progressor.start("Meshing the multi-scale tessellation")
        command = "neper -M {}.tess".format(OUTPUT_PATH)
        commander.run(command)
        self.progressor.end()
    
    # Visualise the mesh
    def visualise_mesh(self):
        self.progressor.start("Visualising multi-scale mesh")
        options = "-dataelsetcol ori -dataelsetcolscheme 'ipf(y)' -cameraangle 14.5 -imagesize 800:800"
        command = "neper -V {}.tess,{}.msh {} -print {}_3".format(OUTPUT_PATH, OUTPUT_PATH, options, IMAGE_PREFIX)
        commander.run(command)
        self.progressor.end()

# Removes .geo and .msh files from current directory
def remove_mesh_files():
    files = [file for file in os.listdir(".") if os.path.isfile(file)]
    for file in files:
        if file.endswith(".geo") or file.endswith(".msh"):
            os.remove(file)

# Creates an empty directory
def create_empty_directory(directory_path):
    if not os.path.exists(directory_path):
        os.mkdir(directory_path)
    for file in os.listdir(directory_path):
        try:
            os.remove(directory_path + file)
        except:
            pass