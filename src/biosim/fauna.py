# -*- coding: utf-8 -*-a

__author__ = 'Hans Kristian Lunda, Mikko Rekstad'
__email__ = 'hans.kristian.lunda@nmbu.no, mikkreks@nmbu.no'

import numpy as np
from math import exp


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

    def __init__(self, weight=0, age=0, seed=1):
        """
        This function initializes the Fauna object.
        """
        np.random.seed(seed=seed)
        self.age = age
        self.weight = weight
        self.state = False
        self.have_mated = False
        self.have_migrated = False
        self.have_eaten = False

    def birth(self, population):
        """
        Will return a baby if the creature is supposed to give birth.
        :param population: int
        :return:
        """
        birth_weight = self.find_birth_weight(population)
        if birth_weight > 0 and not self.have_mated:
            self.weight -= self.xi * birth_weight
            self.have_mated = True
            return self.__class__(weight=birth_weight, age=0)

    def find_birth_weight(self, population):
        """
        The function calculates the probability of giving birth,
        and the birth weight.
        :param population: int
        :return: float
        """
        birth_probability = min(1, self.gamma
                                * self.fitness * (population - 1))

        birth_weight = np.random.normal(self.w_birth, self.sigma_birth)

        if self.weight > self.zeta * (self.w_birth + self.sigma_birth):
            if birth_probability > np.random.rand() and self.age > 0:
                return birth_weight
        return 0

    @property
    def fitness(self):
        """
        Returns the creatures fitness
        :return: float
        """
        if self.weight <= 0:
            return 0.0
        else:
            q_pos = 1.0 / (1.0 + exp(self.phi_age * (self.age - self.a_half)))
            q_neg = 1.0 / (1.0 + exp(-self.phi_weight
                                     * (self.weight - self.w_half)))
            phi = q_pos * q_neg
            return phi

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
        reduction = (self.weight * self.eta)
        self.weight -= reduction

    def get_age(self):
        """
        Returns the creatures age
        :return: int
        """
        return self.age

    @property
    def survival_chance(self):
        return 1 - (self.omega * (1 - self.fitness))

    def death(self):
        """
        Returns True/False if the creature dies.
        :return: boolean
        """
        fitness = self.fitness
        death_number = np.random.random()
        if fitness <= 0:
            return True
        else:
            if death_number > self.survival_chance:
                return True
            elif self.weight < 0:
                return True
            else:
                return False

    def wants_to_migrate(self):
        """
        Returns True if the creature wants to migrate.
        :return: boolean
        """
        return (self.mu * self.fitness) > np.random.random()


class Herbivore(Fauna):

    def __init__(self, weight, age=0):
        self.w_birth = 8.0
        self.sigma_birth = 1.5
        self.beta = 0.9
        self.eta = 0.05
        self.a_half = 40.0
        self.phi_age = 0.2
        self.w_half = 10
        self.phi_weight = 0.1
        self.mu = 0.25
        self.lambda1 = 1.0
        self.gamma = 0.2
        self.zeta = 3.5
        self.xi = 1.2
        self.omega = 0.4
        self.F = 10.0
        self.DeltaPhiMax = None
        super().__init__(weight, age)


class Carnivore(Fauna):
    """
    This class contains all methods which are related to the carnivore objects.
    """
    def __init__(self, weight, age=0):
        self.w_birth = 6.0
        self.sigma_birth = 1.0
        self.beta = 0.75
        self.eta = 0.125
        self.a_half = 60.0
        self.phi_age = 0.8
        self.w_half = 4.0
        self.phi_weight = 0.4
        self.mu = 0.4
        self.lambda1 = 1.0
        self.gamma = 0.8
        self.zeta = 3.5
        self.xi = 1.1
        self.omega = 0.9
        self.F = 50.0
        self.DeltaPhiMax = 10.0
        super().__init__(weight, age)

    def eat(self, fodder_amount=0, herbivore_already_eaten=0):
        """
        This function will increase the creatures weight when it eats.
        """
        if fodder_amount > 50:
            fodder_amount = 50
        else:
            fodder_amount = fodder_amount

        if(fodder_amount + herbivore_already_eaten) > self.F:
            fodder_amount = self.F - herbivore_already_eaten
        self.weight += self.beta * fodder_amount
        return fodder_amount
