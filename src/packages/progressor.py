"""
 Title:         Progress Visualiser
 Description:   For updating steps of a process
 Author:        Janzen Choi

"""

# Libraries
import time

# For visualising the progress of a process
class Progressor:

    # Constructor
    def __init__(self):
        self.start_time = time.time()
        self.module_start_time = self.start_time
        self.index = 1
        self.max_chars = 35

    # Updates and returns the time string
    def update_time(self):
        time_string = str(round((time.time() - self.module_start_time) * 1000)) + "ms"
        return time_string
    
    # Starts a step in the process
    def start(self, message):
        padding = " " * (self.max_chars - len(message))
        print(" {}) {} ... {}".format(self.index, message, padding), end="", flush=True)
        self.module_start_time = time.time()

    # Ends a step in the process
    def end(self):
        time_string = str(round((time.time() - self.module_start_time) * 1000)) + "ms"
        print("Done! ({})".format(time_string))
        self.index += 1