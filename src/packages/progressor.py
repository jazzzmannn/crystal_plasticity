"""
 Title:         Progress Visualiser
 Description:   For updating steps of a process
 Author:        Janzen Choi

"""

# Libraries
import time, os

# Constants
DEFAULT_PATH        = "/"
DEFAULT_INDEX       = 1
DEFAULT_MAX_CHARS   = 40

# For visualising the progress of a process
class Progressor:

    # Constructor
    def __init__(self, index = DEFAULT_INDEX, max_chars = DEFAULT_MAX_CHARS):
        self.start_time = time.time()
        self.module_start_time = self.start_time
        self.index = index
        self.max_chars = max_chars
        self.messages = ""

    # Updates and returns the time string
    def update_time(self):
        time_string = str(round((time.time() - self.module_start_time) * 1000)) + "ms"
        return time_string
    
    # Prints and stores message
    def update(self, message):
        os.system('cls' if os.name == 'nt' else 'clear')
        self.messages += message
        print("\n  Progress Report:\n")
        print(self.messages)

    # Starts a step in the process
    def start(self, message):
        padding = " " * (self.max_chars - len(message))
        self.update("   {}) {} ... {}".format(self.index, message, padding))
        self.module_start_time = time.time()

    # Ends a step in the process
    def end(self):
        time_string = str(round((time.time() - self.module_start_time) * 1000)) + "ms"
        self.update("Done! ({})\n".format(time_string))
        self.index += 1