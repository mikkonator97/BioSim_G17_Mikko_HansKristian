
# These tests will go through the needs and specifications for the faunas.
# Fauna is the superclass, and all other creatures will be found under.
from math import exp
from biosim.fauna import Fauna, Herbivore

class TestFauna:
    """
    These tests will go through everything that all the creatures have
    in common. There will be separate tests for each class as well.
    """

    def test_age(self):
        """
        Will test that the age is correct when a new fauna is born.
        Will also test that the age is the same amount if we set to something
        other than zero.
        Ageing will not be testet here, because that is manipulated in cell.
        :return:
        """
        test_baby = Fauna()
        test_adult = Fauna(age=30)
        assert test_baby.age == 0
        assert test_adult.age == 30


    def test_weight(self):
        """
        Will test that the weight is not 0 for a newborn.
        Doing this test on a Herbivore, because __init__ function for Fauna
        does not give proper parameters to give birth.
        Will also test that the animals is able to gain weight.
        Weight will also be tested in test_birth.

        :return:
        """
        mother = Herbivore(weight=40, age =10)
        baby = mother.birth(10)
        assert baby.weight != 0
        test_herbi = Herbivore(weight=100, age=10)
        test_herbi.reduce_weight()
        assert test_herbi.weight == 95



    def test_migration(self):
        """
        Will test that the animals move towards a location based on the
        amount of fodder.
        Will also test that animals unable to move because of low fitness
        have to stay behind.
        :return:
        """
        pass

    def test_birth(self):
        """
        Will test that there has to be multiple fauna in the same cell in
        order to give birth.
        Will test that an animal only gives birth to one offspring per year!!
        Will test that the mother loses weight equals the baby's weight.
        Will test that the mother does not lose weight if there is no birth.!!
        Will test that the birth comes through if weight is correct.!!
        :return:
        """

        # Mother doesn't give birth if there are only 1 creature in cell.
        mother1 = Herbivore(weight=40, age =10)
        baby1 = mother1.birth(1)
        assert baby1 is None

        # Mother loses weight equal to babys weigh.
        mother2 = Herbivore(weight=40, age =10)
        mother2_weight_before_birth = 40
        baby2 = mother2.birth(10)
        assert baby2.weight + mother2.weight == mother2_weight_before_birth

        # Will test that mother don't create offspring if underweight.
        mother3 = Herbivore(weight=20, age =10)
        baby3 = mother3.birth(100)
        mother4 = Herbivore(weight=30, age =10)
        baby4 = mother4.birth(100)
        mother5 = Herbivore(weight=32, age =10)
        baby5 = mother5.birth(100)
        assert baby3 is None
        assert baby4 is None
        assert baby5 is None

        # Will test that the mother can only give birth to one baby per year
        mother6 = Herbivore(weight=50, age =10)
        baby6 = mother6.birth(100)
        baby7 = mother6.birth(100)
        assert baby6 is not None
        # assert baby7 is None MIGHT IMPLEMENT SAFETY FOR THIS LATER


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
