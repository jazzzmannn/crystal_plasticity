"""
 Title:         Slicer
 Description:   Slices a 3D raster tessellation
 Author:        Janzen Choi

"""

# Libraries
import subprocess, csv, os
import packages.progressor as progressor

# Constants
RESOLUTION  = 1
NUM_SLICES  = 10 # per axis
INPUT_DIR   = "./results/output_220802_140411_2d2000/"
OUTPUT_DIR  = INPUT_DIR + "output/"
INPUT_TESR  = INPUT_DIR + "parent"
OUTPUT_TESR = OUTPUT_DIR + "2d"
OUTPUT_IMG  = OUTPUT_DIR + "2d"
OUTPUT_CSV  = OUTPUT_DIR + "2d"

# Main function
def main():
    prog = progressor.Progressor()
    slicer = Slicer()
    prog.queue(slicer.set_up_slicer,        message = "Setting up the slicing environment")
    prog.queue(slicer.get_voxel_list,       message = "Reading RVE from raster tessellation")
    prog.queue(slicer.slice_voxel_list,     message = "Slicing RVE into 2D sheets of grains")
    prog.queue(slicer.slice_to_tesr,        message = "Converting slices into 2D raster tessellations")
    prog.queue(slicer.visualise_slices,     message = "Visualise 2D raster tessellations")
    prog.run()

# The Slicer Class
class Slicer:

    # Sets up the environment
    def set_up_slicer(self):
        if os.path.exists(OUTPUT_DIR):
            output_files = os.listdir(OUTPUT_DIR)
            for file in output_files:
                os.remove(OUTPUT_DIR + file)
        else:
            os.mkdir(OUTPUT_DIR)

    # Returns a list of voxels
    def get_voxel_list(self):

        # Get volume shape information
        vol_data = extract_data("general", INPUT_TESR + ".tesr")
        self.volume_length = int(vol_data[2])

        # Get positions and derive coordinates
        pos_data = extract_data("data", INPUT_TESR + ".tesr")
        pos_data = [int(p) for p in pos_data[2:]]
        
        # Prepare data for each voxel
        self.voxel_list = []
        for i in range(len(pos_data)):
            self.voxel_list.append({
                "voxel_id": i,
                "grain_id": pos_data[i],
                "x": i % self.volume_length,
                "y": i // self.volume_length % self.volume_length,
                "z": i // self.volume_length // self.volume_length,
            })

    # Takes a slice from the voxel list
    def slice_voxel_list(self):
        self.slice_list = []
        for axis in ["x", "y", "z"]:
            for value in range(0, self.volume_length, NUM_SLICES):
                slice = [voxel for voxel in self.voxel_list if voxel[axis] == value]
                self.slice_list.append(slice)
                break
            break
    
    # Converts the slices into raster tessellation files
    def slice_to_tesr(self):
        for i in range(len(self.slice_list)):

            # Convert slice to list of ids
            id_list = [voxel["grain_id"] for voxel in self.slice_list[i]]
            num_grains = max([int(id) for id in id_list])
            id_list = [str(id) for id in id_list]

            # Generate string
            data_string         = " **cell\n   {}\n **data\n   ascii\n{}\n".format(num_grains, " ".join(id_list))
            length_string       = "{} {} ".format(self.volume_length, self.volume_length)
            resolution_string   = "{} {} ".format(RESOLUTION, RESOLUTION)
            pre_data_string     = "***tesr\n **format\n   2.1\n **general\n   2\n   {}\n   {}\n".format(length_string, resolution_string)
            post_data_string    = "***end"

            # Write to file
            with open(OUTPUT_TESR + "_" + str(i + 1) + ".tesr", "w+") as file:
                file.write(pre_data_string)
                file.write(data_string)
                file.write(post_data_string)
    
    # Visualises the slices
    def visualise_slices(self):
        for i in range(len(self.slice_list)):
            file_name = OUTPUT_TESR + "_" + str(i + 1)
            options = "-cameraangle 14.5 -imagesize 800:800"
            run("neper -V {}.tesr {} -print {}_{}".format(file_name, options, file_name, i + 1))

# Searches for a keyword in a text file and extracts the contained data
def extract_data(keyword, filename):
    
    # Read the file
    with open(filename, "r") as file:
        data = file.read()

    # Searches for the data encased by the keyword
    start = data.find(keyword)
    data  = data[start:]
    end   = data.find("*")
    data  = data[:end]

    # Process the extracted data and return
    data = data.replace("\n", " ")
    data = data.split(" ")
    data = [d for d in data if d != ""]
    return data

# Converts a list of dictionaries to a CSV format
def dict_to_csv(dictionary_list):
    headers = list(dictionary_list[0].keys())
    data = [[d[1] for d in dictionary.items()] for dictionary in dictionary_list]
    return headers, data

# Writes to CSV
def write_to_csv(headers, data, path):
    with open(path, "w+") as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        for row in data:
            writer.writerow(row)

# Runs a command using a single thread
def run(command):
    subprocess.run(["OMP_NUM_THREADS=1 " + command], shell = True, check = True)

# Main function caller
if __name__ == "__main__":
    main()