"""
 Title:         The Main File
 Description:   Outputs all the necessary files for Neper to generate the volume
 Author:        Janzen Choi

"""

# Libraries
import packages.progressor as progressor
import packages.generator as generator

# Properties
DIMENSIONS      = 3
SHAPE_LENGTH    = 500 # microns
CSL_SIGMA       = "3"

# Statistics
PARENT_EQ_RADIUS    = { "mu": 2.94032, "sigma": 0.99847, "mean": 31.1491, "variance": 1659.11, "min": 2.60941, "max": 302.370 }
PARENT_SPHERICITY   = { "mu": -1.6229, "sigma": 0.40402, "mean": 0.21410, "variance": 0.00813, "min": 0.02316, "max": 0.57725 } # 1-sphericity
TWIN_THICKNESS      = { "mu": 1.46831, "sigma": 0.79859, "mean": 5.97259, "variance": 31.8271, "min": 0.63383, "max": 86.4995 }

# Main function
if __name__ == "__main__":
    prog = progressor.Progressor()
    gen = generator.Generator(DIMENSIONS, SHAPE_LENGTH, CSL_SIGMA, PARENT_EQ_RADIUS, PARENT_SPHERICITY, TWIN_THICKNESS)
    prog.queue(gen.tessellate_parents,          message = "Tessellating the parent grains")
    prog.queue(gen.visualise_parents,           message = "Visualising parent grains")
    prog.queue(gen.extract_parent_properties,   message = "Extracting parent grain properties")
    prog.queue(gen.generate_twins,              message = "Generating twins structures")
    prog.queue(gen.generate_orientations,       message = "Generating crystal orientations")
    prog.queue(gen.export_grain_statistics,     message = "Exporting the statistics")
    prog.queue(gen.tessellate_volume,           message = "Tessellating multi-scale volume")
    prog.queue(gen.visualise_volume,            message = "Visualising multi-scale tessellation")
    # prog.queue(gen.mesh_volume,                 message = "Meshing multi-scale tessellation")
    # prog.queue(gen.visualise_mesh,              message = "Visualising multi-scale mesh")
    prog.queue(gen.remove_auxiliary_files,      message = "Removing auxiliary files")
    prog.run(gen.output_dir_name)
