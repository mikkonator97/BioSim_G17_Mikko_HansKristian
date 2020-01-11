from math import exp
import numpy as np
from biosim import Cell


class Fauna:
    """
    This class will include the common properties for all creatures on
    Rossumøya.
    """

    omega = [0.4, 0.9]
    eta = [0.05, 0.125]

    def __init__(self, species=None, weight=None, age=0):
        if species == 'herbivore':
            self.species_id = 0
        else:
            self.species_id = 1
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

    def reduce_weight(self):
        # self.weight -= (self.weight*eta[self.species_id])
        self.weight -= (self.weight * self.eta[self.species_id])

    def get_age(self):
        return self.age

    def get_position(self):
        return self.position

    def calculate_fitness(self):
        """
        Function which computes the herbivore fitness according to the formula
        :return:
        """
        age = self.age
        weight = self.weight
        a_half = [40.0, 60.0]
        w_half =[10.0, 4.0]
        phi_age = [0.2, 0.4]
        phi_weight = [0.1, 0.4]

        if self.weight <= 0:
            return 0
        else:
            q_pos = (1.0 / (1.0 + exp(phi_age[self.species_id]*(age - a_half[self.species_id]))))
            q_neg = (1.0 / (1.0 + exp(-phi_weight[self.species_id]*(weight - w_half[self.species_id]))))
            phi = q_pos * q_neg
            return phi

    def death(self):
        fitness = self.get_fitness()
        if fitness <= 0:
            return True

        else:
            random_death_probability = np.random.random()
            death_probability = self.omega[self.species_id]*(1 - fitness)
            if random_death_probability < death_probability:
                return True




class Herbivore(Fauna):

    def __init__(self, weight, fitness, age=0):
        super().__init__(weight, fitness, age)

    def migrate(self, north, east, south, west):
        """
        Moves the creature to the most eligable adjecent position on the map.
        """
        pass

    def vegetarian_feast(self, fodder_amount=0):
        """
        This function will let the creature eat.
        """
        if fodder_amount > 10:
            fodder_amount =10
        if fodder_amount > 0:
            self.weight += 0.9 * fodder_amount

