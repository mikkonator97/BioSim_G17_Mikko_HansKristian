
# These tests will go through the needs and specifications for the faunas.
# Fauna is the superclass, and all other creatures will be found under.
from math import exp

class TestFauna:
    """
    These tests will go through everything that all the creatures have
    in common. There will be separate tests for each class as well.
    """

    def test_age(self):
        """
        Will test that the age is correct when a new fauna is born.
        :return:
        """
        test_baby = Fauna()
        assert test_baby.get_age() == 0


    def test_weight(self):
        """
        Will test that the weight is not 0.
        Will also test that the animals is able to gain weight.
        Weight will also be tested in test_birth.
        :return:
        """
        test_baby = Fauna()
        assert test_baby.get_weight() != 0



    def test_migration(self):
        """
        Will test that the animals move towards a location based on the
        amount of fodder.
        Will also test that animals unable to move because of low fitness
        have to stay behind.
        :return:
        """

    def test_birth(self):
        """
        Will test that there has to be multiple fauna in the same cell in
        order to give birth.
        Will test that an animal only gives birth to one offspring per year.
        Will test that the mother loses weight equals the baby's weight.
        Will test that the mother does not lose weight if there is no birth.
        Will test that the birth comes through if weight is correct.
        :return:
        """

    def test_death(self):
        """
        Will test that animals with fitness 0 dies.
        Will test the statistics behind the casualties.
        :return:
        """
        fitness = Fauna.get_fitness()
        assert fitness > 0


class TestHerbivores:
    """
    Will test properties special for herbivores.
    """

    def test_eating(self):
        """
        Will test that the creatures with highest amount of fitness eats first.
        Will test that they eat if they are able to.
        :return:
        """
        fodder = Landscape.get_fodder()
        if fodder > 0:
            herbivore_one = Herbivore()
            herbivore_two = Herbivore()
            fitness_one = herbivore_one.get_fitness()
            fitness_two = herbivore_two.get_fitness()





    def test_herbivore_fitness(self):
        """
        Will test that the fitness formula works.
        :return:
        """
        phi = Herbivore.get_fitness()
        assert 0 <= phi <= 1

# Test stats?


class TestCarnivores:
    """
    Will test properties special for carnivores.
    """

    def test_eating(self):
        """
        Will test that carnivores try to eat until it has passed 50 units
        of food in a year or there are no herbivores left in the cell.
        Will test that

        :return:
        """

    def test_carnivore_fitness(self):
        """
        Will test that carnivores increases fitness whenever it eats.
        :return:
        """
        phi = Carnivore.get_fitness()
        assert 0 <= phi <= 1
