"""
 Title:         Generator
 Description:   For generating the RVE using Neper
 Author:        Janzen Choi

"""

# Libraries
import os, time, subprocess, csv
import packages.lognormal as lognormal
import packages.orientation.csl as csl
import packages.orientation.angle as angle

# Directories
RESULTS_DIR         = "results"
AUXILIARY_DIR       = "auxiliary"
OUTPUT_DIR          = "output"

# Other constants
MAX_EXPECTED_TWINS  = 10

# The Generator Class
class Generator:

    # Constructor
    def __init__(self, dimensions, shape_length, csl_sigma, parent_eq_radius, parent_sphericity, twin_thickness):

        # Initialise
        self.shape_length       = shape_length
        self.dimensions         = dimensions
        self.csl_sigma          = csl_sigma
        self.parent_eq_radius   = parent_eq_radius
        self.parent_sphericity  = parent_sphericity # 1-sphericity
        self.twin_thickness     = twin_thickness
        self.grain_list         = [] # dictionary of grain properties
        self.auxiliary_file_list = []

        # Define shape
        dim         = "-dim {}".format(dimensions)
        domain_3d   = "-domain \"cube({},{},{})\"".format(self.shape_length, self.shape_length, self.shape_length)
        domain_2d   = "-domain \"square({},{})\"".format(self.shape_length, self.shape_length)
        domain      = domain_3d if dimensions == 3 else domain_2d
        self.shape  = "{} {}".format(dim, domain)

        # Determine file name based on inputs and time
        curr_time = time.strftime("%y%m%d_%H%M%S", time.localtime(time.time()))
        inputs = "{}d{}".format(self.dimensions, self.shape_length)
        self.output_dir_name = "{}_{}_{}".format(OUTPUT_DIR, curr_time, inputs)

        # Define output files
        self.output_dir     = "{}/{}".format(RESULTS_DIR, self.output_dir_name)
        self.rve_path       = "{}/{}".format(self.output_dir, "rve")
        self.image_path     = "{}/{}".format(self.output_dir, "img")
        self.stats_path     = "{}/{}".format(self.output_dir, "stats")
        self.parent_path    = "{}/{}".format(self.output_dir, "parent")

        # Define auxiliary files
        self.auxiliary_dir      = "{}/{}".format(self.output_dir, AUXILIARY_DIR)
        self.twin_width_path    = "{}/{}".format(self.auxiliary_dir, "twin_width")
        self.crystal_ori_path   = "{}/{}".format(self.auxiliary_dir, "crystal_ori")

        # Prepares the environment
        safe_mkdir(RESULTS_DIR)
        safe_mkdir(self.output_dir)
        safe_mkdir(self.auxiliary_dir)
    
    # For writing a file to the helper directory
    def write_auxiliary(self, file_name, content):
        if not os.path.exists(self.auxiliary_dir):
            os.mkdir(self.auxiliary_dir)
        with open(file_name, "w+") as file:
            file.write(content)
        self.auxiliary_file_list.append(file_name)

    # Generates the tessellation of the parent grains
    def tessellate_parents(self):
        diameq      = "diameq:lognormal({},{})".format(2 * self.parent_eq_radius["mean"], round(2 * self.parent_eq_radius["variance"]**0.5, 5))
        sphericity  = "1-sphericity:lognormal({},{})".format(self.parent_sphericity["mean"], round(self.parent_sphericity["variance"]**0.5, 5))
        morpho      = "-morpho \"{},{}\"".format(diameq, sphericity)
        reg         = "-reg 1"
        tess_format = "-format tess,tesr -tesrsize {} -tesrformat ascii".format(self.shape_length)
        run("neper -T -n from_morpho {} {} {} {} -statcell diameq,sphericity -o {}".format(morpho, self.shape, reg, tess_format, self.parent_path))

    # Visualises the parent grains
    def visualise_parents(self):
        options = "-datacellcol ori -datacellcolscheme 'ipf(y)' -cameraangle 14.5 -imagesize 800:800"
        run("neper -V {}.tess {} -print {}_1".format(self.parent_path, options, self.image_path))

    # Extracts parent properties
    def extract_parent_properties(self):
        self.auxiliary_file_list.append(self.parent_path + ".stcell")
        with open(self.parent_path + ".stcell", "r") as file:
            all_lines = file.readlines()
            for i in range(len(all_lines)):
                values = all_lines[i].replace("\n", "").split(" ")
                self.grain_list.append({
                    "id":           i + 1,
                    "diameter":     float(values[0]),
                    "sphericity":   float(values[1]),
                })

    # Generates the twins
    def generate_twins(self):

        # Initialise
        width_string = ""
        max_parent_diameter = max([grain["diameter"] for grain in self.grain_list])
        twin_lognormal = lognormal.Lognormal(self.twin_thickness["mu"], self.twin_thickness["sigma"], self.twin_thickness["min"], self.twin_thickness["max"])

        # Generate values for the twin widths and gaps
        for i in range(len(self.grain_list)):
            grain = self.grain_list[i]

            # Determine the number of twins per grain
            num_expected_twins = round(MAX_EXPECTED_TWINS * grain["diameter"] / max_parent_diameter)
            
            # If there are no twins
            if num_expected_twins == 0 or i == 0:
                grain["num_twins"]      = 0
                grain["twin_widths"]    = []
                grain["twin_gaps"]      = []
                width_string += "{} {}\n".format(grain["id"], self.shape_length)
            
            # If there are twins
            else:
                grain["num_twins"]      = num_expected_twins
                grain["twin_widths"]    = twin_lognormal.get_vals(num_expected_twins)
                grain["twin_gaps"]      = twin_lognormal.get_norm_vals(num_expected_twins, grain["diameter"])
                lamellae_widths         = 2 * grain["num_twins"] * [None]
                lamellae_widths[::2]    = grain["twin_gaps"]
                lamellae_widths[1::2]   = grain["twin_widths"]
                width_string += "{} {}\n".format(grain["id"], ":".join([str(lw) for lw in lamellae_widths]))
        
        # Write the results
        self.write_auxiliary(self.twin_width_path, width_string)

    # Generates the crystallographic orientations
    def generate_orientations(self):
        crystal_ori_index = ""
        
        # Generate crystal orientations for parent and twins
        for grain in self.grain_list:

            # Generate crystal orientations
            euler_pair = csl.get_csl_euler_angles(self.csl_sigma)
            euler_pair = angle.rad_to_deg(euler_pair)
            grain["parent_ori"] = euler_pair[0]
            grain["twin_ori"] = euler_pair[1]

            # Convert to string
            parent_ori  = " ".join(str(ori) for ori in grain["parent_ori"])
            twin_ori    = " ".join(str(ori) for ori in grain["twin_ori"])
            crystal_ori = (parent_ori + "\n" + twin_ori + "\n") * MAX_EXPECTED_TWINS
            
            # Write the results
            crystal_ori_path = "{}_{}".format(self.crystal_ori_path, grain["id"])
            self.write_auxiliary(crystal_ori_path, crystal_ori)
            crystal_ori_index += "{} file({},des=euler-bunge)\n".format(grain["id"], crystal_ori_path)
        
        # Create an index directing to results
        self.write_auxiliary(self.crystal_ori_path, crystal_ori_index)

    # Export grain statistics
    def export_grain_statistics(self):

        # Export parent data
        parent_header = ["id", "eq_radius", "sphericity", "num_twins", "phi_1", "Phi", "phi_2"]
        parent_data = [[
            grain["id"],
            grain["diameter"] / 2,
            grain["sphericity"],
            grain["num_twins"],
            grain["parent_ori"][0],
            grain["parent_ori"][1],
            grain["parent_ori"][2]
        ] for grain in self.grain_list]
        write_to_csv(self.stats_path + "_parent.csv", parent_header, parent_data)
        
        # Export twin data
        twin_header = ["twin_id", "parent_id", "width", "gap", "phi_1", "Phi", "phi_2"]
        twin_data = []
        for grain in self.grain_list:
            for i in range(grain["num_twins"]):
                print(grain["num_twins"], grain["twin_widths"])
                twin_data.append([
                    len(twin_data) + 1,
                    grain["id"],
                    grain["twin_widths"][i],
                    grain["twin_gaps"][i],
                    grain["twin_ori"][0],
                    grain["twin_ori"][1],
                    grain["twin_ori"][2]
                ])
        write_to_csv(self.stats_path + "_twin.csv", twin_header, twin_data)

    # Generates the tessellation with parents and twins
    def tessellate_volume(self):

        # Define the morphology and crystal orientation
        morpho          = "-morpho \"voronoi::lamellar(w=file({}),v=crysdir(1,0,0))\"".format(self.twin_width_path)
        optiini         = "-morphooptiini \"file({})\"".format(self.parent_path + ".tess")
        crystal_ori     = "-ori \"random::msfile({},des=euler-bunge)\"".format(self.crystal_ori_path)
        output_format   = "-oridescriptor euler-bunge -format tess,tesr -tesrsize {} -tesrformat ascii".format(self.shape_length)

        # Assemble and run command
        options = "{} {} {} {} {}".format(morpho, self.shape, optiini, crystal_ori, output_format)
        run("neper -T -n {}::from_morpho {} -o {}".format(len(self.grain_list), options, self.rve_path))
    
    # Visualises the tessellation
    def visualise_volume(self):
        options = "-datacellcol ori -datacellcolscheme 'ipf(y)' -cameraangle 14.5 -imagesize 800:800"
        run("neper -V {}.tess {} -print {}_2".format(self.rve_path, options, self.image_path))

    # Mesh the volume (all .msh and .geo files go to the auxiliary directory)
    def mesh_volume(self):
        destination = "{}/{}".format(os.getcwd(), self.rve_path)
        os.chdir("{}/{}".format(os.getcwd(), self.auxiliary_dir))
        run("neper -M {}.tess".format(destination))
        os.chdir("../../..")
    
    # Visualise the mesh
    def visualise_mesh(self):
        options = "-dataelsetcol ori -dataelsetcolscheme 'ipf(y)' -cameraangle 14.5 -imagesize 800:800"
        run("neper -V {}.tess,{}.msh {} -print {}_3".format(self.rve_path, self.rve_path, options, self.image_path))

    # Removes all auxiliary files
    def remove_auxiliary_files(self):
        for file in self.auxiliary_file_list:
            os.remove(file)
        os.rmdir(self.auxiliary_dir)

# For safely making a directory
def safe_mkdir(dir_path):
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)

# For writing to CSV files
def write_to_csv(path, header, data):
    with open(path, "w+") as file:
        writer = csv.writer(file)
        writer.writerow(header)
        for row in data:
            writer.writerow(row)

# Runs a command using a single thread
def run(command):
    subprocess.run(["OMP_NUM_THREADS=1 " + command], shell = True, check = True)