__author__ = 'Hans Kristian Lunda, Mikko Rekstad'
__email__ = 'hans.kristian.lunda@nmbu.no, mikkreks@nmbu.no'

from math import exp
import numpy as np


class Fauna:
    """
    This class will include the common properties for all creatures on
    Rossumøya.
    """
    w_birth = [8.0, 6.0]
    sigma_birth = [1.5, 1.0]
    beta = [0.9, 0.75]
    eta = [0.05, 0.125]
    a_half = [40.0, 60.0]
    phi_age = [0.2, 0.4]
    w_half = [10.0, 4.0]
    phi_weight = [0.1, 0.4]
    mu = [0.25, 0.4]
    lambda1 = [1.0, 1.0]
    gamma = [0.2, 0.8]
    zeta = [3.5, 3.5]
    xi = [1.2, 1.1]
    omega = [0.4, 0.9]
    F = [10.0, 50.0]
    DeltaPhiMax = [None, 10.0]

    def __init__(self, species=None, weight=None, age=0):
        if species == 'herbivore':
            self.species_id = 0
        else:
            self.species_id = 1
        self.species = species
        self.age = age
        self.weight = weight
        self.fitness = self.calculate_fitness()
        self.state = False
        self.have_mated = True
        self.desired_location = tuple()

    def ageing(self):
        """
        Increases the creatures age
        :return:
        """
        self.age += 1

    def get_fitness(self):
        """
        Returns the creatures fitness
        :return: float
        """
        return self.fitness

    def get_weight(self):
        """
        Returns the creatures weight
        :return: float
        """
        return self.weight

    def reduce_weight(self):
        """
        Reduces the creatures weight
        :return:
        """
        test = self.weight
        self.weight -= (self.weight * self.eta[self.species_id])
        test -= self.weight
        # print('Animal has lost ', self.weight)

    def get_age(self):
        """
        Returns the creatures age
        :return: int
        """
        return self.age

    def calculate_fitness(self):
        """
        Function which computes the herbivore fitness according to the formula
        :return: float
        """
        # age = self.age
        # weight = self.weight
        # a_half = [40.0, 60.0]
        # w_half =[10.0, 4.0]
        # phi_age = [0.2, 0.4]
        # phi_weight = [0.1, 0.4]

        if self.weight <= 0:
            return 0
        else:
            q_pos = (1.0 / (1.0 + exp(self.phi_age[self.species_id]
                                      * (self.age
                                         - self.a_half[self.species_id]))))
            q_neg = (1.0 / (1.0 + exp(-self.phi_weight[self.species_id]
                                      * (self.weight
                                         - self.w_half[self.species_id]))))
            phi = q_pos * q_neg
            return phi

    def death(self):
        """
        Returns True/False if the creature dies.
        :return: boolean
        """
        fitness = self.get_fitness()
        print('Weight: ', self.weight, 'Fitness: ',fitness)
        if fitness <= 0:
            return True
        else:
            random_death_probability = np.random.random()
            death_probability = self.omega[self.species_id]*(1 - fitness)
            if random_death_probability < death_probability:
                return True
            else:
                return False

    def wants_to_migrate(self):
        """
        Depends that we already have calculated fitness.
        Returns True if the creature wants to migrate.
        :return: boolean
        """
        return (self.mu * self.fitness) > np.random.random()

class Herbivore(Fauna):

    def __init__(self, weight, fitness, age=0):
        super().__init__(weight, fitness, age)
        self.w_birth = 8.0
        self.sigma_birth = 1.5
        self.xi = 1.2

    def migrate(self, north, east, south, west):
        """
        Moves the creature to the most eligible adjacent position on the map.
        """
        pass

    def give_birth(self):
        """
        This function will calculate the birth weight of the baby
         and update the weight of the parent.
        :return: float
        """
        birth_weight = np.random.normal(self.w_birth, self.sigma_birth)
        self.weight -= birth_weight * self.xi
        self.have_mated = True
        # print('A baby has been born')
        return birth_weight

    def vegetarian_feast(self, fodder_amount=0):
        """
        This function will let the creature eat.
        """
        self.weight += 0.4 * fodder_amount
        """
        if fodder_amount > 10:
            fodder_amount =10
        if fodder_amount > 0:
            self.weight += 0.4 * fodder_amount
        """

