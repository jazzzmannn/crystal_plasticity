"""
 Title:         Data Exporter after
 Description:   Exports statistics from a raster tessellation file
 Author:        Janzen Choi

"""

# Libraries
import csv
import packages.progressor as progressor

# Constants
RESOLUTION  = 1
RESULTS_DIR = "results/"
TESR_PATH   = RESULTS_DIR + "output.tesr"
CSV_PREFIX  = RESULTS_DIR + "output"

# Main function
def main():
    
    # Get volume shape information
    prog = progressor.Progressor(max_chars = 35)
    prog.start("Initiate the system")
    vol_data        = extract_data("general", TESR_PATH)
    dimensions      = int(vol_data[1])
    volume_length   = int(vol_data[2])
    cell_data       = extract_data("cell", TESR_PATH)
    num_grains      = int(cell_data[1])
    prog.end()

    # Get orientation (euler-gunge)
    prog.start("Extracting Euler angles")
    ori_data = extract_data("ori", TESR_PATH)
    ori_data = [float(o) for o in ori_data[2:]]
    prog.end()

    # Get positions and derive coordinates
    prog.start("Extracting position information")
    pos_data = extract_data("data", TESR_PATH)
    pos_data = [int(p) for p in pos_data[2:]]
    prog.end()
    
    # Prepare data for each voxel
    prog.start("Preparing data for each voxel")
    voxel_data_list = []
    for i in range(len(pos_data)):
        voxel_ori = ori_data[3 * (pos_data[i] - 1): 3 * pos_data[i]]
        voxel_data = {
            "voxel_id": i,
            "grain_id": pos_data[i],
            "x": i % volume_length,
            "y": i // volume_length % volume_length,
            "z": i // volume_length // volume_length,
            "euler_1": round(voxel_ori[0], 3),
            "euler_2": round(voxel_ori[1], 3),
            "euler_3": round(voxel_ori[2], 3),
        }
        voxel_data_list.append(voxel_data)
    prog.end()

    # Convert dictionary to CSV
    prog.start("Processing data for CSV")
    headers = list(voxel_data_list[0].keys())
    rows = [[vd[1] for vd in voxel_data.items()] for voxel_data in voxel_data_list]
    prog.end()

    # Write to CSV
    prog.start("Writing to CSV file")
    csv_path = "{}_{}d_{}.csv".format(CSV_PREFIX, dimensions, num_grains)
    file = open(csv_path, "w+")
    writer = csv.writer(file)
    writer.writerow(headers)
    for row in rows:
        writer.writerow(row)
    file.close()
    prog.end()

# Searches for a keyword in a text file and extracts the contained data
def extract_data(keyword, filename):
    
    # Read the file
    file = open(filename, "r")
    data = file.read()
    file.close()

    # Searches for the data encased by the keyword
    start = data.find(keyword)
    data = data[start:]
    end = data.find("*")
    data = data[:end]

    # Process the extracted data and return
    data = data.replace("\n", " ")
    data = data.split(" ")
    data = [d for d in data if d != ""]
    return data

# Calls the main function
if __name__ == "__main__":
    main()