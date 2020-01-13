
__author__ = 'Hans Kristian Lunda, Mikko Rekstad'
__email__ = 'hans.kristian.lunda@nmbu.no, mikkreks@nmbu.no'

"""
This class contains information about the Cell object, methods for getting
information out of this cell, and methods for adding fodder to jungel and 
savannah cells.
"""



class Cell:
    alpha = 0.3
    f_max = [800.0, 300.0]
    gamma = [0.2, 0.8]


    def __init__(self, coordinates=None, landscape=None, fodder=None):
        self.coordinates = coordinates
        self.landscape = landscape
        self.fodder = fodder

    def get_fodder(self):
        """
        Amount of fodder in the cell
        :return: int
        """
        return self.fodder

    def add_fodder(self):
        """
        Function which adds fodder to the jungle and savannah cells.
        The jungle cells gets a fixed amount, and the savannah gets an amount
        based on the available fodder in the cell.
        :return:
        """
        if self.landscape == "J":
            self.fodder = self.f_max[0]
        elif self.landscape == "S":
            available_fodder = self.get_fodder()
            self.fodder = (available_fodder
                           + self.alpha * (self.f_max[1] - available_fodder))









