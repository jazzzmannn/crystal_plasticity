"""
 Title:         Custom Lognormal Distribution
 Description:   For defining a custom lognormal distribution
 Author:        Janzen Choi

"""

# Libraries
import paramnormal
import numpy as np
import random

# Constants
DEFAULT_SIZE    = 1000
DEFAULT_MAX     = 1000000
DEFAULT_MIN     = 0

# Lognormal Class
class Lognormal:

    # Constructor
    def __init__(self, mu, sigma, min = DEFAULT_MIN, max = DEFAULT_MAX, amount = DEFAULT_SIZE):
        self.distribution = np.random.lognormal(mu, sigma, amount)
        self.distribution = [d for d in self.distribution if d >= min and d <= max]

    # Gets a value from the lognormal distribution
    def get_val(self):
        return round(self.distribution[random.randrange(len(self.distribution))], 5)

    # Gets values from the lognormal distribution
    def get_vals(self, size):
        return [self.get_val() for _ in range(size)]

    # Gets normalised values from the lognormal distribution
    def get_norm_vals(self, size, norm_value):
        values = self.get_vals(size)
        factor = norm_value / sum(values)
        return [value * factor for value in values]

# Fits a set of data to a lognormal distribution and returns the statistics
def fit_lognormal(data):
    params = paramnormal.lognormal.fit(data)
    return {
        "mu": params[0],
        "sigma": params[1],
        "mean": np.average(data),
        "stdev": np.std(data),
        "max": max(data),
        "min": min(data),
    }