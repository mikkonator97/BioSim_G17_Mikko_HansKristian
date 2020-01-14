
__author__ = 'Hans Kristian Lunda, Mikko Rekstad'
__email__ = 'hans.kristian.lunda@nmbu.no, mikkreks@nmbu.no'

"""
This class contains information about the Cell object, methods for getting
information out of this cell, and methods for adding fodder to jungel and 
savannah cells.
"""

from biosim.fauna import Fauna, Herbivore
import numpy as np


class Cell:



    def __init__(self, coordinates=None, landscape=None, fodder=None):
        self.f_max = [0.0, 0.0, 0.0, 300.0, 800.0]
        self.alpha = [None, None, None, 0.3, None]
        # self.f_max = self.f_max[landscape]
        # self.alpha = self.alpha[landscape]
        self.coordinates = coordinates
        self.landscape = landscape
        self.fodder = fodder
        self.number_of_herbivores = 0
        self.number_of_carnivores = 0
        self.population = []
        self.gamma_herbivore = 0.2
        self.adjecent_cells = []

    def find_migration(self):
        highest_relevance = []
        for tup in self.adjacent_cells:
            i, j = tup
            if self.cell_map[i][j].landscape == 'M' or 'O':
                break
            else:
                fodder = self.cell_map[i][j].attractiveness_herbivore()
                propensity = np.exp(Fauna.lambda1[0]*fodder)
                highest_relevance.append(propensity)

        probability_to_move = []
        for i in highest_relevance:
            probability_to_move.append(highest_relevance[i]/sum(highest_relevance))
        return probability_to_move

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

        if self.landscape == 3:
            available_fodder = float(self.get_fodder())
            f_max = self.f_max[3]
            self.fodder = (available_fodder + self.alpha[3] * (f_max - available_fodder))
        elif self.landscape == 4:
            self.fodder = int(self.f_max[4])


    def add_pop(self, cell_pop):
        # creatures = cell_pop.get

        for creature in cell_pop:
            species = creature.get('species')
            weight = creature.get('weight')
            age = creature.get('age')
            self.population.append(Herbivore(species, weight, age))
            self.number_of_herbivores += 1
        print('Current population: ', self.population)


    def remove_pop(self):
        """
        Removes an animal from the population list if it is dead.
        :return:
        """
        for creature in self.population:
            will_die = creature.death()
            print('Død: ', will_die)
            if will_die:
                creature.state = 'dying'

        for index in range(self.number_of_herbivores):
            if self.population[index].state == 'dying':
                if index != 0:
                    self.population.pop(index)
                    self.number_of_herbivores = len(self.population)

    def alter_population(self):
        index = 0
        while index < self.number_of_herbivores:
            self.population[index].state =self.population[index].death()
            if self.population[index].state:
                self.population.pop(index)
                self.number_of_herbivores = len(self.population)
                index -= 1
            index += 1

    def feed_herbivores(self):
        for creature in self.population:
            if self.fodder > 10:
                # print('A creature got 10 fodder')
                self.fodder -= 10
                fodder = 10
                #print('Ate 10 fodder')
            else:
                fodder = self.fodder
                # print('A creature got ', fodder, ' food this year.')
                self.fodder = 0
            omega = 0.4
            creature.weight += omega * fodder

    def feed_carnivores(self):
        pass

    def mating_season(self):
        if self.number_of_herbivores > 1:
            for herbivore in self.population:
                if herbivore.species == 'herbivore' and herbivore.have_mated == False:
                    if min(1, 0.2 * herbivore.fitness *
                            (self.number_of_herbivores - 1)) >\
                            np.random.rand() and herbivore.age > 0:
                        birth_weight = herbivore.give_birth()
                        self.population.append(Herbivore('herbivore',
                                                         birth_weight, 0))
                        self.number_of_herbivores = len(self.population)

    def ranked_fitness(self):
        self.population.sort(key=lambda x: x.fitness)

    def attractiveness_herbivore(self, F=10.0):
        return self.fodder / ((self.number_of_herbivores+1)* F)

    def attractiveness_carnivore(self, F=50.0):
        food = 0
        for creature in self.population:
            if creature.species == 'herbivore':
                food += creature.weight
        return food / ((self.number_of_carnivores+1)* F)

    def add_age(self):
        # print('All creatures will age')
        for creature in self.population:
            creature.age += 1

    def lose_weight(self):
        for creature in self.population:
            creature.reduce_weight()



class Ocean(Cell):
    def __init__(self, habitable=False):
        super().__init__(coordinates=None, landscape=0, fodder=0)
        self.habitable = habitable


class Mountain(Cell):
    def __init__(self, habitable=False):
        super().__init__(coordinates=None, landscape=1, fodder=0)
        self.habitable = habitable


class Desert(Cell):
    def __init__(self, habitable=True):
        super().__init__(coordinates=None, landscape=2, fodder=0)
        self.habitable = habitable


class Savannah(Cell):

    def __init__(self, habitable = True):
        super().__init__(coordinates=None, landscape=3, fodder=0)
        self.habitable = habitable


class Jungle(Cell):
    def __init__(self, habitable=True):
        super().__init__(coordinates=None, landscape=4, fodder=0)
        self.habitable = habitable


