"""
 Title:         Progress Visualiser
 Description:   For visualising the steps of a process
 Author:        Janzen Choi

"""

# Libraries
import time, os
import packages.printer as printer

# Constants
DEFAULT_PATH        = "/"
DEFAULT_START_INDEX = 1
DEFAULT_MAX_CHARS   = 40
DEFAULT_MAX_INDEX   = 99

# For visualising the progress of a process
class Progressor:

    # Constructor
    def __init__(self, index = DEFAULT_START_INDEX, max_index = DEFAULT_MAX_INDEX, max_chars = DEFAULT_MAX_CHARS):
        self.start_time = time.time()
        self.start_time_string = time.strftime("%H:%M:%S", time.localtime(self.start_time))
        self.module_start_time = self.start_time
        self.index = index
        self.max_chars = max_chars
        self.max_index = max_index
        self.messages = ""
        self.header_padding = " " * (len(str(self.max_index)))

    # Updates and returns the time string
    def update_time(self):
        time_string = str(round((time.time() - self.module_start_time) * 1000)) + "ms"
        return time_string
    
    # Prints and stores message
    def update(self, message):
        os.system('cls' if os.name == 'nt' else 'clear')
        self.messages += message
        printer.print("\n{}Progress Report (started at {}):\n".format(self.header_padding, self.start_time_string), ["bold", "orange"])
        printer.print(self.messages)

    # Starts a step in the process
    def start(self, message):
        index_padding = " " * (len(str(self.max_index)) - len(str(self.index)))
        completion_padding = "." * (self.max_chars - len(message))
        self.update("  {}{}) {} {} ".format(index_padding, self.index, message, completion_padding))
        printer.print("")
        self.module_start_time = time.time()

    # Ends a step in the process
    def end(self):
        time_string = str(round((time.time() - self.module_start_time) * 1000)) + "ms"
        self.update("Done! ({})\n".format(time_string))
        self.index += 1
    
    # Ends the process
    def end_all(self):
        time_diff = round(time.time() - self.start_time, 2)
        printer.print("{}Finished in {} seconds!\n".format(self.header_padding, time_diff), ["bold", "orange"])