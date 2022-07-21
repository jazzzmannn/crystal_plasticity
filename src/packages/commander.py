"""
 Title:         Commander
 Description:   Uses the subprocess library to run commands
 Author:        Janzen Choi

"""

# Libraries
import subprocess

# Runs a command using a single thread
def run(command):
    subprocess.run(["OMP_NUM_THREADS=1 && " + command], shell = True, check = True)

# Prints with boldening
def bold_print(text):
    subprocess.run(["echo \"\\033[1m{}\\033[0m\"\n".format(text)], shell = True)