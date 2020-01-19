

__author__ = 'Hans Kristian Lunda, Mikko Rekstad'
__email__ = 'hans.kristian.lunda@nmbu.no, mikkreks@nmbu.no'

import numpy as np
import math


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
        self.w_birth = w_birth[species_id]
        self.sigma_birth = sigma_birth[species_id]
        self.beta = beta[species_id]
        self.eta = eta[species_id]
        self.a_half = a_half[species_id]
        self.phi_age = phi_age[species_id]
        self.w_half = w_half[species_id]
        self.phi_weight = phi_weight[species_id]
        self.mu = mu[species_id]
        self.lambda1 = lamda1[species_id]
        self.gamma = gamma[species_id]
        self.zeta = zeta[species_id]
        self.xi = xi[species_id]
        self.omega = omega[species_id]
        self.F = F[species_id]
        self.DeltaPhiMax = DeltaPhiMax[species_id]
        """
        np.random.seed(seed=seed)
        # self.species = species
        self.age = age
        self.weight = weight
        self.fitness = self.calculate_fitness()
        # print(self.fitness)
        self.state = False
        self.have_mated = False
        self.have_migrated = False
        self.have_eaten = False
        self.desired_location = tuple()
        self.desired_cell = None
        self.survival_chance = 1
        self.adjacent_cells = None
        self.adjacent_cell_attractiveness_for_herbivores = None
        self.adjacent_cell_attractiveness_for_carnivores = None

    def birth(self, population):
        birth_weight = self.find_birth_weight(population)
        if birth_weight > 0 and not self.have_mated:
            self.weight -= self.xi * birth_weight
            self.have_mated = True
            return self.__class__(weight=birth_weight, age=0)



    def find_birth_weight(self, population):
        birth_probability = min(1, 0.2 * self.fitness * (population - 1))
        birth_weight = np.random.normal(self.w_birth, self.sigma_birth)


        if self.weight > self.zeta * (9.5):
            if birth_probability > np.random.rand() and self.age > 0:
                return birth_weight
        return 0

    # remove this function? has a similar in cell
    # def ageing(self):
    #     """
    #     Increases the creatures age
    #     :return:
    #     """
    #     self.age += 1

    def get_fitness(self):
        """
        Returns the creatures fitness
        :return: float
        """
        self.fitness = self.calculate_fitness()
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
        reduction = (self.weight * self.eta)
        self.weight -= reduction

    def get_age(self):
        """
        Returns the creatures age
        :return: int
        """
        return self.age

    # @property
    def calculate_fitness(self):
        """
        Function which computes the herbivore fitness according to the formula
        :return: float
        """

        if self.weight <= 0:
            return 0
        else:
            q_pos = 1.0 / (1.0 + math.exp(self.phi_age * (self.age - self.a_half)))
            q_neg = 1.0 / (1.0 + math.exp(-self.phi_weight * (self.weight - self.w_half)))
            phi = q_pos * q_neg
            return phi

    def death(self):
        """
        Returns True/False if the creature dies.
        :return: boolean
        """
        fitness = self.get_fitness()
        death_number = np.random.random()
        self.survival_chance = 1 - (self.omega * (1 - fitness))
        # print('Death number: ', death_number)
        # print('Weight: ', self.weight, 'Fitness: ',fitness)
        if fitness <= 0:
            # print('Dies because of negative fitness.')
            return True
        else:
            if death_number > self.survival_chance:
                # print('-----> New Creature death, fitness: ', fitness)
                # print('Random number: ', death_number)
                # print('The probability: ', self.survival_chance)
                # print('Will die at age: ',self.age,' and fitness: ', fitness)
                return True
            elif self.weight < 0:
                # print('Dies because of negative weight.')
                return True
            else:
                # print('Survives and thrives!')
                return False

    def wants_to_migrate(self):
        """
        Depends that we already have calculated fitness.
        Returns True if the creature wants to migrate.
        :return: boolean
        """
        return (self.mu * self.fitness) > np.random.random()


    #def propensity(self, relative_abundance_of_fodder):
    #    """
    #    Calculates the propensity based on the amount of fodder
    #    :param relative_abundance_of_fodder:
    #    :return: float
    #    """
    #    try:
    #        propensity = math.exp(self.lambda1 * relative_abundance_of_fodder)
    #    except OverflowError:
    #        print("        except OverflowError")
    #        propensity = 1000

     #   return propensity

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

        # self.w_birth = 8.0
        # self.sigma_birth = 1.5
        # self.xi = 1.2

    def migrate(self):
        """
        If the creature has not migrated and wants to migrate,
        then returns the desired cell.
        """
        # print("migrate function called!")
        if self.have_migrated is False:
            if self.wants_to_migrate():
                # print("Creature wants to migrate")
                destination_probabilities = self.get_destination_probabilities()
                # print("destination probabilities: ",destination_probabilities)
                self.desired_cell = np.random.choice(self.adjacent_cells, p=destination_probabilities)
                # print("index destination: ", self.desired_cell)
                return self.desired_cell

    def get_destination_probabilities(self):
        """
        Calculates the probability of moving to each of the adjacent cells,
        then returns a list with these probabilities.
        :return: list
        """
        highest_relevance = []
        probability_to_move = []
        herb_adjacent_cells = self.adjacent_cell_attractiveness_for_herbivores
        # print(adjacent_cells)
        # print('adjacent cells', herb_adjacent_cells)
        if herb_adjacent_cells is None:
            probability_to_move = [0.25, 0.25, 0.25, 0.25]
            return probability_to_move
        else:
            for relative_abundance_of_fodder in herb_adjacent_cells:
                propensity = self.propensity(relative_abundance_of_fodder)
                highest_relevance.append(propensity)
            # print("highest relevance: ", highest_relevance)
            for value in highest_relevance:
                probability_to_move.append(value/sum(highest_relevance))
            # print("probabilities to move: ", probability_to_move)
            return probability_to_move

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


    def eat(self, fodder_amount=0):
        """
        This function will let the creature eat.
        """
        self.weight += self.beta * fodder_amount
        # print('Creature just ate and gained: ', self.beta * fodder_amount)


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
        # print('Creature just ate and gained: ', self.beta * fodder_amount)

    def give_birth(self):
        """
        This function will calculate the birth weight of the baby
         and update the weight of the parent.
        :return: float
        """
        birth_weight = np.random.normal(self.w_birth, self.sigma_birth)
        self.weight -= birth_weight * self.xi
        self.have_mated = True
        # print('A baby carnivore has been born')
        return birth_weight

    def migrate(self):
        """
        If the creature has not migrated and wants to migrate,
        then returns the desired cell.
        """
        # print("migrate function called!")
        if self.have_migrated is False:
            if self.wants_to_migrate():
                # print("Creature wants to migrate")
                destination_probabilities = self.get_destination_probabilities()
                # print("destination probabilities: ",destination_probabilities)
                self.desired_cell = np.random.choice(self.adjacent_cells, p=destination_probabilities)
                # print("index destination: ", self.desired_cell)
                return self.desired_cell

    def get_destination_probabilities(self):
        """
        Calculates the probability of moving to each of the adjacent cells,
        then returns a list with these probabilities.
        :return: list
        """
        highest_relevance = []
        adjacent_cells = self.adjacent_cell_attractiveness_for_carnivores
        # print(adjacent_cells)
        # print('adjacent cells', adjacent_cells)
        probability_to_move = []
        if adjacent_cells is None:
            probability_to_move = [0.25, 0.25, 0.25, 0.25]
            return probability_to_move
        else:
            for relative_abundance_of_fodder in adjacent_cells:
                propensity = self.propensity(relative_abundance_of_fodder)
                highest_relevance.append(propensity)
            # print("highest relevance: ", highest_relevance)
            """
            If there are many herbivores in a cell, it might cause infinite 
            propensity, which gives inf as a value. np.random.choice will
            then get NaN as a probability which causes error.
            """
            for index in range(len(highest_relevance)):
                if math.isinf(highest_relevance[index]):
                    highest_relevance[index] = 1000
            # print("highest relevance: ", highest_relevance)

            for value in highest_relevance:
                probability_to_move.append(value/sum(highest_relevance))
            # print("probabilities to move: ", probability_to_move)
            # print("probabilities to move: ", probability_to_move)
            return probability_to_move
