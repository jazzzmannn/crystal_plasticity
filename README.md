## Introduction

The following repository is maintained by Janzen Choi as part of his PhD candidature, supervised by Jay Kruzic, Ondrej Muránksy, Luiz Borterlan Neto, and Mark Messner. The document contains code for the development and parameter optimisation of a microstructure-informed crystal plasticity model for the prediction of elevated-temperature creep.

### Generating an RVE in Neper

The following instructions are for developing an RVE in Neper, which uses lamellae to represent annealling twin structures.

1) Install Neper ([LINK](https://github.com/neperfepx/neper)).
2) Clone the repository by running `git clone https://github.com/janzennnnn/crystal_plasticity` in the terminal.
3) Go to the directory where the code is located by running `cd crystal_plasticity/src`.
5) Open the script, `main.py`, and change the parameters based on the desired properties of the RVE. These parameters include the grain and twin statistics, the dimensions of the tessellation / mesh, as well as the length of the plane / volume.
6) Open the terminal and run the script via `python3 main.py`.
7) The script will create an `output` directory inside the `results` directory, which will contain all the generated tessellations, meshes, visualisations, and auxiliary files.
8) Throughput, the script will continuously display the progress of the process in the terminal, and will indicate when the process finishes.
