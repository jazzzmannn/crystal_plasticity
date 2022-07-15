"""
 Title:         Custom Lognormal Distribution
 Description:   For defining a custom lognormal distribution
 Author:        Janzen Choi

"""

# Libraries
import numpy as np
import random

# Lognormal Class
class Lognormal:

    # Constructor
    def __init__(self, mu, sigma, min = 0, max = 1000000, amount = 1000):
        self.distribution = np.random.lognormal(mu, sigma, amount)
        self.distribution = [d for d in self.distribution if d > min and d < max]

    # Gets a value from the lognormal distribution
    def get_val(self):
        return round(self.distribution[random.randrange(len(self.distribution))], 5)
