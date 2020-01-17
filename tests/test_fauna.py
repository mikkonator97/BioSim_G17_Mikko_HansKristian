
# These tests will go through the needs and specifications for the faunas.
# Fauna is the superclass, and all other creatures will be found under.
# from math import exp
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
        mother = Herbivore(weight=40, age=10)
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
        test_herbivore = Herbivore(weight=100, age=10)
        test_herbivore.eat(10)
        assert test_herbivore.weight == 109

    def test_herbivore_fitness(self):
        """
        Will test that the fitness formula works.
        :return:
        """
        # This was the easiest combination to calculate by hand...
        # NB! Works with default parameters.
        test_herbivore = Herbivore(weight=10, age=40)
        assert test_herbivore.get_fitness() == 0.25

    def test_migrate(self):
        """
        Test that a creature stays in place if it does not want to migrate.
        Test that a creature will migrate if it wants to
        :return:
        """
        test_herbivore = Herbivore(age=10, weight=30)
        test_herbivore.have_migrated = True
        desired_cell_pre_migration = test_herbivore.desired_cell
        test_herbivore.migrate()
        assert desired_cell_pre_migration == test_herbivore.desired_cell
        # """Needs a test object with adjacent cells to make this work"""
        # test_herbivore.have_migrated = False
        # desired_cell_pre_migration = test_herbivore.desired_cell
        # test_herbivore.migrate()
        # assert desired_cell_pre_migration != test_herbivore.desired_cell

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
        pass

    def test_carnivore_fitness(self):
        """
        Will test that carnivores increases fitness whenever it eats.
        :return:
        """
        # phi = Carnivore.get_fitness()
        # ssert 0 <= phi <= 1
        pass
