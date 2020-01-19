
__author__ = 'Hans Kristian Lunda, Mikko Rekstad'
__email__ = 'hans.kristian.lunda@nmbu.no, mikkreks@nmbu.no'

"""
This class contains information about the Cell object, methods for getting
information out of this cell, and methods for adding fodder to jungel and 
savannah cells.
"""

from biosim.fauna import Fauna, Herbivore, Carnivore
import numpy as np


class Cell:

    def __init__(self, coordinates=None, landscape=None, fodder=0):
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
        self.adjacent_cells2 = []
        self.probability_herbivores = [0, 0, 0, 0]
        # self.probability_carnivores = [0, 0, 0, 0]

        self.adjacent_cells_herbivore_attractiveness = []
        self.adjacent_cells_carnivore_attractiveness = []
        self.F_h = 10

        # self.abundance_herbivore = 0
        # self.abundance_carnivore = 0

    def send_adjacent_cells_to_fauna(self):
        for creature in self.population_herbivores:
            creature.adjacent_cells = self.adjacent_cells
            creature.adjacent_cell_attractiveness_for_herbivores = self.adjacent_cells_herbivore_attractiveness
        for creature in self.population_carnivores:
            creature.adjacent_cells = self.adjacent_cells
            creature.adjacent_cell_attractiveness_for_carnivores = self.adjacent_cells_carnivore_attractiveness

    # def get_abundance_herbivore(self):
    #     return self.fodder / ((self.number_herbivores() + 1) * self.F_h)
    #
    # def get_abundance_carnivore(self):
    #     """
    #     Returns the relative abundance of fodder for carnivores.
    #     :return:
    #     """
    #     return sum(self.population_herbivores.weight) / ((len(self.population_carnivores) + 1) * self.F_h)

    # def number_creatures(self):
    #     """
    #     Returns the total number of creatures in the cell
    #     :return: int
    #     """
    #     return self.number_herbivores() + self.number_carnivores()

    def number_herbivores(self):
        return len(self.population_herbivores)

    # def get_herbivores(self):
    #     return self.population_herbivores

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

    # def get_adjacent_cells(self):
    #     """
    #     Returns the coordinates of the adjacent cells.
    #     :return:
    #     """
    #     return self.adjacent_cells

    def add_pop(self, cell_pop):
        """
        Adds a herbivore or a carnivore object to a cell.
        Species, weight and age are supplied from a dictionary.
        :param cell_pop: dictionary
        :return:
        """
        for creature in cell_pop:
            species = creature.get('species')
            weight = creature.get('weight')
            age = creature.get('age')
            if species.lower() == 'herbivore':
                self.population_herbivores.append(Herbivore(weight=weight, age=age))
            else:
                self.population_carnivores.append(Carnivore(weight=weight, age=age))
                # self.number_of_carnivores += 1




    def alter_population(self):
        """
        Removes an animal from the list if it is supposed to die.
        :return:
        """

        index = 0
        number_of_herbivores = len(self.population_herbivores)
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
            # print('Herbivore weighs: ', creature.weight)
            if self.fodder > 10:
                self.fodder -= 10
                fodder = 10
            else:
                fodder = self.fodder
                self.fodder = 0
            # beta = 0.9
            # print('Creature weighing ', creature.weight,' going in for a snack.')
            # print('Creatures fitness is ', creature.fitness)
            creature.weight += creature.beta * fodder
            # print('Creature just ate and gained: ', creature.beta * fodder, ' now weighs: ', creature.weight)

    def feed_carnivores(self):
        """
        This function will feed the carnivores,
         where each carnivore will feast on the herbivores based on both carnivore and herbivore fitness.
        :return:
        """

        self.ranked_fitness_herbivores_weakest()
        self.ranked_fitness_carnivores()
        for carnivore in self.population_carnivores:
            herbivore_eaten = 0
            # print("new carnivore")
            for herbivore in self.population_herbivores:
                if herbivore_eaten >= 50:
                    print("herb_eaten over 50", herbivore_eaten)
                    break

                probability_of_successful_hunt = self.successful_hunt(carnivore, herbivore)
                if probability_of_successful_hunt == 0:
                    continue

                kill_probability = np.random.random()
                if kill_probability < probability_of_successful_hunt:
                    # print("A carnivore has killed: ")
                    herbivore_eaten += carnivore.eat(herbivore.weight, herbivore_eaten)
                    # print("herb_eaten", herbivore_eaten)
                    carnivore.calculate_fitness()
                    self.population_herbivores.remove(herbivore)

    def successful_hunt(self, carnivore, herbivore):
        """
        Function which returns the probability of a successful hunt where the carnivore will pray.
        :return: float
        """
        if herbivore.fitness >= carnivore.fitness:
            return 0.0
        elif carnivore.DeltaPhiMax > (carnivore.fitness - herbivore.fitness):
            return (carnivore.fitness - herbivore.fitness) / carnivore.DeltaPhiMax
        else:
            return 1.0

    def mating_season(self):
        for herbivore in self.population_herbivores:
            new_creature = (herbivore.birth(self.number_herbivores()))
            if new_creature != None:
                # print('---X--------------->', len(self.population_herbivores))
                self.population_herbivores.append(new_creature)
                # print('New pop: ', self.number_herbivores())
        for carnivore in self.population_carnivores:
            new_creature = (carnivore.birth(self.number_carnivores()))
            if new_creature != None:
                # print('---X--------------->', len(self.population_herbivores))
                self.population_carnivores.append(new_creature)

    def ranked_fitness_herbivores(self):
        self.population_herbivores.sort(key=lambda x: x.fitness, reverse=True)

    def ranked_fitness_herbivores_weakest(self):
        self.population_herbivores.sort(key=lambda x: x.fitness, reverse=False)

    def ranked_fitness_carnivores(self):
        self.population_carnivores.sort(key=lambda x: x.fitness, reverse=True)

    def attractiveness_herbivore(self, f=10.0):
        """
        Calculates the relative attractiveness for herbivores based on the
        amount of fodder, number of herbivores and their relative appetite.
        :param f: float
        :return: float
        """
        # self.chance_herbivore = self.fodder / ((self.number_of_herbivores()+1) * f)
        attractiveness = self.fodder / ((self.number_herbivores() + 1) * f)
        return attractiveness

    def attractiveness_carnivore(self, f=50.0):
        """
        Calculates the relative attractiveness for carnivores based on the
        weight of the herbivores, number of carnivores and their
        relative appetite.
        :param f: float
        :return: float
        """
        food = 0
        for creature in self.population_herbivores:
            food += creature.weight
        attractiveness = food / ((self.number_carnivores() + 1) * f)
        return attractiveness

    def add_age(self):
        """
        Increases the age for all the creatures in the population list.
        :return:
        """
        # print('All creatures will age')
        for creature in self.population_herbivores:
            creature.age += 1
        for creature in self.population_carnivores:
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
        self.coordinates = None
        self.habitable = habitable
        self.f_max = self.f_max[4]
        self.fodder = self.f_max
