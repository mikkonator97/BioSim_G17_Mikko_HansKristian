from math import exp
import numpy as np
class Fauna:
    """
    This class will include the common properties for all creatures on
    Rossumøya.
    """

    omega = [0.4, 0.9]

    def __init__(self, position=None, species=None, weight=None, age=0):
        self.position = position
        self.species = species
        self.age = age
        self.weight = weight
        self.fitness = None

    def ageing(self):
        self.age += 1

    def get_fitness(self):
        return self.fitness

    def get_weight(self):
        return self.weight

    def get_age(self):
        return self.age

    def get_position(self):
        return self.position

    def death(self):
        fitness = self.get_fitness()
        if fitness <= 0:
            Cell.population.remove()
        random_death_probability = np.random.random()
        elif (self.species == 'Herbivore'):
            death_probability = self.omega[0]*(1 - fitness)
            if random_death_probability < death_probability:
                pass
            pass




class Herbivore(Fauna):

    def __init__(self, position, weight, fitness, age=0):
        super().__init__(position, weight, fitness)

    def herbivore_fitness(self, age, weight, fitness):
        """
        Function which computes the herbivore fitness according to the formula
        :return:
        """
        weight = Fauna.get_weight()
        if weight <= 0:
            return 0
        else:
            age = Fauna.get_age()
            a_half = 40.0
            w_half = 10.0
            fitness = Fauna.get_fitness()
            q_pos = (1.0 / (1.0 + exp(fitness(age - a_half))))
            q_neg = (1.0 / (1.0 + exp(-fitness(weight - w_half))))
            phi = q_pos * q_neg
            return phi

    def migrate(self, north, east, south, west):
        """
        Moves the creature to the most eligable adjecent position on the map.
        """
        pass

    def vegetarian_feast(self, fodder_amount):
        """
        This function will let the creature eat.
        """
        pass

