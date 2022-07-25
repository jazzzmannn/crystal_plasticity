"""
 Title:         Twin width exporter
 Description:   Exports the raw data from the generated twin_width file
 Author:        Janzen Choi

"""

# Libraries
import csv

# Constants
INPUT_PATH = "./auxiliary/twin_width"
OUTPUT_PATH = "./twin_widths.csv"

# Extract widths
twin_widths = []
with open(INPUT_PATH, "r") as file:
    all_lines = file.readlines()
    for line in all_lines:
        
        line = line.replace("\n","")
        line_array = line.split(" ")
        width_string = line_array[1]

        width_array = [float(w) for w in width_string.split(":")]
        width_array = [width_array[i] for i in range(len(width_array)) if i % 2 == 1]
        twin_widths += width_array

# Export extracted widths
file = open(OUTPUT_PATH, "w+")
writer = csv.writer(file)
writer.writerow(["twin_widths"])
for twin_width in twin_widths:
    writer.writerow([twin_width])
file.close()