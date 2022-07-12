"""
 Title:         Randomiser
 Description:   For defining a lognormal distribution
 Author:        Janzen Choi

"""

# Libraries
import numpy as np
import random

# Lognormal Class
class Lognormal:

    # Constructor
    def __init__(self, statistic):
        self.amount = 1000
        self.distribution = np.random.lognormal(statistic["mu"], statistic["sigma"], self.amount)

    # Gets a value from the lognormal distribution
    def get_val(self):
        return round(self.distribution[random.randrange(len(self.distribution))], 5)
