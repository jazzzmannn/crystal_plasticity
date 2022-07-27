"""
 Title:         Generator
 Description:   For generating the RVE using Neper
 Author:        Janzen Choi

"""

# Libraries
import os
import subprocess
import packages.progressor as progressor
import packages.lognormal as lognormal
import packages.orientation.csl as csl
import packages.orientation.misorienter as misorienter
import packages.orientation.angle as angle

# Directories
RESULTS_DIR         = "results"
AUXILIARY_DIR       = "auxiliary"
OUTPUT_DIR          = "output"

# Files
PARENT_DIAM_FILE    = "parent"
TWIN_WIDTH_FILE     = "twin_width"
CRYSTAL_ORI_FILE    = "crystal_ori"
CRYSTAL_MORI_FILE   = "crystal_mori"
OUTPUT_FILE         = "output"
IMAGE_FILE          = "img"

# Other constants
MAX_EXPECTED_TWINS  = 10
MAX_RESULTS         = 999

# The Generator Class
class Generator:

    # Constructor
    def __init__(self, dimensions, shape_length):
        self.progressor = progressor.Progressor()
        self.progressor.start("Initialising the system")

        # Initialise
        self.shape_length = shape_length
        self.dimensions = dimensions
        dim         = "-dim {}".format(dimensions)
        domain_3d   = "-domain \"cube({},{},{})\"".format(self.shape_length, self.shape_length, self.shape_length)
        domain_2d   = "-domain \"square({},{})\"".format(self.shape_length, self.shape_length)
        domain      = domain_3d if dimensions == 3 else domain_2d
        self.shape  = "{} {}".format(dim, domain)

        # Determine directory and file names
        dirs = [dir for dir in os.listdir(RESULTS_DIR)]
        self.output_file        = "{}_{}".format(OUTPUT_DIR, str(len(dirs) + 1).zfill(len(str(MAX_RESULTS))))
        self.output_dir         = "{}/{}".format(RESULTS_DIR, self.output_file)
        self.output_path        = "{}/{}".format(self.output_dir, OUTPUT_FILE)
        self.image_path         = "{}/{}".format(self.output_dir, IMAGE_FILE)
        self.auxiliary_dir      = "{}/{}".format(self.output_dir, AUXILIARY_DIR)
        self.parent_diam_path   = "{}/{}".format(self.auxiliary_dir, PARENT_DIAM_FILE)
        self.twin_width_path    = "{}/{}".format(self.auxiliary_dir, TWIN_WIDTH_FILE)
        self.crystal_ori_path   = "{}/{}".format(self.auxiliary_dir, CRYSTAL_ORI_FILE)
        self.crystal_mori_path  = "{}/{}".format(self.auxiliary_dir, CRYSTAL_MORI_FILE)

        # Prepares the environment
        os.mkdir(self.output_dir)
        os.mkdir(self.auxiliary_dir)
        remove_mesh_files()
        self.progressor.end()
    
    # For writing a file to the helper directory
    def write_auxiliary(self, file_name, content):
        if not os.path.exists(self.auxiliary_dir):
            os.mkdir(self.auxiliary_dir)
        with open(file_name, "w+") as file:
            file.write(content)

    # Generates the tessellation of the parent grains
    def tessellate_parents(self, parent_eq_radius, parent_sphericity):
        self.progressor.start("Tessellating the parent grains")
        
        # Define the morphology
        diameq      = "diameq:lognormal({},{})".format(2 * parent_eq_radius["mean"], round(2 * parent_eq_radius["variance"]**0.5, 5))
        sphericity  = "1-sphericity:lognormal({},{})".format(parent_sphericity["mean"], round(parent_sphericity["variance"]**0.5, 5))
        morpho      = "-morpho \"{},{}\"".format(diameq, sphericity)
        reg         = "-reg 1"

        # Assemble and run the command
        command = "neper -T -n from_morpho {} {} {} -statcell diameq,sphericity -o {}".format(morpho, self.shape, reg, self.parent_diam_path)
        run(command)
        self.progressor.end()

    # Visualises the parent grains
    def visualise_parents(self):
        self.progressor.start("Visualising the parent grains")
        options = "-datacellcol ori -datacellcolscheme 'ipf(y)' -cameraangle 14.5 -imagesize 800:800"
        command = "neper -V {}.tess {} -print {}_1".format(self.parent_diam_path, options, self.image_path)
        run(command)
        self.progressor.end()

    # Generates the twins
    def generate_twins(self, twin_thickness):
        self.progressor.start("Generating the twin widths")
        
        # Read parent diametres and sphericities
        file = open(self.parent_diam_path + ".stcell", "r")
        parent_diametre_list, parent_sphericity_list = [], []
        for line in file.readlines():
            values = line.replace("\n", "").split(" ")
            parent_diametre_list.append(float(values[0]))
            parent_sphericity_list.append(float(values[1]))
        max_parent_diametre = max(parent_diametre_list)
        self.num_grains = len(parent_diametre_list)
        file.close()

        # Generate twin width distributions
        twin_lognormal = lognormal.Lognormal(twin_thickness["mu"], twin_thickness["sigma"], twin_thickness["min"], twin_thickness["max"])
        
        # Generate twin widths and gaps
        width_string = "{} {}\n".format(1, self.shape_length)
        for i in range(1, self.num_grains):
            num_expected_twins = round(MAX_EXPECTED_TWINS * parent_diametre_list[i] / max_parent_diametre)
            if num_expected_twins == 0:
                width_string += "{} {}\n".format(i + 1, self.shape_length)
                continue
            factor = parent_diametre_list[i] / parent_sphericity_list[i]
            lamellae_widths       = 2 * num_expected_twins * [None]
            lamellae_widths[::2]  = twin_lognormal.get_norm_vals(num_expected_twins, factor)
            lamellae_widths[1::2] = twin_lognormal.get_vals(num_expected_twins)
            width_string += "{} {}\n".format(i + 1, ":".join([str(lw) for lw in lamellae_widths]))

        # Write generated data
        self.write_auxiliary(self.twin_width_path, width_string)
        self.progressor.end()

    # Writes the crystallographic orientations
    def generate_crystal_orientations(self, csl_sigma, crystal_type = ""):
        self.progressor.start("Generating the crystal orientations")

        # Initialise
        crystal_ori_index = ""
        crystal_mori = ""

        # Iterate through grains
        for i in range(self.num_grains):

            # Generate a pair of euler angles with a defined misorientation
            euler_pair_raw = csl.get_csl_euler_angles(csl_sigma)
            euler_pair = angle.rad_to_deg(euler_pair_raw)
            euler_pair = [" ".join([str(e) for e in euler]) for euler in euler_pair]

            # Write alternating string of euler angles
            crystal_ori = (euler_pair[0] + "\n" + euler_pair[1] + "\n") * MAX_EXPECTED_TWINS
            crystal_ori_path = "{}_{}".format(self.crystal_ori_path, i)
            self.write_auxiliary(crystal_ori_path, crystal_ori)
            crystal_ori_index += "{} file({},des=euler-bunge)\n".format(i + 1, crystal_ori_path)

            # If crystal type defined, export misorientation
            if crystal_type != "":
                mori = misorienter.get_misorientation_angle(euler_pair_raw[0], euler_pair_raw[1], crystal_type)
                crystal_mori += str(angle.rad_to_deg(mori)) + "\n"
        
        # Write files
        self.write_auxiliary(self.crystal_ori_path, crystal_ori_index)
        if crystal_type != "":
            self.write_auxiliary(self.crystal_mori_path, crystal_mori)
        self.progressor.end()

    # Generates the tessellation with parents and twins
    def tessellate_volume(self):
        self.progressor.start("Tessellating the multi-scale volume")

        # Define the morphology and crystal orientation
        morpho          = "-morpho \"voronoi::lamellar(w=file({}),v=crysdir(1,0,0))\"".format(self.twin_width_path)
        optiini         = "-morphooptiini \"file({})\"".format(self.parent_diam_path + ".tess")
        crystal_ori     = "-ori \"random::msfile({},des=euler-bunge)\"".format(self.crystal_ori_path)
        output_format   = "-oridescriptor euler-bunge -format tess,tesr -tesrsize {} -tesrformat ascii".format(self.shape_length // 2)

        # Assemble and run command
        options = "{} {} {} {} {}".format(morpho, self.shape, optiini, crystal_ori, output_format)
        command = "neper -T -n {}::from_morpho {} -o {}".format(self.num_grains, options, self.output_path)
        run(command)
        self.progressor.end()
    
    # Visualises the tessellation
    def visualise_volume(self):
        self.progressor.start("Visualising multi-scale tessellation")
        options = "-datacellcol ori -datacellcolscheme 'ipf(y)' -cameraangle 14.5 -imagesize 800:800"
        command = "neper -V {}.tess {} -print {}_2".format(self.output_path, options, self.image_path)
        run(command)
        self.progressor.end()

    # Mesh the volume
    def mesh_volume(self):
        self.progressor.start("Meshing the multi-scale tessellation")
        command = "neper -M {}.tess".format(self.output_path)
        run(command)
        self.progressor.end()
    
    # Visualise the mesh
    def visualise_mesh(self):
        self.progressor.start("Visualising multi-scale mesh")
        options = "-dataelsetcol ori -dataelsetcolscheme 'ipf(y)' -cameraangle 14.5 -imagesize 800:800"
        command = "neper -V {}.tess,{}.msh {} -print {}_3".format(self.output_path, self.output_path, options, self.image_path)
        run(command)
        self.progressor.end()
    
    # Finishes generating the RVE
    def end_generator(self):
        self.progressor.start("Cleaning up the system")
        remove_mesh_files()
        os.rename(self.output_dir, "{} ({}d,{})".format(self.output_dir, self.dimensions, self.shape_length))
        self.progressor.end()
        self.progressor.end_all(self.output_file)

# Removes .geo and .msh files from current directory
def remove_mesh_files():
    files = [file for file in os.listdir(".") if os.path.isfile(file)]
    for file in files:
        if file.endswith(".geo") or file.endswith(".msh"):
            os.remove(file)

# Runs a command using a single thread
def run(command):
    subprocess.run(["OMP_NUM_THREADS=1 " + command], shell = True, check = True)