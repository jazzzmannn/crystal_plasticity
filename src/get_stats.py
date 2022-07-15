"""
 Title:         Data Exporter after
 Description:   Exports statistics from a raster tessellation file
 Author:        Janzen Choi

"""

# Libraries
import csv

# Constants
RESOLUTION  = 1
RESULTS_DIR = "results/"
TESR_PATH   = RESULTS_DIR + "output.tesr"
CSV_PREFIX  = RESULTS_DIR + "output"

# Main function
def main():

    # Get volume shape information
    vol_data        = extract_data("general", TESR_PATH)
    dimensions      = int(vol_data[1])
    volume_length   = int(vol_data[2])
    cell_data       = extract_data("cell", TESR_PATH)
    num_grains      = int(cell_data[1])

    # Get orientation (euler-gunge)
    ori_data = extract_data("ori", TESR_PATH)
    ori_data = [float(o) for o in ori_data[2:]]

    # Get positions and derive coordinates
    pos_data = extract_data("data", TESR_PATH)
    pos_data = [int(p) for p in pos_data[2:]]
    
    # Prepare data for each voxel
    voxel_data_list = []
    for i in range(len(pos_data)):
        voxel_ori = ori_data[3 * (pos_data[i] - 1): 3 * pos_data[i]]
        voxel_data = {
            "voxel_id": i,
            "grain_id": pos_data[i],
            "x": i % volume_length,
            "y": i // volume_length % volume_length,
            "z": i // volume_length // volume_length,
            "euler_1": voxel_ori[0],
            "euler_2": voxel_ori[1],
            "euler_3": voxel_ori[2],
        }
        voxel_data_list.append(voxel_data)

    # Convert dictionary to CSV
    headers = list(voxel_data_list[0].keys())
    rows = [[vd[1] for vd in voxel_data.items()] for voxel_data in voxel_data_list]

    # Write to CSV
    csv_path = "{}_{}d_{}".format(CSV_PREFIX, dimensions, num_grains)
    file = open(csv_path, "w+")
    writer = csv.writer(file)
    writer.writerow(headers)
    for row in rows:
        writer.writerow(row)
    file.close()

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