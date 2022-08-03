# Introduction

The following repository is maintained by Janzen Choi as part of his PhD candidature, supervised by Jay Kruzic, Ondrej Muránksy, and Mark Messner. The document contains code for the development and parameter optimisation of a microstructure-informed crystal plasticity model for the prediction of elevated-temperature creep.

# Download

Before any of the code can be run, the following instructions must be executed.

First, install Neper via [LINK](https://github.com/neperfepx/neper).

Next, run `git clone https://github.com/janzennnnn/crystal_plasticity`, to clone the repository.

Finally, run `cd crystal_plasticity/src` to go to the directory where the code is located by running.

# Testing the Algorithmic code

Run `python3 test.py` to run the main, algorithmic code used.

# Generating an RVE in Neper

Code has been developed to generate an RVE in Neper, which uses lamellae to represent annealling twin structures. It is worth noting that the developers of Neper contributed significantly to the script, especially for answering so many of my questions on the discussion board [LINK](https://github.com/neperfepx/neper/discussions).

To begin, open the script, `generator.py`, and change the parameters based on the desired properties of the RVE. These parameters include the grain and twin statistics, the CSL value, the crystal type, the dimensions of the tessellation / mesh, as well as the length of the plane / volume. Once the parameters have been defined, run `python3 generator.py` to begin generating the RVE.

The script will create an `output` directory inside the `results` directory, which will contain all the generated tessellations, meshes, and visualisations. The `output` directory will also contain an `auxiliary` directory filled with helper files - this directory can be deleted after the program finishes to save space.

Throughout, the script will continuously display the progress of the process in the terminal. When the script finishes, it will be indicated in the terminal. Note that multiple instances of the program can be run with no significant impact on the process time.

# Analysing the RVE

Code has also been developed to analyse a 3D RVE. Specifically, the code slices the volume into a many 2D maps, and analyses the statistics of each map.

To begin, open the script, `slicer.py`, and point the script towards the directory with the RVE to be analysed. Then, change the parameters (i.e., resolution and number of slices) to fit the user's needs. Finally, run `python3 slicer.py` to begin slicing the RVE.

The script will create a `sliced` directory insides the `output` directory (created when generating the RVE using `generator.py`). The output of the script can be found inside the `sliced` directory.
