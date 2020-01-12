
__author__ = 'Hans Kristian Lunda, Mikko Rekstad'
__email__ = 'hans.kristian.lunda@nmbu.no, mikkreks@nmbu.no'

"""
This class contains information about the Cell object, methods for getting
information out of this cell, and methods for adding fodder to jungel and 
savannah cells.
"""

from fauna import Herbivore

class Cell:
    alpha = 0.3
    f_max = [800.0, 300.0]

    def __init__(self, coordinates=None, landscape=None, fodder=None):
        self.coordinates = coordinates
        self.landscape = landscape
        self.fodder = fodder
        self.number_of_herbivores = 0
        self.number_of_carnivores = 0
        self.population = []

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
        for element in cell_pop:

            for creature in element['pop']:
                # print(item.get('species'))
                species = creature.get('species')
                weight = creature.get('weight')
                age = creature.get('age')
                # print(item['species'])
                #self.population.append(Fauna(species, weight, age))
                self.number_of_herbivores += 1

                if species == 'herbivore':
                    self.population.append(Herbivore(species, weight, age))
                    print('Added a herbivore to the population in this cell.')


    def remove_pop(self):
        """
        Removes an animal from the population list if it is dead.
        :return:
        """
        for creature in self.population:
            will_die = creature.death()
            print('Død: ', will_die)
            if will_die:
                # self.population.remove(creature)
                creature.state = 'dying'
                print('A creature is dying at age: ', creature.get_age())
                # print('Hallo')

        for index in range(self.number_of_herbivores):
            if self.population[index].state == 'dying':
                if index != 0:
                    print(self.population[index])
                    self.population.pop(index)
                    self.number_of_herbivores = len(self.population)
                    print('Remaining population: ',self.number_of_herbivores)

    def alter_population(self):

        # for index in range(self.number_of_herbivores):
        index = 0
        while index < self.number_of_herbivores:
            # print(self.number_of_herbivores)
            # print(self.population[index].death)
            if self.population[index].state == True:
                print(self.population[index].age,' should be dead')
                self.population.pop(index)
                self.number_of_herbivores = len(self.population)
                index += 1
            index += 1




    def ranked_fitness(self):
        self.population.sort(key=lambda x: x.fitness)

    def yearly_cycle(self):
        pass

