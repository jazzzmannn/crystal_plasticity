## Introduction

The following repository is maintained by Janzen Choi as part of his PhD candidature, supervised by Jay Kruzic, Ondrej Muránksy, Luiz Borterlan Neto, and Mark Messner. The document contains code for the development and parameter optimisation of a microstructure-informed crystal plasticity model for the prediction of elevated-temperature creep.

### Generating an RVE in Neper

The following instructions are for developing an RVE in Neper, which uses lamellae to represent annealling twin structures. It is worth noting that the developers of Neper contributed significantly to the script, especially for answering so many of my questions on the discussion board [LINK](https://github.com/neperfepx/neper/discussions).

1) Install Neper ([LINK](https://github.com/neperfepx/neper)).
2) Clone the repository by running `git clone https://github.com/janzennnnn/crystal_plasticity` in the terminal.
3) Go to the directory where the code is located by running `cd crystal_plasticity/src`.
5) Open the script, `main.py`, and change the parameters based on the desired properties of the RVE. These parameters include the grain and twin statistics, the CSL value, the crystal type, the dimensions of the tessellation / mesh, as well as the length of the plane / volume.
6) Open the terminal and run the script via `python3 main.py`.

In following these instructions, the script will create an `output` directory inside the `results` directory, which will contain all the generated tessellations, meshes, and visualisations. The `output` directory will also contain an `auxiliary` directory filled with helper files - this directory can be deleted after the program finishes to save space. Throughput, the script will continuously display the progress of the process in the terminal. When the script finishes, it will be indicated in the terminal. Note that multiple instances of the program can be run with no significant impact on the process time.

Additionally, to test the main algorithmic code in the program, the user can run the test file. This simply involves going to the `crystal_plasticity/src` directory and running  the test file via `python3 test.py`.
