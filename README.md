## Introduction

The following repository is maintained by Janzen Choi as part of his PhD candidature, supervised by Jay Kruzic, Ondrej Muránksy, Luiz Borterlan Neto, and Mark Messner. The document contains code for the development and parameter optimisation of a microstructure-informed crystal plasticity model for the prediction of elevated-temperature creep.

### Generating an RVE in Neper

The following instructions are for developing an RVE, which uses lamellae to represent annealling twin structures.

1) Install Neper ([LINK](https://github.com/neperfepx/neper)).
2) Go to the directory where the code is located ([LINK](https://github.com/jazzzmannn/crystal_plasticity/tree/main/src/neper_gen)).
3) Open the script, `main.py`, and change the parameters based on the desired properties of the RVE.
4) Open the terminal and run the script via `python3 main.py`. This should create a bash file, `run.sh`.
5) Run the bash file via `./run.sh`.
