

__author__ = 'Hans Kristian Lunda, Mikko Rekstad'
__email__ = 'hans.kristian.lunda@nmbu.no, mikkreks@nmbu.no'

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
        self.desired_location = tuple()
        self.survival_chance = 1
        self.adjacent_cell_attractiveness = None

    def birth(self, population):
        birth_weight = self.find_birth_weight(population)
        # print(birth_weight)
        if birth_weight > 0 and not self.have_mated:
            self.weight -= birth_weight
            print('A baby has been born weighs: ', birth_weight)
            self.have_mated = True
            return self.__class__(weight=birth_weight, age=0)



    def find_birth_weight(self, population):
        birth_probability = min(1, 0.2 * self.fitness * (population - 1))
        birth_weight = np.random.normal(self.w_birth, self.sigma_birth)
        print(self.weight)
        if self.weight > self.zeta * (9.5):
            if birth_probability > np.random.rand() and self.age > 0:
                return birth_weight
        return 0


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
        print('Creature that weighs: ', self.weight, ' lost : ', reduction)

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
            q_pos = 1.0 / (1.0 + np.exp(self.phi_age * (10.0 - self.a_half)))
            q_neg = 1.0 / (1.0 + np.exp(-self.phi_weight * (self.weight - self.w_half)))
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
        print('Death number: ', death_number)
        # print('Weight: ', self.weight, 'Fitness: ',fitness)
        if fitness <= 0:
            print('Dies because of negative fitness.')
            return True
        else:
            if death_number > self.survival_chance:
                print('-----> New Creature death, fitness: ', fitness)
                print('Random number: ', death_number)
                print('The probability: ', self.survival_chance)
                print('Will die at age: ',self.age,' and fitness: ', fitness)
                return True
            elif self.weight < 0:
                print('Dies because of negative weight.')
                return True
            else:
                print('Survives and thrives!')
                return False

    def wants_to_migrate(self):
        """
        Depends that we already have calculated fitness.
        Returns True if the creature wants to migrate.
        :return: boolean
        """
        return (self.mu * self.fitness) > np.random.random()


    def propensity(self, relative_abundance_of_fodder):
        """
        Calculates the propensity based on the amount of fodder
        :param fodder:
        :return: float
        """
        return np.exp(self.lambda1[self.species_id] * relative_abundance_of_fodder)

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

    def migrate(self, north, east, south, west):
        """
        Moves the creature to the most eligible adjacent position on the map.
        """
        pass


    def get_destination_probabilities(self):
        """
        Calculates the probability of moving to each of the adjacent cells,
        then returns a list with these probabilities.
        :return: list
        """
        highest_relevance = []
        adjacent_cells = self.adjacent_cell_attractiveness

        # print('adjacent cells', adjacent_cells)
        for relative_abundance_of_fodder in adjacent_cells:
            propensity = self.propensity(relative_abundance_of_fodder)
            highest_relevance.append(propensity)

            # print('tup', tup)
            # new_x_coord, new_y_coord = tup


            # current_cell_map = cell_map
            # if current_cell_map[new_x_coord][new_y_coord].landscape in {3, 4}:
            #     relevant_fodder = current_cell_map[new_x_coord][new_y_coord].attractiveness_herbivore()
            #     print("Fodder ", relevant_fodder)
            #     propensity = propensity(relevant_fodder)
            #     highest_relevance.append(propensity)

        probability_to_move = []
        for index in highest_relevance:
            probability_to_move.append(highest_relevance[index]/sum(highest_relevance))
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
        self.weight += 0.9 * fodder_amount
        print('Creature just ate and gained: ', 0.9 * fodder_amount)

