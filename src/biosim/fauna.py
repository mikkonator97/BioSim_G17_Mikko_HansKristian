from math import exp
class Fauna:
    """
    This class will include the common properties for all creatures on
    Rossumøya.
    """

    def __init__(self, position, age=0, weight,fitness):
        """"""
        self.position = position
        self.age = age
        self.weight = weight
        self.fitness = fitness

        pass


    def get_fitness(self):
        return self.fitness

    def get_weight(self):
        return self.weight

    def get_age(self):
        return self.age

    def get_position(self):
        return self.position


class Herbivore:



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

class Carnivore:
    pass

    def carnivore_fitness(self):
        """
        Function which computes the carnivore fitness according to the formula
        :return:
        """
        weight = Fauna.get_weight()
        if weight <= 0:
            return 0
        else:
            age = Fauna.get_age()
            a_half = 60.0
            w_half = 4.0
            fitness = Fauna.get_fitness()
            q_pos = (1.0 / (1.0 + exp(fitness(age - a_half))))
            q_neg = (1.0 / (1.0 + exp(-fitness(weight - w_half))))
            phi = q_pos * q_neg
            return phi
