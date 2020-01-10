
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

    def __init__(self, coordinates=None, landscape=None, fodder=None):
        self.coordinates = coordinates
        self.landscape = landscape
        self.fodder = fodder
        self.number_of_herbivores = None
        self.number_of_carnivores = None
        self.population = None

    def get_creatures(self):
        """
        Returns the total number of creatures in the cell
        :return: int
        """
        return self.number_of_carnivores + self.number_of_herbivores

    def get_number_of_carnivores(self):
        """
        Returns the number of carnivores in the cell
        :return: int
        """
        return self.number_of_carnivores

    def get_number_of_herbivores(self):
        """
        Returns the number of herbivores in the cell
        :return: int
        """
        return self.number_of_herbivores

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

    def add_pop(self, cell_pop):
        """
        Calls the Fauna class to add animals to the cell.
        :param cell_pop: dictionary containing species, age, and weight
        :return:
        """
        for item in cell_pop:
            species = item['species']
            weight = item['weight']
            age = item['age']
            self.population.append(Fauna(species, weight, age))

    def remove_pop(self):
        """
        Removes an animal from the population list if it is dead.
        :return:
        """
        for i in self.population:
            if i.death():
                del i

