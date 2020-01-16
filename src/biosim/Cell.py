
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

        self.population = []
        self.population_herbivores = []
        self.population_carnivores = []
        self.gamma_herbivore = 0.2
        self.adjacent_cells = []


    # def find_migration(self):
    #     highest_relevance = []
    #     print("adjacent cells", self.adjacent_cells)
    #
    #     # print('adjacent cells', adjecent_cells)
    #     for tup in self.adjacent_cells:
    #         print('tup', tup)
    #         i, j = tup
    #         if Map.cell_map[i][j].landscape == 'M' or 'O':
    #             break
    #         else:
    #             fodder = self.cell_map[i][j].attractiveness_herbivore()
    #             propensity = np.exp(Fauna.lambda1[0]*fodder)
    #             highest_relevance.append(propensity)
    #
    #     probability_to_move = []
    #     for i in highest_relevance:
    #         probability_to_move.append(highest_relevance[i]/sum(highest_relevance))
    #     return probability_to_move

    def number_creatures(self):
        """
        Returns the total number of creatures in the cell
        :return: int
        """
        return self.number_herbivores() + self.number_carnivores()

    def number_herbivores(self):
        return len(self.population_herbivores)

    def number_carnivores(self):
        return len(self.population_carnivores)

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
            f_max = self.f_max
            self.fodder = (available_fodder + self.alpha[3] * (f_max - available_fodder))
        elif self.landscape == 4:
            self.fodder = self.f_max

    def get_adjacent_cells(self):
        """
        Returns the coordinates of the adjacent cells.
        :return:
        """
        return self.adjacent_cells

    def add_pop(self, cell_pop):
        """
        Adds a herbivore or a carnivore object to a cell.
        Species, weight and age are supplied from a dictionary.
        :param cell_pop: dictionary
        :return:
        """
        # creatures = cell_pop.get

        for creature in cell_pop:
            print(creature)
            species = creature.get('species')
            weight = creature.get('weight')
            age = creature.get('age')
            if species == 'herbivore':
                self.population_herbivores.append(Herbivore(weight=weight, age=age))
            # else:
            #     self.population.append(Carnivore(species, weight, age))
            #     self.number_of_carnivores += 1

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
        """
        Removes an animal from the list if it is supposed to die.
        :return:
        """

        index = 0
        number_of_herbivores = self.number_herbivores()
        while index < number_of_herbivores:
            self.population_herbivores[index].state = self.population_herbivores[index].death()
            if self.population_herbivores[index].state:
                self.population_herbivores.pop(index)
                number_of_herbivores -= 1
                index -= 1
            index += 1

    def feed_herbivores(self):
        """
        For each creature in the population of the cell, fodder is subtracted
        from the cell, and the creature gets an increase in weight.
        :return:
        """
        for creature in self.population_herbivores:
            print('Herbivore weighs: ', creature.weight)
            if self.fodder > 10:
                self.fodder -= 10
                fodder = 10
            else:
                fodder = self.fodder
                self.fodder = 0
            # beta = 0.9
            print('Creature weighing ', creature.weight,' going in for a snack.')
            print('Creatures fitness is ', creature.fitness)
            creature.weight += creature.beta * fodder
            print('Creature just ate and gained: ', creature.beta * fodder, ' now weighs: ', creature.weight)

    def feed_carnivores(self):
        pass

    def mating_season(self):
        for herbivore in self.population_herbivores:
            new_creature = (herbivore.birth(self.number_herbivores()))
            if new_creature != None:
                print('---X--------------->', len(self.population_herbivores))
                self.population_herbivores.append(new_creature)
                print('New pop: ', self.number_herbivores())

    def ranked_fitness(self):
        """
        Ranks the fitness of creatures from highest to lowest.
        :return:
        """
        self.population_herbivores.sort(key=lambda x: x.fitness, reverse=True)

    def attractiveness_herbivore(self, f=10.0):
        """
        Calculates the relative attractiveness for herbivores based on the
        amount of fodder, number of herbivores and their relative appetite.
        :param f: float
        :return: float
        """
        return self.fodder / ((self.number_of_herbivores+1) * f)

    def attractiveness_carnivore(self, f=50.0):
        """
        Calculates the relative attractiveness for carnivores based on the
        weight of the herbivores, number of carnivores and their
        relative appetite.
        :param f: float
        :return: float
        """
        food = 0
        for creature in self.population:
            if creature.species == 'herbivore':
                food += creature.weight
        return food / ((self.number_of_carnivores+1) * f)

    def add_age(self):
        """
        Increases the age for all the creatures in the population list.
        :return:
        """
        # print('All creatures will age')
        for creature in self.population:
            creature.age += 1

    def lose_weight(self):
        """
        Calls the reduce weight method for each creature in the population
        list.
        :return:
        """
        for creature in self.population_herbivores:
            creature.reduce_weight()
        for creature in self.population_carnivores:
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
        self.f_max = self.f_max[3]
        self.habitable = habitable
        self.fodder = self.f_max


class Jungle(Cell):
    def __init__(self, habitable=True):
        super().__init__(coordinates=None, landscape=4, fodder=0)
        self.habitable = habitable
        self.f_max = self.f_max[4]
        self.fodder = self.f_max


