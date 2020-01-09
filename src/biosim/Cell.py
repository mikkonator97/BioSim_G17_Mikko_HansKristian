
__author__ = 'Hans Kristian Lunda, Mikko Rekstad'
__email__ = 'hans.kristian.lunda@nmbu.no, mikkreks@nmbu.no'

"""
This class contains information about the Cell object, methods for getting
information out of this cell, and methods for adding fodder to jungel and 
savannah cells.
"""


class Cell:

    def __init__(self, coordinates=None, landscape=None, fodder=None):
        self.coordinates = coordinates
        self.landscape = landscape
        self.fodder = fodder
        self.number_of_herbivores = None
        self.number_of_carnivores = None

    def get_creatures(self):
        return self.number_of_carnivores + self.number_of_herbivores

    def get_number_of_carnivores(self):
        return self.number_of_carnivores

    def get_number_of_herbivores(self):
        return self.number_of_herbivores

    def get_fodder(self):
        return self.fodder

    def add_fodder_jungle(self):
        f_max = 800.0
        return self.fodder + f_max

    def add_fodder_savannah(self):
        alpha = 0.3
        f_max = 300.0
        available_fodder = self.get_fodder()
        self.fodder = (available_fodder + alpha * (f_max - available_fodder))
        return self.fodder
