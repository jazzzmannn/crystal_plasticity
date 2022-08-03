"""
 Title:         Data Exporter
 Description:   Exports statistics from a raster tessellation file
 Author:        Janzen Choi

"""

# Libraries
import csv

# Constants
RESOLUTION  = 1
RESULTS_DIR = "./"
TESR_PATH   = RESULTS_DIR + "rve.tesr"
CSV_PREFIX  = RESULTS_DIR + "output"

# Main function
def main():
    
    # Get volume shape information
    print("Extracting volume shape ...")
    vol_data        = extract_data("general", TESR_PATH)
    dimensions      = int(vol_data[1])
    volume_length   = int(vol_data[2])

    # Get orientation (euler-gunge)
    print("Extracting orientations ...")
    ori_data = extract_data("ori", TESR_PATH)
    ori_data = [float(o) for o in ori_data[2:]]

    # Get positions and derive coordinates
    print("Extracting positional information ...")
    pos_data = extract_data("data", TESR_PATH)
    pos_data = [int(p) for p in pos_data[2:]]

    # Write data of each voxel to CSV (directly, to avoid RAM issues)
    print("Writing data to CSV ...")
    csv_path = "{}_{}d{}.csv".format(CSV_PREFIX, dimensions, volume_length)
    with open(csv_path, "w+") as file:
        writer = csv.writer(file)

        # Write headers
        headers = ["voxel_id", "grain_id", "x", "y", "z", "euler_1", "euler_2", "euler_3"]
        writer.writerow(headers)

        # Iterate through each voxel
        for i in range(len(pos_data)):

            # Provides progress updates
            if i % (len(pos_data) / 100) == 0:
                print("  Update ({}%)".format(1 + round(100 * i / len(pos_data))))

            # Prepares the data
            voxel_ori = ori_data[3 * (pos_data[i] - 1): 3 * pos_data[i]]
            row = [
                i,
                pos_data[i],
                i % volume_length,
                i // volume_length % volume_length,
                i // volume_length // volume_length,
                round(voxel_ori[0], 3),
                round(voxel_ori[1], 3),
                round(voxel_ori[2], 3),
            ]

            # Writes the data
            writer.writerow(row)
    
    # Finish message
    print("Finished everything!")

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