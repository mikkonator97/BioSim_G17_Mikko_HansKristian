
__author__ = 'Hans Kristian Lunda, Mikko Rekstad'
__email__ = 'hans.kristian.lunda@nmbu.no, mikkreks@nmbu.no'


import mock
import unittest
from biosim.fauna import Fauna, Herbivore, Carnivore
import pytest

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
        assert test_adult.get_age() == 30

    def test_weight(self):
        """
        Will test that the weight is not 0 for a newborn.
        Doing this test on a Herbivore, because __init__ function for Fauna
        does not give proper parameters to give birth.
        Will also test that the animals is able to gain weight.
        Weight will also be tested in test_birth.

        :return:
        """
        mother = Herbivore(weight=40, age=10)
        baby = mother.birth(10)
        assert baby.weight != 0
        test_herbi = Herbivore(weight=100, age=10)
        test_herbi.reduce_weight()
        assert test_herbi.weight == 95
        assert test_herbi.get_weight() == 95

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
        mother1 = Herbivore(weight=40, age=10)
        baby1 = mother1.birth(1)
        assert baby1 is None

        # Mother loses weight equal to babys weigh.
        mother2 = Herbivore(weight=40, age=10)
        mother2_weight_before_birth = 40
        baby2 = mother2.birth(10)
        assert 1.2 * baby2.weight + mother2.weight == mother2_weight_before_birth

        # Will test that mother don't create offspring if underweight.
        mother3 = Herbivore(weight=20, age=10)
        baby3 = mother3.birth(100)
        mother4 = Herbivore(weight=30, age=10)
        baby4 = mother4.birth(100)
        mother5 = Herbivore(weight=32, age=10)
        baby5 = mother5.birth(100)
        assert baby3 is None
        assert baby4 is None
        assert baby5 is None

        # Will test that the mother can only give birth to one baby per year
        mother6 = Herbivore(weight=50, age=10)
        baby6 = mother6.birth(100)
        # baby7 = mother6.birth(100)
        assert baby6 is not None
        # assert baby7 is None MIGHT IMPLEMENT SAFETY FOR THIS LATER

    def test_death(self):
        """
        Once again, Faunas can't die, executing tests for herbivores.
        Will test that animals with fitness 0 dies.
        Will test the statistics behind the casualties.
        NB! We need a test in cell that checks that only dying creatures are
        removed.
        :return:
        """
        # Will first test that the fitness is zero if the weight is 0
        test_creature1 = Herbivore(age=0, weight=0)
        assert test_creature1.fitness == 0
        # Then test if the animal dies.
        assert test_creature1.death()
        # Will now test some statistics.
        test_creature2 = Herbivore(age=10, weight=100)
        assert not test_creature2.death()
        test_creature3 = Herbivore(age=10, weight=15)
        # assert test_creature3.fitness == 0
        # assert test_creature3.death()
        test_creature3.death()
        chance_of_survival = 1 - 0.4*(1.0-0.6209202238454615)
        assert test_creature3.survival_chance == chance_of_survival

        # We know that the death number is ≈ 0.45, and survival chance is 0.85
        # And therefore want to test that the creature survives.
        test_creature4 = Herbivore(age=10, weight=15)
        assert not test_creature4.death()

    @mock.patch("fauna.random", return_value=0.5, autospec=True)
    def test_wants_to_migrate(self, mock_randint):
        test_creature = Herbivore(10, 10)
        # return (self.mu * self.fitness) > np.random.random()
        assert test_creature.wants_to_migrate()

    @pytest.mark.parametrize('age, weight', [[50, 3], [60, 5], [70, 10]])
    def test_wants_to_migrate(self, age, weight):
        """
        Will test that animals unable to move because of low fitness
        have to stay behind.
        :return:
        """
        test_creature1 = Herbivore(age, weight)
        assert test_creature1.wants_to_migrate() is False


class TestHerbivores:
    """
    Will test properties special for herbivores.
    """

    def test_herbivore_fitness(self):
        """
        Will test that the fitness formula works.
        :return:
        """
        # This was the easiest combination to calculate by hand...
        # NB! Works with default parameters.
        test_herbivore = Herbivore(weight=10, age=40)
        assert test_herbivore.fitness == 0.25

class TestCarnivores:
    """
    Will test properties special for carnivores.
    """

    @pytest.mark.parametrize('age, weight', [[50, 50], [60, 55], [70, 60]])
    def test_eat(self, age, weight):
        """
        Will test that carnivores try to eat until it has passed 50 units
        of food in a year or there are no herbivores left in the cell.
        Will test that
        :return:
        """
        amount_eaten = 0
        test_herbivores = [Herbivore(age, weight), Herbivore(age=2, weight=20)]
        test_carnivore = Carnivore(weight=25, age=5)
        for herbivore in test_herbivores:
            amount_eaten += test_carnivore.eat(herbivore.weight, amount_eaten)
        assert amount_eaten == 50

        amount_eaten = 0
        test_carnivore = Carnivore(weight=25, age=5)
        old_weight = test_carnivore.weight
        test_small_herbivores = [Herbivore(age=20, weight=15),
                                 Herbivore(age=2, weight=20)]
        for herbivore in test_small_herbivores:
            amount_eaten += test_carnivore.eat(herbivore.weight, amount_eaten)
        assert (amount_eaten <= 50)\
        and (test_carnivore.weight == (old_weight + 26.25))

    def test_carnivore_fitness(self):
        """
        Will test that a fit carnivore is actually fit.
        :return:
        """
        test_carnivore = Carnivore(weight=25, age=5)
        assert test_carnivore.fitness >= 0.999

    def test_eat(self):
        """
        This test will check that the eat function increases if the creature
        eats. Also checks that the creature does not eat if it is full.
        Also checks that the correct of fodder is returned.
        self, fodder_amount=0, herbivore_already_eaten=0
        """
        carnivore = Carnivore(10, 10)
        # Checks that the amount returned is correct.
        assert carnivore.eat(100, 10) == 40
        assert carnivore.weight == 10 + 40 * carnivore.beta
        # Checks that no food over 50 is eaten, and also tests same weight.
        assert carnivore.eat(100, 50) == 0
        assert carnivore.weight == 10 + 40 * carnivore.beta

