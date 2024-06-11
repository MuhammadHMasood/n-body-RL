# An idea about code structure
# this is a class to represent a specific setup of an n-body problem
# It will store the full information, but will be able to convert it into
# various condensed forms suitable for machine learning
# Maybe we could also have a Chain class to hold a sequence of settings to have a complete simulation

class Setting:
    # this represents the time in which the AI will make predictions
    step = 0.01

    def __init__(self, g, *planets):
        self.g = g
        self.planets = planets

    def simulate(self):
        # will use the library to give the "perfect" prediction
        return NotImplemented

    def max_reduction(self):
        # will return the input vector with the maximum dimensional reduction
        return NotImplemented
